![Logo of the project](library.png)

# LIBRARY SERVICE API

API for library with next futures:
- Added and manage books
- Added borrowing 
- Added payments for borrowing
- Notifications for borrowing in telegram chat

## Installing / Getting started

```shell
git clone https://github.com/volodymyr-vereshchak/library-service-api
cd library-service-api
initilize enviroment variables .env
You must install docker
docker-compose up --build
For retrive the notifications you must create telegram bot and inicialize his token in .env file
You can use payment system. For this need initialize your Stripe Payment account.
```
## Links

You can test api on the next links:

- Heroes API: https://library-service-api.onrender.com/
- User API: https://library-service-api.onrender.com/users/ (/token/refresh)
- For get notifications add to telegram group @library_mate
- After borrowing book in payments you can pay you borrow (test card for pay 4242 4242 4242 4242; exp: 12/34; cvv: any three digits )
- There is no celery worker on render (this is a paid service)