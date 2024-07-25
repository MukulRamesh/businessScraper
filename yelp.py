import requests

url = "https://api.yelp.com/v3/businesses/search?location=trenton&term=food&radius=30&sort_by=best_match&limit=20"

headers = {
    "accept": "application/json",
    "Authorization": "O_DBg2hPFLOIIU4ZHFO3K7FWICfsYxvvc2G3UvuelWq_zY8fb0x0AZ9TmQ_pHQuazuMn6LincYpR-AQhmWkOR4rhwwO5ie8AMSP5g0BXZhFQB_sGiBXeQc7I9EehZnYx"
}

response = requests.get(url, headers=headers)

print(response.text)