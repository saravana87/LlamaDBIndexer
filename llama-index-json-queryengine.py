from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.readers.json import JSONReader
import glob
import os
from llama_index.llms.openai import OpenAI

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo", max_tokens=512)
# Function to load and index JSON data
def load_and_index_json(directory_path):
    reader = JSONReader(
        levels_back=0,             # Set levels back as needed
        collapse_length=None,      # Set collapse length as needed
        ensure_ascii=False,        # ASCII encoding option
        is_jsonl=False,            # Set if input is JSON Lines format
        clean_json=True            # Clean up formatting-only lines
    )

    # Find all JSON files in the specified directory
    json_files = glob.glob(os.path.join(directory_path, "*.json"))

    # Load the data from each JSON file
    documents = []
    for json_file in json_files:
        documents.extend(reader.load_data(input_file=json_file, extra_info={}))

    # Create an index for querying
    index = VectorStoreIndex.from_documents(documents)
    return index

# Specify the directory containing your JSON files
json_directory = "./json_files"

# Load JSON and create an index
index = load_and_index_json(json_directory)
print("Indexing completed!")
print(index)

# Query the index
def query_index(index, query):
    response = index.as_query_engine()
    return response.query(query)

# Example usage: Querying the index
user_query = "Explain respiratory disorders and its medical codes."
response = query_index(index, user_query)
print(f"Response: {response}")
