# PiGreen - Station

Supported sensors = "DHT22", "Clock"

## Sensor CRUD
### Create
`http POST localhost:5000/sensors/ pin={PIN_NUMBER} name={NAME} type={SENSOR_TYPE}`

### Get all
`http GET localhost:5000/sensors/`

`response = {"{SENSOR_TYPE}": [ids]`

### Get one
`http GET localhost:5000/sensors/{SENSOR_TYPE}/{SENSOR_ID}/`

### Delete one
`http DELETE localhost:5000/sensors/{SENSOR_TYPE}/{SENSOR_ID}/`

### Edit
Not supported