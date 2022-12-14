
# Stock market auction model backend

Backend for a stock market auction model



## API Reference

#### Get trade history

```http
  GET /tradehistory
```
returns
```
{
  type:"buy"/"sell",
  quantity:"1.0" //float,
  price:"20.2" //float
  user1:"who buys",
  user2:"who sells"
}
```

#### Get all prices

```http
  GET /price
```
returns
```
{
  quantity:"1.0" //float,
  price:"20.2" //float
  time:"timstamp"
}
```

#### Get all limit orders

```http
  GET /limitorder
```
returns
```
{
    type:"buy"/"sell",
    user:"id of the user"
    quantity:"1.0" //float,
    price:"20.2" //float
    time:"timstamp"
}
```

#### CRUD on users

```http
  /users
```
user model:

```
{
    name:"string",
    email:"email"
    fiat:"total currency" //float,
    stocks:"23" //float
}
```

#### limit order

```http
 POST /trade
```
request sample:

```
{
    tradetype:"buy"/"sell",
    ordertype:"limit",
    price:"30",
    quantity:"20",
    id:"id"
}

```

returns:

```
message: "Insufficient funds 
    or 
Order placed
    or 
Order cant be placed "
```

#### market order

```http
 POST /trade
```
request sample:

```
{
    tradetype:"buy"/"sell",
    ordertype:"market",
    quantity:"20",
    id:"id"
}

```

returns:

```
message: "Insufficient funds
    or
Insufficient stocks
    or 
Order placed
    or
order placed partially
    or 
Order cant be placed "
```