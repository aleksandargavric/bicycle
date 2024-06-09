from flask import Flask, request, jsonify, render_template, Response
import os
import torch
from imagebind import data
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType
import random
import string
import time
import ollama
from moviepy.editor import VideoFileClip, AudioFileClip
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
EXPORT_FOLDER = 'static/exports/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'avi', 'txt'}
chunk_size_sec = 2

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXPORT_FOLDER'] = EXPORT_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(extension):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{timestamp}_{random_str}.{extension}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/single')
def single():
    return render_template('uploadsinglefile.html')

def append_and_get_index(lst, element):
    lst.append(element)
    return len(lst) - 1

@app.route('/upload-pm', methods=['POST'])
def upload_pm_file():
    if ('files[]' not in request.files) and ('textModality' not in request.form):
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('files[]')
    results = []
    date_key = f'date_0'
    date_string = request.form[date_key]
    timestamp = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    image_paths = []
    txt_paths = []
    audio_paths = []
    request_id = generate_unique_filename('id')

    if 'textModality' in request.form:
        textModality = request.form['textModality']
        split_strings = textModality.split('|')
        # Iterate over the split strings
        for index, item in enumerate(split_strings):
            filename = generate_unique_filename('txt')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(file_path, "w") as file:
                file.write(item)
            txtLog = append_and_get_index(txt_paths, file_path)
            results.append({
                "filename": filename,
                "message": "Textual file processed",
                "timestamp_start": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "timestamp_end": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "caseid": f"manualtxtinput-#{index}",
                "analysis" : f"{request_id}-txt-{txtLog}"
            })
    print(files)
    for i, file in enumerate(files):
        date_key = f'date_{i}'
        date_string = request.form[date_key]
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        if file.filename == '' or not allowed_file(file.filename):
            continue  # Skip invalid files

        filename = generate_unique_filename(extension)
        caseid = filename[:-4]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print("File uploaded to:", file_path)
    
        if extension in {'mp4', 'avi'}:
            # Handle video file
            result = process_video_file(file_path, date_string, caseid, audio_paths, image_paths, request_id)
            results.append(result)
        elif extension in {'mp3', 'wav'}:
            # Handle audio file
            result = process_audio_file(file_path, date_string, caseid, audio_paths, request_id)
            results.append(result)
        elif extension in {'png', 'jpg', 'jpeg', 'gif'}:
            # Handle image file
            imageLog = append_and_get_index(image_paths, file_path)
            results.append({"filename": filename, "message": "Image file processed", "timestamp_start": timestamp.strftime('%Y-%m-%d %H:%M:%S'), "timestamp_end": timestamp.strftime('%Y-%m-%d %H:%M:%S'), "caseid": caseid, 'analysis': f"{request_id}-img-{imageLog}"})
        elif extension in {'txt'}:
            # Handle txt file
            txtLog = append_and_get_index(txt_paths, file_path)
            results.append({"filename": filename, "message": "Txt file processed", "timestamp_start": timestamp.strftime('%Y-%m-%d %H:%M:%S'), "timestamp_end": timestamp.strftime('%Y-%m-%d %H:%M:%S'), "caseid": caseid, 'analysis': f"{request_id}-txt-{txtLog}"})
        else:
            # Assume image or other file types not needing special handling
            results.append({"filename": filename, "message": "File uploaded but not processed"})

    output_path = os.path.join(app.config['EXPORT_FOLDER'], generate_unique_filename('csv'))
    convert_to_df_and_export(results, output_path)
    output = {'results': results, 'csv': output_path, 'request_id': request_id, 'txt_paths': txt_paths, 'image_paths': image_paths, 'audio_paths': audio_paths}
    return jsonify(output)

def process_video_file(file_path, date_string, caseId, audio_paths, image_paths, request_id):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        frame_results = []
        imageLog = {}
        audioLog = {}
        frame_path = ""
        # Get file modification time as the starting timestamp
        timestamp_start = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        for start in range(0, int(duration), chunk_size_sec):
            end = min(start + chunk_size_sec, duration)
            chunk_duration = end - start
            timestamp_end = timestamp_start + timedelta(seconds=chunk_duration)
            frame_filename = generate_unique_filename('png')
            frame_path = os.path.join(app.config['UPLOAD_FOLDER'], frame_filename)
            clip.save_frame(frame_path, t=start)
            # Process and save audio chunk, if present
            if clip.audio:
                chunkAudio_filename = generate_unique_filename('wav')
                chunkAudio_path = os.path.join(app.config['UPLOAD_FOLDER'], chunkAudio_filename)
                clip.audio.subclip(start, end).write_audiofile(chunkAudio_path)
                audioLog = append_and_get_index(audio_paths, chunkAudio_path)
                frame_results.append({
                    "filename": chunkAudio_filename, 
                    "message": "Audio chunk processed",
                    "timestamp_start": timestamp_start.strftime('%Y-%m-%d %H:%M:%S'),
                    "timestamp_end": timestamp_end.strftime('%Y-%m-%d %H:%M:%S'), 
                    "caseid": caseId,
                    "analysis": f"{request_id}-aud-{audioLog}"
                })

            # Process and save video chunk, including audio if present
            chunkVideo_filename = generate_unique_filename('mp4')
            chunkVideo_path = os.path.join(app.config['UPLOAD_FOLDER'], chunkVideo_filename)
            clip.subclip(start, end).write_videofile(chunkVideo_path, audio_codec='aac')
            imageLog = append_and_get_index(image_paths, frame_path)
            frame_results.append({
                "filename": chunkVideo_filename, 
                "message": "Video chunk processed",
                "timestamp_start": timestamp_start.strftime('%Y-%m-%d %H:%M:%S'),
                "timestamp_end": timestamp_end.strftime('%Y-%m-%d %H:%M:%S'), 
                "caseid": caseId,
                "analysis": f"{request_id}-img-{imageLog}"
            })
            
            # Update timestamp_start for the next chunk
            timestamp_start = timestamp_end

        imageLog = append_and_get_index(image_paths, frame_path)
        return {
            "filename": os.path.basename(file_path),
            "chunks": frame_results,
            "timestamp_start": frame_results[0]['timestamp_start'],
            "timestamp_end": frame_results[-1]['timestamp_end'],
            "message": "Video file processed", 
            "caseid": caseId,
            "analysis": f"{request_id}-img-{imageLog}"
        }
    except Exception as e:
        return {"filename": os.path.basename(file_path), "error": str(e)}

@app.route('/compute-event-log', methods=['POST'])
def compute_modalities():
    requestData = request.form
    txt_paths = [path for path in requestData['txt_paths'].split(",") if path.strip()]
    image_paths = [path for path in requestData['image_paths'].split(",") if path.strip()]
    audio_paths = [path for path in requestData['audio_paths'].split(",") if path.strip()]
    request_id = requestData['request_id']
    labels = []
    for item in requestData['labels'].split(","):
        labels.extend(label.strip() for label in item.split("|") if label.strip())
    # If labels list is empty (should not happen), add elements "Action start" and "Action end"
    if not labels:
        labels.extend(["Action start", "Action end"])

    csv = requestData['csv']
    print(txt_paths, image_paths, audio_paths, labels)
    results = []

    if(txt_paths):
        txtresults = similarity_search_text(labels, txt_paths)
        for index, item in enumerate(txtresults):
            results.append({ 'id': f"{request_id}-txt-{index}", 'result': item })
        
    if(image_paths):
        imagesults = similarity_search_vision(labels, image_paths)
        for index, item in enumerate(imagesults):
            results.append({ 'id': f"{request_id}-img-{index}", 'result': item })
        
    if(audio_paths):
        audioresults = similarity_search_audio(labels, audio_paths)
        for index, item in enumerate(audioresults):
            results.append({ 'id': f"{request_id}-aud-{index}", 'result': item })
    

    output_path = os.path.join(app.config['EXPORT_FOLDER'], generate_unique_filename('csv'))
    newcsv = update_df(results, csv)
    print(results)
    output = {'results': results, 'csv': newcsv, 'request_id': request_id}
    return jsonify(output)

def update_df(results, csv):

    data_df = pd.read_csv(csv)
    # Create a mapping of ids to their corresponding analysis results
    id_to_result = {result['id']: result for result in results}
    # Update the 'analysis' column in csv DataFrame
    data_df['analysis'] = data_df['analysis'].map(lambda x: id_to_result[x])
    data_df.to_csv(csv, index=False)
    return csv

def process_audio_file(file_path, date_string, caseId, audio_paths, request_id):
    try:
        clip = AudioFileClip(file_path)
        duration = clip.duration
        chunk_results = []
        # Get file modification time as the starting timestamp
        timestamp_start = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        for start in range(0, int(duration), chunk_size_sec):
            end = min(start + chunk_size_sec, duration)
            chunk_filename = generate_unique_filename('wav')
            chunk_path = os.path.join(app.config['UPLOAD_FOLDER'], chunk_filename)
            subclip = clip.subclip(start, end)
            subclip.write_audiofile(chunk_path)
            audioLog = append_and_get_index(audio_paths, chunk_path)
            # Calculate end timestamp for each chunk
            chunk_duration = end - start
            timestamp_end = timestamp_start + timedelta(seconds=chunk_duration)
            
            chunk_results.append({
                "filename": chunk_filename,
                "message": "Audio chunk processed",
                "timestamp_start": timestamp_start.strftime('%Y-%m-%d %H:%M:%S'),
                "timestamp_end": timestamp_end.strftime('%Y-%m-%d %H:%M:%S'), 
                "caseid": caseId,
                "analysis": f"{request_id}-aud-{audioLog}"
            })
            
            # Update timestamp_start for the next chunk
            timestamp_start = timestamp_end

        # Calculate the overall end timestamp
        overall_end_timestamp = timestamp_start + timedelta(seconds=duration % chunk_size_sec)
        audioLog = append_and_get_index(audio_paths, chunk_path)
        return {
            "filename": os.path.basename(file_path),
            "chunks": chunk_results,
            "timestamp_start": chunk_results[0]['timestamp_start'],
            "timestamp_end": overall_end_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "message": "Audio file processed", 
            "caseid": caseId,
            "analysis": f"{request_id}-aud-{audioLog}"
        }
    except Exception as e:
        return {"filename": os.path.basename(file_path), "error": str(e)}

def convert_to_df_and_export(data, csv_filename):
    # Initialize empty lists to store data
    case_ids = []
    filenames = []
    messages = []
    analyses = []
    timestamp_starts = []
    timestamp_ends = []

    # Loop through each item in the data
    for item in data:
        # Extract main information
        case_id = item["caseid"]
        filename = item["filename"]
        message = item["message"]
        analysis = item["analysis"]
        timestamp_start = item["timestamp_start"]
        timestamp_end = item["timestamp_end"]

        # Append main information to lists
        case_ids.append(case_id)
        filenames.append(filename)
        messages.append(message)
        analyses.append(analysis)
        timestamp_starts.append(timestamp_start)
        timestamp_ends.append(timestamp_end)

        # Extract chunks information if available
        if "chunks" in item:
            for chunk in item["chunks"]:
                # Append chunk information to lists
                case_ids.append(chunk["caseid"])
                filenames.append(chunk["filename"])
                messages.append(chunk["message"])
                analyses.append(chunk["analysis"])
                timestamp_starts.append(chunk["timestamp_start"])
                timestamp_ends.append(chunk["timestamp_end"])

    # Create DataFrame
    df = pd.DataFrame({
        "caseid": case_ids,
        "timestamp_start": timestamp_starts,
        "timestamp_end": timestamp_ends,
        "filename": filenames,
        "message": messages,
        "analysis": analyses
    })

    # Export DataFrame to CSV
    df.to_csv(csv_filename, index=False)

def similarity_search_vision(labels, image_paths):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # Instantiate model
    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)

    # Load data
    inputs = {
        ModalityType.TEXT: data.load_and_transform_text(labels, device),
        ModalityType.VISION: data.load_and_transform_vision_data(image_paths, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)
    response = torch.softmax(embeddings[ModalityType.VISION] @ embeddings[ModalityType.TEXT].T, dim=-1)
    print("Model: ", response)
  # Parse response into a JSON
    results = parse_response(labels, response)
    print("Response: ", results)
    return results

def parse_response(labels, response):
    results = []
    for j, row in enumerate(response):
        result = {}
        for i, text in enumerate(labels):
            result[text] = float(row[i])
        results.append(result)
    return results

def similarity_search_audio(labels, audio_paths):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # Instantiate model
    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)

    # Load data
    inputs = {
        ModalityType.TEXT: data.load_and_transform_text(labels, device),
        ModalityType.AUDIO: data.load_and_transform_audio_data(audio_paths, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)
    response = torch.softmax(embeddings[ModalityType.AUDIO] @ embeddings[ModalityType.TEXT].T, dim=-1)
    print("Model: ", response)
    results = parse_response(labels, response)
    print("Response: ", results)
    return results

def similarity_search_text(labels, txt_paths):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # Instantiate model
    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)

    # Load data
    inputsLabels = {
        ModalityType.TEXT: data.load_and_transform_text(labels, device)
    }
    inputsTxts = {
        ModalityType.TEXT: data.load_and_transform_text(txt_paths, device),
    }
    with torch.no_grad():
        embeddingsLabels = model(inputsLabels)
    with torch.no_grad():
        embeddingsTxts = model(inputsTxts)

    response = torch.softmax(embeddingsTxts[ModalityType.TEXT] @ embeddingsLabels[ModalityType.TEXT].T, dim=-1)
    print("Model: ", response)
    results = parse_response(labels, response)
    print("Response: ", results)
    return results


@app.route('/upload-ref', methods=['POST'])
def upload_ref_file():
    if ('files[]' not in request.files) and ('textModality' not in request.form):
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('files[]')
    results = []
    image_paths = []
    txt_paths = []
    request_id = generate_unique_filename('id')
    requestData = request.form
    labels = []
    for item in requestData['labels'].split(","):
        labels.extend(label.strip() for label in item.split("|") if label.strip())
    if not labels:
        labels.extend(["Action start", "Action end"])

    if 'textModality' in request.form:
        textModality = request.form['textModality']
        split_strings = textModality.split('|')
        # Iterate over the split strings
        for index, item in enumerate(split_strings):
            filename = generate_unique_filename('txt')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(file_path, "w") as file:
                file.write(item)
            txtLog = append_and_get_index(txt_paths, file_path)
            results.append({
                "filename": filename,
                "message": "Textual file processed",
                "analysis" : f"{request_id}-txt-{txtLog}"
            })

    for i, file in enumerate(files):
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        if file.filename == '' or not allowed_file(file.filename):
            continue  # Skip invalid files

        filename = generate_unique_filename(extension)
        caseid = filename[:-4]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print("File uploaded to:", file_path)
    
        if extension in {'png', 'jpg', 'jpeg', 'gif'}:
            # Handle image file
            imageLog = append_and_get_index(image_paths, file_path)
            results.append({"filename": filename, "message": "Image file processed", 'analysis': f"{request_id}-img-{imageLog}"})
        elif extension in {'txt'}:
            # Handle txt file
            txtLog = append_and_get_index(txt_paths, file_path)
            results.append({"filename": filename, "message": "Txt file processed", 'analysis': f"{request_id}-txt-{txtLog}"})
        else:
            # Assume image or other file types not needing special handling
            results.append({"filename": filename, "message": "File uploaded but not processed"})

    output = {'results': results, 'request_id': request_id, 'txt_paths': txt_paths, 'image_paths': image_paths}
    return jsonify(output)


@app.route('/stream-llm', methods=['POST'])
def stream():
    post_data = request.json
    file = post_data.get('file')[1:]
    labels =  post_data.get('labels')
    return Response(streamLLMResponse(file, labels), mimetype='text/event-stream')

def streamLLMResponse(file, labels):
    extension = file.rsplit('.', 1)[1].lower()
    prompt = f"For each of business features [{labels}], explain how it is connected to the file. Then propose a new list of business features to better fit the provided file."
    print(prompt)
    stream = None
    with open(file, 'rb') as fileRaw:
        if extension in {'png', 'jpg', 'jpeg', 'gif'}:
            stream = ollama.chat(
                model='llava',
                messages=[
                {
                    'role': 'user',
                    'content': prompt,
                    'images': [fileRaw.read()],
                },
                ],
                stream=True
            )
        elif extension in {'txt'}:
            prompt = f"{prompt} File: {fileRaw.read()}"
            stream = ollama.chat(
                model='llava',
                messages=[
                {
                    'role': 'user',
                    'content': prompt
                },
                ],
                stream=True
            )
    for chunk in stream:
        yield chunk['message']['content']


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5000)