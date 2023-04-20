# LocationAPI

This API allows users to share interesting places in their neighborhoods.
Users can find places in given categories that are closest to them or have
the highest average score. For each place user can submit review with description
and rating from 1 to 5 stars.

This API is made in Python with FastAPI. For database I used Postgres with
PostGIS for geographical features of this API, SQLAlchemy is used as ORM.

I used this project to become more familiar with FastAPI and SQLAlchemy
libraries as well as PostGIS extension for Postgres.

## Run localy

Right now there is no easy way to run this project on your local machine. Docker version is coming soon :).

If you want you can edit `database.py` file with your local postgres credentials (database requires that postgis is installed and enabled!)

## API endpoints

All list views are paginated with argument `page` used for selecting page. Default is 1.

All patch, delete and post besides `/user/register` and `/user/login` require authentication token.

## places

### /places/list

#### get
Returns list of places that are set as published.

response:
```
[
  {
    "name": "string",
    "description": "string",
    "category": "string",
    "published": false,
    "latitude": 0,
    "longitude": 0,
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "avg_score": 0,
    "distance": 0
  }
]
```
code: `200`

#### post
Creating new place (unpublished).

example request:
```
{
  "name": "string",
  "description": "string",
  "category": "string",
  "latitude": 0,
  "longitude": 0
}
```
example response:
```
{
    "name": "home",
    "description": "start",
    "published": true,
    "latitude": 18.641569510838686,
    "longitude": 50.29024815035388,
    "id": 183627629719111602088909013496092281661
    },
```

success code: `200`

error codes: 
```
422 - validation error
403 - unauthorized
```

### /places/list-published

#### get

Returns list of places that aren't set as published. This view is restricted to admin users.

example:
```
[
  {
    "name": "string",
    "description": "string",
    "category": "string",
    "latitude": 0,
    "longitude": 0,
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "avg_score": 0,
    "distance": 0,
    "published": false
  }
]
```

success code: `200`
error code: `401` - unauthorized

### /places/id/{id}

#### get
returns place with given id

```
{
  "name": "string",
  "description": "string",
  "category": "string",
  "latitude": 0,
  "longitude": 0,
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "avg_score": 0,
  "distance": 0,
  "published": false
}
```

success code: `200`
error code: `404` - not found

#### patch

updating place data. Only creator of place and admin are allowed to perform this action.

example request:
```
{
  "name": "string",
  "description": "string",
  "category": "string",
  "latitude": 0,
  "longitude": 0
}
```

success code: 200

error code: 
```
422 - validation error
403 - unauthorized
404 - not found
```

#### delete

deleting place. Only creator of place and admin are allowed to perform this action.

success code: 204

error code: 
```
404 - not found
403 - unauthorized
```

### /places/list-in-radius/{radius}/{lat}/{lon}

#### get
returns list of places that are inside circle of given center and radius (in meters).
List can be sorted by specifying `order_by` parameter.

Allowed parameters:
```
avg_score_desc - descending by average opinion score
avg_score_asc - ascending by average opinion score
disatnce_asc - ascending by distance from center
disatnce_desc - descending by distance from center
```


success code: `200`

### /places/list-in-radius/{category}/{radius}/{lat}/{lon}

#### get
returns list of places of given category, that are inside circle of given center and radius (in meters).
List can be sorted by specifying `order_by` parameter.

Allowed parameters:
```
avg_score_desc - descending by average opinion score
avg_score_asc - ascending by average opinion score
disatnce_asc - ascending by distance from center
disatnce_desc - descending by distance from center
```

example response:

```
[
    {
      "name": "string",
      "description": "string",
      "category": "string",
      "latitude": 0,
      "longitude": 0,
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "avg_score": 0,
      "distance": 0,
      "published": false
    }
]
```

success code: `200`

### /places/distance-between/{uuid}}/{lat}/{lon}

Returns distance between location and place in meters.

example response:
```
[
    {
      "name": "string",
      "description": "string",
      "category": "string",
      "latitude": 0,
      "longitude": 0,
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "avg_score": 0,
      "distance": 0,
      "published": false
    }
]
```
success code: `200`

### /places/unpublished/id/{uuid}

#### get
returns unpublished place with given id. Only admins are allowed to perform this action.

```
{
  "name": "string",
  "description": "string",
  "category": "string",
  "latitude": 0,
  "longitude": 0,
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "avg_score": 0,
  "distance": 0,
  "published": false
}
```

success code: `200`
error code: `404` - not found

#### patch

updating place data. Only admins are allowed to perform this action.

example request:
```
{
  "name": "string",
  "description": "string",
  "category": "string",
  "latitude": 0,
  "longitude": 0,
  "published": true
}
```

success code: 200

error code: 
```
422 - validation error
403 - unauthorized
404 - not found
```

#### delete

deleting place. Only admins are allowed to perform this action.

success code: 204

error code: 
```
404 - not found
403 - unauthorized
```

## Categories

### /category/

#### get

returns list of categories.

example response:

```
[
  {
    "category": "string",
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
]
```

success code: `200`

#### post

Adding new category. Only for admin users.

example request:

```
{
  "category": "string"
}
```

example response:
```
[
  {
    "category": "string",
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
]
```

success code: `200`

error code: 
```
404 - not found
422 - validation error
403 - unauthorized
```

### /category/{name}

#### patch

Updating category name, only for admins.

example request:
```
{
  "category": "string"
}
```

example response:
```
{
  "category": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

success code: `200`

error code: 
```
404 - not found
422 - validation error
403 - unauthorized
```

#### delete

Deleting category, only for admins.

success code: `204`

error code: 
```
404 - not found
422 - validation error
403 - unauthorized
```

## Opinions

### /opinion/place/id/{uuid}

#### get

returns list of opinions for place with given id.

example response:
```
[
  {
    "stars": 4,
    "opinion": "string",
    "place": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_on": "2023-04-20T13:28:26.713Z",
    "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
]
```

success code: `200`

error code: `404 - not found`

#### post

adds new opinion to place with given uuid.

example request:
```
{
    "stars": 4,
    "opinion": "string",
    "place": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}
```

success code: `200`

error code:

```
404 - not found
422 - validation error
401 - unauthorized 
```

### /opinion/id/{uuid}

#### get
returns opinion with given id.

example response:
```
{
  "stars": 0,
  "opinion": "string",
  "place": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_on": "2023-04-20T13:33:29.662Z",
  "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

success code: `200`

error code: `404 - not found`

#### patch

updating opinion data. Only admins and creator are allowed to perform this action.

example request:

```
{
  "stars": 0,
  "opinion": "string"
}
```

success code: `200`

error code:

```
404 - not found
422 - validation error
401 - unauthorized 
```

#### delete
deleting opinion data. Only admins and creator are allowed to perform this action.

success code: `204`

error code:

```
404 - not found
422 - validation error
401 - unauthorized 
```

## Users

### /user/register

#### post

Creating new user

example request:

```
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

example response:

```
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

success code: `200`

error code: `422 - validation error, 208 - user already exists`

### /user/login

### post

Returns access and refresh tokens.

example request:
```
{
    "username":"string",
    "password":"string"
}
```

example response:

```
{
    "access_token":"string",
    "refresh_token":"string"
}
```

success code: `200`

error code:
```
404 - not found
403 - wrong login/password
422 - validation error
```

### /user/settings

#### get

Returns currently logged-in user.

example response:
```
{
  "password": "string",
  "id": "string",
  "username": "string",
  "email": "string",
  "is_admin": false
}
```

#### delete

deletes user account

success code: `204`

error code: `403`

### /user/settings/password

#### patch

changes user password

example request:

```
{
  "password": "string"
}
```

example response:
```
{
  "password": "string",
  "id": "string",
  "username": "string",
  "email": "string",
  "is_admin": false
}
```

### /user/settings/email

#### patch

changes user email

example request:

```
{
  "email": "string"
}
```

example response:
```
{
  "password": "string",
  "id": "string",
  "username": "string",
  "email": "string",
  "is_admin": false
}
```

### /user/list

#### get

returns list of users. Only for admin users

### /user/id/{uuid}

#### get

returns user with given uuid

example response:
```
{
  "password": "string",
  "id": "string",
  "username": "string",
  "email": "string",
  "is_admin": false
}
```

#### patch

enables to admin user to change given user to admin.

example request: 
```
{
  "is_admin": true
}
```
 
example response:

```
{
  "password": "string",
  "id": "string",
  "username": "string",
  "email": "string",
  "is_admin": false
}
```















