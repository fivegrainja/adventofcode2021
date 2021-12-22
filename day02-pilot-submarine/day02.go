
package main

import (
	string
	strconv
)

// def part_a(lines):
//     forward = 0
//     depth = 0
//     for line in lines:
//         command, amount = line.split(' ')
//         amount = int(amount)
//         match command:
//             case 'forward':
//                 forward += amount
//             case 'down':
//                 depth += amount
//             case 'up':
//                 depth -= amount
//             case _:
//                 raise Exception(f'Unrecognized command {command}')
//     print(f'{forward=}')
//     print(f'{depth=}')
//     return forward * depth

func partA(lines []string) int {
	forward := 0
	depth := 0
	for _, line:= range lines {
		command, amountStr := string.Fields(line)
		amount := strconv.Atoi(amountStr)
		switch command {
		case "forward":
			forward += amount
		case "down":
			depth += amount
		case "up":
			depth -= amount
		}
	}
	return forward * depth
}