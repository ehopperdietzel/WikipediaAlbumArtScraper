import requests
import shutil
from bs4 import BeautifulSoup

#https://en.wikipedia.org/w/index.php?title=Category:Album_covers&pagefrom=0&subcatfrom=0&filefrom=Acanofbees.jpg%0AAcanofbees.jpg#mw-category-media
baseURL = "https://en.wikipedia.org";
firstURL = "https://en.wikipedia.org/wiki/Category:Album_covers?from=0"
counter = 0

def getArtwork(URL):
    global baseURL
    global counter
    print("Pagina actual: "+URL)
    r = requests.get(url = URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    group = soup.find("div", {"class": "mw-category-group"})
    aTags = group.findAll("a");
    for a in aTags:
        counter = counter + 1
        photoPage = requests.get(url = baseURL+a["href"])
        photoSoup = BeautifulSoup(photoPage.content, 'html.parser')
        imageCont = photoSoup.find("div", {"id": "file"})
        imageTag = imageCont.find("a")["href"]
        imageURL = "https:"+imageTag
        imageData = requests.get(imageURL, stream=True)
        with open("albums/"+str(counter)+'.png', 'wb') as out_file:
            shutil.copyfileobj(imageData.raw, out_file)
        del imageData
    nextURLa = soup.find("a", string= "next page")["href"]
    getArtwork(baseURL+nextURLa)
getArtwork(firstURL)
