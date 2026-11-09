# MQTT Broker - Eclipse Mosquitto

In this configuration we are going to use the official Eclipse Mosquitto Broker image available on Docker Hub at the following link: [https://hub.docker.com/_/eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto)

The target used image and version for this playground is: `eclipse-mosquitto:2.0.22`

The `mosquitto.conf` file of this folder enables a listener on port `1883` accepting anonymous connections:

```
listener 1883
allow_anonymous true
```

We are customizing our MQTT Broker using the following customization at runtime:

- local configuration file `mosquitto.conf` using `-v <LOCAL_PATH>/mosquitto.conf:/mosquitto/config/mosquitto.conf`
- local folder for data in order to keep a local persistence of exchanged information supporting QoS 1 and QoS 2 scenarios using `-v <LOCAL_PATH>/data:/mosquitto/data`
- local folder to collect logs locally using `-v <LOCAL_PATH>/log:/mosquitto/log` and having access also if the container will be destroyed
- mapping port with `-p 1883:1883`
- restart always parameter `--restart always`
- daemon mode `-d`

The resulting Run command is:

```bash
docker run --name=my-mosquitto-broker -p 1883:1883 -v <LOCAL_PATH>/mosquitto.conf:/mosquitto/config/mosquitto.conf -v <LOCAL_PATH>/data:/mosquitto/data -v <LOCAL_PATH>/log:/mosquitto/log --restart always -d eclipse-mosquitto:2.0.22
```

On Linux and macOS (and in Windows PowerShell) you can use `${PWD}` to refer to the current folder:

```bash
docker run --name=my-mosquitto-broker -p 1883:1883 -v ${PWD}/mosquitto.conf:/mosquitto/config/mosquitto.conf -v ${PWD}/data:/mosquitto/data -v ${PWD}/log:/mosquitto/log --restart always -d eclipse-mosquitto:2.0.22
```
