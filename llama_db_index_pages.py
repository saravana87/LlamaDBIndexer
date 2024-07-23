from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from sqlalchemy import create_engine, MetaData, Table
import json
import os

# Database connection
engine = create_engine('mysql+pymysql://testuser:testpassword@localhost/databasename')

metadata = MetaData()
metadata.reflect(bind=engine)

# Define the WordPress tables
posts = Table('wp_posts', metadata, autoload=True, autoload_with=engine)

# Query to extract page data

page_query = posts.select().where(posts.c.post_type == 'page')

try:
    # Execute the query
    with engine.connect() as connection:
        page_data = connection.execute(page_query).fetchall()
    print("Query executed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

# Convert the extracted data to a list of dictionaries
pages_list = []
for row in page_data:
    pages_list.append({
        'ID': row.ID,
        'post_author': row.post_author,
        'post_date': str(row.post_date),
        'post_content': row.post_content,
        'post_title': row.post_title,
        'post_status': row.post_status,
        'post_name': row.post_name,
        'post_modified': str(row.post_modified),
        'post_parent': row.post_parent,
        'guid': row.guid,
        'menu_order': row.menu_order,
        'post_type': row.post_type,
        'post_mime_type': row.post_mime_type,
        'comment_count': row.comment_count
    })

# Save the data to a JSON file
output_file = './data/pages_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(pages_list, f, ensure_ascii=False, indent=4)

print(f"Data successfully saved to {output_file}")