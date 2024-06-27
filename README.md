# shop_deploy
A test deploy for the shop api
Performs CRUD operation on product and create orders

GET Endpoints:

shop_api/products

shop_api/products/id

shop_api/orders

shop_api/orders/id

Post endpoints

shop_api/products/create { "title": "Your product title", "description": "Product description", "price": 19.99,
"available_quantity": 10
}

shop_api/orders/create { "product": <product_id>, "quantity": <desired_quantity> }

Put endpoints shop_api/products/id/update { "title": "Updated product title", # Optional "description": "Updated description", # Optional "price": 24.99, # Optional "available_quantity": 5 # Optional }

shop_api/orders/id { "status": "CANCELLED" }

Delete endpoints shop_api/products/id/delete

shop_api/orders/id/delete



[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/33323959-846a2418-7b4d-4921-bf58-4f8a26095cce?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D33323959-846a2418-7b4d-4921-bf58-4f8a26095cce%26entityType%3Dcollection%26workspaceId%3Dce05bcf2-e736-4453-9fcc-6cd8e52edf0f)
