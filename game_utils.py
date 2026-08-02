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
END  = [0  ,  0]

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
        if None in (title, manufacturer): raise ValueError("no nulls allowed")
        self.title = title
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
            print(f'{self.title} ({self.manufacturer})')
            print(f'Input Buffer: {self.input_buffer}')
            print(f'Output Buffer: {self.output_buffer}')
            print(f"----------------------------\n")

class Evaluator(Machine):
    def __init__(self, title, manufacturer, loud_debug=False):
        super().__init__(title, manufacturer, loud_debug)

class Evaluator_1(Evaluator):
    def __init__(self, title, manufacturer, loud_debug=False):
        super().__init__(title, manufacturer, loud_debug)
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


class Simple_Adder(Machine):
    def __init__(self, operand, title, manufacturer, loud_debug=False):
        super().__init__(title, manufacturer, loud_debug)
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
        if new_operand not in range(1,999) or isinstance(new_operand, bool): raise ValueError("Improper operand")
        self.operand = new_operand


class Input_Stream(Machine):
    def __init__(self, input_data, title, manufacturer, loud_debug=False):
        super().__init__(title, manufacturer, loud_debug)
        if not input_data or not isinstance(input_data, list): raise ValueError("input failure")
        self.input_buffer["main"] = input_data
        self.output_buffer["main"] = []
        self.num_inputs  = 1
        self.num_outputs = 1
        
    def print_logic(self):
        return ""

    def run(self):
        self.print_debug()
        if not self.input_buffer["main"] or self.input_buffer["main"] == []:
            raise ValueError("Cannot run input stream with empty input buffer")
        self.output_buffer["main"] = self.input_buffer["main"]


class Map:
    def __init__(self, GRID_SIZE_LOCAL, loud_debug=False):
        self.grid = [[copy.deepcopy(CELL_TEMPLATE) for _ in range(GRID_SIZE_LOCAL["cols"])] for _ in range(GRID_SIZE_LOCAL["rows"])]
        self.loud_debug = loud_debug

    def install_machine(self, obj, install_location, output_directions):
        row, col = install_location
        if not (0 <= row < len(self.grid)) or not (0 <= col < len(self.grid[0])): raise ValueError("install_location out of bounds")
        if self.grid[row][col]["status"] != "empty": raise ValueError("install location already occupied")
        if output_directions is not None and not isinstance(output_directions, list):
            raise ValueError('Directions not entered as list')
        self.grid[row][col]["obj"] = obj
        self.grid[row][col]["status"] = "occupied"
        self.grid[row][col]["output_directions"] = []
        if output_directions is not None:
            for x in output_directions:
                self.grid[row][col]["output_directions"].append(x)

    def new_print_grid(self):
        print('\n\n')

        for row_idx, row in enumerate(self.grid):
            formatted_row = []
            for cell in row:
                display = "|------------------"
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if UP in cell["output_directions"]:
                    display = "|        ^         "
                else:
                    display = "|                  "
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if cell['status'] == 'empty':
                    display = '|                  '
                else:
                    display = '|' + cell["obj"].title.center(18)
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if cell['status'] == 'empty':
                    display = '|                  '
                else:
                    display = '| ' + cell["obj"].print_logic().center(16) + ' '
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if cell['status'] == 'empty':
                    display = '|                  '
                elif RIGHT in cell['output_directions']:
                    display = '|                 ' + '>'
                elif LEFT in cell['output_directions']:
                    display = '|<                 '
                else:
                    display = '|                  '
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if cell['status'] == 'empty':
                    display = '|                  '
                else:
                    display = '|   INPUT (MAIN):  '
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if cell['status'] == 'empty':
                    display = '|                  '
                elif cell['status'] == 'occupied':
                    list_just_numbers = ",".join(str(x) for x in cell["obj"].input_buffer["main"])
                    display = '|' + list_just_numbers.center(18)
                else:
                    display = '|               '
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if cell['status'] == 'empty':
                    display = '|                  '
                else:
                    display = '|  OUTPUT  (MAIN): '
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if cell['status'] == 'empty':
                    display = '|                  '
                elif cell['status'] == 'occupied':
                    list_just_numbers = ",".join(str(x) for x in cell["obj"].output_buffer["main"])
                    display = '|' + list_just_numbers.center(18)
                else:
                    display = '|                  '
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

            for cell in row:
                if DOWN in cell["output_directions"]:
                    display = "|        \/        "
                else:
                    display = "|                  "
                formatted_row.append(f"{display}")
            print("".join(formatted_row) + '|')
            formatted_row = []

        print('\n\n')

    def search_grid(self, function=None):
        collection = []
        if function:
            for index_row, row in enumerate(self.grid):
                for index_col, col in enumerate(row):
                    if function(self.grid[index_row][index_col]["obj"]) == True:
                        temp = [index_row, index_col]
                        collection.append(temp)
                        #print(f'row {index_row}, col {index_col}')
        return collection

    def run_simple_route(self):
        # find input stream and output directions
        coordinates_input_stream = self.search_grid(is_input_stream)
        if len(coordinates_input_stream) != 1: raise ValueError("improper number of input streams")
        row_input_stream, col_input_stream = coordinates_input_stream[0]
        obj_input_stream = self.grid[row_input_stream][col_input_stream]['obj']

        # find input stream's output
        direction_output = self.grid[row_input_stream][col_input_stream]['output_directions']
        if len(direction_output) != 1: raise ValueError("only one output allowed")
        row_output = row_input_stream + direction_output[0][0]
        col_output = col_input_stream + direction_output[0][1]
        obj_output = self.grid[row_output][col_output]['obj']
        
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
            else:
                direction_output = self.grid[row_current][col_current]['output_directions']
                if len(direction_output) != 1: raise ValueError("only one output allowed")
                row_output = row_current + direction_output[0][0]
                col_output = col_current + direction_output[0][1]
                obj_next = self.grid[row_output][col_output]['obj']




#-----------HELPER FUNCTIONS-------------------------

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


def connect_and_run(machine1, machine2)->bool:
    '''
    Calls run() member method on machine 1, copies relevant output(s)
    from machine 1 and passes it to machine 2's input(s) via the 
    ingest() member method.

    PARAMETERS: machine1 and machine2, which must be subclasses
    of Machine.

    RETURNS: True upon success, False upon failure
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
    success = True

    try:
        machine1.run()
        temp = machine1.get_output('main')
        if not temp: 
            raise ValueError("machine1 output is null")
        machine2.ingest_data(data=temp, channel='main', method='replace')
    except:
        print(f'Unspecified error: {Exception}')
        success = False

    return success