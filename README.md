# Credit Card Validator API

## General Information

It's a validation API for credit cards. It checks:
1. Is card expired.
2. Does card number satisfy [Luhn check](https://en.wikipedia.org/wiki/Luhn_algorithm).
3. Card issuer and does card number length corresponds to the issuer.

## Local Deployment

### Docker startup

Inside of the repository directory run the following commands:
```shell
docker build --tag cardvalidator .
docker-compose up --build
```

### Docker shutdown

```shell
docker-compose down
```

### Direct app startup
You also can locally start the app even without docker:
```shell
( cd src && uvicorn main:app --reload )
```

## API Usage

API has only 1 endpoint: '/validate' POST. 
I recommend using Postman.

Request example (valid):

<img width="400" src="https://github.com/dmytromk/credit-card-validator/assets/96624185/a5231265-19f1-4c76-bcf4-7881908ebd11">

Response example (valid):

<img width="400" src="https://github.com/dmytromk/credit-card-validator/assets/96624185/8587617c-54e9-4460-aef7-5013b98c96ec">

Full example (invalid):

<img width="650" src="https://github.com/dmytromk/credit-card-validator/assets/96624185/05d58292-1574-4792-971f-692ed9dbe362">
