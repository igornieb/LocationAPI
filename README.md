# LocationAPI

## API endpoints

### /places/list

#### get
Returns list of places that are set as published.

response:
```
[
    {
        "published": true,
        "name": "content",
        "description": "content",
        "id": "b8ce49eb-ff60-4779-8a94-2d17dab2c864"
    },
    {
        "published": true,
        "name": "content",
        "description": "content",
        "id": "b1d5c3c2-a1d5-4175-9bb3-68b7f1b0a135"
    }
]
```
code: `200`

#### post
Creating new place for admins to publish.

example:
```
{
    "name": "content",
    "description": "content",
}
```