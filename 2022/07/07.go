package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Inode struct {
	Name      string
	Size      int
	Directory bool
	Children  map[string]*Inode
	Parent    *Inode
}

func (n *Inode) AddInode(name string, size int, directory bool) *Inode {
	child := Inode{
		Name:      name,
		Size:      size,
		Directory: directory,
		Children:  make(map[string]*Inode),
		Parent:    n,
	}
	n.Children[name] = &child
	for p := n; p != nil; p = p.Parent {
		p.Size += size
	}
	return &child
}

func (n Inode) DoTree(indent int, fn func(Inode, int)) {
	fn(n, indent)
	if n.Directory {
		children := make([]string, 0)
		for child, _ := range n.Children {
			children = append(children, child)
		}
		sort.Strings(children)
		for _, child := range children {
			n.Children[child].DoTree(indent+1, fn)
		}
	}
}

func PrintNode(n Inode, indent int) {
	for i := 0; i < indent; i++ {
		fmt.Printf("  ")
	}
	var dStr string
	if n.Directory {
		dStr = "dir"
	} else {
		dStr = "file"
	}
	fmt.Printf("- %v (%v, size=%v)\n", n.Name, dStr, n.Size)
}

func main() {
	bs, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}

	root := &Inode{
		Name:      "/",
		Size:      0,
		Directory: true,
		Children:  make(map[string]*Inode),
		Parent:    nil,
	}
	pwd := root
	for _, line := range strings.Split(string(bs), "\n") {
		if line == "" {
			continue
		}
		fmt.Printf("Input line: '%v'\n", line)
		toks := strings.Split(line, " ")
		if toks[0] == "$" {
			switch cmd := toks[1]; cmd {
			case "ls":
				continue
			case "cd":
				switch arg := toks[2]; arg {
				case "/":
					pwd = root
				case "..":
					pwd = pwd.Parent
				default:
					pwd = pwd.Children[arg]
				}
			default:
				log.Fatalf("Unknown command '%v'", cmd)
			}
			continue
		}

		if toks[0] == "dir" {
			pwd.AddInode(toks[1], 0, true)
		} else {
			size, e := strconv.Atoi(toks[0])
			if e != nil {
				log.Fatalf("Couldn't parse size '%v': %v", toks[1], e)
			}
			pwd.AddInode(toks[1], size, false)
		}
	}
	root.DoTree(0, PrintNode)

	smallDirSum := 0
	root.DoTree(0, func(n Inode, _ int) {
		if n.Directory && n.Size <= 100000 {
			fmt.Printf("Adding %v, %v\n", n.Name, n.Size)
			smallDirSum += n.Size
		}
	})
	fmt.Printf("Sum of small directories: %v\n", smallDirSum)

	freeSpace := 70000000 - root.Size
	const needFree = 30000000
	needSpace := needFree - freeSpace
	sizeToDelete := 70000000
	root.DoTree(0, func(n Inode, _ int) {
		if !n.Directory {
			return
		}
		if n.Size < sizeToDelete && n.Size >= needSpace {
			sizeToDelete = n.Size
		}
	})
	fmt.Printf("Delete a directory with size: %v\n", sizeToDelete)
}
