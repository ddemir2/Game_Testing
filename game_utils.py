import pandas as pd
import numpy as np
import time as t
import inspect
import random
import copy
import logging

logging.basicConfig(
    level=logging.DEBUG, # Capture all levels from DEBUG up to CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s', # Output layout
)

RIGHT = [0  ,  1]
LEFT  = [0  , -1]
UP    = [-1 ,  0]
DOWN  = [1  ,  0]
END  = [0  ,  0]
UP_LEFT    = [-1 , -1]
UP_RIGHT   = [-1 ,  1]
DOWN_LEFT  = [1  , -1]
DOWN_RIGHT = [1  ,  1]

ZERO = 0
MIN_ADDER_OPERAND = 0
MAX_ADDER_OPERAND = 999

GRID_SIZE = {"rows" : 4, "cols" : 4}
GRID_SIZE["MAX_ROW_INDEX"] = (GRID_SIZE["rows"]-1) 
GRID_SIZE["MAX_COLUMN_INDEX"] = (GRID_SIZE["cols"]-1)

CELL_TEMPLATE = {
    "status" : "empty",
    "obj"    : None,
    "output_directions" : [],
    "input_directions" : [],
    } 

DIRECTION_NAMES = {
    tuple(RIGHT) : "RIGHT",
    tuple(LEFT)  : "LEFT",
    tuple(UP)    : "UP",
    tuple(DOWN)  : "DOWN",
    tuple(END)   : "END",
    tuple(UP_LEFT)    : "UP_LEFT",
    tuple(UP_RIGHT)   : "UP_RIGHT",
    tuple(DOWN_LEFT)  : "DOWN_LEFT",
    tuple(DOWN_RIGHT) : "DOWN_RIGHT",
}

def direction_name(direction) -> str:
    return DIRECTION_NAMES.get(tuple(direction), str(direction))


class Machine:
    def __init__(self, title_private, manufacturer, title_public='!(deflt parent)!', loud_debug=False):
        if None in (title_private, manufacturer): raise ValueError("no nulls allowed")
        self.title_private = title_private
        self.title_public = title_public
        self.manufacturer = manufacturer
        self.input_buffer = {"main" : [], "aux" : []}
        self.output_buffer = {"main" : [], "aux" : []}
        self.loud_debug = loud_debug
        self.num_inputs  = None
        self.num_outputs = None

    def get_output(self, channel) -> list:
        if not self.output_buffer[channel] or len(self.output_buffer[channel]) == 0:
            raise ValueError("cannot output an empty list")
        return self.output_buffer[channel]

    def ingest_data(self, data, channel='main', method='replace'):
        if not isinstance(data, list): raise ValueError("Ingest type is not list!")
        if method != 'replace': raise ValueError("Only replace implemented")
        if method == 'replace':
            self.input_buffer[channel] = list(data)
        self.print_debug()

    def run(self):
        print("parent class run!!")
    
    def report_materials(self):
        print("parent class report_materials!!")
    
    def print_logic(self):
        return f"parent logic!"

    def print_debug(self, status = None):
        if status is None:
            status = self.loud_debug
        if status == True:
            print(f"\n[MACHINE DEBUG]  Curr Line: {inspect.currentframe().f_lineno}, Calling Line : {inspect.currentframe().f_back.f_lineno}, Calling Function: {inspect.currentframe().f_back.f_code.co_name}()")
            print(f'{self.title_private} ({self.manufacturer})')
            print(f'Input Buffer: {self.input_buffer}')
            print(f'Output Buffer: {self.output_buffer}')
            print(f"----------------------------\n")

    def modify_object(self, num):
        raise TypeError(f"this method must be run by subclass of Machine ({num})")

class Evaluator(Machine):
    def __init__(self, title_private, manufacturer, title_public='!(deflt eval)!', loud_debug=False):
        super().__init__(title_private, manufacturer, title_public, loud_debug)
    
    def check_success(self):
        temp_list    = self.get_output('main')
        if len(temp_list) != 1: raise ValueError("output of evaluator must have one element")
        temp_num     = temp_list[0]
        if isinstance(temp_num, int) and temp_num in (0,1):
            return temp_num
        else:
            raise ValueError(f"output of Evaluator object is invalid: {temp_num}")



class Evaluator_1(Evaluator):
    def __init__(self, title_private, manufacturer, title_public='!(deflt eval_1)!', loud_debug=False):
        super().__init__(title_private, manufacturer, title_public, loud_debug)
        self.num_inputs  = 1
        self.num_outputs = 1
    
    def print_logic(self):
        return "All #s > 10"

    def run(self):
        self.print_debug()
        if len(self.input_buffer["main"]) == 0 or self.input_buffer["main"] is None: raise ValueError("Cannot evaluate empty input buffer")
        if all(x > 10 for x in self.input_buffer["main"]):
            self.output_buffer["main"] = [1]
        else:
            self.output_buffer["main"] = [0]

class Concatenator(Machine):
    def __init__(self, mode, title_private, manufacturer, title_public='!(deflt concat)!', loud_debug=False):
        super().__init__(title_private, manufacturer, title_public, loud_debug)
        self.mode = mode
        self.num_inputs = 2
        self.num_outputs = 1
        if self.mode != "default": raise ValueError("concatenator only has default mode enabled")
    
    def run(self):
        if not self.input_buffer['main']: raise ValueError("main input can't be null")
        if not self.input_buffer['main']: raise ValueError("aux input can't be null")
        temp = self.input_buffer['main'] + self.input_buffer['aux']
        self.output_buffer['main'] = temp
    
    def print_logic(self):
        return f"combine 2 lists"
    
    def update_mode(self):
        raise ValueError("only default mode supported")

class Splitter(Machine):
    def __init__(self, mode, title_private, manufacturer, title_public='!(deflt splitter)!', loud_debug=False):
        super().__init__(title_private, manufacturer, title_public, loud_debug)
        self.mode = mode
        self.num_inputs = 1
        self.num_outputs = 2
        if self.mode != "default": raise ValueError("splitter only has default mode enabled")
    
    def run(self):
        temp = self.input_buffer["main"]
        length = len(temp)
        if length % 2 == 1:
            extra = temp[-1]
            temp = temp.copy()
            temp.append(extra)
            length += 1
        half_len = length // 2
        main_output = temp[:half_len]
        aux_output  = temp[half_len:]
        self.output_buffer['main'] = main_output.copy()
        self.output_buffer['aux']  = aux_output.copy()

    def print_logic(self):
        return f"splits list into 2"
    
    def update_mode(self):
        raise ValueError("only default mode supported")

class Simple_Adder(Machine):
    def __init__(self, operand, title_private, manufacturer, title_public='!(deflt adder)!', loud_debug=False):
        super().__init__(title_private, manufacturer, title_public, loud_debug)
        self.operand = operand
        self.num_inputs  = 1
        self.num_outputs = 1
        if not isinstance(self.operand, int): raise ValueError("adder operand must be integer")
    
    def print_logic(self):
        return f"+ ({self.operand})"

    def run(self):
        temp = np.array(self.input_buffer["main"])
        result = np.add(temp, self.operand)
        self.output_buffer["main"] = result.tolist()
    
    def update_operand(self, new_operand):
        if new_operand not in range(MIN_ADDER_OPERAND, MAX_ADDER_OPERAND) or isinstance(new_operand, bool): raise ValueError("Improper operand")
        self.operand = new_operand

    def modify_object(self, num):
        self.update_operand(num)

class Input_Stream(Machine):
    def __init__(self, input_data, title_private, manufacturer, title_public='!(deflt istream)!', loud_debug=False):
        super().__init__(title_private, manufacturer, title_public, loud_debug)
        if not input_data or not isinstance(input_data, list): raise ValueError("input failure")
        self.input_buffer["main"] = input_data
        self.output_buffer["main"] = []
        self.num_inputs  = 1
        self.num_outputs = 1
        
    def print_logic(self):
        return print_list(self.input_buffer["main"])

    def run(self):
        self.print_debug()
        if not self.input_buffer["main"] or self.input_buffer["main"] == []:
            raise ValueError("Cannot run input stream with empty input buffer")
        self.output_buffer["main"] = self.input_buffer["main"]


class Map:
    def __init__(self, rows, cols, loud_debug=False):
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise TypeError("rows and cols must be integers")
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")

        self.rows = rows
        self.cols = cols
        self.grid = [[copy.deepcopy(CELL_TEMPLATE) for _ in range(cols)] for _ in range(rows)]
        self.loud_debug = loud_debug

    def is_in_bounds(self, row, col):
        row_in_bounds = (0 <= row < self.rows)
        col_in_bounds = (0 <= col < self.cols)
        return row_in_bounds and col_in_bounds

    def is_evaluator(self, obj):
        if isinstance(obj, Evaluator):
            return True
        else:
            return False     

    def get_cell(self, row, col):
        if not self.is_in_bounds(row, col):
            raise ValueError(f"Row {row} Col {col} is out of bounds!")
        return self.grid[row][col]

    def get_obj_at_coordinates(self, row, col):
        cell   = self.get_cell(row, col)
        object = cell['obj']
        if object:
            return object
        else:
            return None

    def get_output_directions(self, row, col):
        if not self.is_in_bounds(row, col):
            raise ValueError(f"Row {row} Col {col} is out of bounds!")
        if self.is_empty(row, col):
            raise ValueError(f"Row {row} Col {col}: obj is null, so it can't have output directions")
        return self.get_cell(row, col)['output_directions']

    def set_cell(self, row, col, data):
        if not self.is_in_bounds(row, col):
            raise ValueError(f"Row {row} Col {col} is out of bounds!")
        self.grid[row][col] = data

    def iter_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                yield row, col, self.grid[row][col]
    
    def is_empty(self, row, col):
        cell_status = self.get_cell(row, col)['status']
        obj = self.get_cell(row, col)['obj']
        if cell_status == 'empty' and obj:
            raise ValueError(f"row {row}, col {col}: cell marked empty but object exists")
        elif cell_status == 'occupied' and not obj:
            raise ValueError(f"row {row}, col {col}: cell marked occupied but object doesn't exist")
        
        if cell_status == 'empty':
            return True
        else: 
            return False

    def get_starting_machine(self):
        coordinates_input_stream = self.search_grid(is_input_stream)
        if len(coordinates_input_stream) != 1: raise ValueError("improper number of input streams")
        row_input_stream, col_input_stream = coordinates_input_stream[0]
        obj_input_stream = self.get_cell(row_input_stream, col_input_stream)['obj']
        return row_input_stream, col_input_stream, obj_input_stream

    def get_outputs(self, row_start, col_start, output_direction):
        row_output = row_start + output_direction[0][0]
        col_output = col_start + output_direction[0][1]
        if not self.is_in_bounds(row_output, col_output):
            raise ValueError(f'Row {row_output} Col {col_output} is out of bounds')
        obj_output = self.grid[row_output][col_output]['obj']
        return row_output, col_output, obj_output

    def install_machine(self, obj, install_location, output_directions):
        row, col = install_location
        if not self.is_in_bounds(row, col):
            raise ValueError("install_location out of bounds")
        if not self.is_empty(row, col):
            raise ValueError("install location already occupied")
        if output_directions is not None and not isinstance(output_directions, list):
            raise ValueError('Directions not entered as list')

        cell = self.get_cell(row, col)
        cell["obj"] = obj
        cell["status"] = "occupied"
        cell["output_directions"] = []
        if output_directions is not None:
            for direction in output_directions:
                cell["output_directions"].append(direction)
                inverted_direction = invert_direction(direction)
                target_row, target_col, _ = self.get_outputs(row, col, [direction])
                target_cell = self.get_cell(target_row, target_col)
                target_cell["input_directions"].append(inverted_direction)

    def search_grid(self, function=None):
        collection = []
        if function:
            for row, col, cell in self.iter_cells():
                if function(cell["obj"]) == True:
                    collection.append([row, col])
        return collection

    def run_complex_route(self, tails : list[list[int]]) -> None:
        if not isinstance(tails, list) or not all(isinstance(t, list) for t in tails) : raise ValueError(f"tail parameter improper: {tails}")


    def run_simple_route(self):
        # find the input stream
        row_input_stream, col_input_stream, obj_input_stream = self.get_starting_machine()
        
        # find input stream's output
        direction_output = self.get_output_directions(row_input_stream, col_input_stream)
        row_output, col_output, obj_output = self.get_outputs(row_input_stream, col_input_stream, direction_output)
        
        # set up loop and run
        obj_current = obj_input_stream
        obj_next    = obj_output
        while obj_current and obj_next:
            connect_and_run(obj_current, obj_next)
            row_current     = row_output
            col_current     = col_output
            obj_current     = obj_next
            
            if isinstance(obj_current, Evaluator):
                obj_current.run()
                obj_current = None
                obj_next = None
            else:
                if self.is_empty(row_current, col_current):
                    raise ValueError("Cannot output from empty cell")
                direction_output = self.get_output_directions(row_current, col_current)
                if len(direction_output) != 1:
                    raise ValueError("only one output allowed")
                row_output, col_output, obj_next = self.get_outputs(row_current, col_current, direction_output)
                if self.is_empty(row_output, col_output):
                    raise ValueError("Cannot output to empty cell")

    def check_all_win_conditions(self):
        list_of_evaluators = self.search_grid(self.is_evaluator)
        if not list_of_evaluators or list_of_evaluators == []: raise ValueError("no evaluators found")
        list_of_evaluator_results = [self.get_obj_at_coordinates(row, col).check_success() for row, col in list_of_evaluators]
        if all(list_of_evaluator_results):
            return True
        else:
            return False

#-----------HELPER FUNCTIONS-------------------------

def invert_direction(direction : list[int]) -> list[int]:
    if any([x not in (-1,0,1) for x in direction]): raise ValueError(f"invalid input direction: {direction}")
    return [x*-1 for x in direction]

def print_list(input_list) -> str:
    if not input_list or len(input_list) == 0:
        return None
    elif not all(isinstance(x, int) or isinstance(x, str) for x in input_list):
        raise TypeError("List elements must be either string or int")
    else:
        length = len(input_list)
        last_element = length-1
        output = [f'{element}, ' for element in input_list[:last_element]]
        output.append(str(input_list[last_element]))
        return ''.join(output)

def is_evaluator(obj) -> bool:
    if isinstance(obj, Evaluator_1):
        return True
    else:
        return False
    
def is_input_stream(obj) -> bool:
    if isinstance(obj, Input_Stream):
        return True
    else:
        return False

def is_any_machine(obj) -> bool:
    if isinstance(obj, Machine):
        return True
    else:
        return False

def uninitialized_i_o(obj) -> bool:
    if not obj:
        return False
    elif not obj.num_inputs or not obj.num_outputs:
        return True
    else:
        return False

def complex_connect_and_run(machine1, machine2):
    pass


def connect_and_run(machine1, machine2) -> None:
    '''
    Calls run() member method on machine 1, copies relevant output(s)
    from machine 1 and passes it to machine 2's input(s) via the 
    ingest() member method.

    PARAMETERS: machine1 and machine2, which must be subclasses
    of Machine.
    '''

    if not isinstance(machine1, Machine) or type(machine1) == Machine: 
        raise ValueError("improper class")
    if not isinstance(machine2, Machine) or type(machine2) == Machine: 
        raise ValueError("improper class")
    if machine1.num_outputs != 1 or machine2.num_inputs != 1: 
        raise ValueError("Only 1 output to 1 input is supported at this time")
    if not machine1.input_buffer["main"] or machine1.input_buffer["main"] == []: 
        raise ValueError("Machine1 Input Buffer is empty or null")

    temp = None

    try:
        machine1.run()
        temp = machine1.get_output('main')
        if not temp: 
            raise ValueError("machine1 output is null")
        machine2.ingest_data(data=temp, channel='main', method='replace')
    except TypeError as Te:
        logging.error(f'Typerror: {Te}')
        raise
    except ValueError as Ve:
        logging.error(f'Value Error: {Ve}')
        raise
    except Exception as e:
        logging.error(f'Unspecified Error: {e}')
        raise
