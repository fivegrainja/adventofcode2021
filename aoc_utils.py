from pathlib import Path
import time
from rich import print
import rich.traceback
rich.traceback.install(show_locals=True)

def test_and_execute(the_func, day=None, test_assertion=None):
    """ Read both the test and actual input files for the given day.
    Call the_func twice passing it a list of stripped lines read first
    from the test input then from the actual input. If we have a value
    for test_assertion then assert that the return value from
    the_func(<test input>) is equal to test_assertion.
    Print return value from both runs of the_func.
    """
    assert(isinstance(day, str)) 

    for input_index, input_path in enumerate((
            Path(__file__).parent / f'day{day}' / f'day{day}-test.txt',
            Path(__file__).parent / f'day{day}' / f'day{day}-input.txt')):
        with input_path.open('r') as f:
            lines = [line.strip() for line in f.readlines()]
        start = time.time()
        result = the_func(lines)
        duration = time.time() - start
        print(f'{"test" if input_index == 0 else "actual"}  ({duration} seconds) result: {result}')
        if input_index == 0:
            assert(result == test_assertion)