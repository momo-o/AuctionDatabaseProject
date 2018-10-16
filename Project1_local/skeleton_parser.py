
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        columnSeparator = "|"
        tableitems = ""
        tablecategory = ""
        tableuser = ""
        tablebid = ""
        tablecatitem = ""
        tablesell =""
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            itemID = item["ItemID"]

            name = item["Name"]
            name = "\"" + name.replace("\"","\"\"") + "\""

            currently = transformDollar(item["Currently"])
            first_bid = transformDollar(item["First_Bid"])
            number_of_bids = item["Number_of_Bids"]

            started = transformDttm(item["Started"])
            started = "\"" + started.replace("\"","\"\"") + "\""

            ends = transformDttm(item["Ends"])
            ends = "\"" + ends.replace("\"","\"\"") + "\""

            if item["Description"] != None:
                description = item["Description"]
                description = "\"" + description.replace("\"","\"\"") + "\""
            else:
                Description = 'NULL'

            location = item["Location"]
            location = "\"" + location.replace("\"","\"\"") + "\""

            country = item["Country"]
            country = "\"" + country.replace("\"","\"\"") + "\""

            userID = item["Seller"]["UserID"]
            userID = "\"" + userID.replace("\"","\"\"") + "\""

            rating = item["Seller"]["Rating"]
            rating = "\"" + rating.replace("\"","\"\"") + "\""

            if "buy_price" in item:
                buy_price = transformDollar(item["Buy_price"])
            else:
                buy_price = 'NULL' 

            for category in  item["Category"]:
                tablecategory += category + '\n'
                tablecatitem += category + columnSeparator + itemID + '\n'

            
            tableitems += itemID + columnSeparator + name + columnSeparator + currently + columnSeparator + buy_price + columnSeparator + first_bid + columnSeparator + number_of_bids + columnSeparator + started + columnSeparator + ends + columnSeparator + description + '\n'      
            tableuser += userID + columnSeparator + location + columnSeparator + country + columnSeparator + rating + '\n' 
            tablesell += itemID + columnSeparator + userID + '\n'

            if item["Bids"] != None:
                for bid in item["Bids"]:
                    bidUserId = bid["Bid"]["Bidder"]["UserID"]
                    bidUserId = "\"" + bidUserId.replace("\"","\"\"") + "\""
                    bidTime = transformDttm(bid["Bid"]["Time"])
                    bidAmmount = transformDollar(bid["Bid"]["Amount"])
                    bidRating = bid["Bid"]["Bidder"]["Rating"]

                    if "location" in bid["Bid"]["Bidder"]:
                        bidlocation = bid["Bid"]["Bidder"]["Location"]
                        bidlocation = "\"" + bidlocation.replace("\"","\"\"") + "\""
                    else:
                        bidlocation = 'NULL'

                    if"country" in bid["Bid"]["Bidder"]:
                        bidcountry = bid["Bid"]["Bidder"]["Country"]
                        bidcountry = "\"" + bidcountry.replace("\"","\"\"") + "\""
                    else:
                        bidcountry = 'NULL'

                    tableuser += bidUserId + columnSeparator + bidlocation + columnSeparator + bidcountry + columnSeparator + bidRating + '\n'
                    tablebid += bidUserId + columnSeparator + itemID + columnSeparator + bidTime + columnSeparator + bidAmmount + '\n'



        f_sell = open( "tableSell.dat", "a" )
        f_sell.write( tablesell +'\n' )
        f_sell.close()

        f_category = open( "tableCategory.dat", "a" )
        f_category.write( tablecategory +'\n' )
        f_category.close()

        f_user = open( "tableUser.dat", "a" )
        f_user.write( tableuser + '\n' )
        f_user.close()

        f_catItem = open( "tableCatItem.dat", "a" )
        f_catItem.write( tablecatitem + '\n' )
        f_catItem.close()

        f_bid = open( "tableBid.dat", "a" )
        f_bid.write( tablebid +'\n' )
        f_bid.close()

        f_item = open( "tableItem.dat", "a" )
        f_item.write( tableitems +'\n' )
        f_item.close()


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
