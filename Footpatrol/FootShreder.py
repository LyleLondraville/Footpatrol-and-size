
import requests, json, time, random
from threading import Thread 

class FootShredder:

    def __init__(self):
        self.headers = {
            'Host':                   'commerce.mesh.mx',                                                                  
            'Content-Type':           'application/json',                                                                               
            'Connection':             'keep-alive',                                                                          
            'X-API-Key':              '5F9D749B65CD44479C1BA2AA21991925',                                                    
            'Accept':                 '*/*',                                                                                 
            'X-Debug':                '1',                                                                                   
            'Accept-Language':        'en-us',                                                                               
            'User-Agent':             'FootPatrol/2.0 CFNetwork/808.1.4 Darwin/16.1.0',                                   
            'Accept-Encoding':        'gzip, deflate',                                                                      
            'MESH-Commerce-Channel':  'iphone-app'}
 
    
    def t(self):
        
        return str(time.strftime('%H:%M:%S', time.localtime()))

    
    def checkFrontPage(self, keywordList):

        jLoads = json.loads 
        jDumps = json.dumps
        Found = False 
        
        headers = self.headers

        while Found == False : 
            print ('Checking...')
            
            homepage = requests.get('https://commerce.mesh.mx/stores/footpatrol/products/category/footwear?from=0&max=30&channel=iphone-app&sort=created_date', headers = headers)
            
            for i in json.loads(homepage.text)['products']:
                j = jLoads(jDumps(i))
                if all(kw in j['name'].lower() for kw in keywordList):
                    link = j['href']
                    Found = True 


        return link

    
    def checkForNew(self, keywordList):
        old = []
        new = []

        Found = False 
        
        oldAppend = old.append 
        newAppend = new.append 

        jLoads = json.loads 
        jDumps = json.dumps

        headers = self.headers

        homepage = requests.get('https://commerce.mesh.mx/stores/footpatrol/products/category/footwear?from=0&max=30&channel=iphone-app&sort=created_date', headers = headers)


        for i in json.loads(homepage.text)['products']:
            oldAppend(i)

        while Found == False  :
            
            homepage = requests.get('https://commerce.mesh.mx/stores/footpatrol/products/category/footwear?from=0&max=30&channel=iphone-app&sort=created_date', headers = headers)
            
            for i in json.loads(homepage.text)['products']:
                newAppend(i)

            newLis = list(set(new) - set(old))

            if newLis != []:
                
                for i in newLis:
                    j = jLoads(jDumps(i))
                    
                    if all(kw in j['name'].lower() for kw in keywordList):
                        link = j['href']
                        Found = False 
                        break 

                    else :
                        oldAppend(i)
            else :
                pass 

            newLis[:] = []  

        return link

    
    def getSizes(self, href):

        jLoads = json.loads
        jDumps = json.dumps
        
        headers = self.headers

        masterDict = {}

        jData = jLoads((requests.get('{}?expand=variations,informationBlocks,customisations&channel=iphone-app'.format(href), headers = headers)).text)

        options = jLoads(jDumps(jData['options']))

        for o in options :
            j = jLoads(jDumps(options[o]))
            masterDict.update( {float(o) : j['SKU']} )

        return masterDict
  
    
    def refPID(self, pid, timeout):
        
        masterDict = {}
        found = False 
        
        headers = {
            'Host':'commerce.mesh.mx' ,                                                                   
            'Connection':'keep-alive' ,                                                                        
            'X-API-Key': '5F9D749B65CD44479C1BA2AA21991925' ,                                                  
            'Accept':'*/*' ,                                                                            
            'X-Debug':'1' ,                                                                                
            'Accept-Language':'en-us'  ,                                                                          
            'User-Agent':'FootPatrol/2.0 CFNetwork/808.1.4 Darwin/16.1.0' ,                                  
            'Accept-Encoding':'gzip, deflate'}



        while found == False :

            time.sleep(timeout)

            try :

                r = requests.get(('https://commerce.mesh.mx/stores/footpatrol/products/%s' % ( pid)), headers = headers)

                text = r.text

                if 'Product could not be found' in text :
                    print ('Data not loaded for pid {}'.format(pid))


                else :
                    data = json.loads(text)

                    if data['oneSize'] == False :
                        sizeData = json.loads(json.dumps(data['options']))
                        
                        if sizeData != {}:
                            
                            for i in sizeData:
                                
                                d = json.loads(json.dumps(sizeData[i]))
                                sku = d['SKU']

                                masterDict.update({float(i):str(sku)})

                            found = True 


                        else :
                            pass 
                    else :
                        pass


            
            except :
                print ('Error')

        return masterDict
    

    def test(self):


        r = requests.get('https://commerce.mesh.mx/stores/footpatrol/carts/key here', headers= self.headers)
        print (r.text)

    def mobileBot(self, pid, checkoutPreset):
        
        headers = self.headers

        
        sesh = requests.Session()

        email = checkoutPreset['Email']

        print('[{}] - [{}] : Retrieving cart data...'.format(self.t(), email, pid))

        cart = sesh.get('https://commerce.mesh.mx/stores/footpatrol/carts/key here', headers = headers)

        print('[{}] - [{}] : Removing cart products...'.format(self.t(), email, pid))

        products = json.loads(cart.text)['products']

        for p in products:
            j = json.loads(json.dumps(p))
            sku = j['SKU']
            sesh.put('https://commerce.mesh.mx/stores/footpatrol/carts/key here/{}'.format(sku), data = json.dumps({'quantity' : 0}), headers = headers)

        print('[{}] - [{}] : Done removing cart products, adding to cart...'.format(self.t(), email, pid))

        qtyJson = json.dumps({"quantity": 1})

        while True :
            print ('[{}] - [{}] : Adding to cart with PID {}'.format(self.t(), email, pid))

            try :  
                add = sesh.put('https://commerce.mesh.mx/stores/footpatrol/carts/key here/{}'.format(pid) , headers = headers, data = qtyJson)

                text = add.text

                if 'error' not in text:
                    if text != '':
                        addJson = json.loads(text)
                        break
                    else :
                        print('[{}] - [{}] : Could not add to cart with PID {}, retrying...'.format(self.t(), email, pid))
                else :
                    print ('[{}] - [{}] : Could not add to cart with PID {}, retrying...'.format(self.t(), email, pid))

            except :
                print ('[{}] - [{}] : Error to cart with PID {}, retrying'.format(self.t(), email, pid))


        print ('[{}] - [{}] : Succsesfully added to cart with PID {}, cart total {}, checking out...'.format(self.t(), email, pid, addJson['cartCount']))

        addyData = json.dumps({         
            "addresses": [{
                "address1": checkoutPreset['addy1'],
                "country": "United States",
                "county": checkoutPreset['state'],
                "isPrimaryAddress": True,
                "isPrimaryBillingAddress": True,
                "locale": "us",
                "postcode": checkoutPreset['zip'],
                "town": checkoutPreset['city']}],
            "email": email,
            "firstName": checkoutPreset['FirstName'],
            "gender": "",
            "isGuest": True,
            "lastName": checkoutPreset['LastName'],
            "phone": checkoutPreset['phone'],
            "title": ""})

        
        while True:
            print ('[{}] - [{}] : Submitting address data...'.format(self.t(), email))

            try :
                addySubmit = sesh.post('https://commerce.mesh.mx/stores/footpatrol/customers', data = addyData, headers = headers)

                try :
                    print('[{}] - [{}] : Successfully submitted address data, loading response...'.format(self.t(), email))

                    addyJson = json.loads(addySubmit.text)

                    cID = addyJson['ID']
                    aID = (json.loads(json.dumps(addyJson['addresses'][0])))['ID']

                    keyData = json.dumps({
                        "billingAddressID": aID,
                        "customerID": cID,
                        "deliveryAddressID": aID
                    })

                    break

                except :
                    print('[{}] - [{}] : Failed to load address response, retrying...'.format(self.t(), email))
            
            except :
                print ('[{}] - [{}] : Failed to submit address data, retrying...'.format(self.t(), email))
            



        while True :
            print ('[{}] - [{}] : Submitting checkout data...'.format(self.t(), email))

            try :
                checkout = sesh.put('https://commerce.mesh.mx/stores/footpatrol/carts/key here', data = keyData, headers = headers)
                json.loads(checkout.text)
                break
            
            except :
                print ('[{}] - [{}] : Error submitting checkout data, retrying...'.format(self.t(), email))

        print ('[{}] - [{}] : Finished submitting checkout data, moving to card page...'.format(self.t(), email))
        
        cardPostData = json.dumps({
            "terminals": {
                "failureURL": "https://fail",
                "successURL": "https://ok",
                "timeoutURL": "https://timeout"
                },
            "type": "CARD"
        })

        while True :
            print ('[{}] - [{}] :  Attempting to reach card page...'.format(self.t(), email))
            
            try :
                cardPost = sesh.post('https://commerce.mesh.mx/stores/footpatrol/carts/key here/hostedPayment', data = cardPostData, headers = headers)

                print('[{}] - [{}] :  Reached card page, loading json data...'.format(self.t(), email))

                print (cardPost.text)

                try :
                    jsonCartsData = json.loads(cardPost.text)
                    hostedPaymentID = jsonCartsData['ID']
                    terminalEndPoints = jsonCartsData['terminalEndPoints']
                    cardEntryURL = json.loads(json.dumps(terminalEndPoints))['cardEntryURL']

                    httpsSessID = cardEntryURL[44:80]

                    print('[{}] - [{}] : Done loading json data, succsesfully got card page data, getting card page...'.format(self.t(), email))

                    break

                except :
                    print('[{}] - [{}] : Failed loading json data, retring...'.format(self.t(), email))

            except :
                print ('[{}] - [{}] : Failed reaching card page, retring...'.format(self.t(), email))



        while True :
            print ('[{}] - [{}] : Getting card page, HTTPS session id - {}'.format(self.t(), email, httpsSessID))
            
            try :
                cardEntry = sesh.get(cardEntryURL)
                break 
            except :
                print ('[{}] - [{}] : Failed getting card page, HTTPS session id - {}, retrying....'.format(self.t(), email, httpsSessID))

        print ('[{}] - [{}] : Succsesfully got card page, HTTPS session id - {}, submiting card data...'.format(self.t(), email, httpsSessID))

        cardData = {
            'card_number':   checkoutPreset['Card'],
            'exp_month':     checkoutPreset['CardExpMonth'],
            'exp_year':      checkoutPreset['CardExpYear'],
            'cv2_number':    checkoutPreset['CVV'],
            'issue_number':  '',
            'HPS_SessionID':  httpsSessID,
            'action':        'confirm',
        }

        while True :
            print ('[{}] - [{}] : Subbmiting card data, HTTPS session id - {}'.format(self.t(), email, httpsSessID))

            try :
                sesh.post('https://hps.datacash.com/hps/?', data = cardData )
            
            except requests.exceptions.RequestException as e:  
                try:
                    dts = str(e)[89:105]
                    int(dts)
                    break 
                
                except :
                    print ('[{}] - [{}] : Failed submiting card data, HTTPS session id - {}, retrying...'.format(self.t(), email, httpsSessID))

        

        print ('[{}] - [{}] : Succsesfully submited card data, HTTPS session id - {}, checking to see if the payment went through'.format(self.t(), email, httpsSessID))
        

        checkResultData = json.dumps({
            "HostedPaymentPageResult": "https://ok/?dts_reference={}".format(dts)
        })
    
        while True :
            print ('[{}] - [{}] : Checking payment status, DTS ID - {}, Hosted Payment ID - {}'.format(self.t(), email, dts, hostedPaymentID))
            
            try :
                checkResult = sesh.post('https://commerce.mesh.mx/stores/footpatrol/payments/{}/hostedpaymentresult'.format(hostedPaymentID), headers = headers,  data = checkResultData) 
                status = json.loads(checkResult.text)['status']
                print ('[{}] - [{}] : Finished checking payment status, Status - {}'.format(self.t(), email, status))
                break 
            
            except:
                print ('[{}] - [{}] : Failed checking payment status, DTS ID - {}, Hosted Payment ID - {}, retrying...'.format(self.t(), email, dts, hostedPaymentID))

        
        print ('[{}] - [{}] : Finished task, status - {}'.format(self.t(), email, status))


    def Shred(self, keywordList, checkForNew, sizeList, checkoutPreset):

        
        if checkForNew == False :
            url = self.checkForNew(keywordList)
        else :
            url = self.checkFrontPage(keywordList)

        sDict = self.getSizes(url)
        count = 1
        baseEmail = checkoutPreset['Email']

        for i in sizeList:
            
            checkoutPreset['Email'] = '{}+{}@gmail.com'.format(baseEmail, count)
            
            try :
                size = sDict[i]
            except:
                size = sDict[random.randrange(0, len(sDict.keys()), 1)]

            Thread( target = self.mobileBot, args = (size, checkoutPreset)).start()

            count += 1

    
    def ShredPID(self, pidList, checkoutPreset):
       
        count = 1
        baseEmail = checkoutPreset['Email']
        
        for i in pidList:
            checkoutPreset['Email'] = '{}+{}@gmail.com'.format(baseEmail, count)
            Thread(target = self.mobileBot, args = (i, checkoutPreset)).start()
            count += 1


checkoutPreset = {
    'Email' : '',
    'FirstName' : '',
    'LastName' : '',
    'addy1' : '',
    'addy2' : '',
    'state' : '',
    'city' : '',
    'zip' : '',
    'phone' : '',
    'Card' : '',
    'CardExpMonth' : '',
    'CardExpYear' : '',
    'CVV' : ''
}


s = FootShredder()

#print (s.refPID(253917 , 1))
#d = {6.5: '253917.472433', 7.0: '253917.472091', 8.0: '253917.472093', 8.5: '253917.472095', 11.0: '253917.472275', 14.0: '253917.472431'}
#s.mobileBot('253917.472275', checkoutPreset)
s.test()
'''
s = FootShredder()
masterDict = s.refPID(287004, 3) 
pidList = []

try :
    for i in range(0,10):
        pidList.append(masterdict[10.0])
        pidList.append(masterdict[11.0]) 
except :
    for i in range(0,20):
        pidList.append(masterdict[masterdict.keys()[0]])


s.ShredPID(pidList, checkoutPreset)
'''
         





















