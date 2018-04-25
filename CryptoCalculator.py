import time
import urllib
import json
import datetime

try:
    #tries to read file   
    f = open("Coins.json", "r")
    userCoin = json.loads(f.read())
    f.close()
except IOError:
    #if file doesn't exist then it's created
    f = open("Coins.json", "w+")
    json.dump({}, f)
    f.close()
    f = open("Coins.json", "r")
    userCoin = json.loads(f.read())
    f.close()

choice1 = raw_input("Would you like to add or update cryptocurrency transactions? (y/n) ")
#verifies answer is valid
while choice1 != "y" and choice1 != "n":
    print "Answer must be a y (for yes) or an n (for no)"
    choice1 = raw_input("Would you like to add or update cryptocurrency transactions? (y/n) ")

if choice1 == "y":    

    badInput = True
    while badInput:
        coinName = raw_input("What Coin? (Use symbol,ex:BTC): ")
        #accesses API for list of cryptocurrencies
        webpage = urllib.urlopen("https://www.cryptocompare.com/api/data/coinlist")
        data = json.loads(webpage.read())
        for coin in data["Data"]:
            if coin == coinName:
                badInput = False
                break
        if badInput:
            print "Answer must use the correct symbol for the cryptocurrency you would like to enter (case sensitive)"

    badInput = True
    while badInput:
        badInput = False
        date = raw_input("Day? (MM/DD/YYYY): ")
        try:
            #parses for correct date
            year = int(date[6:])
            month = int(date[:2])
            day = int(date[3:5])
            hour = 0
            #datetime.datetime(year,month,day,hour)

            localTime = time.struct_time((year, month, day, 0, 0, 0, 0, 0, 0))
            #converts to epoch time
            epochTime = int(time.mktime(localTime))
        except:
            print("Make sure the date you input is in the correct format")
            badInput = True
            continue

        #validates date is within earliest time on API
        if epochTime > time.time() or epochTime < 1314316800:
            print("Make sure date is valid")
            badInput = True
        if not badInput:
            epTime = str(epochTime)
            webpage = urllib.urlopen("https://min-api.cryptocompare.com/data/pricehistorical?fsym="+coinName+"&tsyms=USD&ts=" + epTime)
            data = json.loads(webpage.read())
            #checks to see if inputted date is after the creation of that cryptocurrency 
            if data[coinName]["USD"] == 0:
                badInput = True
                print("Make sure date is not before cryptocurrency was created")
    epTime = str(epochTime)

    
    webpage = urllib.urlopen("https://min-api.cryptocompare.com/data/pricehistorical?fsym="+coinName+"&tsyms=USD&ts=" + epTime)
    data = json.loads(webpage.read())
    
    badInput = True
    while badInput:
        badInput = False
        coinUSD = raw_input("How much money did you spend on " + coinName + " on " + date + ": ")
        try:
            #checks if amount is a float
            coinUSD = float(coinUSD)
        except:
            print("Make sure you entered a valid answer")
            badInput = True
            continue
        #makes sure input amount is a positive number
        if coinUSD < 0:
            badInput = True
            print "Make sure answer is not negative"
    #gets amount of coins that was purchased at the time, so that system can convert to current price
    coinAmount = coinUSD/data[coinName]["USD"]
                               
    try:
        #tries to update an existing coin
        userCoin[coinName]["amount"] += coinAmount
        userCoin[coinName]["paid"] += coinUSD

    except:
        #if coin doesn't exist this adds it
        userCoin.update({coinName:{"paid": coinUSD,"amount":coinAmount}})
    #writes all new information to file for saving
    with open('Coins.json', 'w') as outfile:
        json.dump(userCoin, outfile)


#loops through all coins in file
for coin in userCoin:
    #gets current price information for coin being accessed
    webpage = urllib.urlopen("https://min-api.cryptocompare.com/data/pricehistorical?fsym="+coin+"&tsyms=USD&ts=" + str(int( time.time() ) ) )
    data = json.loads(webpage.read())

    print "Your net gain/loss for " + coin + ": " + str(float(data[coin]["USD"]) * userCoin[coin]["amount"] - userCoin[coin]["paid"])
