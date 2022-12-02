package aocutils

import (
	"bufio"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

type GridCell interface {
	Row() int
	Col() int
}

type Grid[T GridCell] [][]T

func (g *Grid[T]) Cell(row, col int) T {
	return (*g)[row-1][col-1]
}

func (g *Grid[T]) RowLen() int {
	return len(*g)
}

func (g *Grid[T]) ColLen() int {
	return len((*g)[0])
}

func GridNeighbors[T GridCell](g *Grid[T], cell T, diagonals bool) []T {
	var neighbors []T
	r := cell.Row()
	c := cell.Col()
	if diagonals && r > 1 && c > 1 {
		neighbors = append(neighbors, g.Cell(r-1, c-1))
	}
	if r > 1 {
		neighbors = append(neighbors, g.Cell(r-1, c))
	}
	if diagonals && r > 1 && c < g.ColLen() {
		neighbors = append(neighbors, g.Cell(r-1, c+1))
	}
	if c > 1 {
		neighbors = append(neighbors, g.Cell(r, c-1))
	}
	if c < g.ColLen() {
		neighbors = append(neighbors, g.Cell(r, c+1))
	}
	if diagonals && r < g.RowLen() && c > 1 {
		neighbors = append(neighbors, g.Cell(r+1, c-1))
	}
	if r < g.RowLen() {
		neighbors = append(neighbors, g.Cell(r+1, c))
	}
	if diagonals && r < g.RowLen() && c < g.ColLen() {
		neighbors = append(neighbors, g.Cell(r+1, c+1))
	}
	return neighbors
}

func LoadGrid[T GridCell](path string, convFn func(byte, int, int) T, g *Grid[T]) {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	rowNumber := 0
	for {
		var row []T
		line, err := reader.ReadString('\n')
		if err == nil {
			rowNumber += 1
			line = strings.TrimSuffix(line, "\n")
			for i := 0; i < len(line); i++ {
				char := line[i]
				convChar := convFn(char, rowNumber, i+1)
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
		if err == nil {
			convLine := convFn(line)
			lines = append(lines, convLine)
		} else if err == io.EOF {
			return lines
		} else {
			log.Fatalf("Error reading %v: %v", path, err)
		}
	}
}

func Records[T any](path, separator string, convFn func(string) T) []T {
	bs, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}

	s := string(bs)
	rs := strings.Split(s, separator)
	var records []T
	for i := 0; i < len(rs); i++ {
		records = append(records, convFn(rs[i]))
	}
	return records
}
