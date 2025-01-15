
CREATE TABLE tours (
    tourid INT NOT NULL AUTO_INCREMENT,
    tourname VARCHAR(50) NOT NULL,
    agerestriction int not null,
    PRIMARY KEY (tourid)
);

CREATE TABLE customers (
	customerid INT NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(50),
    familyname VARCHAR(50) NOT NULL,
    dob date,
    email VARCHAR(320), 
    phone VARCHAR(12),
    PRIMARY KEY (customerid)
);

create table destinations (
	destinationid INT NOT NULL AUTO_INCREMENT,
    destinationname VARCHAR(30) NOT NULL,
     PRIMARY KEY (destinationid)
);

create table itineraries (
	itineraryid INT NOT NULL AUTO_INCREMENT,
    tourid INT NOT NULL,
    destinationid INT NOT NULL,
      PRIMARY KEY (itineraryid),
    CONSTRAINT fk_tourid FOREIGN KEY (tourid)
        REFERENCES tours (tourid)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT fk_destinationid FOREIGN KEY (destinationid )
        REFERENCES destinations (destinationid)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

create table tourgroups (
	tourgroupid INT NOT NULL AUTO_INCREMENT,
    tourid INT,
    startdate date,
    PRIMARY KEY (tourgroupid),
    CONSTRAINT fk_tourid_tourgroups FOREIGN KEY (tourid)
        REFERENCES tours (tourid)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

create table tourbookings (
		bookingid INT NOT NULL AUTO_INCREMENT,
    tourgroupid INT,
    customerid INT,
     PRIMARY KEY (bookingid),
    CONSTRAINT fk_tourgroupid FOREIGN KEY (tourgroupid)
        REFERENCES tourgroups (tourgroupid)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT fk_customerid FOREIGN KEY (customerid)
        REFERENCES customers (customerid)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

INSERT INTO customers (customerid, firstname, familyname, dob, email) VALUES (816, 'Simon', 'Charles', '1952-07-15', 'simon@charles.nz');
INSERT INTO customers (customerid, firstname, familyname, dob, email) VALUES (923, 'Simone', 'Charles', '1987-09-11', 'simone.charles@kiwi.nz');
INSERT INTO customers (customerid, firstname, familyname, dob, email) VALUES (343, 'Charlie', 'Charles', '1954-01-25', 'charlie@charles.nz');
INSERT INTO customers (customerid, firstname, familyname, dob, email) VALUES (810, 'Kate', 'McArthur', '1972-09-30', 'K_McArthur94@gmail.com');
INSERT INTO customers (customerid, firstname, familyname, dob, email) VALUES (786, 'Jack', 'Hopere', '1980-02-10', 'Jack643@gmail.com');
INSERT INTO customers (customerid, firstname, familyname, dob, email) VALUES (801, 'Chloe', 'Mathewson', '1980-03-15', 'Chloe572@gmail.com');
INSERT INTO customers (customerid, firstname, familyname, dob, email) VALUES (121, 'Kate', 'McLeod', '1952-07-15', 'KMcLeod112@gmail.com');
INSERT INTO customers (customerid, firstname, familyname, dob, email) VALUES (924, 'Samantha', 'Charles', '2013-07-24', 'simone.charles@kiwi.nz');

INSERT INTO tours (tourid, tourname, agerestriction ) VALUES (17, "UK", 0);
INSERT INTO tours (tourid, tourname, agerestriction ) VALUES (23, "West Europe", 0);
INSERT INTO tours (tourid, tourname, agerestriction ) VALUES (41, "East Europe", 18);

INSERT INTO destinations (destinationid, destinationname) VALUE (11, "London");
INSERT INTO destinations (destinationid, destinationname) VALUE (12, "Stoke-On-Trent");
INSERT INTO destinations (destinationid, destinationname) VALUE (17, "Cotswolds");
INSERT INTO destinations (destinationid, destinationname) VALUE (24, "Ambleside");
INSERT INTO destinations (destinationid, destinationname) VALUE (37, "Glasgow");
INSERT INTO destinations (destinationid, destinationname) VALUE (38, "Edinburgh");
INSERT INTO destinations (destinationid, destinationname) VALUE (40, "Inverness");
INSERT INTO destinations (destinationid, destinationname) VALUE (39,"Loch Ness");
INSERT INTO destinations (destinationid, destinationname) VALUE (35, "Paris");
INSERT INTO destinations (destinationid, destinationname) VALUE (22,"Madrid");
INSERT INTO destinations (destinationid, destinationname) VALUE (9,"Berlin");
INSERT INTO destinations (destinationid, destinationname) VALUE (60, "Bucharest");
INSERT INTO destinations (destinationid, destinationname) VALUE (4,"Budapest");
INSERT INTO destinations (destinationid, destinationname) VALUE (94,"Minsk");

INSERT INTO itineraries (tourid, destinationid) VALUE (17, 11);
INSERT INTO itineraries (tourid, destinationid) VALUE (17, 12);
INSERT INTO itineraries (tourid, destinationid) VALUE (17, 17);
INSERT INTO itineraries (tourid, destinationid) VALUE (17, 24);
INSERT INTO itineraries (tourid, destinationid) VALUE (17, 37);
INSERT INTO itineraries (tourid, destinationid) VALUE (17, 38);
INSERT INTO itineraries (tourid, destinationid) VALUE (17, 40);
INSERT INTO itineraries (tourid, destinationid) VALUE (17, 39);

INSERT INTO itineraries (tourid, destinationid) VALUE (23, 11);
INSERT INTO itineraries (tourid, destinationid) VALUE (23, 35);
INSERT INTO itineraries (tourid, destinationid) VALUE (23, 22);
INSERT INTO itineraries (tourid, destinationid) VALUE (23, 9);

INSERT INTO itineraries (tourid, destinationid) VALUE (41, 9);
INSERT INTO itineraries (tourid, destinationid) VALUE (41, 60);
INSERT INTO itineraries (tourid, destinationid) VALUE (41, 4);
INSERT INTO itineraries (tourid, destinationid) VALUE (41, 94);

INSERT INTO tourgroups (tourgroupid, tourid, startdate) VALUES (171,17,'2025-07-10');

INSERT INTO tourbookings (tourgroupid, customerid) VALUES (171,816);
INSERT INTO tourbookings (tourgroupid, customerid) VALUES (171,923);
INSERT INTO tourbookings (tourgroupid, customerid) VALUES (171,343);



INSERT INTO tourgroups (tourgroupid, tourid, startdate) VALUES (231,23,'2025-08-15');
INSERT INTO tourbookings (tourgroupid, customerid) VALUES (231,810);
INSERT INTO tourbookings (tourgroupid, customerid) VALUES (231,801);



INSERT INTO tourgroups (tourgroupid, tourid, startdate) VALUES (411,41,'2024-02-20');
INSERT INTO tourgroups (tourgroupid, tourid, startdate) VALUES (412,41,'2025-02-21');
INSERT INTO tourgroups (tourgroupid, tourid, startdate) VALUES (413,41,'2025-06-24');
INSERT INTO tourbookings (tourgroupid, customerid) VALUES (413,786);
INSERT INTO tourbookings (tourgroupid, customerid) VALUES (412,121);
INSERT INTO tourbookings (tourgroupid, customerid) VALUES (411,121);