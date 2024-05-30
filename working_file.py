import os
from file_operation_functions import read_txt_file
from file_operation_functions import write_txt_file
from openai_functions import get_chat_completion


working_file = 'data/Whole Numbers and Half Truths/input/10 How India falls sick and gets better.txt'
data = read_txt_file(working_file)

system_message = "You are an expert summariser. Summarise only the text in the user input. Do not add any new information. Do not include your opinion. The input text incorporates many important statistics and annecdotal examples. Make sure to include them in the summary. The summary should have three parts. The first part should give the complete picture of the chapter with anecdotal examples. The second part should be bullet points of all the important ideas in the text. The third part should include the statistics and numbers mentioned in the text. There are no constraints on the length of the summary. Give a complete picture of the chapter."

chat_completion = get_chat_completion(system_message, data)

output_folder = 'data/Whole Numbers and Half Truths/summary'
input_file_name = os.path.basename(working_file)
output_file_name = input_file_name.replace('.txt', ' - Summary.txt')
output_file = os.path.join(output_folder, output_file_name)

write_txt_file(output_file, chat_completion)

