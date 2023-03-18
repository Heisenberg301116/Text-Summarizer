# Text-Summarizer
Summarizing the content using OpenAI GPT models extracted from the web using Beautiful Soup and automating the search using Selenium.

************************************************************************************************************************************************************************

Important: 
1) The application was built in Python 3.9 and won't run on Python 3.5.
2) Create a '.env' file in the project's directory and write ypur OpenAI API key into it. Refer 'sample.env' file to know the syntax.
3) The application accepts test cases only through command line.
4) Make sure your presently working directly in the terminal is same as the one where main.py file is present before running the below test cases !!!
5) The following are the input flags that a user has to specify to run the application:
   a) --link: The wikipedia link from where you have to scrap content.                    (mandatory)
   b) --keywords: The section in the wikipedia page which you want to scrap               (mandatory)
   c) --model: The OpenAI text summarization model which you want to use.                 (mandatory)
   d) --out: The name of the .json file where ypu want to store the generated summary.    (not mandatory)

************************************************************************************************************************************************************************

Testcases:

Testcase 1:
python main.py --link "https://www.wikipedia.org/" --keywords "Biodiversity" --model "text-ada-001"

Testcase 2:
python main.py --link "https://www.wikipedia.org/" --keywords "Biodiversity" --out "india-biodiversity-ada-summary.json" --model "text-ada-001"

Testcase 3:
python main.py --link "https://www.wikipedia.org/" --keywords "Biodiversity" --out "india-biodiversity-davinci-summary.json" --model "text-davinci-003"

Testcase 4:
python main.py --link "https://www.wikipedia.org/" --keywords "Biodiversity" --out "india-biodiversity-gpt-3.5-summary.json" --model "gpt-3.5-turbo"