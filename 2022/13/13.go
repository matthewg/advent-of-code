package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Item struct {
	Val *int
	Sub *Liszt
}

func Indent(indent int) {
	for i := 0; i < indent; i++ {
		fmt.Print(" ")
	}
}

func (i *Item) Compare(j *Item, indent int) int {
	Indent(indent)
	fmt.Printf("- Compare %v vs %v\n", *i, *j)
	if i.Val != nil && j.Val != nil {
		if *i.Val < *j.Val {
			Indent(indent + 2)
			fmt.Printf("- Left side is smaller, so inputs *are* in the right order.\n")
			return -1
		} else if *i.Val > *j.Val {
			fmt.Printf("- Right side is smaller, so inputs are *not* in the right order.\n")
			return 1
		} else {
			return 0
		}
	} else if i.Sub != nil && j.Sub != nil {
		ii := 0
		ij := 0
		var curI, curJ *Item
		for ii < len(i.Sub.Items) || ij < len(j.Sub.Items) {
			if ii < len(i.Sub.Items) && ij >= len(j.Sub.Items) {
				Indent(indent + 2)
				fmt.Printf("- Right side ran out of items, so inputs are *not* in the right order.\n")
				return 1
			} else if ii >= len(i.Sub.Items) && ij < len(j.Sub.Items) {
				Indent(indent + 2)
				fmt.Printf("- Left side ran out of items, so inputs *are* in the right order.\n")
				return -1
			}

			if ii < len(i.Sub.Items) {
				curI = &i.Sub.Items[ii]
			}
			if ij < len(j.Sub.Items) {
				curJ = &j.Sub.Items[ij]
			}

			if ret := curI.Compare(curJ, indent+2); ret != 0 {
				return ret
			}

			ii++
			ij++
		}
	} else {
		var newI, newJ *Item
		if i.Sub == nil {
			newJ = j
			sub := Liszt{Parent: nil, Items: []Item{*i}}
			item := Item{Val: nil, Sub: &sub}
			newI = &item
		} else {
			newI = i
			sub := Liszt{Parent: nil, Items: []Item{*j}}
			item := Item{Val: nil, Sub: &sub}
			newJ = &item
		}
		Indent(indent + 2)
		fmt.Printf("- Mixed types; convert and retry\n")
		return newI.Compare(newJ, indent)
	}
	return 0
}

func (i Item) String() string {
	if i.Val != nil {
		return fmt.Sprintf("%v", *i.Val)
	} else {
		return i.Sub.String()
	}
}

type Liszt struct {
	Parent *Liszt
	Items  []Item
}

func (l *Liszt) String() string {
	var x []string
	for _, i := range l.Items {
		x = append(x, i.String())
	}
	return fmt.Sprintf("[%v]", strings.Join(x, ","))
}

type PacketPair struct {
	A, B Item
}

func ParseLiszt(s string) Liszt {
	ret := Liszt{Parent: nil}
	tok := ""
	cur := &ret
	for c := 1; c < len(s); c++ {
		ch := s[c]
		if ch == ',' {
			if tok != "" {
				i, _ := strconv.Atoi(tok)
				//fmt.Printf("xxx %v: %v => %v\n", s, tok, i)
				cur.Items = append(cur.Items, Item{Val: &i, Sub: nil})
				tok = ""
			}
		} else if ch == '[' {
			l := Liszt{Parent: cur}
			cur.Items = append(cur.Items, Item{Val: nil, Sub: &l})
			cur = &l
		} else if ch == ']' {
			if tok != "" {
				i, _ := strconv.Atoi(tok)
				cur.Items = append(cur.Items, Item{Val: &i, Sub: nil})
				tok = ""
			}
			cur = cur.Parent
		} else {
			tok += string(s[c])
		}
	}
	fmt.Printf("Parse: %v => %v\n", s, ret)
	return ret
}

func ParsePacketPair(s string) PacketPair {
	toks := strings.Split(s, "\n")
	l1 := ParseLiszt(toks[0])
	l2 := ParseLiszt(toks[1])
	return PacketPair{
		Item{Val: nil, Sub: &l1},
		Item{Val: nil, Sub: &l2},
	}
}

type ByPacket []Item

func (a ByPacket) Len() int           { return len(a) }
func (a ByPacket) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByPacket) Less(i, j int) bool { return a[i].Compare(&a[j], 0) == -1 }

func main() {
	packetPairs := aocutils.Records(os.Args[1], "\n\n", ParsePacketPair)
	sm := 0

	packets := []Item{}
	for i, pair := range packetPairs {
		packets = append(packets, pair.A)
		packets = append(packets, pair.B)
		fmt.Printf("\n== Compare ==\n")
		fmt.Printf("%v\n", pair.A)
		fmt.Printf("%v\n", pair.B)
		if pair.A.Compare(&pair.B, 0) == -1 {
			fmt.Printf("Pair in right order: %v\n", i+1)
			sm += i + 1
		} else {
			fmt.Printf("Pair in wrong order: %v\n", i+1)
		}
	}
	fmt.Printf("Total: %v\n", sm)

	p := ParsePacketPair("[[2]]\n[[6]]")
	packets = append(packets, p.A)
	packets = append(packets, p.B)
	sort.Sort(ByPacket(packets))
	ss := 1
	for i, x := range packets {
		if x == p.A || x == p.B {
			ss *= (i + 1)
		}
	}
	fmt.Printf("Part 2: %v\n", ss)
}
