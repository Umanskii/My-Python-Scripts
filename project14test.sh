#!/bin/bash


echo $(date)
#cpu use threshold
cpu_threshold="80"
 #mem idle threshold
mem_threshold="80"
#disk use threshold
disk_threshold="90"


tentech_webhook="https://hooks.slack.com/services/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"
echo -e"\n#################### Checking Memory, Disk space, and CPU on $HOSTNAME  ####################"

ssh ec2-user@54.167.247.196 disk_utilization
# Check if disk utilization exceeds the threshold
if [[ "$disk_utilization" -gt "$disk_threshold" ]]; then
    echo "Disk utilization is above $disk_threshold%. Alert required!"
else
    echo "Disk utilization is below $disk_threshold%. No immediate action required."
fi
ssh ec2-user@54.167.247.196 mem_utilization
# Check if mem utilization exceeds the threshold
if [[ "$mem_utilization" -gt "$mem_threshold" ]]; then
    echo "Memory utilization is above $mem_threshold%. Alert required!"
else
    echo "Memory utilization is below $mem_threshold%. No immediate action required."
fi
ssh ec2-user@54.167.247.196 cpu_utilization
# Check if disk utilization exceeds the threshold
if [[ "$cpu_utilization" -gt "$cpu_threshold" ]]; then
    echo "Cpu utilization is above $cpu_threshold%. Alert required!"
else
    echo "Cpu utilization is below $cpu_threshold%. No immediate action required."
fi