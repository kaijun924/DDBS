# setup DNS server for solving docker container hostnames,打开一个新的terminal
sudo docker rm -f dns-proxy-server > /dev/null
sudo docker run --hostname dns.mageddo --name dns-proxy-server -p 5380:5380 \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /etc/resolv.conf:/etc/resolv.conf \
defreitas/dns-proxy-server