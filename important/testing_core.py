import os
import threading
import subprocess

PYTHON_LOCATION = 'python3'
DIRECTORY = os.getcwd()
TIMEOUT_TIME = 5
RESULT = ""
current_module = ""
current_file = ""

def load_module(name):
    global RESULT
    global current_module
    result = {'output': None, 'error': None}

    def import_module():
        try:
            process = subprocess.Popen([PYTHON_LOCATION, f'/autograder/submission/{name}.py'],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate(timeout=TIMEOUT_TIME)
            result['output'] = output
            result['error'] = error
        except subprocess.TimeoutExpired as te:
            process.kill()
            result['error'] = f"TimeoutExpired"
    import_thread = threading.Thread(target=import_module)
    import_thread.start()
    import_thread.join()
    if result['error'].find('TimeoutExpired') != -1:
        raise TimeoutError(result['error'])

    current_module = name
    RESULT = result['output']

def ptest(expected): # short for print-test, as in, check stdout for particular outputs
    global RESULT
    if RESULT.find(expected) == -1:
        return False
    else: 
        return True

def ftest(actual, expected): # short for functional-test, as in, compares function with actual output
    try:
        print(f'Expected: {expected}')
        print(f'Actual: {eval(current_module + "." + actual)}')
        return expected == eval(current_module + '.' + actual)
    except:
        print(f'Expected: {expected}')
        print(f'Actual: {eval(current_module + "." + actual)}')
        return False

def import_code_from_file(file_path):
    try:
        file = open(file_path, 'r')
        file_content = file.read()
        return file_content
    finally:
        file.close()

def itest(substring): # short for instance-test, as in, counted instances
    global current_file
    return current_file.count(substring)