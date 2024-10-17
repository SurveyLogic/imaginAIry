## API Routes

Routes are defined in the `routes` folder.


## Agent routes
## GET /agent

Return the agent information

```json
[
    {
        "description": "This is an agent to summarize the given video of VideoDB.",
        "name": "summary"
    },
    {
        "description": "Get the download URLs of the VideoDB generated streams.",
        "name": "download"
    },
    {
        "description": "Agent to get information about the pricing and usage of VideoDB, it is also helpful for running scenarios to get the estimates.",
        "name": "pricing"
    }
]
```

## Session routes

## GET /session

Returns all the sessions

```json
[
    {
        "collection_id": "c-890bd0a5-2ec3-47c0-86dc-685953995206",
        "created_at": 1729092742,
        "metadata": {},
        "session_id": "52881f6b-7560-4844-ac35-52af41d07ab8",
        "updated_at": 1729092742,
        "video_id": "m-138de44f-d963-4a4c-a239-a30df4dc496a"
    },
    {
        "collection_id": "c-890bd0a5-2ec3-47c0-86dc-685953995206",
        "created_at": 1729092642,
        "metadata": {},
        "session_id": "6bf075a7-e7d4-4aba-985c-4cf0d3dc6f5b",
        "updated_at": 1729092642,
        "video_id": "m-13d436a6-ad61-410d-b51c-5ebd80e87066"
    }
]
```
