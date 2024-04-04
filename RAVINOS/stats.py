#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import time
import ravinos as ro

cfg = ro.get_config()
log_file_path = cfg['log_file']

threshold = 3 * 60

hash_rate_regex = r'GPU #(\d+): (\d+) it/s'
cpu_hash_rate_regex = r'\| (\d+) it/s \|'
solution_regex = r'SOL: (\d+)/(\d+)'

# Delete statistic file if time from las change > threshold
if os.path.exists(log_file_path):
    last_modified = os.path.getmtime(log_file_path)
    current_time = time.time()

    if current_time - last_modified > threshold:
        open(log_file_path, 'w').close()

# If file big - flush
file_size = os.path.getsize(log_file_path)
if file_size > 100 * 1024:
    with open(log_file_path, 'r') as log_file_read:
        lines = log_file_read.readlines()[-200:]
    with open(log_file_path, 'w') as log_file_write:
        log_file_write.writelines(lines)

stats = ro.get_stats()

top = {}
total_accepted_gpu = 0
total_rejected_gpu = 0
total_accepted_cpu = 0
total_rejected_cpu = 0
cpu_hash_rate = 0

try:
    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()[-150:]

        client_type = 'gpu'

        for line in lines:

            if 'xGPU' in line:
                client_type = 'gpu'
            elif 'xCPU' in line:
                client_type = 'cpu'

            if 'Trainer:' in line and client_type == 'gpu':
                matches = re.findall(hash_rate_regex, line)
                for match in matches:
                    gpu_id, hash_rate = int(match[0]), int(match[1])
                    if gpu_id not in top or top[gpu_id] < hash_rate:
                        top[gpu_id] = hash_rate

            elif client_type == 'cpu':
                cpu_match = re.search(cpu_hash_rate_regex, line)
                if cpu_match:
                    cpu_hash_rate = int(cpu_match.group(1))

            sol_match = re.search(solution_regex, line)
            if sol_match:
                accepted, rejected = map(int, sol_match.groups())
                if client_type == 'gpu':
                    total_accepted_gpu = accepted
                    total_rejected_gpu = rejected
                elif client_type == 'cpu':
                    total_accepted_cpu = accepted
                    total_rejected_cpu = rejected

        for gpu in stats['mpu']:
            if gpu['id'] in top:
                gpu['hash_rate1'] = top[gpu['id']]
                if gpu['id'] == 0:
                    gpu['hash_rate2'] = cpu_hash_rate

        stats['shares']['accepted'] = total_accepted_gpu + total_accepted_cpu
        stats['shares']['rejected'] = (total_accepted_gpu + total_accepted_cpu) - (total_rejected_gpu + total_rejected_cpu)
        stats['shares']['invalid'] = (total_accepted_gpu + total_accepted_cpu) - (total_rejected_gpu + total_rejected_cpu)

except IOError as e:
    print("Error while extracting stats: {}".format(str(e)))

ro.set_stats(stats)
