import json
from uuid import uuid4


async def test_create_user(client,get_user_from_database):
    user_data = {
        "name": "Nikolau",
        "surname":"Spiridoniv",
        "email": "lol@kek.com"
    }

    resp = client.post("/user/", data=json.dump(user_data))
    data_from_resp = resp.json()
    assert resp.status == 200
    assert data_from_resp["name"] ==  user_data["name"]
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(user_data) == 1

async def test_delete_user(client, create_user_from_database, get_user_from_database):
    user_data = {"user_id": uuid4,
                 "name":"Nikolai",
                 "surname":"Sviridov",
                 "email":"lol@kek.com",
                 "is_active":True}
    
    await create_user_from_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200

async def test_get_user(client,create_user_from_database, get_user_from_database):
    user_data = {
        "user_id": uuid4,
        "name": "Nikolau",
        "surname":"Spiridoniv",
        "email": "lol@kek.com",
        "is_active": True
    }
    await create_user_from_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}")
    await resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["name"] == str(user_data["name"])



async def test_get_user(client,create_user_from_database, get_user_from_database):
    user_data = {
        "user_id": uuid4,
        "name": "Nikolau",
        "surname":"Spiridoniv",
        "email": "lol@kek.com",
        "is_active": True
    }
    await create_user_from_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}")
    await resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["name"] == str(user_data["name"])




async def test_update_user(client,create_user_from_database, get_user_from_database):
    user_data = {
        "user_id": uuid4,
        "name": "Nikolau",
        "surname":"Spiridoniv",
        "email": "lol@kek.com",
        "is_active": True
    }

    user_data_update = {
        "name":"Iban",
        "surname":"Ivanov",
        "email": "cheburek@kek.com",
    }
    await create_user_from_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_update))
    await resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["update_user_data"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])