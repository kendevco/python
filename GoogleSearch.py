import csv 
from googleapiclient.discovery import build 

api_key = 'AIzaSyB0rv0QDGWy7Gno284IybZVNB9BDJzSEPs' 
search_engine_id = '16331af4b4dc043f5'

service = build("customsearch", "v1", developerKey=api_key)

query = "site:www.bjc.org/newsroom"
page_size = 10
num_pages = 10

csv_file = open('bjc_newsroom_links.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Link'])

for page in range(1, num_pages+1):
  start = page_size * (page - 1) + 1

  response = service.cse().list(q=query, cx=search_engine_id, start=start).execute()
  
  items = response.get('items', [])

  if not items: 
    print(f"No items found on page {page}")
    continue

  for item in items:
    csv_writer.writerow([item['link']])

csv_file.close()