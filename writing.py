import requests  
  
def check_with_prowritingaid(text, api_key):  
    url = "https://api.prowritingaid.com/analysis/grammar"  
    headers = {  
        'Content-Type': 'application/json',  
        'Authorization': f"Bearer {api_key}"  
    }  
    payload = {  
        'text': text,  
        'language': 'en'  
    }  
  
    response = requests.post(url, headers=headers, json=payload)  
    if response.status_code == 200:  
        results = response.json()  
        # Process the results as needed  
        print("Analysis Results:", results)  
    else:  
        print(f"Error: {response.status_code}, {response.text}")  
  
def main():  
    api_key = "YOUR_API_KEY_HERE"  
    text = "Yesterday, she goes to the store and buy some fruits."  
    check_with_prowritingaid(text, api_key)  
  
if __name__ == "__main__":  
    main()  
