base response
```json
{
    "result": true,
    "error": false,
    "message": "success",
    "data": {
      "type": "some_type",
      ...
    }
}
```

room.create
```json
{
  "type": "room.create", 
  "payload": { 
    "join_type": "OPEN", 
    "room_type": "PUBLIC", 
    "room_name": "test", 
    "max_users": 8
  }
}
```

response of room.create
```json

```