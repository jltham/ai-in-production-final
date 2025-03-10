# Final Project for AI in Production

This application gives a Gradio interface to query an underlying LLM (DeepSeek-R1-Distill-Llama-8B) hosted on Ollama. The application is also equipped with RAG capabilities with Weaviate as its vector database using an underlying embedding model (nomic-embed-text) that is also hosted on Ollama. The ingested data is webscraped from the publicly available [Red Dragon AI website](https://reddragonai.com/).

Docker images of Ollama and Weaviate are used, and the docker image of this application is built at runtime according to the Docker Compose file.

Try to ask what is Red Dragon AI with retrieve context enabled and disabled to see how RAG can help ground output generation!