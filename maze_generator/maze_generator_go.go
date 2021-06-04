package main

import "C"

import (
	"fmt"
	"log"
	"math/rand"
	"os"
)

func main() {
	// labyrinthe(25, 35)
}

//export labyrinthe
func labyrinthe(l int, h int, seed int) {
	/*
		Function that will be called by python program to generate a maze
		it create every variables that the program need to work
		:param l : length of the maze
		:param h : the height of the maze
		:param seed: the seed for the maze
	*/
	// init vars

	// dimensions
	var longueur int = l
	var hauteur int = h

	// board dimension
	var boardl int = longueur*2 + 1
	var boardh int = hauteur*2 + 1

	// list of case with number in labyrinthe
	var possiblex = make_range_two(1, boardl)
	var possibley = make_range_two(1, boardh)

	// terrain
	var board [][]int

	// generate corectly the board
	for y := 0; y < boardh; y++ {
		temp_slice := []int{}
		for x := 0; x < boardl; x++ {
			temp_slice = append(temp_slice, -1)
		}

		board = append(board, temp_slice)
	}

	// random
	var posx = make_range_two(1, boardl)
	var posy = make_range_two(1, boardh)

	var posxs = randomize_list(longueur, posx)
	var posys = randomize_list(hauteur, posy)

	// generate

	// set random seed
	rand.Seed(int64(seed))

	// create new random list
	posxs = randomize_list(longueur, posxs)
	posys = randomize_list(hauteur, posys)

	// prepare board
	board = set_numbers(board, possiblex, possibley, longueur, hauteur)

	// generate
	generate_labyrinthe(board, longueur, hauteur, posxs, posys, possiblex, possibley)
	// affiche(board, boardl, boardh)
	save_board(board, boardh, boardl)

}

func generate_labyrinthe(board [][]int, length, height int, posxs, posys, possiblex, possibley []int) {
	/*
		This function is the main function that will generate a maze
		:param board : the main maze
		:param length: the length of the maze
		:param height: the height of the maze
		:param posxs, posys, possiblex, possibley : list that tell where randomely break the maze
	*/
	rx := 0
	ry := 0
	rx++
	ry++

	// in first time break randomely every case by following the random instruction of posxs and posys
	for y := 0; y < height; y++ {
		for x := 0; x < length; x++ {
			board = update_case(board, posxs[x], posys[y], length, height)

		}
	}

	// now while the maze is not finished  coninue breaking randomly case

	for {

		if is_finished(board, length, height) == true {
			break
		}
		for i := 0; i < 100; i++ {
			rx = possiblex[random(0, length)]
			ry = possibley[random(0, height)]
			board = update_case(board, rx, ry, length, height)
		}

	}
}

func affiche(arr [][]int, boardh int, boardl int) {
	/*
		This function is for debug and show in console the maze
	*/
	for y := 0; y < boardh; y++ {
		for x := 0; x < boardl; x++ {
			if arr[y][x] == -1 {
				fmt.Print("■ ")
			} else {
				fmt.Print("  ")
			}
		}
		fmt.Print("\n")
	}
}

func save_board(arr [][]int, boardh int, boardl int) {
	/*
		This function will save the maze if a data file
		:param arr: the maze
		:param boardl: the length of the maze
		:param boardh: the height of the maze
		:return Nothing
	*/
	f, err := os.Create("data")

	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()

	for y := 0; y < boardh; y++ {
		for x := 0; x < boardl-1; x++ {
			if arr[y][x] == -1 {
				f.WriteString("0 ")
			} else {
				f.WriteString("1 ")
			}
		}
		f.WriteString("0")
		f.WriteString("\n")

	}
}

func update_case(arr [][]int, cx, cy, length, height int) [][]int {
	/*
		The generator of maze // the code is very dirty i made a better version in C available in this project, less dirty than this one
		:param arr: the maze
		:param cx, cy : coordinate in x and y where a wall will be destroyed
		:param length: the length of the maze
		:param height: the height of the maze
		:return a maze with one side destroyed

	*/

	hmax := int((height*2 + 1) - 2)

	lmax := int((length*2 + 1) - 2)

	r := random(0, 4)

	for {
		if cx > 2 && cx < lmax && cy > 2 && cy < hmax {
			r = random(0, 4)
			break
		}
		if cx < 2 {
			if cy < 2 {
				s := []int{2, 1}
				r = random_choice(s)
				break
			}
			if cy >= hmax {
				s := []int{2, 3}
				r = random_choice(s)
				break
			} else {
				s := []int{2, 1, 3}
				r = random_choice(s)
				break
			}

		}

		if cx >= lmax {
			if cy < 2 {
				s := []int{0, 1}
				r = random_choice(s)
				break
			}
			if cy >= hmax {
				s := []int{0, 3}
				r = random_choice(s)
				break
			} else {
				s := []int{1, 0, 3}
				r = random_choice(s)
				break
			}
		}
		if cy < 2 {
			if cx < 2 {
				s := []int{1, 2}
				r = random_choice(s)
				break
			}
			if cx >= lmax {
				s := []int{1, 0}
				r = random_choice(s)
				break
			} else {
				s := []int{1, 0, 2}
				r = random_choice(s)
				break
			}
		}
		if cy >= hmax {
			if cx < 2 {
				s := []int{3, 2}
				r = random_choice(s)
				break
			}
			if cx >= lmax {
				s := []int{3, 0}
				r = random_choice(s)
				break
			} else {
				s := []int{3, 0, 2}
				r = random_choice(s)
				break
			}
		}

		r = -1
		break

	}

	if r == 0 {
		if arr[cy][cx-2] != arr[cy][cx] {

			if random(0, 2) == 1 {
				arr[cy][cx-1] = arr[cy][cx]
				arr = replace(arr, arr[cy][cx-2], arr[cy][cx], length, height)

			} else {
				arr[cy][cx-1] = arr[cy][cx-2]
				arr = replace(arr, arr[cy][cx], arr[cy][cx-2], length, height)
			}

		}
	}

	if r == 1 {
		if arr[cy+2][cx] != arr[cy][cx] {

			if random(0, 2) == 1 {
				arr[cy+1][cx] = arr[cy][cx]
				arr = replace(arr, arr[cy+2][cx], arr[cy][cx], length, height)

			} else {
				arr[cy+1][cx] = arr[cy+2][cx]
				arr = replace(arr, arr[cy][cx], arr[cy+2][cx], length, height)
			}
		}
	}

	if r == 2 {
		if arr[cy][cx+2] != arr[cy][cx] {

			if random(0, 2) == 1 {
				arr[cy][cx+1] = arr[cy][cx]
				arr = replace(arr, arr[cy][cx+2], arr[cy][cx], length, height)

			} else {
				arr[cy][cx+1] = arr[cy][cx+2]
				arr = replace(arr, arr[cy][cx], arr[cy][cx+2], length, height)
			}

		}

	}

	if r == 3 {
		if arr[cy-2][cx] != arr[cy][cx] {

			if random(0, 2) == 1 {
				arr[cy-1][cx] = arr[cy][cx]
				arr = replace(arr, arr[cy-2][cx], arr[cy][cx], length, height)
			} else {
				arr[cy-1][cx] = arr[cy-2][cx]

				arr = replace(arr, arr[cy][cx], arr[cy-2][cx], length, height)
			}
		}
	}

	return arr
}

func set_numbers(arr [][]int, possiblex, possibley []int, length, hauteur int) [][]int {
	/*
		This function will place a different value in each case of the maze
		:param arr : the maze
		:param possiblex ; possibley: random array that will tell wich coordinate put a random value in the array
		:param length: the length of the maze
		:param height: the height of the maze
		:return the maze with random value inside

	*/
	n := 0

	for y := 0; y < hauteur; y++ {
		for x := 0; x < length; x++ {
			n++
			arr[possibley[y]][possiblex[x]] = n
		}
	}

	return arr
}

func replace(arr [][]int, what, bywhat, length, height int) [][]int {
	/*
		This function will relaplce every in what by int of bywhat in the maze
		:param what: the int to replace
		:param bywhat: whith what replace what
		:return the maze with what replace by bywhat
	*/
	for y := 0; y < height; y++ {
		for x := 0; x < length; x++ {
			if arr[y*2+1][x*2+1] == what {
				arr[y*2+1][x*2+1] = bywhat
			}
		}
	}

	return arr
}

func is_finished(arr [][]int, length, height int) bool {
	/*
		This function will return True if the maze is finished (if the maze if resolvable)
		A maze if fully ended when there is only one value inside
		so we juste need to check if there is any différent value in the maze
		:param arr: the maze
		:param length: the length of the maze
		:param height: the height of the maze
		:return True if the maze is finished esle False
	*/

	// create a list that willl containe all value of the maze
	total_list := make([]int, length*height)

	for y := 0; y < height; y++ {
		for x := 0; x < length; x++ {
			total_list[int(x+(y*length))] = arr[y*2+1][x*2+1]

		}
	}

	// check if there is any different value
	for i := 0; i < len(total_list); i++ {
		if total_list[0] != total_list[i] {
			// if there is any different value return False
			return false
		}
	}
	// else return True
	return true
}

// other functions

func make_range_two(min, max int) []int {
	/*
		Create and return a alist of element separated by two
		example : make_range_two(1, 7) = [1, 3, 5]
		:param min: the minimum range for the list
		:param max: the maximum range for the list
	*/
	// create a range
	a := make([]int, int(max/2)-min+1)
	for i := range a {
		a[i] = min + i*2
	}
	return a
}

func removes(lst []int, del int) []int {
	/*
		This function will return a list without a specified element
		:param lst: a list of int
		:param del: the lement to delete in lst
		:return lst without del inside of it
	*/
	var new_array []int

	for i := 0; i < len(lst); i++ {
		if lst[i] != del {
			new_array = append(new_array, lst[i])
		}
	}

	return new_array
}

func randomize_list(lenght int, pos []int) []int {
	/*
		This function will take a list and mix them
		:param lenght: the length of the list
		:param pos: the list to mix
		:return a mixed arrray of int
	*/

	r := 0
	c := 0

	var return_pos []int

	for i := 0; i < lenght; i++ {
		r = random(0, lenght-i)
		c = pos[r]
		pos = removes(pos, c)
		return_pos = append(return_pos, c)
	}
	return return_pos
}

func random(min int, max int) int {
	/*
		This function will return a random number between min and max (max exclude)
		:param min: the minimum range for the random
		:param max: the maximum range for the random // exclude
		:return int: random number (min, max)
	*/

	return rand.Intn(max-min) + min
}

func random_choice(seq []int) int {
	/*
		This function will return a random element from a array
		:param seq: a list of int (no specified size)
		:return a random int in a list
	*/
	return seq[random(0, len(seq))]
}
