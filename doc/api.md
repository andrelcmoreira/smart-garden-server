# sg-server

### 1. Brief Introduction

This document aims to describe the usage of all resources provided by sg-server
API, giving all information related to each defined endpoint (arguments,
available operations and expected results).

### 2. Endpoints

#### 2.1 Login

**Log an user**

`POST /login`

**Arguments**

|   parameter   | mandatory |         description         |
|---------------|-----------|-----------------------------|
|      user     |    yes    | User's name                 |
|    password   |    yes    | User's password             |

**Expected response**

- **200** on success

```json
{
    "token": "jwt-token"
}
```

- **400** on error (when lacking the user name or password):

```json
{
    "message": "invalid user credentials!"
}
```

#### 2.2 Devices

**Get a specific device**

`GET /devices/<string:id>`

**Arguments**

|   parameter   | mandatory |           description              |
|---------------|-----------|------------------------------------|
|   device-id   |    yes    | The ID of device                   |

**Expected response**

- **200** on success

```json
{
    "desc": "foo-desc",
    "dev_id": "foo-id",
    "group": "foo-group",
    "serial": "foo-number"
}
```

- **404** on error (when the device doesn't exist):

```json
{
    "message": "the device isn't registered on database!"
}
```

**Get all devices**

`GET /devices`

**Expected response**

- **200** on success

```json
[
    {
        "desc": "foo-desc",
        "dev_id": "foo-id",
        "group": "foo-group",
        "serial": "foo-number"
    },
    {
        "desc": "bar-desc",
        "dev_id": "bar-id",
        "group": "bar-group",
        "serial": "bar-number"
    }
]
```

- **404** on error (when there's no devices registered on database):

```json
{
    "message": "there's no devices registered on database!"
}
```

**Register a new device**

`POST /devices`

**Arguments**

|   parameter   | mandatory |           description              |
|---------------|-----------|------------------------------------|
|   device-id   |    yes    | The ID of device                   |
| serial-number |    yes    | The serial number of device        |
|  description  |    no     | The description of device e        |
|     group     |    yes    | The group of device                |

**Expected response**

- **201** on success

```json
{
    "message": "device registered with success!"
}
```

**Unregister a device**

`DELETE /devices/<string:id>`

**Arguments**

|   parameter   | mandatory |           description              |
|---------------|-----------|------------------------------------|
|   device-id   |    yes    | The ID of device                   |

**Expected response**

- **200** on success
```json
{
    "message": "device unregistered with success!"
}
```

- **404** on error
```json
{
    "message": "the device isn\'t registered on database!"
}
```

**Update a device**

`PUT /devices/<string:id>`

**Arguments**

|  parameter  | mandatory |                   description                   |
|-------------|-----------|-------------------------------------------------|
|  device-id  |    yes    | The ID of device                                |
|    param    |    yes    | Parameter to be updated                         |
|    value    |    yes    | New value of the parameter to be updated        |

**Expected response**

- **200** on success

```json
{
    "message": "device updated with success!"
}
```

- **404** on error

```json
{
    "message": "the device isn't registered on database!"
}
```
