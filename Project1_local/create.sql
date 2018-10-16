DROP TABLE IF EXISTS ITEMS;
CREATE TABLE ITEMS(
	itemID    		INTEGER  PRIMARY KEY,
	name      		text,
	currently 		text,
	buy_price 		text,
	first_bid 		text,
	number_of_bids  INTEGER,
	started         text,
	ends			text,
	description     text
);

DROP TABLE IF EXISTS CATEGORY;
CREATE TABLE CATEGORY(
	categoryName  text PRIMARY KEY
);

DROP TABLE IF EXISTS USER;
CREATE TABLE USER(
	userID		text  PRIMARY KEY,
	location	text,
	country		text,
	rating		INTEGER
);

DROP TABLE IF EXISTS BID;
CREATE TABLE BID(
	time		text,
	amount		text,
	userID		text,
	itemID		text,
	PRIMARY KEY (userID, itemID),
	FOREIGN KEY (userID) REFERENCES USER,
	FOREIGN KEY (itemID) REFERENCES ITEMS
);

DROP TABLE IF EXISTS CATITEM;
CREATE TABLE CATITEM(
	category   text,
	itemID 	   INTEGER,
	PRIMARY KEY (category, itemID),
	FOREIGN KEY (category) REFERENCES CATEGORY,
	FOREIGN KEY (itemID)   REFERENCES ITEMS
);

DROP TABLE IF EXISTS SELL;
CREATE TABLE SELL(
	userID		text,
	itemID 		text,
	PRIMARY KEY (itemID),
	FOREIGN KEY (userID) REFERENCES USER,
	FOREIGN KEY (itemID) REFERENCES ITEMS 
);
