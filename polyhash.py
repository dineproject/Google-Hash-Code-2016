from os import path, makedirs
from sys import setrecursionlimit
from math import ceil, sqrt
from classes import Simulation
from polyparser import parse_challenge
from polysolver import solve
import argparse

setrecursionlimit(10000)

def main():
    parser = argparse.ArgumentParser(description='Solve Polyhash 2016 challenge')
    parser.add_argument('file_path', type=str, help='Path to the input file')

    args = parser.parse_args()
    file_path = args.file_path

    var_optimize = 1

    file_path_optimize = file_path.split('/')[-1]
    
    if file_path_optimize == "a_example.in":
        var_optimize = 0.1
    elif file_path_optimize == "b_busy_day.in":
        var_optimize = 0.4627
    elif file_path_optimize == "c_redudancy.in":
        var_optimize = 0.0889
    elif file_path_optimize == "d_mother_of_all_warehouses.in":
        var_optimize = 0.2147   


    challenge = parse_challenge(file_path)
    solve(challenge, var_optimize)

if __name__ == "__main__":
    main()
