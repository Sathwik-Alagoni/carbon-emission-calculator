# functions/streamlit.py
import subprocess

def handler(event, context):
    subprocess.Popen(["streamlit", "run", "app.py"])
    return {
        "statusCode": 200,
        "body": "✅ Streamlit app is starting..."
    }
