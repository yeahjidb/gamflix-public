from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import csv

f = open("C:\projects\myproject\pybo\static\game.csv", "r", encoding="utf-8")
_csv = csv.reader(f)
s = open("C:\projects\myproject\pybo\static\game.csv", "w", encoding="utf-8")
_csv2 = csv.writer(s)

count = sum(1 for row in _csv)
print("Total Count : " + str(count))
proceed = 1

f.seek(0)
for line in _csv:
    print("Get Game Data... (" + str(proceed) + "/" + str(count) + ")...\t\t", end='')

    total = []
    response = urllib.request.urlopen(line[0])
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    if (line[1] == "Steam"):
        game_title = soup.find('div', {'class': 'apphub_AppName'})
        total.append(game_title.get_text())

        print("Done.\t\t", end='')
        print(game_title.get_text() + "(Steam)")

        try:
            game_price = soup.find('div', {'class': 'game_purchase_price price'})
            total.append(game_price.get_text().strip())
        except:
            try:
                game_price = soup.find('div', {'class': 'discount_original_price'})
                total.append(game_price.get_text().strip())
            except:
                game_price = "UNKNOWN"
                total.append(game_price)

        game_sub = soup.find('div', {'class': 'glance_ctn_responsive_right'})
        game_sub = game_sub.get_text().replace("+", "").replace("\t", " ").split("\n")
        for i in range(0, len(game_sub)):
            game_sub[i] = game_sub[i].strip()
        total = total + game_sub[6:-3]

        # print(total)
        _csv2.writerow(total)

    proceed = proceed + 1
