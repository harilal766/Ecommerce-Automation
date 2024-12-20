# Ecom-Dashboard : A Django based web application made for E-commerce sellers to automate and simplify their daily tasks.
## Supported Ecommerce platforms.
1. Amazon Seller Central
2. Shopify

# Contents
- [Installation] (#Installation)
- [Amazon Selling Parner API (SP API)] (# SP API)



## Installation
1. `python -m venv {{env_name}}`.
2. pip install -r requirements.txt
3. Activate the environment.
4. Create a .env file on the root directory and store these credentials on this format.
    `ACCESS_TOKEN = {{your Access  token}}`
    `REFRESH_TOKEN = {{Your Refresh token}}`
    `CLIENT_ID = {{Your Client id}}`
    `CLIENT_SECRET = {{Your Client secret}}`

    NB : make sure .env file is included in `.gitignore`.


## SP API

## API Structure

## Important Model details and their API fields
### Orders Model
#### Unshipped Orders (Orders that are confirmed but not scheduled for pickup).
- Order id : AmazonOrderID
- Scheduled / Unscheduled : OrderStatuses -> Shipped / Unshipped.
- Ship by date  : LatestShipDate.

### Reports Model
- ReportType : 






Models : Orders, Reports, Easy ship



