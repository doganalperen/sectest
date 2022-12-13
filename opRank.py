from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tranco import Tranco
import csv

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
t = Tranco(cache=True, cache_dir='.tranco')
latest_list = t.list()

with open("targets_ua.csv", 'r') as inputFile:
	csvreader = csv.reader(inputFile)
	with open("operationsl.csv", 'w', newline='') as outputFile:
		writer = csv.writer(outputFile)
		i = 0
		for row in csvreader:
			print('in for')
			if(i > 0):
				newRow = row
				try:
					if(row[2][0:4] != 'http'):
						url = 'http://' + row[2]
					else:
						url = row[2]
					urlForRank = url
					if urlForRank.find('http') != -1:
						urlForRank = urlForRank[(urlForRank.find("//") + 2):]
					if urlForRank[0:4] == "www." or urlForRank[0:4] == "web.":
						urlForRank = urlForRank[4:]
					if urlForRank.find('/') != -1:
						urlForRank = urlForRank[:urlForRank.find('/')]
					rank = latest_list.rank(urlForRank)
					driver.get(url)
					newRow.append('True')
				except:
					newRow.append('False')
				finally:
					newRow.append(str(rank))
					writer.writerow(newRow)
			else:
				newRow = row
				newRow.append('IsOperational')
				newRow.append('Ranking')
				writer.writerow(row)
			i = i + 1
			print(i)

driver.quit()


