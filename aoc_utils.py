from pathlib import Path
import time
from rich import print
import rich.traceback
rich.traceback.install(show_locals=True)

from rich.panel import Panel

def test_and_execute(the_func, day=None, test_assertion=None):
    """ Run the_func for both test and actual inputs, comparing
    the results from the test run with test_assertion.
    Prints results.    
    """
    assert(isinstance(day, str)) 

    output = []
    for input_index, input_path in enumerate((
            Path(__file__).parent / f'day{day}' / f'day{day}-test.txt',
            Path(__file__).parent / f'day{day}' / f'day{day}-input.txt')):
        with input_path.open('r') as f:
            lines = [line.strip() for line in f.readlines()]
        start = time.time()
        result = the_func(lines)
        duration = time.time() - start
        output.append(f'{"test" if input_index == 0 else "actual"} result: {result}')
        if input_index == 0:
            assert(result == test_assertion)
    print(Panel('\n'.join(output), title=f'{the_func.__name__} Results'))
