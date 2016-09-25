#for ubuntu 1404
#add service command
#modify line 205 to add cuda lib path
#export LD_LIBRARY_PATH="/usr/local/cuda/lib64"
sudo cp celeryobjdetd /etc/init.d/
#add service configuration
#need to adjust configuration
sudo cp celeryobjdetd-default /etc/default/celeryobjdetd
#to add startup at boot
sudo update-rc.d celeryobjdetd defaults 
#to remove startup at boot
#sudo update-rc.d -f celeryobjdetd remove
