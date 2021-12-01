from pathlib import Path
import time
from rich import print
import rich.traceback
rich.traceback.install(show_locals=True)

def test_and_execute(the_func, day=None, test_assertion=None):
    """ Run the_func for both test and actual inputs, comparing
    the results from the test run with test_assertion.
    Prints results.    
    """
    assert(isinstance(day, str)) 

    print(f'For {the_func.__name__}')
    for input_index, input_path in enumerate((
            Path(__file__).parent / f'day{day}' / f'day{day}-test.txt',
            Path(__file__).parent / f'day{day}' / f'day{day}-input.txt')):
        with input_path.open('r') as f:
            lines = [line.strip() for line in f.readlines()]
        start = time.time()
        result = the_func(lines)
        duration = time.time() - start
        print(f'  {"test" if input_index == 0 else "actual"}  ({duration} seconds) result: {result}')
        if input_index == 0:
            assert(result == test_assertion)