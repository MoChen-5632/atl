# atl

## Design decisions

I made this web app in mainly four sections and one hidden sections(All customer list). The four sections are :Customer List, Customersearch, add booking and add customer, which represents task 3-6 fro the requirement. task 7-Edit customer and task 8- customer booking overview is embedded in Customer List, Customersearch as well as All customers list.

Customer List, I made this page as easy and simple as possible: User only need to select Tour and tourgroup, then the customer detail will be reviewed within a second. In daily life of a ATL booking manager, it will be convinient to check all their details, that's why I showed everything in the database for customers: ID, name, birthday, email and phone. In the far right side, I also embedded two functions: edit customer, and booking overview. Which is very straightforward and ituitive. user can edit customer details when needed, or check what tourgroup a particular customer attends.

When user click edit customer, it will forward to "Edit customer" page. In the beginning I made it the same as the "Add customer page", just like the library program(add customer and edit customer goes to the same customerform.html). Then I realise it's very hard to use. User will only use this fuction when they made a typo when adding new customer, or udpate user's email/phone number. And in this ATL web app there's a differnece from the library program: the customer data has a customer ID. So before I go too far and make this "customerform.html" super complex, I decided to make a customeredit.html file. Only for Edit customer function. It's eaiser for me to handle it. And moreover, for a better user experience, as I fetch the original data form the database, user will take less time editing them. 

Customersearch: This is probably the easiest task. Using like operator to search any part in customer's firstname and family name, so that user can quickly get a customer's data and booking details. Just like customer list, I add "edit customer" and "booking overview" within this page. Because everyone has his own preference to interact with the web app. Some people may prefer to find customer via customer list, while others think that customer search is better. So it's better to add them on both pages.

Add booking: This is probably the most difficult one as it involves both customer part and booking part. Plus, there's so many things to validate. Firstly I need to make sure all fields are selected. Secondly, the tourgroup has to be in the future. Thirdly, it must meet the age requirement, which means I need the data from both tourgroup age restriction, and the customer's age. Then during my test part, I am trying to create numerous customer, insert them into random tourgroup, then I found there's a lot of double booking. So, before final data insert, I still need to validate that this customer hasn't been added to the group. Which makes this function the longest of all.


Add customer: This page is simple: friendly interface and validation is all.

All customers list: Firstly I made this page visible on the navigation bar. However, it is a bit confusing to have a item called "customer list" and another item called "all customers list". Also, it has part of the function being overlapped with customer search. So I remove it from the bar, I still keep this html file in the templates folder. So that after "add customer", it will direct to this "All customers list" page, to give user a list to reference. Convinient!

Customer Booking Overview: Like Edit customer, this page is embedded into customer list and customer search page. It gives a breifing of the customer's booking. I think it is nesessery to distingish past, current and future booking. So the booking overview is divided into three parts. For tour booking manager, it's very important to see their past bookings, current bookings as well as future bookings.



## References   

Makalu. (2025). New zealand, Lake matheson, Mount tasman image. Free for use. https://pixabay.com/photos/new-zealand-lake-matheson-4863003/

## Database questions

1.CREATE TABLE tours (
    tourid INT NOT NULL AUTO_INCREMENT,
    tourname VARCHAR(50) NOT NULL,
    agerestriction int not null,
    PRIMARY KEY (tourid)
);

2.create table tourgroups (
	tourgroupid INT NOT NULL AUTO_INCREMENT,
    tourid INT,
    startdate date,
    PRIMARY KEY (tourgroupid),
    CONSTRAINT fk_tourid_tourgroups FOREIGN KEY (tourid)
        REFERENCES tours (tourid)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

3.CREATE TABLE families (
    familyid INT NOT NULL AUTO_INCREMENT,
    familyname VARCHAR(50) NOT NULL,
    shortdescription VARCHAR(100),
    PRIMARY KEY (familyid)
);

4.INSERT INTO families (familyname, shortdescription)
    VALUES ('Chen', '');

5.I should add a foreign key "familyid" under table "tourbookings" , which links to the primary key of table families. So that family booking can be possible.





