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
  "msg": "Invalid user credentials"
}
```

#### 2.2 Devices

**Get a specific device**

`GET /devices/<id>`

**Expected response**

- **200** on success

```json
{
  "desc": "foo-desc",
  "dev_id": "foo-id",
  "model": "foo-model",
  "serial": "foo-number"
}
```

- **404** on error (when the device doesn't exist):

```json
{
  "msg": "The device isn't registered on database"
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
    "model": "foo-model",
    "serial": "foo-number"
  },
  {
    "desc": "bar-desc",
    "dev_id": "bar-id",
    "model": "bar-model",
    "serial": "bar-number"
  }
]
```

- **404** on error (when there's no devices registered on database):

```json
{
  "msg": "There's no devices registered on database"
}
```

**Register a new device**

`POST /devices`

**Arguments**

|   parameter   | mandatory |           description              |
|---------------|-----------|------------------------------------|
| serial-number |    yes    | The serial number of device        |
|     model     |    yes    | The model of device                |
|  description  |    no     | The description of device e        |

**Expected response**

- **201** on success

```json
{
  "msg": "Device registered with success"
}
```

**Unregister a device**

`DELETE /devices/<id>`

**Expected response**

- **200** on success
```json
{
  "msg": "Device unregistered with success"
}
```

- **404** on error
```json
{
  "msg": "The device isn\'t registered on database"
}
```

**Update a device**

`PUT /devices/<id>`

**Arguments**

|  parameter  | mandatory |                   description                   |
|-------------|-----------|-------------------------------------------------|
|    param    |    yes    | Parameter to be updated                         |
|    value    |    yes    | New value of the parameter to be updated        |

**Expected response**

- **200** on success

```json
{
  "msg": "Device updated with success"
}
```

- **404** on error

```json
{
  "msg": "The device isn't registered on database"
}
```

#### 2.2 Device configuration

**Get a specific device configuration**

`GET /devices/<id>/config`

**Expected response**

- **200** on success

```json
{
  "dev_id": "foo-id",
  "group": "foo-group",
  "interval": "foo-interval",
}
```

- **404** on error (when the config doesn't exist):

```json
{
  "msg": "There's not configuration for the specified device"
}
```

**Get all configurations**

`GET /devices/config`

**Expected response**

- **200** on success

```json
[
  {
    "dev_id": "foo-id",
    "group": "foo-group",
    "interval": "foo-interval"
  },
  {
    "dev_id": "bar-id",
    "group": "bar-group",
    "interval": "bar-interval"
  }
]
```

- **404** on error (when there's no config registered on database):

```json
{
  "msg": "There's no configuration registered on database"
}
```

**Register a new device configuration**

`POST /devices/<id>/config`

**Arguments**

|   parameter   | mandatory |           description              |
|---------------|-----------|------------------------------------|
|     group     |    no     | The group of device                |
|    interval   |    yes    | The operation interval of device   |

**Expected response**

- **201** on success

```json
{
  "msg": "Configuration registered with success"
}
```

**Unregister a device configuration**

`DELETE /devices/<id>/config`

**Expected response**

- **200** on success
```json
{
  "msg": "Configuration unregistered with success"
}
```

- **404** on error
```json
{
  "msg": "The device has no configuration"
}
```

**Update a device configuration**

`PUT /devices/<id>/config`

**Arguments**

|  parameter  | mandatory |                   description                   |
|-------------|-----------|-------------------------------------------------|
|    param    |    yes    | Parameter to be updated                         |
|    value    |    yes    | New value of the parameter to be updated        |

**Expected response**

- **200** on success

```json
{
  "msg": "Configuration updated with success"
}
```

- **404** on error

```json
{
  "msg": "There's no configuration for the specified device"
}
```
