from flashrank.Ranker import Ranker, RerankRequest
import streamlit as st
import json
from random import choice

print("Loading model...")

def get_rerank_response(query, passages,choice): 
    #switch case  
    if choice =='Nano':
        ranker = Ranker()
    elif choice == 'Small':
        ranker = Ranker(ranking_model="ms-marco-MiniLM-L-12-v2",cache_dir="/opt")
    elif choice == 'Medium':
        ranker = Ranker(ranking_model="rank-T5-Flan", cache_dir="/opt")
    elif choice == 'Large':
        ranker = Ranker(ranking_model="ms-marco-MultiBERT-L-12", cache_dir="/opt")
    reRankRequest = RerankRequest(query=query, passages=passages)
    results = ranker.rerank(reRankRequest)
    return results
#streamlit page info
st.set_page_config(page_title="FlashRank - ReRanking app", page_icon="🤖", layout="wide")

def main():
    st.title("FlashRank- ReRanking App")
    st.markdown("FlashRank is a fast and lightweight reranking model for large language models. It is designed to be used in production environments. It is open source and available on GitHub. It is also available on HuggingFace.")
    st.sidebar.write("Choose according to the Model size")
    menu = ["Nano", "Small", "Medium", "Large"]

    choice = st.sidebar.selectbox("Model Size", menu)
    st.sidebar.write("You selected:", choice)
    st.sidebar.info(""" 
                    **Model Options:**
                    - **Nano**:~4MB blazing fast model with competitive performance (Ranking precision).
                    - **Small**:~34MB slightly slower with the best perfomance.
                    - **Medium**:~110MB, slower model with the best zero-shot performance.
                    - **Large**:~150MB, slower model with competive performance for 100+ languages.
                    """)
    
    with st.expander("About FlashRank"):
        st.markdown("""
                      ***Flash Rank*** : Ultra-lite & Super-fast Python library to add re-ranking to your existing search & retrieval pipelines.
                    
                    - **Ultra-lite**: 
                    - **Super-fast**:
                    - **Cost-efficient**:
                    - **Based on SoTA Cross-encoders and other models**:
                    """)
    with st.form(key="input_form"):
        query_input = st.text_input("Enter your query")
        context_input = st.text_area("Enter your passages")
        submit_button = st.form_submit_button(label="Rerank")

        if submit_button:
            with st.spinner("Reranking..."):                
                if query_input and context_input:
                    context_input = json.loads(context_input)
                    results = get_rerank_response(query_input, context_input, choice)
                    with st.expander("Results", expanded=True):
                        st.json(results, expanded=True)
                    for result in results:
                        st.write(result)
                        st.write("----")
                else:
                    st.write("Please enter a query and passages")

if __name__ == "__main__":
    main()

    # #input
    # query = st.text_input("Enter your query")
    # passages = st.text_area("Enter your passages")
    # passages = passages.split("\n")
    # passages = [p.strip() for p in passages]
    # passages = [p for p in passages if p]
    # passages = [json.loads(p) for p in passages]
    # if st.button("Rerank"):
    #     if query and passages:
    #         results = get_rerank_response(query, passages, choice)
    #         for result in results:
    #             st.write(result)
    #             st.write("----")
    #     else:
    #         st.write("Please enter a query and passages")