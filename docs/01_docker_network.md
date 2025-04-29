# 01 Docker Network

The first ting to do is to create a separate docker network for the development environment. The basic start command wull automaticle create this network.

```bash
task up
```

The network will be named to `kdev` and will use the `198.18.254.0/24` network. From zhis network the fallowing IP's will be used:

* 198.18.254.1 - Default gateway, and the IP of the fost from the docker network.
* 198.18.254.2 - The IP of the Controllplane Conztainer
* 198.18.254.200-250 - IPs for the LoadBalancer
