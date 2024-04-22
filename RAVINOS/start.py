import json
import os
import re
import ravinos
import io


def process_user_config(custom_user_config, settings):
    # Remove unnecessary spaces around colon and double quotes
    custom_user_config = custom_user_config.replace(' :', ':')
    custom_user_config = custom_user_config.replace(': ', ':')
    custom_user_config = custom_user_config.replace('"', '')

    # Iterate through each line in the custom user config
    for line in custom_user_config.split(' '):
        line = line.strip()
        if not line:
            continue
        else:
            # Split parameter and value using regex
            param, value = re.split(r':\s*', line, 1)
            param_high = param.upper()
            modified_param = param_high
            modified_param = modified_param.replace('PAYOUTID', 'payoutId')
            modified_param = modified_param.replace('ACCESSTOKEN', 'accessToken')
            modified_param = modified_param.replace('HUGEPAGES', 'hugePages')
            modified_param = modified_param.replace('ALIAS', 'alias')
            modified_param = modified_param.replace('TRAINER', 'trainer')
            if param != modified_param:
                param = modified_param
            if value:
                if param == 'trainer':
                    value = value.replace("{", "").replace("}", "").replace(" ", "")
                    pairs = value.split(',')

                    if 'trainer' in settings:
                        trainer_data = settings['trainer']
                    else:
                        trainer_data = {}

                    for pair in pairs:
                        param_2, value_2 = pair.split(':')
                        if value_2 == 'false':
                            trainer_data[param_2] = False
                        elif value_2 == 'true':
                            trainer_data[param_2] = True
                        elif re.match(r'^[0-9]+(\.[0-9]+)?$', value_2):
                            trainer_data[param_2] = int(value_2)
                        else:
                            trainer_data[param_2] = value_2

                    settings['trainer'] = trainer_data
                else:
                    if value == 'null':
                        settings[param] = None
                    elif re.match(r'^[0-9]+(\.[0-9]+)?$', value):
                        settings[param] = int(value)
                    else:
                        settings[param] = value
    return settings


def run_program(mode, miner_dir, log_file, hugePages):
    run_command = "{}/qubminer.sh {} {} {} {}".format(miner_dir, miner_dir, log_file, mode, hugePages)
    ravinos.run(run_command)


def check_and_run(miner_dir, log_file, hugePages):
    # Check if CPU and GPU config files exist
    cpu_exists = os.path.exists("{}/cpu/appsettings.json".format(miner_dir))
    gpu_exists = os.path.exists("{}/gpu/appsettings.json".format(miner_dir))

    # Run program based on the existence of CPU and GPU config files
    if cpu_exists and gpu_exists:
        run_program(3, miner_dir, log_file, hugePages)  # Both CPU and GPU
    elif cpu_exists:
        run_program(2, miner_dir, log_file, hugePages)  # Only CPU
    elif gpu_exists:
        run_program(1, miner_dir, log_file, hugePages)  # Only GPU
    else:
        # Exit if no CPU and GPU config files are found
        print("ERROR: No CPU and GPU config file found, exiting")
        exit(1)


# Main script logic
cfg = ravinos.get_config()
miner_dir = cfg['miner_dir']
log_file = cfg['log_file']

# Read global settings
with io.open("{}/appsettings_global.json".format(miner_dir), 'r', encoding='utf-8-sig') as f:
    global_settings = json.load(f)['Settings']

# Copy qli-Client to CPU and GPU directories
os.system("cp {}/qli-Client {}/cpu/qli-Client".format(miner_dir, miner_dir))
os.system("cp {}/qli-Client {}/gpu/qli-Client".format(miner_dir, miner_dir))

# Copy lscpu tool to CPU and GPU directories
os.system("cp {}/syslib/lscpu {}/cpu/lscpu".format(miner_dir, miner_dir))
os.system("cp {}/syslib/lscpu {}/gpu/lscpu".format(miner_dir, miner_dir))

# Delete old settings files for CPU and GPU
os.system("rm -rf {}/cpu/appsettings.json".format(miner_dir))
os.system("rm -rf {}/gpu/appsettings.json".format(miner_dir))

# Processing the alias
if cfg['auth_config']['worker']:
    global_settings.update({"alias": cfg['auth_config']['worker']})

# Processing user configuration
if cfg['args']:
    args_string = " ".join(cfg['args'])
    global_settings = process_user_config(args_string, global_settings)

# Adding URL settings
url = cfg['coins'][0]['pools'][0]['url']
match = re.match(r"(https?://[^?]+)", url)
if match:
    global_settings.update({"baseUrl": match.group(1)})

# Settings for hugePages parameter
hugePages = global_settings.get('hugePages')

# Additional check in the Settings for only CPU mining
if global_settings.get('trainer', {}).get('gpu'):
    settings_gpu = global_settings.copy()
    settings_gpu['alias'] += '-gpu'
    settings_gpu.pop('hugePages', None)
    settings_gpu.setdefault('trainer', {}).update({'cpu': False})
    settings_gpu.setdefault('trainer', {}).update({'gpu': True})
    with open("{}/gpu/appsettings.json".format(miner_dir), 'w') as f:
        json.dump({'Settings': settings_gpu}, f)

# Additional check and modification in the Settings for CPU mining
if global_settings.get('trainer', {}).get('cpuThreads') and global_settings.get('trainer', {}).get('cpuThreads') != 0:
    settings_cpu = global_settings.copy()
    settings_cpu['alias'] += '-cpu'
    settings_cpu.pop('hugePages', None)
    settings_cpu.setdefault('trainer', {}).update({'cpu': True})
    settings_cpu.setdefault('trainer', {}).update({'gpu': False})
    with open("{}/cpu/appsettings.json".format(miner_dir), 'w') as f:
        json.dump({'Settings': settings_cpu}, f)

# Copy necessary libs
os.system("cp {}/syslib/*.* /usr/lib/".format(miner_dir))
os.system("cp {}/syslib/bash /bin/".format(miner_dir))

# Update LD_LIBRARY_PATH
os.environ['LD_LIBRARY_PATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('LD_LIBRARY_PATH', ''))

# Check and run the miner
check_and_run(miner_dir, log_file, hugePages)