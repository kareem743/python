import openai

# Set OpenAI API key
openai.api_key = "your_openai_api_key"

def rag_retrieve_and_generate(query, knowledge_graph, github_code_snippets):
    """
    RAG Function to retrieve relevant data, augment with context, and generate a response.

    Args:
        query (str): The user query.
        knowledge_graph (networkx.Graph): The Knowledge Graph loaded using NetworkX.
        github_code_snippets (list): A list of code/documentation snippets from GitHub.

    Returns:
        str: The generated response.
    """
    # Step 1: Retrieve Relevant Knowledge Graph Nodes
    relevant_nodes = [node for node in knowledge_graph.nodes if query.lower() in node.lower()]
    kg_context = "\n".join(relevant_nodes) if relevant_nodes else "No relevant context found in Knowledge Graph."

    # Step 2: Retrieve Relevant GitHub Snippets
    relevant_snippets = [snippet for snippet in github_code_snippets if query.lower() in snippet.lower()]
    github_context = "\n".join(relevant_snippets) if relevant_snippets else "No relevant GitHub snippets found."

    # Combine contexts
    combined_context = f"Knowledge Graph Context:\n{kg_context}\n\nGitHub Context:\n{github_context}"

    # Step 3: Generate Response with ChatGPT
    prompt = (
        f"You are a helpful assistant for code-related queries.\n\n"
        f"User Query: {query}\n\n"
        f"Retrieved Context:\n{combined_context}\n\n"
        f"Provide a detailed response:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        generated_response = response["choices"][0]["message"]["content"]
    except Exception as e:
        generated_response = f"Error generating response: {e}"

    return generated_response
