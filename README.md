# Group8 -- Assignment 2

Running the following commands will start 3 Flask servers.

```python
python3 RESTful_api.py
```


```python
python3 user_management.py
```


```python
python3 JWT_service.py
```



## JWT service endpoints

| **Path & Method**       | **Parameters**                                        | **Return Value (HTTP Code, Body)**                      | **Description** |
|-------------------------|------------------------------------------------------|---------------------------------------------------------|----------------|
| `/auth - POST`          | `username`: string                                   | `200`, `{ "username": username, "token": JWT }`        | Generates a JWT for authenticated users |
|                         |                                                      | `400`, `{ "error": "Username is required" }`           | |
| `/auth/validate - POST` | **Header:** `Authorization: Bearer <token>`          | `200`, `{ "valid": true, "username": username }`       | Validates a token |
|                         |                                                      | `401`, `{ "error": "Token missing" }`                   | |
|                         |                                                      | `401`, `{ "error": "Token expired" }`                   | |
| `/auth/logout - PUT`    | **Header:** `Authorization: Bearer <token>`          | `200`, `{ "message": "Successfully logged out" }`      | Adds token to a blacklist (logout) |
|                         |                                                      | `400`, `{ "error": "Token required" }`                 | |


## User management service end points

| **Path & Method**       | **Parameters**                                        | **Return Value (HTTP Code, Body)**                      | **Description** |
|-------------------------|------------------------------------------------------|---------------------------------------------------------|----------------|
| `/users - POST`        | `username`: string, `password`: string               | `201`, `{ "message": "User added successfully" }`       | User registration |
|                         |                                                      | `400`, `{ "error": "Invalid request" }`                 | |
|                         |                                                      | `409`, `{ "error": "Username already exists" }`         | |
| `/users/login - POST`   | `username`: string, `password`: string               | `200`, `{ "message": "Login successful", "token": JWT }` | User login |
|                         |                                                      | `403`, `{ "error": "Username not found" }`             | |
|                         |                                                      | `403`, `{ "error": "Incorrect password" }`             | |
| `/users - PUT`         | `username`, `password`, `new_password`                | `200`, `{ "message": "Password updated successfully" }` | Update user password |
|                         | **Header:** `Authorization: Bearer <token>`          | `403`, `{ "error": "Invalid token" }`                   | |
| `/users/logout - POST`  | **Header:** `Authorization: Bearer <token>`          | `200`, `{ "message": "Successfully logged out" }`       | User logout |
|                         |                                                      | `403`, `{ "error": "Invalid token" }`                   | |



## URL shortener service endpoints

| **Path & Method**       | **Parameters**                                        | **Return Value (HTTP Code, Body)**                      | **Description** |
|-------------------------|------------------------------------------------------|---------------------------------------------------------|----------------|
| `/:id - GET`           | **Header:** `Authorization: Bearer <token>`          | `301`, `{ "value": "Original URL" }`                    | Redirect to the original URL |
|                         |                                                      | `403`, `{ "error": "Forbidden" }`                       | |
|                         |                                                      | `404`, `{ "error": "ID not found" }`                    | |
| `/:id - PUT`           | **Header:** `Authorization: Bearer <token>`          | `400`, `{ "error": "Invalid URL" }`                     | Update a stored URL |
|                         | `url`: new URL                                      | `403`, `{ "error": "Forbidden" }`                       | |
|                         |                                                      | `200`, `{ "message": "Updated successfully" }`          | |
| `/:id - DELETE`        | **Header:** `Authorization: Bearer <token>`          | `204`, No Content                                       | Delete a shortened URL |
|                         |                                                      | `403`, `{ "error": "Forbidden" }`                       | |
| `/ - GET`              | **Header:** `Authorization: Bearer <token>`          | `200`, `{ "keys": ["id1", "id2"] }`                     | List all stored URLs for the user |
| `/ - POST`             | **Header:** `Authorization: Bearer <token>`          | `201`, `{ "id": "generated_id" }`                       | Shorten a new URL |
|                         | `value`: URL                                        | `400`, `{ "error": "Invalid URL" }`                     | |
| `/ - DELETE`           | **Header:** `Authorization: Bearer <token>`          | `404`, `{ "error": "Not found" }`                       | Delete all URLs |