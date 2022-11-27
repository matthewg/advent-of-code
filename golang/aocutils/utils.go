package aocutils

import (
	"bufio"
	"io"
	"log"
	"os"
)

func Lines(path string) []string {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var lines []string
	reader := bufio.NewReader(file)
	for {
		line, err := reader.ReadString('\n')
		if err == nil {
			lines = append(lines, line)
		} else if err == io.EOF {
			return lines
		} else {
			log.Fatalf("Error reading %v: %v", path, err)
		}
	}
}
