package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) == 1 {
		fmt.Println("This program checks for broken links. Please specify -h for help.")
		os.Exit(1)
	}

	parseArgs()
}

func parseArgs() {
	if len(os.Args) < 3 {
		printUsage()
	}

	option := os.Args[1]
	switch option {
	case "-h":
		printUsage()
	case "-u":
		processLink(os.Args[2])
	case "-f":
		processFile(os.Args[2])
	default:
		printUsage()
	}
}

func printUsage() {
	fmt.Println("Usage: hdj -f [filename.html] or hdj -u [url]")
	os.Exit(0)
}

func processLink(link string) {
	fmt.Println(link)
	os.Exit(0)
}

func processFile(filename string) {
	fmt.Println(filename)
	os.Exit(0)
}
