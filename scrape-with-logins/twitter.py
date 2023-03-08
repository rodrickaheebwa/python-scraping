# Method 1
# copying the get request

import json

"""
Visit your twitter homepage
Under the network tab, pick a 'HomeTimeline' or 'HomeLatestTimeline' request
Generate its python code from curlconvertor.com and paste it here
"""

response = '' # placeholder for the response variable to avoid errors
data = json.loads(response.text)
# loads deserializes, so 'data' is now an object(dictionary)
# while 'response.text' is actually a json string

# with open('.\\test\\twitter.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

entries = data["data"]["home"]["home_timeline_urt"]["instructions"][0]["entries"]
number_of_untweets = 0

for entry in entries:
    try:
        tweet_results = entry["content"]["itemContent"]["tweet_results"]["result"] # core (only for user), legacy
        user_results = entry["content"]["itemContent"]["tweet_results"]["result"]["core"]["user_results"]["result"] # legacy
        account_name = user_results["legacy"]["name"]
        screen_name = user_results["legacy"]["screen_name"]
        tweet_text = tweet_results["legacy"]["full_text"]
        tweet_date = tweet_results["legacy"]["created_at"]
        
        print(account_name)
        print(screen_name)
        print(tweet_text)
        print(tweet_date)
        print('\n')
    except:
        number_of_untweets += 1
        continue

print('\n Number of entries: ', len(entries), '\n')
print('\n Number of tweets: ', len(entries) - number_of_untweets)