
# BookMyShow
APIS:

1)/register

2)/login

3)/user

4)/airports

5)/passengers

6)/flight_details

7)/booking-authentication required 

Curl for last API

curl --location --request POST 'http://127.0.0.1:8000/api/v1/booking' \
--header 'Content-Type: application/json' \
--header 'Cookie: token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjUzMzAzMDY3LCJpYXQiOjE2NTMyOTk0Njd9.K6VI3o890h9y4CdCgImYRXWRSPcehJKgHHffTgaS-9Q' \
--data-raw '{
    "trip_date": "2022-05-28",
    "num_of_passengers": "2",
    "total_price": "13500",
    "user": 2,
    "flight": 1,
    "passengers": [
       {
            "aadharno":"6677889910",
            "name": "Alka Joshi",
            "address": "address4",
            "telephone_number": "7984795244",
            "emailid": "aj@gamil.com",
            "gender": "female",
            "age": "50",
            "user": 2
        },
        {
            "aadharno":"66778893434",
            "name": "Jayesh Joshi",
            "address": "address6",
            "telephone_number": "7984795244",
            "emailid": "jj@gamil.com",
            "gender": "male",
            "age": "50",
            "user": 2
        }
    ]
}'


