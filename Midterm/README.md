# Task 1Dealing with the Data
Review the two PDFs and decide how best to chunk up the data with a single strategy to optimally answer the variety of questions you expect to receive from people.

Deliverables:
1. Describe the default chunking strategy that you will use.
    - I chose the chunk by length (i.e., specify CHUNK_SIZE,CHUNK_OVERLAP)
2. Articulate a chunking strategy that you would also like to test out.
    - Chunk by section/paragraph
3. Describe how and why you made these decisions
    - I picked 10 random piece of chunks and generated 2 questions per chunk - This will the "ground truth"
    - Then I created 2 retrievers based on different chunk size (500 VS 1000), along with a retriever that is based on text split by section/paragraph
    - Ran through generated questions and calculate the "is_hit" rate (i.e., if retriever retrieved correct chunk, then 1 else 0)
    - Ideally ran it multiple times (since our questions are randomly generated) and check the mean "is_hit" rate
    - I ran it couple time, in general chunk_size = 1000 and overlap = 200 always gives the but resutls

# Task 2 Building a Quick End-to-End Prototype
Build an end-to-end RAG application using an industry-standard open-source stack and your choice of commercial off-the-shelf models
Deliverables:
1. Build a live public prototype on Hugging Face, and include the public URL link to your space.
    - https://huggingface.co/spaces/yinong333/ChatwithLegalPDF

2. How did you choose your stack, and why did you select each tool the way you did?
    - Qdrant
        - Qdrant is a fully-fledged vector database that speeds up the search process by using a graph-like structure to find the closest objects in sublinear time. So we don’t calculate the distance to every object from the database, but some candidates only. It uses Hierarchical Navigable Small World (HNSW) algorithm so we are able to compare the distance to some of the objects from the database, not to all of them. This allows a fast response
    - Langchain
        - LangChain provides a comprehensive framework designed specifically for building conversational AI applications. It abstracts many complex aspects of developing these applications, such as document retrieval, context management, and conversational memory and allows user to define and customize chains of operations, which are sequences of steps that process user input, retrieve relevant information, and generate responses. LangChain integrates seamlessly with vector databases like Qdrant, facilitating efficient document retrieval based on semantic search. This is crucial for applications that need to fetch and utilize large volumes of document-based data dynamically. It also supports embeddings and vector search, crucial for building efficient, AI-driven search and retrieval systems within conversational applications.
    - OpenAI:
        - OpenAI offers some of the most advanced language models available, such as GPT-3.5. These models are pre-trained on a diverse range of internet text, making them highly capable of understanding and generating human-like text. OpenAI’s infrastructure is designed to handle high request volumes, ensuring that our application can scale seamlessly as user demand increases. It provides easy-to-use APIs for integrating their language models into applications. This simplifies the development process and allows you to focus on application-specific functionalities rather than the complexities of model training and maintenance.
    - Chainlit:
        - Chainlit offers a variety of features and advantages that can be particularly beneficial when building interactive, data-driven web applications, especially for AI and machine learning models. It requires less boilerplate code compared to traditional web development frameworks, which can significantly speed up development time. It also provides out-of-the-box UI components that are pre-configured to work well with data-driven applications, reducing the need to develop these components from scratch. Chainlit facilitates easy handling of streaming data, making it ideal for applications that need to display or process real-time information.

# Task 3 Creating a Golden Test Data Set
Generate a synthetic test data set and baseline an initial evaluation
Deliverables:
1. Assess your pipeline using the RAGAS framework including key metrics faithfulness, answer relevancy, context precision, and context recall.  Provide a table of your output results.
    - I generated 20 synthetic questions, the overal scores are: {'faithfulness': 0.8481, 'answer_relevancy': 0.9196, 'context_recall': 0.8833, 'context_precision': 0.8819, 'answer_correctness': 0.6919}
    detailed tables is showing in the notebook
2. What conclusions can you draw about performance and effectiveness of your pipeline with this information?
    - I think overall, both based on the generation part and the retrieval part, the performance is pretty ok

# Task 4 Fine-Tuning Open-Source Embeddings
Generate synthetic fine-tuning data and complete fine-tuning of the open-source embedding model