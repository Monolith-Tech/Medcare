# Summarize test results for fitting it in the context

from utils.tools import (
    get_openai_response,
    Models
)

from utils.prompts import summarize_prompt

import os
from PyPDF2 import PdfReader


# PDF loader
def load_PDFs(directory):
    all_text = ""
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    
    if not pdf_files:
        return "No PDF files found in the directory."

    for filename in pdf_files:
        file_path = os.path.join(directory, filename)
        
        try:
            pdf_reader = PdfReader(file_path)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
                
        except Exception as e:
            print(f"Could not read {filename}: {e}")

    return all_text


# clean the data extracted (removing all the noises and unwanted parts)
def summarize_test_results(dir: str) -> str:
    """
    Summarize the test results and extract all and only the important data.
    """
    
    print("* Extracting test results...")
    test_results = load_PDFs(directory=dir)
    
    data = get_openai_response(
        prompt = summarize_prompt(test_results),
        model = Models.model_4_turbo
    )

    return data



# main
if __name__ == "__main__":
    print(summarize_test_results('database/1/tests/'))



# tests_dir = 'Demo'

# # from llama_index.core.readers import SimpleDirectoryReader
# # from llama_index.indices.managed.vectara import VectaraIndex

# # documents = SimpleDirectoryReader(tests_dir).load_data()
# # index = VectaraIndex.from_documents(documents)






# from llama_index.core import ManagedIndex, SimpleDirectoryReade
# from llama_index.indices.managed.vectara import VectaraIndex

# # Load documents and build index
# vectara_customer_id = os.environ.get("VECTARA_CUSTOMER_ID")
# vectara_corpus_id = os.environ.get("VECTARA_CORPUS_ID")
# vectara_api_key = os.environ.get("VECTARA_API_KEY")
# documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()
# index = VectaraIndex.from_documents(
#     documents,
#     vectara_customer_id=vectara_customer_id,
#     vectara_corpus_id=vectara_corpus_id,
#     vectara_api_key=vectara_api_key,
# )

# # Query index
# query_engine = index.as_query_engine()
# response = query_engine.query("What did the author do growing up?")







# from langchain import OpenAI
# from llama_index import LLMPredictor

# llm_predictor = LLMPredictor(
#     llm=OpenAI(
#         temperature=0, 
#         model_name='text-ada-001', 
#         max_tokens=num_outputs
#     ),
# )
