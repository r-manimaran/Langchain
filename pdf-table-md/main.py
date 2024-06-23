from llama_parse import LlamaParse
import os
from dotenv import load_dotenv
load_dotenv()

document = LlamaParse(result_type="markdown", api_key=os.getenv("LLAMA_CLOUD_API_KEY")).load_data("apple_10k.pdf")


# print(document[0].text[:1000])

'''
### Save as text file
file_name = "apple_10k.txt"
with open(file_name, "w") as f:
    f.write(document[0].text)
'''

### Save as markdown file


### Add Instrcutions
''''
documents_with_instructions = LlamaParse(result_type="markdown", 
                                         api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
                                         parsing_instruction="""
                                         Summarize the document in 100 words or less.
                                         """).load_data("apple_10k.pdf")
'''
documents_with_instructions = LlamaParse(result_type="markdown", 
                                         api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
                                         parsing_instruction="""
                                         This is apple annual report
                                         """).load_data("apple_10k.pdf")


#print(documents_with_instructions[0])
## Save as markdown file
file_name = "apple_10k_with_instructions.md"
with open(file_name, "w") as f:
    f.write(documents_with_instructions)