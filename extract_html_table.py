from bs4 import BeautifulSoup
import urllib3
import csv
import sys, os

for i in range(1992, 2018):
    print('Extracting ', str(i), 'data...')
    url = 'https://www.foxsports.com/nba/team-stats?season='+ str(i) + '&category=SCORING&group=1&sort=1&time=0&pos=0&team=1&qual=1&sortOrder=0&opp=0'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features='lxml')
    table = soup.find("table", attrs={"class": "wisbb_standardTable tablesorter"})
    headers = [th.text.encode("utf-8") for th in table.select("tr th")]
    new_headers = []
    for header in headers:
        new_headers.append(header.strip())

    with open(str(i) + '-' + str(i+1) + ".csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(new_headers)
        for row in table.select(".wisbb_fvStand "):
            new_row = []
            tds = [td.text.encode("utf-8") for td in row.find_all("td")]
            for td in tds:            
                new_row.append(' '.join(td.strip().split()))
            wr.writerow(new_row)
        