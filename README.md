# NewstoUse
Project which will use news to predict stock movements
 1. 📦 Install Prerequisites
Open Anaconda Prompt or Command Prompt, then run the following:

bash
Copy
Edit
pip install streamlit newsapi-python textblob spacy pandas
python -m textblob.download_corpora
python -m spacy download en_core_web_sm
✅ 2. 📁 Prepare Your Folder
Create a folder like:

makefile
Copy
Edit
D:\Swapneel\NewsToUse\
Put the following in this folder:

✅ app.py 👉 Download here

✅ stocks.csv 👉 Your stock list CSV with Symbol and Company Name columns (I'll provide sample if needed)

✅ 3. 📄 Sample stocks.csv File Format
Make sure your CSV file looks like this:

Symbol	Company Name
AAPL	Apple Inc
MSFT	Microsoft Corporation
GOOGL	Alphabet Inc

Save it as stocks.csv in the same folder.

✅ 4. ▶️ Run the Streamlit App
Open Command Prompt (or Anaconda Prompt) and run:

bash
Copy
Edit
cd D:\Swapneel\NewsToUse
streamlit run app.py
After a few seconds, your browser will open at:

arduino
Copy
Edit
http://localhost:8501
✅ 5. 🧠 How to Use the App
Once open in your browser:

🔑 Enter NewsAPI Key (Get from https://newsapi.org)

📁 Upload your stocks.csv

📝 Enter keywords, like: stocks, finance, economy

📊 Adjust number of pages to fetch (optional)

🚀 Click Run News Analysis

📥 Download results as CSV if needed

