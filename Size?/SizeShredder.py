
import requests, json, time 


class SizeAccountShredder:
    
    def makeAcount(self, firstName, lastName, email, passwd):

        headers = {
            'Host': 'www.size.co.uk',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Origin': 'https://www.size.co.uk',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/json',
            'Referer': 'https://www.size.co.uk/myaccount/register/?',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8'}
        
        data = {
            "saveDetails":"on",
            "firstName":firstName,
            "lastName":lastName,
            "email":email,
            "phone":"",
            "password":passwd,
            "confirmPassword":passwd,
            "billingCountry":"United States|us",
            "billingPostcode":"",
            "billingAddress1":"",
            "billingAddress2":"",
            "billingTown":"",
            "billingCounty":"",
            "useBillingAddress":"on",
            "shippingCountry":"United Kingdom|gb",
            "shippingPostcode":"",
            "shippingAddress1":"",
            "shippingAddress2":"",
            "shippingTown":"",
            "shippingCounty":""}

        requests.post('https://www.size.co.uk/myaccount/registerCustomer/', headers = headers, data = json.dumps(data))

        mobileHeaders = {
            'Host':                   'commerce.mesh.mx',                                                                  
            'Content-Type':           'application/json',                                                                               
            'Connection':             'keep-alive',                                                                          
            'X-API-Key':              'EA0E72B099914EB3BA6BE90A21EA43A9',                                                    
            'Accept':                 '*/*',                                                                                 
            'X-Debug':                '1',                                                                                   
            'Accept-Language':        'en-us',                                                                               
            'User-Agent':             'Size-APPLEPAY/4.0 CFNetwork/808.1.4 Darwin/16.1.0',                                   
            'Accept-Encoding':        'gzip, deflate',                                                                      
            'MESH-Commerce-Channel':  'iphone-app'}
    
        loginData = {
            "password": passwd,
            "username": email
        }


        login = requests.post('https://commerce.mesh.mx/stores/size/customers/login', data = json.dumps(loginData), headers = mobileHeaders)
        

        loginJson = json.loads(login.text)

        customerID = loginJson['ID']
        addressID = json.loads(json.dumps(loginJson['addresses'][0]))['ID']

        txtFile = open('SizeAccounts.txt', 'a')
        txtFile.write('Email : {}\nPassword : {}\nCustomer ID : {}\nAddress ID : {}\n\n'.format(email, passwd, customerID, addressID))
        txtFile.close()
    
    def clearCart(self, email, passwd):
        
        sesh = requests.Session()
        
        headers = {
            'Host':                   'commerce.mesh.mx',                                                                  
            'Content-Type':           'application/json',                                                                               
            'Connection':             'keep-alive',                                                                          
            'X-API-Key':              'EA0E72B099914EB3BA6BE90A21EA43A9',                                                    
            'Accept':                 '*/*',                                                                                 
            'X-Debug':                '1',                                                                                   
            'Accept-Language':        'en-us',                                                                               
            'User-Agent':             'Size-APPLEPAY/4.0 CFNetwork/808.1.4 Darwin/16.1.0',                                   
            'Accept-Encoding':        'gzip, deflate',                                                                      
            'MESH-Commerce-Channel':  'iphone-app'}
        

        loginData = {
            "password": passwd,
            "username": email}

        sesh.post('https://commerce.mesh.mx/stores/size/customers/login', data = json.dumps(loginData), headers = headers)

        print ('[{}] : Checking cart'.format(email))
        
        cart = sesh.get('https://commerce.mesh.mx/stores/size/carts/key here' , headers = headers)   
    
        products = json.loads(cart.text)['products']

        if len(products) == 0:
            print ('[{}] : No products in cart'.format(email))
 
        else :
            print ('[{}] : {} products in cart, deleting...'.format(email, len(products)))
            for i in products:
                PID = json.loads(json.dumps(i))['SKU']
                sesh.put('https://commerce.mesh.mx/stores/size/carts/key here/{}'.format(PID) , headers = headers, data = json.dumps({ "quantity": 0 }))
                print ('[{}] : {} delteted'.format(email, PID))

        print ('[{}] : Cart Cleared'.format(email)) 

    def checkCart(self, email, passwd):
        
        sesh = requests.Session()
        
        headers = {
            'Host':                   'commerce.mesh.mx',                                                                  
            'Content-Type':           'application/json',                                                                               
            'Connection':             'keep-alive',                                                                          
            'X-API-Key':              'EA0E72B099914EB3BA6BE90A21EA43A9',                                                    
            'Accept':                 '*/*',                                                                                 
            'X-Debug':                '1',                                                                                   
            'Accept-Language':        'en-us',                                                                               
            'User-Agent':             'Size-APPLEPAY/4.0 CFNetwork/808.1.4 Darwin/16.1.0',                                   
            'Accept-Encoding':        'gzip, deflate',                                                                      
            'MESH-Commerce-Channel':  'iphone-app'}
        

        loginData = {
            "password": passwd,
            "username": email}

        sesh.post('https://commerce.mesh.mx/stores/size/customers/login', data = json.dumps(loginData), headers = headers)
        
        cart = sesh.get('https://commerce.mesh.mx/stores/size/carts/key here' , headers = headers)   
    
        products = json.loads(cart.text)['products']

        print ('[{}] : {} products in cart'.format(email, len(products)))

    def getKeys(self, email, passwd):
        
        headers = {
            'Host': 'www.size.co.uk',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Origin': 'https://www.size.co.uk',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/json',
            'Referer': 'https://www.size.co.uk/myaccount/register/?',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8'}     

        loginData = json.dumps({
            "password": passwd,
            "username": email
        })


        login = requests.post('https://commerce.mesh.mx/stores/size/customers/login', data = loginData, headers = mobileHeaders)
        
        loginJson = json.loads(login.text)

        customerID = loginJson['ID']
        addressID = json.loads(json.dumps(loginJson['addresses'][0]))['ID']

        print ('[{}] : Customer ID - {}, Address ID - {}'.format(email, customerID, addressID))


class SizeShredder:
 
    def t(self):
        
        return str(time.strftime('%H:%M:%S', time.localtime()))

    def checkFrontPage(self):
        
        headers = {
            'Host':                   'commerce.mesh.mx',                                                                  
            'Content-Type':           'application/json',                                                                               
            'Connection':             'keep-alive',                                                                          
            'X-API-Key':              'EA0E72B099914EB3BA6BE90A21EA43A9',                                                    
            'Accept':                 '*/*',                                                                                 
            'X-Debug':                '1',                                                                                   
            'Accept-Language':        'en-us',                                                                               
            'User-Agent':             'Size-APPLEPAY/4.0 CFNetwork/808.1.4 Darwin/16.1.0',                                   
            'Accept-Encoding':        'gzip, deflate',                                                                      
            'MESH-Commerce-Channel':  'iphone-app'}

        homepage = requests.get('https://commerce.mesh.mx/stores/footpatrol/products/category/footwear?from=0&max=30&channel=iphone-app&sort=created_date', headers = headers)


        for i in json.loads(homepage.text)['products']:
            j = json.loads(json.dumps(i))
            print j['name']


    def mobileBot(self, pid, checkoutPreset):
        
        headers = {
            'Host':                   'commerce.mesh.mx',                                                                  
            'Content-Type':           'application/json',                                                                               
            'Connection':             'keep-alive',                                                                          
            'X-API-Key':              'EA0E72B099914EB3BA6BE90A21EA43A9',                                                    
            'Accept':                 '*/*',                                                                                 
            'X-Debug':                '1',                                                                                   
            'Accept-Language':        'en-us',                                                                               
            'User-Agent':             'Size-APPLEPAY/4.0 CFNetwork/808.1.4 Darwin/16.1.0',                                   
            'Accept-Encoding':        'gzip, deflate',                                                                      
            'MESH-Commerce-Channel':  'iphone-app'}

        
        sesh = requests.Session()

        email = checkoutPreset['Email']

        print ('[{}] - [{}] : Task Started'.format(self.t(), email))

        print ('[{}] - [{}] : Logging in with password - {}'.format(self.t(), email, checkoutPreset['Password']))

        loginData = json.dumps({
            "password": checkoutPreset['Password'],
            "username": email
        })

        login = sesh.post('https://commerce.mesh.mx/stores/size/customers/login', data = json.dumps(loginData), headers = headers)
        
        print ('[{}] - [{}] : Login complete, adding to cart '.format(self.t(), email,))

        qtyJson = json.dumps({"quantity": 1})

        while True :
            print ('[{}] - [{}] : Adding to cart with PID {}'.format(self.t(), email, pid))

            try :  
                add = sesh.put('https://commerce.mesh.mx/stores/size/carts/keyhere/{}'.format(pid) , headers = headers, data = qtyJson)

                if 'error' not in add.text:
                    break 
                else :
                    print ('[{}] - [{}] : Could not add to cart with PID {}, retrying...'.format(self.t(), email, pid))

            except :
                print ('[{}] - [{}] : Error to cart with PID {}, retrying'.format(self.t(), email, pid))


        print ('[{}] - [{}] : Succsesfully added to cart with PID {}, checking out...'.format(self.t(), email, pid))

        
        addyData = json.dumps({
            "billingAddressID": checkoutPreset['aID'],
            "customerID": checkoutPreset['cID'],
            "deliveryAddressID": checkoutPreset['aID']
        })

        while True :
            print ('[{}] - [{}] : Submiting checkout data...'.format(self.t(), email))

            try :
                checkout = sesh.put('https://commerce.mesh.mx/stores/size/carts/key here', data = addyData, headers = headers)
                break 
            
            except :
                print ('[{}] - [{}] : Error submiting checkout data, retrying...'.format(self.t(), email))
        

        print ('[{}] - [{}] : Finished submiting checkout data, moving to card page...'.format(self.t(), email))
        
        cardPostData = json.dumps({
            "terminals": {
                "failureURL": "https://fail",
                "successURL": "https://ok",
                "timeoutURL": "https://timeout"
                },
            "type": "CARD"
        })

        while True :
            print ('[{}] - [{}] :  Atempting to reach card page...'.format(self.t(), email))            
            
            try :
                cardPost = sesh.post('https://commerce.mesh.mx/stores/size/carts/key here/hostedPayment', data = cardPostData, headers = headers)
                break 
            except :
                print ('[{}] - [{}] : Failed reaching card page, retring...'.format(self.t(), email))


        print ('[{}] - [{}] : Succsesfully reached card page...'.format(self.t(), email))

        jsonCartsData = json.loads(cardPost.text)
        hostedPaymentID = jsonCartsData['ID']
        terminalEndPoints = jsonCartsData['terminalEndPoints']
        cardEntryURL = json.loads(json.dumps(terminalEndPoints))['cardEntryURL']
        httpsSessID = cardEntryURL[44:80]

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
                cardConfirm = sesh.post('https://hps.datacash.com/hps/?', data = cardData )
            
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
                checkResult = sesh.post('https://commerce.mesh.mx/stores/size/payments/{}/hostedpaymentresult'.format(hostedPaymentID), headers = headers,  data = checkResultData) 
                status = json.loads(checkResult.text)['status']
                print ('[{}] - [{}] : Finished checking payment status, Status - {}'.format(self.t(), email, status))
                break 
            
            except:
                print ('[{}] - [{}] : Failed checking payment status, DTS ID - {}, Hosted Payment ID - {}, retrying...'.format(self.t(), email, dts, hostedPaymentID))

        
        print ('[{}] - [{}] : Finished task, status - {}'.format(self.t(), email, status))



checkoutPreset = {
    'Email' : '',
    'Password' : '',
    'cID' : '',
    'aID' : '',
    'Card' : '',
    'CardExpMonth' : '',
    'CardExpYear' : '',
    'CVV' : ''
}

instance = SizeShredder()
#instance.mobileBot('', checkoutPreset )

instance.checkFrontPage()













