# CORNERSHOP SHOPPER PAYMENT INTEGRATION

 Base flask micro-service implementing Acesso PSP
 for shopper payment integration

 ## Enpoints:

 | namespace          | Methods     |Endpoints                                  | Description                                            | Body               |
 | :----------------- | :---------- |:----------------------------------------- |:------------------------------------------------------ |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  |
 | `list_cards`       |  GET        | `/api/cards`                              | list all cards from PSP                                | None                                                                                                                                                                                                       |                                
 | `get_card_balance` |  GET        | `/api/card/<:card_issuer_id>/balance`     | get detail card for a specific from `card_issuer_id`   | None                                                                                                                                                                                                       |
 | `load_card`        |  POST       | `/api/card/<:card_issuer_id>/load`        | load amount on specific card from `card_issuer_id`     | { "amount": 10 }                                                                                                                                                                                           |
 | `unload_card`      |  POST       | `/api/card/<:card_issuer_id>/unload`      | unload amount on specific card from `card_issuer_id`   | { "amount": 10 }                                                                                                                                                                                           |
 | `assign_card`      |  POST       | `/api/card/<:card_number_id>/assign`      | assign card from `card_number_id` for a specific user  | {"email": "test@test.cl", "name": "Test test", "gender": "male", "id_number": "12345", "birthdate": "21/09/1977", "phone_number": "", "pin_number": "1231", "month": "08",  "year": "2020", "ccv": "123"}  | 
 | `activate_card`    |  POST       | `/api/card/<:card_issuer_id>/activate`    | Not implemented                                        | None                                                                                                                                                                                                       |
 | `deactivate_card`  |  POST       | `/api/card/<:card_number_id>/deactivate`  | Not implemented                                        | None                                                                                                                                                                                                       |
 | `wallet_balance`   |  GET        | `/api/wallet/balance`                     | Not implemented                                        | None                                                                                                                                                                                                       |                                      


 # Endpoints responses:

  * `list_cards`: 

  ```
     { 
        "status": "ok",
        "metadata": [
             {
                 "card_number_id": "",
                 "card_issuer_id": "",
                 "card_status"="",
                 "last_four_digits": ""
             }
        ],
        "error_detail": null 
     }
 ```

  * `get_card_balance`:

  ```
 { 
    "status": "ok",
    "metadata": [
         {
          "balance": 100,
         }
    ],
    "error_detail": null 
 }
 ```

  * `load_card`:
   ```
 { 
    "status": "ok",
    "metadata": null
    "error_detail": null 
 }
 ```

  * `unload_card`:
   ```
 { 
    "status": "ok",
    "metadata": null
    "error_detail": null 
 }
 ```

  * `assign_card`:
   ```
 { 
    "status": "ok",
    "metadata": null
    "error_detail": null 
 }
 ```

  * `active_card`:
   ```
 { 
    "status": "ok",
    "metadata": null
    "error_detail": null 
 }
 ```

  * `deactive_card`:
   ```
 { 
    "status": "ok",
    "metadata": null
    "error_detail": null 
 }
 ```

  * `get_wallet_balance`:
   ```
 { 
    "status": "ok",
    "metadata": {
         "amount": 20,
         "currency": "BRL",
         "country": "BR"   
    },
    "error_detail": null 
 }
 ```

