#!/bin/bash

# Check if the number of arguments is not equal to 4, print usage message and exit if not
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <miner_dir> <log_file> <mode> <hugePages>"
    exit 1
fi

# Assign command line arguments to variables
miner_dir="$1"
log_file="$2"
mode="$3"
hugePages="$4"

# Initialize hugePagesCommand variable
hugePagesCommand=""

# Check if hugePages is not empty and contains only digits, if yes, assign sysctl command to hugePagesCommand
if [[ -n $hugePages && $hugePages != "None" && $hugePages =~ ^[0-9]+$ ]]; then
  hugePagesCommand="sysctl -w vm.nr_hugepages=$hugePages && "
fi

# Run different commands based on the mode using case statement
case $mode in
    1)
        # GPU execution
        tmux new-session -d -s gpu_session "cd $miner_dir/gpu && ./qli-Client | awk '{ print \"xGPU\", \$0 }' | tee -ai $log_file"
        ;;
    2)
        # CPU execution
        tmux new-session -d -s cpu_session "${hugePagesCommand}cd $miner_dir/cpu && ./qli-Client | awk '{ print \"xCPU\", \$0 }' | tee -ai $log_file"
        ;;
    3)
        # GPU execution
        tmux new-session -d -s gpu_session "cd $miner_dir/gpu && ./qli-Client | awk '{ print \"xGPU\", \$0 }' | tee -ai $log_file" &
        # CPU execution
        tmux new-session -d -s cpu_session "${hugePagesCommand}cd $miner_dir/cpu && ./qli-Client | awk '{ print \"xCPU\", \$0 }' | tee -ai $log_file"
        ;;
    *)
        echo "Invalid mode value. Should be 1, 2, or 3."
        exit 1
        ;;
esac