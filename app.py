import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, FilterOperator, FilterCondition
from llama_index.core import VectorStoreIndex

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "companies"
pinecone_index = pc.Index(index_name)

# Setup Pinecone Vector Store
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

def query_search(query, metadata_filters=None, k=10):
    retriever = index.as_retriever(similarity_top_k=k, filters=metadata_filters)
    results = retriever.retrieve(query)
    data_to_return = [
        {
            "id": result.node.metadata['id'],
            "score": result.score
        }
        for result in results
    ]
    return data_to_return

# Make page layout wider
st.set_page_config(layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('sample_with_descriptions.csv')
    df['founded'] = pd.to_numeric(df['founded'], errors='coerce').fillna(0).astype(int)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header('Filter Options')

# Filter by industry
industries = df['industry'].dropna().unique()
selected_industries = st.sidebar.multiselect('Industry', industries)

# Filter by country
countries = df['country'].dropna().unique()
selected_countries = st.sidebar.multiselect('Country', countries)

# Apply filters
filtered_df = df.copy()

if selected_industries:
    filtered_df = filtered_df[filtered_df['industry'].isin(selected_industries)]

if selected_countries:
    filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]

# Display the data
st.write(f"### Filtered Data ({len(filtered_df)} results)")
st.dataframe(filtered_df)

# Query input and results
st.sidebar.header('Query Search')
query = st.sidebar.text_input('Enter your query')

# Top-k selection
k = st.sidebar.slider('Number of top-k results', min_value=1, max_value=100, value=10)

# Metadata filters
metadata_filters = []

# Adding industry filter to metadata filters if selected
if selected_industries:
    metadata_filters.append(MetadataFilter(key="industry", value=selected_industries, operator=FilterOperator.IN))

# Adding country filter to metadata filters if selected
if selected_countries:
    metadata_filters.append(MetadataFilter(key="country", value=selected_countries, operator=FilterOperator.IN))

if query:
    filters = MetadataFilters(filters=metadata_filters, condition=FilterCondition.AND)
    results = query_search(query, metadata_filters=filters, k=k)
    result_ids = [result['id'] for result in results]
    query_filtered_df = df[df['id'].isin(result_ids)]
    st.write(f"### Query Results for '{query}' ({len(query_filtered_df)} results)")
    st.dataframe(query_filtered_df)
