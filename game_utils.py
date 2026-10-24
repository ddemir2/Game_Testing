#import pandas as pd
import numpy as np
#import time as t
import inspect
import copy
import logging
from collections import deque

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
INPUT_NUM_MIN = 1
INPUT_NUM_MAX = 3
CLASSIC_TESTING_GAME_BOARD_SIZE = 4


CELL_TEMPLATE = {
    "status" : "empty",
    "obj"    : None,
    "output_directions" : [],
    } 

VALID_STATUSES = [
    'empty',
    'occupied',
]

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
    def __init__(self, title_private, config, title_public='!(deflt parent)!', loud_debug=False):
        if None in (title_private, config): raise ValueError("no nulls allowed")
        self.title_private = title_private
        self.title_public = title_public
        self.config = config
        self.input_buffer = []
        self.output_channels = {"main" : [], "aux_1" : [], "aux_2" : []}
        self.loud_debug = loud_debug

    def get_output(self, channel) -> list:
            if not self.output_channels[channel] or len(self.output_channels[channel]) == 0:
                raise ValueError("cannot output an empty list")
            return self.output_channels[channel]

    def ingest_data(self, data: list, method: str ='append'):
        if not isinstance(data, list): raise ValueError("Ingest type is not list!")
        if method == 'append':
            self.input_buffer.extend(data)
        elif method == 'replace':
            self.input_buffer = data
        else: 
            raise ValueError(f"uncrecognized ingest method: {method}")

    def run(self):
        if not self.input_buffer or self.input_buffer == []: raise ValueError("cannot run with empty input")
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
            print(f'{self.title_private} ({self.config})')
            print(f'Input Buffer: {self.input_buffer}')
            print(f'Output Channels: {self.output_channels}')
            print(f"----------------------------\n")

    def modify_object(self, num):
        raise TypeError(f"this method must be run by subclass of Machine ({num})")

    def ready_to_run(self):
        if self.input_buffer and self.input_buffer != []:
            return True
        else:
            return False

class Evaluator(Machine):
    def __init__(self, title_private, config, title_public='!(deflt eval)!', loud_debug=False):
        super().__init__(title_private, config, title_public, loud_debug)
    
    def check_success(self):
        temp_list    = self.get_output('main')
        if len(temp_list) != 1: raise ValueError("output of evaluator must have one element")
        temp_num     = temp_list[0]
        if isinstance(temp_num, int) and temp_num in (0,1):
            return temp_num
        else:
            raise ValueError(f"output of Evaluator object is invalid: {str(temp_num)}")

    def run(self):
        if not self.input_buffer or self.input_buffer == [] : raise ValueError("cannot run with empty input")

        if all(value in self.input_buffer for value in self.config['truth_statement']):
            self.output_channels['main'] = [1]
        else:
            self.output_channels['main'] = [0]

    def print_logic(self):
        return self.config['logic_text']


class Input_Stream(Machine):
    def __init__(self, input_data, title_private, config, title_public='!(deflt istream)!', loud_debug=False):
        super().__init__(title_private, config, title_public, loud_debug)
        if not input_data or not isinstance(input_data, list): raise ValueError("input failure")
        self.input_buffer = input_data
        self.output_channels = {"main" : []}

    def print_logic(self):
        return print_list(self.input_buffer)
        
    def run(self):
        self.print_debug()
        if not self.input_buffer or self.input_buffer == []:
            raise ValueError("Cannot run input stream with empty input buffer")
        self.output_channels["main"] = self.input_buffer



class Pipe(Machine):
    def __init__(self, title_private, config, title_public='!(deflt istream)!', loud_debug=False):
        super().__init__(title_private, config, title_public, loud_debug)
        self.output_channels = {"main" : []}

    def print_logic(self):
        return ''

    def run(self):
        if not self.input_buffer or self.input_buffer == []:
            raise ValueError("Cannot run input stream with empty input buffer")
        self.output_channels["main"] = self.input_buffer        


class Naive_Splitter(Machine):
    def __init__(self, title_private, config, title_public='!(deflt splitter)!', loud_debug=False):
        super().__init__(title_private, config, title_public, loud_debug)
        self.output_channels = {"main" : [], "aux_1" : []}
    
    def run(self):
        temp = self.input_buffer
        length = len(temp)
        if length % 2 == 1:
            extra = temp[-1]
            temp = temp.copy()
            temp.append(extra)
            length += 1
        half_len = length // 2
        main_output = temp[:half_len]
        aux_output  = temp[half_len:]
        self.output_channels['main'] = main_output.copy()
        self.output_channels['aux_1']  = aux_output.copy()

    def print_logic(self):
        return f"splits list into 2"
    
    def update_mode(self):
        raise ValueError("only default mode supported")


class Map:
    def __init__(self, rows, cols, loud_debug=False):
        if type(rows) is not int or type(cols) is not int:
            raise TypeError("rows and cols must be integers")
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")
        self.rows = rows
        self.cols = cols
        self.grid = [[copy.deepcopy(CELL_TEMPLATE) for _ in range(cols)] for _ in range(rows)]
        self.loud_debug = loud_debug

    def install_machine(self, obj, install_location, output_directions):
        row, col = install_location
        if not self.is_in_bounds(row, col):
            raise IndexError("install_location out of bounds")
        if not self.is_empty(row, col):
            raise PermissionError("install location already occupied")
        if output_directions is None or not isinstance(output_directions, list) or not all([type(x) == list for x in output_directions]):
            raise TypeError('Directions not entered as list')

        cell = self.get_cell(row, col)
        cell["obj"] = obj
        cell["status"] = "occupied"
        cell["output_directions"] = []
        if output_directions is not None:
            for direction in output_directions:
                cell["output_directions"].append(direction)

    def is_in_bounds(self, row, col):
        row_in_bounds = (0 <= row < self.rows)
        col_in_bounds = (0 <= col < self.cols)
        return row_in_bounds and col_in_bounds

    def get_cell(self, row, col):
        if not self.is_in_bounds(row, col):
            raise KeyError(f"Row {row} Col {col} is out of bounds!")
        return self.grid[row][col]

    def is_empty(self, row, col):
        cell_status = self.get_cell(row, col)['status']
        obj = self.get_cell(row, col)['obj']
        if cell_status == 'empty' and obj:
            raise LookupError(f"row {row}, col {col}: cell marked empty but object exists")
        elif cell_status == 'occupied' and not obj:
            raise LookupError(f"row {row}, col {col}: cell marked occupied but object doesn't exist")
        
        if cell_status == 'empty':
            return True
        else: 
            return False

    def get_obj_at_coordinates(self, row, col):
        cell   = self.get_cell(row, col)
        object = cell['obj']
        if object:
            return object
        else:
            return None

    def get_status_at_coordinates(self, row, col):
        cell   = self.get_cell(row, col)
        status = cell['status']
        if not status or status not in VALID_STATUSES: 
            raise KeyError(f"Status '{str(status)}' is invalid")
        else:
            return status
      
    def get_output_directions_at_coordinates(self, row, col):
        return self.get_cell(row, col)['output_directions']

    def get_output_directions(self, row, col):
        return self.get_output_directions_at_coordinates(row, col)

    def iter_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                yield row, col, self.grid[row][col]

    def search_grid(self, function=None):
        collection = []
        if function:
            for row, col, cell in self.iter_cells():
                if function(cell["obj"]) == True:
                    collection.append([row, col])
        return collection
    
    def clear_cell(self, row, col):
        # set cell attributes to zero equivalents
        cell = self.get_cell(row, col)
        cell['status']            = 'empty'
        cell['obj']               = None
        cell['output_directions'] = []

    def connect_and_run_at_coordinates(self, start_coord, start_channel, dest_coord):
        if type(start_coord) != list or type(dest_coord) != list or not start_coord or not dest_coord:
            raise KeyError("invalid coordinates")
        if not all(type(x) == int for x in start_coord + dest_coord):
            raise TypeError(f"coordinates must all be integers: {start_coord} {dest_coord}")
        if len(start_coord) != 2 or len(dest_coord) != 2:
            raise KeyError("coordinates must be row, col pairs")
        if not all([self.get_obj_at_coordinates(start_coord[0], start_coord[1]), self.get_obj_at_coordinates(dest_coord[0], dest_coord[1])]):
            raise LookupError("coordinate(s) contain(s) no object(s)")

        row_start = start_coord[0]; col_start = start_coord[1]; row_dest  = dest_coord[0];  col_dest  = dest_coord[1]
        machine_start = self.get_obj_at_coordinates(row_start, col_start)
        machine_dest  = self.get_obj_at_coordinates(row_dest,  col_dest)
        connect_and_run(machine_start, start_channel, machine_dest)

    def run_complex_route(self, elements : list[list[int]]) -> None:
        if not elements or not isinstance(elements, list):
            raise TypeError(f"data structure is incorrect")
        if not all(isinstance(t, list) for t in elements):
            raise TypeError(f"individual elements are improper type: {elements}")

        output_channels = ['main', 'aux_1', 'aux_2']
        max_iterations = self.rows * self.cols * len(output_channels)
        frontier = deque(elements)
        visited = set()
        iterations = 0

        while frontier:
            iterations += 1
            if iterations > max_iterations:
                logging.error('endless loop detected')
                break

            processing_row, processing_col = frontier.popleft()
            if not self.is_in_bounds(processing_row, processing_col):
                continue
            if self.is_empty(processing_row, processing_col):
                continue

            key = (processing_row, processing_col)
            if key in visited:
                continue

            obj_current = self.get_obj_at_coordinates(processing_row, processing_col)

            if isinstance(obj_current, Evaluator):
                if obj_current.ready_to_run():
                    obj_current.run()
                    visited.add(key)
                continue

            if not obj_current.ready_to_run():
                continue

            obj_current.run()
            visited.add(key)

            output_directions = self.get_output_directions(processing_row, processing_col)
            for direction_index, direction in enumerate(output_directions):
                if direction == END:
                    continue

                row_neighbor = processing_row + direction[0]
                col_neighbor = processing_col + direction[1]

                if not self.is_in_bounds(row_neighbor, col_neighbor):
                    continue
                if self.is_empty(row_neighbor, col_neighbor):
                    continue

                obj_neighbor = self.get_obj_at_coordinates(row_neighbor, col_neighbor)
                output_channel = output_channels[direction_index]

                try:
                    data = obj_current.get_output(output_channel)
                    obj_neighbor.ingest_data(data=data, method='append')
                    frontier.append([row_neighbor, col_neighbor])
                except ValueError:
                    pass
            

def is_evaluator(obj) -> bool:
    if isinstance(obj, Evaluator):
        return True
    else:
        return False

def is_input_stream(obj) -> bool:
    if isinstance(obj, Input_Stream):
        return True
    else:
        return False

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


def connect_and_run(source : Machine, source_channel : str, destination : Machine) -> None:
    '''
    Calls run() member method on source machine, copies relevant output(s)
    from source and passes it to machine 2's input buffer via the 
    ingest() member method.

    PARAMETERS: source and destination, which must be subclasses
    of Machine.
    '''
    if not all([source, destination]) or not source_channel:
        raise ValueError("source, channel, and/or destination is invalid")
    if type(source) == Machine or type(destination) == Machine:
        raise TypeError("source and destination must be subclasses of Machine")
    if source_channel not in source.output_channels:
        raise KeyError(f"source_channel [{str(source_channel)}] doesn't exist for source object")

    source.run()
    data = source.get_output(source_channel)
    destination.ingest_data(data = data, method = 'append')
    
    '''
    temp = None
    try:
        machine1.run()
        temp = machine1.get_output(output_channel)
        if not temp: 
            raise ValueError("machine1 output is null")
        machine2.ingest_data(data=temp, channel=input_channel, method='append')
    except TypeError as Te:
        logging.error(f'Typerror: {Te}')
        raise
    except ValueError as Ve:
        logging.error(f'Value Error: {Ve}')
        raise
    except Exception as e:
        logging.error(f'Unspecified Error: {e}')
        raise
    '''


    

"""        

### MAP CLASS

    def run_complex_route(self, elements : list[list[int]]) -> None:
        if not elements or not isinstance(elements, list): raise TypeError(f"data structure is incorrect")
        if not all(isinstance(t, list) for t in elements) : raise TypeError(f"individual elements are improper type: {elements}")

        output_channels = ['main', 'aux', 'aux2']
        max_iterations = self.rows * self.cols * len(output_channels)
        frontier = deque(elements)
        visited = set()
        iterations = 0

        while frontier:
            iterations += 1
            if iterations > max_iterations:
                logging.error('endless loop detected')
                break

            processing_row, processing_col = frontier.popleft()
            if not self.is_in_bounds(processing_row, processing_col):
                continue
            if self.is_empty(processing_row, processing_col):
                continue

            key = (processing_row, processing_col)
            if key in visited:
                continue

            obj_current = self.get_obj_at_coordinates(processing_row, processing_col)

            if isinstance(obj_current, Evaluator):
                if obj_current.ready_input_count():
                    obj_current.run()
                    visited.add(key)
                continue

            if not obj_current.ready_input_count():
                continue

            obj_current.run()
            visited.add(key)

            output_directions = self.get_output_directions(processing_row, processing_col)
            for index, direction in enumerate(output_directions):
                row_neighbor, col_neighbor, obj_neighbor = self.get_outputs(processing_row, processing_col, [direction])
                if obj_neighbor is None:
                    raise ValueError("Cannot output to empty cell")

                output_channel = output_channels[index]
                data = obj_current.get_output(output_channel)
                input_channel = self.get_preferred_input_channel(row_neighbor, col_neighbor)
                obj_neighbor.ingest_data(data=data, channel=input_channel, method='append')

                frontier.append([row_neighbor, col_neighbor])
  
    def replace_machine_at_coordinates(self, obj, replace_location, output_directions):
            row, col = replace_location
            if self.get_status_at_coordinates(row, col) == 'empty':
                raise KeyError(f"status not empty: {self.get_status_at_coordinates(row,col)}")
            cell = self.get_cell(row, col)

    def set_cell(self, row, col, data):
        if not self.is_in_bounds(row, col):
            raise ValueError(f"Row {row} Col {col} is out of bounds!")
        self.grid[row][col] = data


    
    

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

    def get_all_output_cells(self, row, col):
        output_directions = self.get_output_directions(row, col)
        return [self.get_outputs(row, col, [direction]) for direction in output_directions]




        


    def run_simple_route(self):
        # find the input stream
        row_input_stream, col_input_stream, obj_input_stream = self.get_starting_machine()
        
        # find input stream's output
        direction_output = self.get_output_directions(row_input_stream, col_input_stream)
        row_output, col_output, obj_output = self.get_outputs(row_input_stream, col_input_stream, direction_output)
        if obj_output is None:
            raise ValueError("Cannot output to empty cell")
        
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
        list_of_evaluators = self.search_grid(is_evaluator)
        if not list_of_evaluators or list_of_evaluators == []: raise ValueError("no evaluators found")
        list_of_evaluator_results = [self.get_obj_at_coordinates(row, col).check_success() for row, col in list_of_evaluators]
        if all(list_of_evaluator_results):
            return True
        else:
            return False

#-----------HELPER FUNCTIONS-------------------------





def uninitialized_i_o(obj) -> bool:
    if not obj:
        return False
    elif not obj.num_inputs or not obj.num_outputs:
        return True
    else:
        return False





        """