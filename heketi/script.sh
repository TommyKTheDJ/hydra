for serverIP in $(cat servers ); do

	echo "
sudo iptables -N HEKETI
sudo iptables -A HEKETI -p tcp -m state --state NEW -m tcp --dport 24007 -j ACCEPT
sudo iptables -A HEKETI -p tcp -m state --state NEW -m tcp --dport 24008 -j ACCEPT
sudo iptables -A HEKETI -p tcp -m state --state NEW -m tcp --dport 2222 -j ACCEPT
sudo iptables -A HEKETI -p tcp -m state --state NEW -m multiport --dports 49152:49251 -j ACCEPT
sudo modprobe dm_thin_pool
	" | ssh $serverIP bash

done
