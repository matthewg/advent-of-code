package aocutils

import (
	"bufio"
	"io"
	"log"
	"os"
	"strings"
)

type GridCell interface {
	Row() int
	Col() int
}

type Grid[T GridCell] [][]T

func (g *Grid[t]) Cell(row, col int) T {
	return (*g)[row-1][col-1]
}

func (g *Grid[T]) RowLen() int {
	return len(*g)
}

func (g *Grid[T]) ColLen() int {
	return len((*g)[0])
}

func GridNeighbors[T GridCell](g *Grid[T], cell T) []T {
	var neighbors []T
	r := cell.Row()
	c := cell.Col()
	if r > 1 && c > 1 {
		neighbors = append(neighbors, g.Cell(r-1, c-1))
	}
	if r > 1 {
		neighbors = append(neighbors, g.Cell(r-1, c))
	}
	if r > 1 && c < g.ColLen() {
		neighbors = append(neighbors, g.Cell(r-1, c+1))
	}
	if c > 1 {
		neighbors = append(neighbors, g.Cell(r, c-1))
	}
	if c < g.ColLen() {
		neighbors = append(neighbors, g.Cell(r, c+1))
	}
	if r < g.RowLen() && c > 1 {
		neighbors = append(neighbors, g.Cell(r+1, c-1))
	}
	if r < g.RowLen() {
		neighbors = append(neighbors, g.Cell(r+1, c))
	}
	if r < g.RowLen() && c < g.ColLen() {
		neighbors = append(neighbors, g.Cell(r+1, c+1))
	}
	return neighbors
}

func LoadGrid[T GridCell](path string, convFn func(byte) T, g *Grid[T]) {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	for {
		var row []T
		line, err := reader.ReadString('\n')
		if err == nil {
			line = strings.TrimSuffix(line, "\n")
			for i := 0; i < len(line); i++ {
				char := line[i]
				convChar := convFn(char)
				row = append(row, convChar)
			}
		} else if err == io.EOF {
			return
		} else {
			log.Fatalf("Error reading %v: %v", path, err)
		}
		*g = append(*g, row)
	}
}

func Lines[T any](path string, convFn func(string) T) []T {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var lines []T
	reader := bufio.NewReader(file)
	for {
		line, err := reader.ReadString('\n')
		line = strings.TrimSuffix(line, "\n")
		convLine := convFn(line)
		if err == nil {
			lines = append(lines, convLine)
		} else if err == io.EOF {
			return lines
		} else {
			log.Fatalf("Error reading %v: %v", path, err)
		}
	}
}
