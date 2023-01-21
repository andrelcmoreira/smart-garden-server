# sg-server

### 1. Brief Introduction

This document aims to describe the usage of all resources provided by sg-server
API, giving all information related to each defined endpoint (arguments,
available operations and expected results).

### 2. Endpoints

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
