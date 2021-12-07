from pathlib import Path
import time
from rich import print
import rich.traceback
rich.traceback.install(show_locals=True)
from rich.panel import Panel

# console can be imported and used from other modules.
from rich.console import Console
console = Console()


def test_and_execute(the_func, day=None, test_assertion=None, path=Path(__file__)):
    """ Run the_func for both test and actual inputs, comparing
    the results from the test run with test_assertion.
    Prints results.    
    """
    assert(isinstance(day, str)) 

    console.rule(f'[bold red]{the_func.__name__}', align='left')
    for input_index, input_path in enumerate((
            path / f'day{day}-test.txt',
            path / f'day{day}-input.txt')):
        with input_path.open('r') as f:
            lines = [line.strip() for line in f.readlines()]
        start = time.time()
        result = the_func(lines)
        duration = time.time() - start
        print(f'[yellow]Duration:[/] {duration}')
        if input_index == 0:
            assert(result == test_assertion)
            console.print(f'[bold red]Test result:[/] [magenta on yellow]{result}[/]')
        else:
            console.print(f'[bold red]Real-deal result:[/] [magenta on yellow]{result}[/]')

    # print(Panel('\n'.join(output), title=f'{the_func.__name__} Results'))
