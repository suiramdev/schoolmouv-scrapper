import requests
from bs4 import BeautifulSoup
import os

baseURL = "https://www.schoolmouv.fr"
classURL = "/terminale"
fetchURLs = [ # HTML pages to download
    "/fiche-de-cours",
    "/fiche-de-revision",
    "/fiche-methode-bac",
    "/auteur",
    "/definition",
    "/personnages-historique"
]

if __name__ == "__main__":
    for subjectEl in BeautifulSoup(requests.get((baseURL + classURL)).text, features="html.parser").find_all(class_="subject-content"):
        parentFolder = subjectEl.get("href").split("/")[-1]
        for sheetNameEl in BeautifulSoup(requests.get(baseURL + subjectEl.get("href")).text, features="html.parser").find_all(class_="sheet-name"):
            childFolder = sheetNameEl.get("href").split("/")[-2]
            for fetchURL in fetchURLs:
                request = requests.get((baseURL + sheetNameEl.get("href"))[:-1] + fetchURL)
                if request.status_code == 200:
                    fileName = f"data/{parentFolder}/{childFolder}{fetchURL}.html"
                    os.makedirs(os.path.dirname(fileName), exist_ok=True)
                    with open(fileName, "w", encoding="utf-8") as f:
                        f.write(request.text)