import streamlit as st
from github import Github
import openai
import networkx as nx
import tempfile
import os

# Set OpenAI API Key
openai.api_key = "your_openai_api_key"

# Initialize GitHub API
def initialize_github(api_key):
    return Github(api_key)

# Load a Knowledge Graph from GitHub (example: .gml file in repo)
def load_knowledge_graph_from_github(repo_name, file_path, github_client):
    try:
        repo = github_client.get_repo(repo_name)
        file_content = repo.get_contents(file_path).decoded_content.decode("utf-8")
        
        # Save temporarily and load into NetworkX
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gml") as temp_file:
            temp_file.write(file_content.encode("utf-8"))
            temp_path = temp_file.name
        graph = nx.read_gml(temp_path)
        os.remove(temp_path)  # Clean up the temporary file
        return graph
    except Exception as e:
        st.error(f"Error loading Knowledge Graph: {e}")
        return None

# Retrieve data using ChatGPT
def chatgpt_response(query, context):
    prompt = f"Query: {query}\nKnowledge Context: {context}\nProvide a detailed response:"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response["choices"][0]["message"]["content"]

# Streamlit Interface
def main():
    st.title("AI Assistant with GitHub and ChatGPT")
    st.write("Query GitHub-based knowledge graphs with enhanced context-aware responses.")

    # GitHub Access
    github_api_key = st.text_input("Enter your GitHub API Key:", type="password")
    if github_api_key:
        github_client = initialize_github(github_api_key)
        st.success("Connected to GitHub!")
    
    # GitHub Repo and File Selection
    repo_name = st.text_input("Enter GitHub Repository (e.g., 'owner/repo'):")
    file_path = st.text_input("Enter Knowledge Graph File Path in Repo (e.g., 'data/graph.gml'):")
    
    knowledge_graph = None
    if st.button("Load Knowledge Graph") and repo_name and file_path and github_client:
        knowledge_graph = load_knowledge_graph_from_github(repo_name, file_path, github_client)
        if knowledge_graph:
            st.success("Knowledge Graph loaded successfully!")

    # Query Input
    query = st.text_input("Enter your query:")
    if query and knowledge_graph:
        # Fetch relevant nodes
        relevant_nodes = [n for n in knowledge_graph.nodes if query.lower() in n.lower()]
        context = "\n".join(relevant_nodes) if relevant_nodes else "No relevant context found in Knowledge Graph."

        # Get response from ChatGPT
        response = chatgpt_response(query, context)
        st.text_area("Response:", value=response, height=200)

if __name__ == "__main__":
    main()
