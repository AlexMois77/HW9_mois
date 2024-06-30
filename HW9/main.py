import subprocess

def run_script(script_name):
    result = subprocess.run(['poetry', 'run', 'python', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error running {script_name}: {result.stderr}")

def main():

    print("Running main9.py...")
    run_script('main9.py')

    # print("Running main9_2.py...")
    # run_script('main9_2.py')

    print("Running main8.py...")
    run_script('main8.py')

if __name__ == '__main__':
    main()

