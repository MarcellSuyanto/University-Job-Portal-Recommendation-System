# University Job Portal Recommendation System
This project is specifically built for University of Hong Kong(HKU)'s Student Job Portal NETJOBS, exclusive to students studying/studied at HKU, with access to HKU CEDARS NERTJOBS site. All rights and property reserved by CEDARS and HKU.

## How to Run
<strong>IMPORTANT</strong>  
Set up an .env file with the following variables:  
UID = "Your HKU email(abc@connect.hku.hk)"  
PASSWORD = "Your HKU Password"  

Set up desired configurations in ```config.yaml```  

Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```


If you want to get the freshest jobs and run the recommendation system, run:
```bash
python main.py --get_data
```

To run the recommendation system on its own:
```bash
python main.py
```


TODO
1. Finish up Similarity Search Feature
2. Set up vector database
3. Optimize scraping feature and edge cases(Connectivity time, invalid inputs, etc.)
4. Multi-page job scraping, optimizer scraping (with batch processing?)
5. Front-end
