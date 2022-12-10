package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Pos struct {
	R, C int
}
type Vector struct {
	dR, dC int
}

func (p Pos) String() string {
	return fmt.Sprintf("(%v,%v)", p.R, p.C)
}
func (v Vector) String() string {
	return fmt.Sprintf("<%v,%v>", v.dR, v.dC)
}

func ParseMove(s string) Vector {
	toks := strings.Split(s, " ")
	m, _ := strconv.Atoi(toks[1])
	switch toks[0] {
	case "U":
		return Vector{dR: 0, dC: -m}
	case "D":
		return Vector{dR: 0, dC: m}
	case "L":
		return Vector{dR: -m, dC: 0}
	case "R":
		return Vector{dR: m, dC: 0}
	default:
		return Vector{dR: 0, dC: 0}
	}
}

type StepIterator struct {
	cur, dst Pos
}

func NewIterator(cur, dst Pos) StepIterator {
	return StepIterator{
		cur: cur,
		dst: dst,
	}
}

func Move(p Pos, v Vector) Pos {
	return Pos{
		R: p.R + v.dR,
		C: p.C + v.dC,
	}
}

type Grid map[Pos]bool

func (g *Grid) Visit(p Pos) {
	(*g)[p] = true
}

func (s *StepIterator) Step() *Pos {
	if s.dst.R > s.cur.R {
		s.cur.R += 1
	} else if s.dst.R < s.cur.R {
		s.cur.R -= 1
	} else if s.dst.C > s.cur.C {
		s.cur.C += 1
	} else if s.dst.C < s.cur.C {
		s.cur.C -= 1
	} else {
		return nil
	}
	return &s.cur
}

func Clamp(i int) int {
	if i >= 1 {
		return 1
	} else if i <= -1 {
		return -1
	} else {
		return 0
	}
}

func Abs(i int) int {
	if i < 0 {
		return i * -1
	} else {
		return i
	}
}

func main() {
	moves := aocutils.Lines(os.Args[1], ParseMove)

	// Day 1
	g := make(Grid)
	head := Pos{
		R: 0,
		C: 0,
	}
	g.Visit(head)
	tail := head

	for _, m := range moves {
		//fmt.Printf("h @ %v, t @ %v: %v\n", head, tail, m)
		newHead := Move(head, m)
		s := StepIterator{head, newHead}
		for h := &head; h != nil; h = s.Step() {
			head = *h

			dR := head.R - tail.R
			dC := head.C - tail.C
			if Abs(dR) > 1 || Abs(dC) > 1 {
				tail = Move(tail, Vector{dR: Clamp(dR), dC: Clamp(dC)})
			}

			g.Visit(tail)
			//fmt.Printf("...h -> %v, t -> %v\n", head, tail)
		}
	}
	fmt.Printf("Visited cells by tail (day 1): %v\n", len(g))

	// Day 2
	g = make(Grid)
	head = Pos{
		R: 0,
		C: 0,
	}
	g.Visit(head)
	knots := [10]Pos{head, head, head, head, head, head, head, head, head, head}

	for _, m := range moves {
		//fmt.Printf("h @ %v, t @ %v: %v\n", head, tail, m)
		newHead := Move(knots[0], m)
		s := StepIterator{knots[0], newHead}
		for h := &knots[0]; h != nil; h = s.Step() {
			knots[0] = *h

			for i := 1; i < len(knots); i++ {
				lead := knots[i-1]
				follow := knots[i]
				dR := lead.R - follow.R
				dC := lead.C - follow.C
				if Abs(dR) > 1 || Abs(dC) > 1 {
					knots[i] = Move(follow, Vector{dR: Clamp(dR), dC: Clamp(dC)})
				}
			}
			g.Visit(knots[9])
			//fmt.Printf("...h -> %v, t -> %v\n", head, tail)
		}
	}
	fmt.Printf("Visited cells by tail (day 2): %v\n", len(g))

}
