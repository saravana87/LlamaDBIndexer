from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage
from llama_index.core import StorageContext
from sqlalchemy import create_engine, MetaData, Table
from llama_index.llms.openai import OpenAI

import json
import os
from dotenv import load_dotenv
load_dotenv()
llm = OpenAI(model="gpt-4")

# Database connection
engine = create_engine('mysql+pymysql://testuser:testpassword@localhost/bgrub')

metadata = MetaData()
metadata.reflect(bind=engine)

# Tables
posts = Table('wp_posts', metadata, autoload=True)
postmeta = Table('wp_postmeta', metadata, autoload=True)
terms = Table('wp_terms', metadata, autoload=True)
term_taxonomy = Table('wp_term_taxonomy', metadata, autoload=True)
term_relationships = Table('wp_term_relationships', metadata, autoload=True)

# Query to extract product data
product_query = posts.select().where(posts.c.post_type == 'product')
#product_data = engine.execute(product_query).fetchall()

try:
    # Execute the query
    with engine.connect() as connection:
        product_data = connection.execute(product_query).fetchall()
    print("Query executed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

# Print a few rows to verify
#for row in product_data[:5]:
    #print(row)

# Function to get metadata
def get_metadata(post_id):
    query = postmeta.select().where(postmeta.c.post_id == post_id)
    with engine.connect() as connection:
        metadata = connection.execute(query).fetchall()
        #for row in metadata[:5]:
            #print(row)
        meta_dict = {meta.meta_key: meta.meta_value for meta in metadata}
    return meta_dict

# Function to get categories
def get_categories(post_id):
    query = term_relationships.select().where(term_relationships.c.object_id == post_id)
    with engine.connect() as connection:
        term_relationships_data = connection.execute(query).fetchall()
    categories = []
    for rel in term_relationships_data:
        taxonomy_query = term_taxonomy.select().where(term_taxonomy.c.term_taxonomy_id == rel.term_taxonomy_id)
        with engine.connect() as connection:
            taxonomy_data = connection.execute(taxonomy_query).fetchone()
        if taxonomy_data.taxonomy == 'product_cat':
            term_query = terms.select().where(terms.c.term_id == taxonomy_data.term_id)
            with engine.connect() as connection:
                term_data = connection.execute(term_query).fetchone()
            categories.append(term_data.name)
    return categories

# Prepare documents for indexing
documents = []
for product in product_data:
    metadata = get_metadata(product.ID)
    categories = get_categories(product.ID)
    product_info = {
        'ID': product.ID,
        'Name': product.post_title.lower(),
        'Description': product.post_content.lower(),
        'Price': metadata.get('_price'),
        'SKU': metadata.get('_sku'),
        'Categories': categories,
        # Add more fields as needed
    }
    sku = metadata.get('_sku')
    if sku:
        file_path = os.path.join(r".data_aug1", f"{sku}.json") #saving each product in a file using sku as the filename.
        with open(file_path, 'w') as f:
            # Assuming you want to write some data to this file
            json.dump(product_info, f)  # Replace 'your_data' with the actual data you want to write
    else:
        print("SKU is not available or invalid")
    documents.append(product_info)
