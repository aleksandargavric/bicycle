import time
import pandas as pd
from data_processing_vision import process_vision_data
from data_processing_auditory import process_auditory_data
from data_definitions import vision_values, audio_values, vision_values_reduced, audio_values_reduced

def append_performance_record(elapsed_time_ms, number_of_input_files, function_name):
    """
    Appends a performance record to the CSV file.
    """
    performance_data = pd.DataFrame({
        'elapsed time in ms': [elapsed_time_ms],
        'number of input files': [number_of_input_files],
        'function_name': [function_name]
    })
    
    # Append or create the performance_evaluation.csv file
    try:
        df = pd.read_csv('performance_evaluation.csv')
        df = pd.concat([df, performance_data], ignore_index=True)
    except FileNotFoundError:
        df = performance_data
    
    df.to_csv('performance_evaluation.csv', index=False)

if __name__ == "__main__":

    # Process extended vision data
    for value in vision_values:
        start_time = time.time()
        
        process_vision_data(value["data"], value["start"], value["end"], value["domain"], 'eval_results_ext')
        
        elapsed_time_ms = (time.time() - start_time) * 1000
        number_of_input_files = value["end"] - value["start"]
        append_performance_record(elapsed_time_ms, number_of_input_files, 'process_vision_data')
        print(f"Processed vision data: {value['start']} -- {value['end']}, Time: {elapsed_time_ms} ms")

    # Process extended auditory data
    for value in audio_values:
        start_time = time.time()
        
        process_auditory_data(value["data"], value["start"], value["end"], value["domain"], 'eval_results_ext')
        
        elapsed_time_ms = (time.time() - start_time) * 1000
        number_of_input_files = value["end"] - value["start"]
        append_performance_record(elapsed_time_ms, number_of_input_files, 'process_auditory_data')
        print(f"Processed auditory data: {value['start']} -- {value['end']}, Time: {elapsed_time_ms} ms")

    # Process reduced vision data
    for value in vision_values_reduced:
        process_vision_data(value["data"], value["start"], value["end"], value["domain"], 'eval_results_red')

    # Process reduced auditory data
    for value in audio_values_reduced:
        process_auditory_data(value["data"], value["start"], value["end"], value["domain"], 'eval_results_red')
