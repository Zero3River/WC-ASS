# Group8 -- Assignment 1

Running the following command will start a Flask server at  `http://127.0.0.1:8000`

```python
python3 RESTful_api.py
```

## Supported API Endpoints

| **Path & Method**  | **Parameters**            | **Return Value (HTTP Code, Body)**                         |
|--------------------|-------------------------|-----------------------------------------------------------|
| `/:id - GET`      |                           | `301`, corresponding URL of the given id                 |
|                    |                           | `404`, error: ID Not Found                               |
| `/:id - PUT`      | `url`: URL to be updated | `400`, error: Invalid URL                                |
|                    |                           | `200`, message: Updated successfully                     |
|                    |                           | `404`, error: ID not found                              |
| `/:id - DELETE`   |                           | `204`, return if delete was successful                  |
|                    |                           | `404`, error: ID not found                              |
| `/ - GET`         |                           | `200`, list of all the ids                              |
| `/ - POST`        | `value: url` (URL to shorten) | `201`, id: generated id                                |
|                    |                           | `400`, error: invalid URL                              |
| `/ - DELETE`      |                           | `404`, return if delete was successful                 |
