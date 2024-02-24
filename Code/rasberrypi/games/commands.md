# Commands
-------------------
# LED Commands
Set Game
```json
{
    "command":"set_game",
    "args1":"speed",
    "args2":"",
}
--RESPONSE-->
{
    "command":"set_game",
    "args1":"speed",
    "args2":"",
}
```

Sends a response in 3 seconds after finised countdown
```json
{
    "command":"start_countdown",
    "args1":"3", # time in seconds
    "args2":"",
}
--RESPONSE-->
{
    "command":"start_countdown",
    "args1":"",
    "args2":""
}
```
Wait for swing or send error if not in time
```json
{
    "command":"wait_swing",
    "args1":"10", # time in seconds
    "args2":"",
}
--RESPONSE-->
{
    "command":"wait_swing",
    "args1":"2", # time taken (-1 on timeout)
    "args2":""
}
```
```json
{
    "command":"set_led",
    "args1":"255;255;255", # farbe
    "args2":255,           # helligkeit
}
```
```json
{
    "command":"animation",
    "args1":"ring",
    "args2":"",
}
```
```json
{
    "command":"flash",
    "args1":"",
    "args2":"",
}
```