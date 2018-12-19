import requests, json, time, sys, urllib
from threading import Thread 


class scrapeO:

	def __init__(self):

		pids = []
		
		txt = open("SizeScrapePIDS.txt", 'r')
		for i in txt :
			pids.append(int(i))

		txt.close()

		self.pids = pids

	
	def scrapeImages(self, start, stop):

		pidsList = self.pids 


		for pid in (start, stop + 1):

			if pid not in pidsList:

				image = requests.get('http://i1.adis.ws//i//jpl//sz_{}_a?w=100&h=100'.format(pid))
				
				if 'File not found' in image.content :
					pass 

				else :
					bigImage = requests.get('http://i1.adis.ws//i//jpl//sz_{}_a?w=1000&h=1000'.format(pid))
					output = open(('{}.png'.format(pid)),"wb")
					output.write(bigImage.content)
					output.close()

					txt = open('SizeScrapePIDS.txt', 'a')
					txt.write(str(pid) + '\n')
					txt.close()
			
			
			
	def checkPID(self, pid):

		sizeList = []
		
		headers = {
			'Host':'commerce.mesh.mx' ,                                                                   
			'Connection':'keep-alive' ,                                                                        
			'X-API-Key': 'EA0E72B099914EB3BA6BE90A21EA43A9' ,                                                  
			'Accept':'*/*' ,                                                                            
			'X-Debug':'1' ,                                                                                
			'Accept-Language':'en-us'  ,                                                                          
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' ,                                  
			'Accept-Encoding':'gzip, deflate'}

		r = requests.get(('https://commerce.mesh.mx/stores/size/products/{}'.format(pid)), headers = headers)

		text = r.text

		if 'Product could not be found' in text :
			print 'Data not loaded for pid {}'.format(pid)


		else :
			#print text
			data = json.loads(text)
			priceData = json.loads(json.dumps(data['price']))

			isVis = data['isVisible']
			name = data['name']
			image = data['mainImage']
			price = priceData['amount'] + ' Pounds'
			stockStatus = data['stockStatus']
			color = data['colourDescription']
			url = data['URL']
			addDate = data['dateAdded']
			maxCart = data['maximumCartQuantity']

			if data['oneSize'] == False :
				sizeData = json.loads(json.dumps(data['options']))
				for i in sizeData:
					d = json.loads(json.dumps(sizeData[i]))

					sku = d['SKU']
					ss = d['stockStatus']
					clr = d['colourDescription']
					sz = d['size']

					sizeList.append('%s :\n\tStock status : %s\n\tSKU : %s\n\tColor : %s\n' % (i, ss, sku, clr)) 
			
			else :
				pass

			fileName = ('%s.txt' % (pid))

			txt = open(fileName, 'w')
			info = 'Name : %s\n\nPID : %s\n\nURL : %s\n\nDate added : %s\n\nPrice : %s\n\nColor : %s\n\nImage URL : %s\n\nIs visable : %s\n\nIs in stock : %s\n\nMax cart quanity : %s\n\n' % (name, pid, url, addDate, price, color, image, isVis, stockStatus, maxCart)
			for i in sizeList:
				info += ('\n'+i) 
			txt.write(info)
			txt.close()



s = scrapeO()


#for i in range(200000, 300000, 5000):
#	Thread(target = s.scrapeImages, args = (i, i+5000)).start()
















