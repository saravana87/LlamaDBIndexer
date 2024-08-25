This is a light weight chat application created with Streamlit
To make it work. Please follow the following

1) Create a query engine with llama-index
  https://docs.llamaindex.ai/en/stable/understanding/querying/querying/

2) Connect the query engine with RAG agent using from_tools function
  
     # Create QueryEngineTools
    RAG_source1 = QueryEngineTool.from_defaults(
        datasource1,
        name="HTML Files",        
    )

    RAG_source2 = QueryEngineTool.from_defaults(
        datasource2,
        name="JSON Data",        
    )

    RAG_source3 = QueryEngineTool.from_defaults(
        datasource3,
        name="API Data",        
    )

    # Create ReActAgent
    agent = ReActAgent.from_tools(
        [RAG_source1, RAG_source2, RAG_source3],
        llm=llm,
        max_iterations=15,
        verbose=False
    )


3) Run "streamlit run llama-index-RAG-Singleagent-Chat.py"
