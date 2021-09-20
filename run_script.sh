#!/bin/bash


while true
do  
  su transfer -c "python /creation_smbk_link.py"
  
  sleep 3600

done
