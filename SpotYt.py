import googleapiclient.discovery as disc


api_service_name = "youtube" 

results = int(input())

api_key = "AIzaSyBvbRoMnW7cE3D7mmEu9eth1XMySnQbgLc"

youtube = disc.build(api_service_name, "v3", developerKey=api_key)

request = youtube.playlistItems().list(part="snippet",playlistId="PL82qkjWzaJ_9CU-qcpCUl1z8jKhADUtjp",maxResults=results)
response = request.execute()
#print(response)
for i in range(results):
    print(response["items"][i]['snippet']['title'])
