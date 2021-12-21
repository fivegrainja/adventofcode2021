package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

// Yeah - my first go program! I'm sure it shows. :-)

// Return num of increases in depth
func numIncreasing(depths []int) int {
	count := 0
	for i, _ := range depths[:len(depths)-1] {
		if depths[i] < depths[i+1] {
			count += 1
		}
	}
	return count
}

// Return sum of a list of ints
func sum(depths []int) int {
	sum := 0
	for _, d := range depths {
		sum += d
	}
	return sum
}

// Compare sliding windows of len 3 with the window starting at the next depth
// and return the number that are smaller than the window immediately following them.
func numIncreasingWindow(depths []int) int {
	count := 0
	for i, _ := range depths[:len(depths)-3] {
		if sum(depths[i:i+3]) < sum(depths[i+1:i+4]) {
			count += 1
		}
	}
	return count
}

// Read the contents of the file and return a string of ints
func readDepths(fname string) []int {
	file, _ := os.Open(fname)
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	var text []string

	for scanner.Scan() {
		text = append(text, scanner.Text())
	}
	file.Close()

	var depths []int
	for _, line := range text {
		i, _ := strconv.Atoi(line)
		depths = append(depths, i)
	}
	return depths
}

func main() {
	// Part A
	var count int
	test_depths := readDepths("day01-test.txt")
	count = numIncreasing(test_depths)
	fmt.Printf("Part a sample: %d\n", count)
	real_depths := readDepths("day01-input.txt")
	count = numIncreasing(real_depths)
	fmt.Printf("Part a actual: %d\n", count)

	// Part B
	count = numIncreasingWindow(test_depths)
	fmt.Printf("Part b sample: %d\n", count)
	count = numIncreasingWindow(real_depths)
	fmt.Printf("Part b actual: %d\n", count)
}
