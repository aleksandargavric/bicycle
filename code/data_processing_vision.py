import pandas as pd
import sys
from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType

def process_vision_data(input_csv_file, start_index, end_index, text_list, output_dir):
    def copy_dataframe_slice(df, start, end):
        if start < 0 or start >= len(df) or end < 0 or end >= len(df):
            raise ValueError("Start and end indices must be within DataFrame range.")
        return df.iloc[start:end+1].copy()

    def get_file_path(row):
        return f"../testdata/{row['path']}/{row['file_id']}.jpg"

    try:
        df = pd.read_csv(input_csv_file)
    except FileNotFoundError:
        print(f"Error: File '{input_csv_file}' not found.")
        sys.exit(1)

    try:
        file_paths= []
        df_slice = copy_dataframe_slice(df, start_index, end_index)
        for index, row in df_slice.iterrows():
            file_path = get_file_path(row)
            if file_path:
                file_paths.append(file_path)
            

        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # Instantiate model
        model = imagebind_model.imagebind_huge(pretrained=True)
        model.eval()
        model.to(device)

        # Load data
        inputs = {
            ModalityType.TEXT: data.load_and_transform_text(text_list, device),
            ModalityType.VISION: data.load_and_transform_vision_data(file_paths, device)
        }

        with torch.no_grad():
            embeddings = model(inputs)

        conformance_check = torch.softmax(embeddings[ModalityType.VISION] @ embeddings[ModalityType.TEXT].T, dim=-1)

        # Convert conformance_check to list
        conformance_check_list = conformance_check.tolist()

        # Assign tensor values to corresponding columns
        for i, col in enumerate(text_list):
            df_slice[col] = [row[i] for row in conformance_check_list]

        # Export df_slice as CSV
        output_csv_file = f"./{output_dir}/results_{start_index}_{end_index}.csv"
        df_slice.to_csv(output_csv_file, index=False)
        print(f"Results exported to {output_csv_file}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
