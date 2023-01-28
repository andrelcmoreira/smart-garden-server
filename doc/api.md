# sg-server

### 1. Brief Introduction

This document aims to describe the usage of all resources provided by sg-server
API, giving all information related to each defined endpoint (arguments,
available operations and expected results).

### 2. Endpoints

**Get a specific device**

`GET /devices/<string:id>`

**Arguments**

- **device-id**: Identification of device

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
    "message": "the device 'dev_id' isn't registered on database!"
}
```

**Register a new device**

`POST /devices`

**Arguments**

|   parameter   | mandatory |           description              |
|---------------|-----------|------------------------------------|
|     user      |    yes    | The user name registered on server |
|     token     |    yes    | The token of the user              |
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
