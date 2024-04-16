import pygame
import numpy as np
import sys

# Needs a '\n' character at the end of a line currently. 
def sdm_unpack(n):
    x = np.zeros((9,9), dtype=np.int8)
    i = 0
    while (n[i] != '\n' and i < len(n)):
        if (n[i] != '.'):
            x[i//9][i%9] = int(n[i])
        i += 1

    return x

# Input: 9x9 sudoku grid, output: 10x9x9 array with candidates in respective grids 1-9 
def candidates(sudoku):
    candidates = np.zeros((9,9,9), dtype=np.int8)
    for g in range(candidates.shape[2]):
        candidates[g, :, :] = g+1
        for r in range(candidates.shape[0]):
            for c in range(candidates.shape[1]):
                if (sudoku[r, c] > 0):
                    candidates[g, r, c] = 0 # taken space elim
                if (sudoku[r, c] == (g+1)):
                    candidates[g, r, :] = 0 # row elim
                    candidates[g, :, c] = 0 # col elim

                    b = ((r//3)*3) + c//3 # block elim
                    ri = (b // 3) * 3
                    ci = (b % 3) * 3
                    candidates[g, ri:(ri+3), ci:(ci+3)] = 0
    #return np.append([sudoku], candidates, axis = 0)                
    return candidates              
        
def by_sudoku(sudoku, candidates):
    for g in range(candidates.shape[2]):
        indices = np.where(candidates[g] == g+1)
        r_arr, c_arr = np.zeros([9], dtype=np.int8), np.zeros([9], dtype=np.int8)
        for row, col in zip(*indices):
            r_arr[row] += 1
            c_arr[col] += 1
        
        print(f"Row appearances: {r_arr}, \ncol: {c_arr}")
        
        unique_r = np.where(r_arr == 1)[0]
        unique_c = np.where(c_arr == 1)[0]
        if (unique_r.size > 0):
            for i in range(unique_r.size):
                index = np.where(indices[0] == unique_r[i])
                sudoku[indices[0][index[0][0]]][indices[1][index[0][0]]] = g+1
        if (unique_c.size > 0):
            for i in range(unique_c.size):
                index = np.where(indices[1] == unique_c[i])
                sudoku[indices[0][index[0][0]]][indices[1][index[0][0]]] = g+1

    return sudoku

        
                



def main():
    # Import game
    if (sys.argv[1] == '-r'):
        if (sys.argv[2] is not None): #error with OOB no sys.argv[2]
            for i in range(3):
                print(sys.argv[i])     

            f = open(sys.argv[2], "r")
            sdm_line = f.readline()
            print(sdm_line)
            f.close()
                
        else:
            print("Please input a file after the '-r' flag.")
    else:
        print("Please input a sudoku with the .sdm file extension with '-r' flag followed by the filename.")
        exit(0)

    sudoku = sdm_unpack(sdm_line) #returns 9x9 2D array

    print(sudoku)
    while (np.any(sudoku==0)):
        c_grid = candidates(sudoku)
        sudoku = by_sudoku(sudoku, c_grid)
    print(sudoku)

if __name__ == "__main__":
    main()
                

        



# Pencil Marks
