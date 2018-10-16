import web

db = web.database(dbn='sqlite',
        db='myData.db' #TODO: add your SQLite database filename
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select CurrTime from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].CurrTime # TODO: update this as well to match the
                                  # column name

#return 0 if a time is successfully selected as current time
def setTime(time):
    updatedTime = False
    t = transaction()
    try:
        query_string = 'UPDATE CurrentTime SET CurrTime = $time'
        updatedTime = db.query(query_string, {'time': time})
    except Exception as e:
        t.rollback()
#       print str(e)
    else:
        t.commit()
    return updatedTime

def addBid(itemID, userID, price):
    addedBid = 0
    now = getTime()
    t = transaction()
    try:
        query_string = 'INSERT into Bids(ItemID, UserID, Time, Amount) values ($itemID, $userID, $now, $price)'
        addedBid = db.query(query_string, {'itemID': itemID, 'userID': userID, 'now': now, 'price': price})
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()
    return addedBid

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(itemID, userID, category, description, minPrice, maxPrice, status):
    # TODO: rewrite this method to catch the Exception in case `result' is empty

    # DEAL WITH ITEMID, USERID, MINPRICE, MAXPRICE
    query_string = 'select * from Items as i, Categories as c where i.ItemID = c.ItemID'
    if itemID:
        query_string += ' and i.ItemID = $itemID'
    if userID:
        query_string += ' and UserID = $userID'
    if category:
        query_string += ' and Category = $category'
    if description:
        query_string += ' and Description like $description'
        query_string += ' and Currently >= $minPrice'
    if maxPrice:
        query_string += ' and Currently <= $maxPrice'
    
    # DEAL WITH STATUS
    now = getTime()
    if status == 'open':
        query_string += ' and Started <= $now and $now <=Ends'
    elif status == 'close':
        query_string += ' and Ends < $now'
    elif status == 'notStarted':
        query_string += ' and $now < Started'
    else:
        pass

    # DEAL WITH DUPLICATES IN DIFFERENT CATEGORY
    query_string += ' group by i.ItemID'

    # DEAL WITH OUTPUT FORMAT
    results = query(query_string, {'itemID': itemID, 'userID': userID, 'minPrice': minPrice, 'maxPrice': maxPrice, 'now': now, 'category': category, 'description': "%{0}%".format(description)})
    show_results = []
    for result in results:
        itemInfo = {}
        itemInfo['ItemID'] = result.ItemID
        itemInfo['Name'] = result.Name
        itemInfo['Currently'] = result.Currently
        itemInfo['Buy_Price'] = result.Buy_Price
        show_results.append(itemInfo)        

    # RETURN TO AUCTIONBASE.PY
    return show_results

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
