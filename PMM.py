import os
import sys
import builtins
from pathlib import Path
import subprocess
import string

DEBUG = True
path_to_PMM = '/Users/guang/Projects/42_piscine/C00/PMM.py'

if 'ipykernel' in sys.modules:
    path = Path(path_to_PMM)
else:
    path = Path(os.path.realpath(__file__))
parent_path = path.parent.absolute()

def get_input(prompt:str, test_vals:list=None, type_cast:str=None):
    u_input = input(prompt)

    if (test_vals == None) and (type_cast == None): return u_input

    caster = getattr(builtins, type_cast)
    try:
        u_input = caster(u_input)
    except Exception as e:
        if DEBUG: print(e)
        return get_input(prompt, test_vals, type_cast)

    if u_input in test_vals:
        return u_input

    return get_input(prompt, test_vals, type_cast)


def run_script(script, stdin=None):
    """
    Returns (stdout, stderr), raises error on non-zero return code
    src: https://stackoverflow.com/questions/2651874/embed-bash-in-python <- dayum beautiful
    """
    # Note: by using a list here (['bash', ...]) you avoid quoting issues, as the
    # arguments are passed in exactly this order (spaces, quotes, and newlines won't
    # cause problems):
    proc = subprocess.Popen(['bash', '-c', script],  # check: may need 'zsh' here
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise ScriptException(proc.returncode, stdout, stderr, script)

    return stdout, stderr


class ScriptException(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        Exception().__init__('Error in script')


def compile_and_run_C(filename):
    outname = filename.split('.')[0]
    gcc_cmd = f'cd {parent_path}; gcc -Wall -Wextra -Werror {filename} -o {outname}; ./{outname}'
    stdout, stderr = run_script(gcc_cmd)
    stdout = stdout.decode("utf-8").split('\n')
    stderr = stderr.decode("utf-8").split('\n')

    return stdout, stderr


def test_ft_putchar():
    stdout, stderr = compile_and_run_C('test_ft_putchar.c')
    if stdout[0] == 'c':
        print('ex00: ft_putchar.c OK!')
        return True
    print('ft_putchar FAILED! Expected "c" Got:')
    print(f'stdout: {stdout}')
    print(f'stderr: {stderr}')

    return False


def test_ft_print_alphabet():
    stdout, stderr = compile_and_run_C('test_ft_print_alphabet.c')
    if stdout[0] == string.ascii_lowercase:
        print('ex01: ft_print_alphabet.c OK!')
        return True
    print('ft_print_alphabet FAILED! Expected "{string.ascii_lowercase}" Got:')
    print(f'stdout: {stdout}')
    print(f'stderr: {stderr}')

    return False


def test_ft_print_reverse_alphabet():
    stdout, stderr = compile_and_run_C('test_ft_print_reverse_alphabet.c')
    if stdout[0] == string.ascii_lowercase[::-1]:
        print('ex02: ft_print_reverse_alphabet.c OK!')
        return True
    print('ft_print_reverse_alphabet FAILED! Expected "{string.ascii_lowercase[::-1]}" Got:')
    print(f'stdout: {stdout}')
    print(f'stderr: {stderr}')

    return False


def test_ft_is_negative():
    stdout, stderr = compile_and_run_C('test_ft_is_negative.c')
    if stdout[0] == 'NPP':
        print('ex03: ft_is_negative.c OK!')
        return True
    print('ft_is_negative Failed! Expected "{string.ascii_lowercase[::-1]}" Got:')
    print(f'stdout: {stdout}')
    print(f'stderr: {stderr}')

    return False

def test_c00():
    test_ft_putchar()
    test_ft_print_alphabet()
    test_ft_print_reverse_alphabet()


def main():
    prompt = 'What\'s the answer to life, the universe, and everything?\n>'
    test_vals = [42]
    type_cast = 'int'
    get_input(prompt, test_vals, type_cast)
    print('You shall proceed...')

    # Empty/Wrong folder convention name check
    def check_empty_submission():
        # todo: move out of main()
        print('Testing empty work... ', end='')
        set_possible_dirs = set([f'ex{i}'  if i >= 10 else f'ex0{i}' for i in range(100)])  # Hopefully 42 will not give us 100 questions
        set_dirs = set(os.listdir(parent_path))
        found_dirs = set_possible_dirs.intersection(set_dirs)
        if len(found_dirs) == 0:
            print(f'failed! Only found: {set_dirs}')
            return False
        print('passed!')
        print(f'Found: {found_dirs}')

        return True

    if not check_empty_submission(): return

    # Check what day you're on, only works if you submit ex00, for now
    def detect_sig():
        """todo: move this outside main()
        """
        ex00_path = os.path.join(parent_path, 'ex00')
        ex00_files = os.listdir(ex00_path)

        day = ''
        count = 0
        if 'ft_putchar.c' in ex00_files:
            print('Signature detected: found: ft_putchar.c. It\'s C00')
            day = "C00"
            count += 1

        if count > 1:  # can't use this 42 may asked for multiple submissions
            print("WARN: Multiple Signature found. You may want to delete files not asked to submit.")
            # return ''

        return day

    day = detect_sig()
    if day == '':
        print('Day not found.')
        return
    if day == 'C00':
        test_c00()

if __name__ == "__main__":
    main()
