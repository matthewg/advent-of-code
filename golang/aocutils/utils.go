package aocutils

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math"
	"os"
	"strconv"
	"strings"

	"github.com/oleiade/lane/v2"
)

func Abs(i int) int {
	if i < 0 {
		return i * -1
	} else {
		return i
	}
}

func Max(a, b int) int {
	if a > b {
		return a
	} else {
		return b
	}
}

func Min(a, b int) int {
	if a < b {
		return a
	} else {
		return b
	}
}

func Atoi(s string) int {
	ret, err := strconv.Atoi(s)
	if err != nil {
		log.Fatalf("Error converting string '%v': %v", s, err)
	}
	return ret
}

type Node[T interface{}] struct {
	Edges []Edge[T]
	Data  T
}

type Edge[T interface{}] struct {
	Weight      int
	Destination *Node[T]
}

func NewNode[T interface{}](d T) *Node[T] {
	return &Node[T]{
		Edges: []Edge[T]{},
		Data:  d,
	}
}

func (n *Node[T]) AddEdge(w int, d *Node[T], symmetric bool) {
	n.Edges = append(n.Edges, Edge[T]{Weight: w, Destination: d})
	if symmetric {
		d.AddEdge(w, n, false)
	}
}

func (n *Node[T]) BFS() []*Node[T] {
	visited := make(map[*Node[T]]bool)
	var unvisited []*Node[T]
	unvisited = append(unvisited, n)

	var ret []*Node[T]
	//fmt.Printf("Running BFS...\n")
	for len(unvisited) > 0 {
		//fmt.Printf("Unvisited len: %v\n", len(unvisited))
		c := unvisited[0]
		unvisited = unvisited[1:]
		visited[c] = true
		ret = append(ret, c)
		for _, e := range c.Edges {
			m := e.Destination
			if _, ok := visited[m]; !ok {
				unvisited = append(unvisited, m)
				visited[m] = true
			}
		}
	}
	return ret
}

func (n *Node[T]) DijkstraShortestPath(d *Node[T]) int {
	distance := make(map[*Node[T]]int)
	distance[n] = 0

	//fmt.Printf("Running Dijkstra...")
	pred := make(map[*Node[T]]*Node[T])
	queue := lane.NewMinPriorityQueue[*Node[T], int]()
	for _, m := range n.BFS() {
		if m != n {
			distance[m] = math.MaxInt
			pred[m] = nil
		}
		queue.Push(m, distance[m])
	}
	//fmt.Printf("Assembled queue: %v\n", queue)

	for queue.Size() > 0 {
		//fmt.Printf("iter, qsize %v\n", queue.Size())
		m, p, _ := queue.Pop()
		if p != distance[m] {
			continue
		}
		for _, e := range m.Edges {
			o := e.Destination
			alt := distance[m] + e.Weight
			if alt < distance[o] {
				distance[o] = alt
				pred[o] = m
				queue.Push(o, distance[o])
			}
		}
	}
	//fmt.Printf("iter done\n")

	pathCost := distance[d]
	/*
		path := []*Node[T]{d}
		c := d
		for c != n {
			fmt.Printf("Current node: %v\n")
			m := pred[c]
			path = append(path, m)
			c = m
		}
	*/
	//fmt.Printf("Done\n")
	return pathCost
}

type GridCell interface {
	Row() int
	Col() int
}
type Vector struct {
	DeltaR, DeltaC int
}

func (v Vector) String() string {
	return fmt.Sprintf("<%v,%v>", v.DeltaR, v.DeltaC)
}

type Grid[T GridCell] [][]T
type GridIterator[T GridCell] struct {
	Row, Col int
	Grid     *Grid[T]
}

func (g *GridIterator[T]) Next() *T {
	g.Col++
	if g.Col > g.Grid.ColLen() {
		g.Col = 1
		g.Row++
	}
	if g.Row > g.Grid.RowLen() {
		return nil
	}
	ret := g.Grid.Cell(g.Row, g.Col)
	return ret
}

func (g *Grid[T]) NewIterator() GridIterator[T] {
	return GridIterator[T]{1, 0, g}
}

func (g *Grid[T]) Cell(row, col int) *T {
	return &(*g)[row-1][col-1]
}

func (g *Grid[T]) RowLen() int {
	return len(*g)
}

func (g *Grid[T]) ColLen() int {
	return len((*g)[0])
}

func GridNeighbors[T GridCell](g *Grid[T], cell T, diagonals bool) []*T {
	var neighbors []*T
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

func LoadGrid[T GridCell](path string, convFn func(rune, int, int) T, g *Grid[T]) {
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
			for i, c := range line {
				convChar := convFn(c, rowNumber, i+1)
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
