import subprocess
import random
import time

# Paths to script_1.py and script_2.py
script1_path = './python/script_1.py'
script2_path = './python/script_2.py'

# Continuously execute script_1.py or script_2.py randomly
while True:
    # Randomly choose between script_1.py and script_2.py
    chosen_script = random.choice([script1_path, script2_path])

    # Execute the chosen script
    subprocess.run(['python3', chosen_script])

    # Wait for a random duration before executing the next script
    time.sleep(random.uniform(1, 3))  # Adjust the range as needed
