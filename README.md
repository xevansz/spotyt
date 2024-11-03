# SpotYt

My learning experience with apis

## Dependencies

Python packages required for:

google-api-python-client  
requests  
urllib (urllib is not installed through pip, it is part of the standard library, so you can just do ```import urllib``` without installation. )  
Flask  
json  
base64

## installation:

```
pip install -U google-api-python-client requests simplejson pybase64 Flask
```

### Working with Both API's

1. re is imported to ignore some common keywords to improve accuracy  
2. Having video or mv in the search query is giving less accuracy, those words are removed.  
3. artist is added along with track in the type of search query because title may contain the artist name. So, adding the artist helps to show related artits songs.  
4. Rest is same, just merge of two codes.  

### /////////////////Things to do////////////////////////
- []adding the songs to playlist.  
- []Adding option to modify the playlist manually.  
- [x]Optimization of code and making it neat.  
- [] Too far goals: adding security protocols.  
- [] Increasing accuracy.  
