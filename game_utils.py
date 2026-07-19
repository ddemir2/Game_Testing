import pandas as pd
import numpy as np
import time as t
import inspect
import random
import copy

RIGHT = [0  ,  1]
LEFT  = [0  , -1]
UP    = [-1 ,  0]
DOWN  = [1  ,  0]
NONE  = [0  ,  0]

ZERO = 0
GRID_SIZE = {"rows" : 4, "cols" : 4}
GRID_SIZE["MAX_ROW_INDEX"] = (GRID_SIZE["rows"]-1) 
GRID_SIZE["MAX_COLUMN_INDEX"] = (GRID_SIZE["cols"]-1)

CELL_TEMPLATE = {
    "status" : "empty",
    "obj"    : None,
    "output_directions" : [],

    } 



class Machine:
    def __init__(self, title, manufacturer, loud_debug=False):
        assert None not in (title, manufacturer), "no nulls allowed"
        self.title = title
        self.manufacturer = manufacturer
        self.input_buffer = []
        self.output_buffer = {"main" : []}
        self.loud_debug = loud_debug

    def ingest_data(self, data, method='replace'):
        if not isinstance(data, list): raise ValueError("Ingest type is not list!")
        if method == 'replace':
            self.input_buffer = list(data)
        self.print_debug()

    def run(self):
        print("parent class run!!")
    
    def report_materials(self):
        print("parent class report_materials!!")

    def print_debug(self, status = None):
        if status is None:
            status = self.loud_debug
        if status == True:
            print(f"\n[MACHINE DEBUG]  Curr Line: {inspect.currentframe().f_lineno}, Calling Line : {inspect.currentframe().f_back.f_lineno}, Calling Function: {inspect.currentframe().f_back.f_code.co_name}()")
            print(f'{self.title} ({self.manufacturer})')
            print(f'Input Buffer: {self.input_buffer}')
            print(f'Output Buffer: {self.output_buffer}')
            print(f"----------------------------\n")


class Evaluator_1(Machine):
    def __init__(self, title, manufacturer, loud_debug=False):
        super().__init__(title, manufacturer, loud_debug)

    def run(self):
        self.print_debug()
        if len(self.input_buffer) == 0 or self.input_buffer is None: raise ValueError("Cannot evaluate empty input buffer")
        if all(x > 10 for x in self.input_buffer):
            return True
        else:
            return False




class Simple_Adder(Machine):
    def __init__(self, operand, title, manufacturer, loud_debug=False):
        super().__init__(title, manufacturer, loud_debug)
        self.operand = operand

    def run(self):
        temp = np.array(self.input_buffer)
        result = np.add(temp, self.operand)
        self.output_buffer["main"] = result.tolist()
        return self.output_buffer["main"]
    
    def update_operand(self, new_operand):
        if new_operand not in range(1,999): raise ValueError("Improper operand")
        self.operand = new_operand

class Input_Stream(Machine):
    def __init__(self, input_data, title, manufacturer, loud_debug=False):
        super().__init__(title, manufacturer, loud_debug)
        assert input_data and isinstance(input_data, list), "input failure"
        self.output_buffer = {"main": input_data}
    
    def run(self):
        self.print_debug()
        return self.output_buffer["main"]



class Map:
    def __init__(self, GRID_SIZE_LOCAL):
        self.grid = [[copy.deepcopy(CELL_TEMPLATE) for _ in range(GRID_SIZE_LOCAL["cols"])] for _ in range(GRID_SIZE_LOCAL["rows"])]
    
    def install_machine(self, obj, install_location, output_directions):
        row, col = install_location
        assert 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]), "install_location out of bounds"
        assert self.grid[row][col]["status"] == "empty", "install location already occupied"
        if output_directions is not None and not isinstance(output_directions, list):
            raise ValueError('Directions not entered as list')
        self.grid[row][col]["obj"] = obj
        self.grid[row][col]["status"] = "occupied"
        self.grid[row][col]["output_directions"] = []
        if output_directions is not None:
            for x in output_directions:
                self.grid[row][col]["output_directions"].append(x)

    def print_grid(self):
        if not self.grid:
            print("Grid is empty.")
            return

        col_count = len(self.grid[0])
        cell_width = 5

        print("   " + " ".join(f"{col:^{cell_width}}" for col in range(col_count)))
        print("   " + "-" * (col_count * (cell_width + 1) + 2))

        for row_idx, row in enumerate(self.grid):
            formatted_row = []
            for cell in row:
                if cell is None:
                    display = "."
                elif hasattr(cell, "title"):
                    display = cell.title
                else:
                    display = str(cell)
                formatted_row.append(f"{display:^{cell_width}}")

            print(f"{row_idx:>2} |" + "|".join(formatted_row))