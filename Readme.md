**Scrapy Booking parser**

_**How to set up "Scrapy Booking parser**"_ 

1. Install Python 3.6
2. Install pipenv
3. Run in "\src" directory next command:
                
                pipenv install --dev
                
4. Create MySQL database with utf8 encoding and utf8-bin collation
5. Copy "\src\booking_parser\booking_parser\settings.example.py" and rename it to "settings.example.py" 
6. At the end of file  "\src\booking_parser\booking_parser\settings.py" specify:
    - SMTP_HOST
    - MAIL_FROM
    - SMTP_USER
    - SMTP_PASS
    - SMTP_PORT
    - SMTP_TLS
    - SMTP_SSL
    - MAIL_RECEIVERS
    - PROXY_CONFIG (necessary only if you want to use --vpn parameter)
    - DB_CONNECTION_STRING  
7. In  "\src\booking_parser\alembic.ini" find variable:
                
                sqlalchemy.url
                
    and assign it with connection string to your database like in example below.
    
                mysql+mysqlconnector://db_username:db_password@localhost/db_name
     
8. In "\src\booking_parser" directory run:
 
                alembic upgrade head
                
Now you are ready to use "Scrapy Booking parser".

_**How to use "Scrapy Booking parser"**_

All commands shown below must be used in "\src\booking_parser" directory of project.

To start parser you need to run: 
                
                  runner.py <country> <city> <check_in_date> <check_out_date>
                  
For more information how to use parser run:

                   runner.py -h
                   
To start 20 parsers with preselected parameters run:

                   python runWithPreSelectedArgs.py
                   
                   
_**How to run multiple processes and spiders of "Scrapy Booking parser"**_

First of all you need to open 'spider_start_config' database table and populate it with some data.

Columns:
- country
- city
- checkin_date
- checkout_date

are required.

Other columns are optional.

If you set **vpn** to 1, then parser will use vpn connection

Column **concurrent_request_amount** stands for CONCURRENT_REQUESTS in scrapy settings. If it has no value, then default value will be used.

Column **state** determine the state of spider.

- 1 - pause
- 2 - resume
- 3 - stop
- other values work like resume






 