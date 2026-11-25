import os
import sys
from urllib import request
from ollama import Client, ChatResponse, chat
from requests import get

client = Client(host=os.getenv('API_HOST', 'http://localhost:11434'),headers={'x-some-header': os.getenv('HEADER_VALUE', 'some-value')})

security_prompt = """You are a security scanner. Your task is to identify
 potential security vulnerabilities in the provided code.
 Please analyze the code and provide a detailed report highlighting
 any security issues, risks, or best practices that should be followed
 to enhance the security of the code. Response in a structured format, including the following information for each identified issue:

 For each issue, provide:
  1. Vulnerability type
  2. Why it is vulnerable (1 sentence)
  3. Impact (1 sentence)
  4. Secure code fix
 
 Code:
{code}
"""

# Check if the user provided a file path as an argument
if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
   print("Usage: python scanner.py <path_to_code_file>")
   sys.exit(1)

# Read the code from the provided file path
print(r"""
⠀⠀⠀⠀⠀⣀⣠⠤⠶⠶⣖⡛⠛⠿⠿⠯⠭⠍⠉⣉⠛⠚⠛⠲⣄⠀⠀⠀⠀⠀
⠀⠀⢀⡴⠋⠁⠀⡉⠁⢐⣒⠒⠈⠁⠀⠀⠀⠈⠁⢂⢅⡂⠀⠀⠘⣧⠀⠀⠀⠀
⠀⠀⣼⠀⠀⠀⠁⠀⠀⠀⠂⠀⠀⠀⠀⢀⣀⣤⣤⣄⡈⠈⠀⠀⠀⠘⣇⠀⠀⠀
⢠⡾⠡⠄⠀⠀⠾⠿⠿⣷⣦⣤⠀⠀⣾⣋⡤⠿⠿⠿⠿⠆⠠⢀⣀⡒⠼⢷⣄⠀
⣿⠊⠊⠶⠶⢦⣄⡄⠀⢀⣿⠀⠀⠀⠈⠁⠀⠀⠙⠳⠦⠶⠞⢋⣍⠉⢳⡄⠈⣧
⢹⣆⡂⢀⣿⠀⠀⡀⢴⣟⠁⠀⢀⣠⣘⢳⡖⠀⠀⣀⣠⡴⠞⠋⣽⠷⢠⠇⠀⣼
⠀⢻⡀⢸⣿⣷⢦⣄⣀⣈⣳⣆⣀⣀⣤⣭⣴⠚⠛⠉⣹⣧⡴⣾⠋⠀⠀⣘⡼⠃
⠀⢸⡇⢸⣷⣿⣤⣏⣉⣙⣏⣉⣹⣁⣀⣠⣼⣶⡾⠟⢻⣇⡼⠁⠀⠀⣰⠋⠀⠀
⠀⢸⡇⠸⣿⡿⣿⢿⡿⢿⣿⠿⠿⣿⠛⠉⠉⢧⠀⣠⡴⠋⠀⠀⠀⣠⠇⠀⠀⠀
⠀⢸⠀⠀⠹⢯⣽⣆⣷⣀⣻⣀⣀⣿⣄⣤⣴⠾⢛⡉⢄⡢⢔⣠⠞⠁⠀⠀⠀⠀
⠀⢸⠀⠀⠀⠢⣀⠀⠈⠉⠉⠉⠉⣉⣀⠠⣐⠦⠑⣊⡥⠞⠋⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡀⠀⠁⠂⠀⠀⠀⠀⠀⠀⠒⠈⠁⣀⡤⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠙⠶⢤⣤⣤⣤⣤⡤⠴⠖⠚⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")
code_file_path = sys.argv[1]
with open(code_file_path, 'r') as code_file:
    code_content = code_file.read()

prompt = security_prompt.format(code=code_content)

try: # check if the model is online before sending the request
    response = client.chat(
      model='qwen2.5:7b',
      messages=[
        {
          'role': 'user',
          'content': prompt,
        },
      ],
    )
    online_check = get("http://localhost:11434/v1/models/qwen2.5:7b")
    if online_check.status_code == 200:
        print("Model is online and ready to process the request.")
    else:
        print("Model is not online. Please check the server status.")

    print("Security Scan Report:")
    print(response.message.content)

# Handle exceptions that may occur during the request
except Exception as e:
    print(f"Connection failed {e}")