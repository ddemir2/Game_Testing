

import unittest

import game_utils as gu
import game_ui as gui
from collections import deque

class General_Test(unittest.TestCase):
    def test_complex_route(self):
        in1     = gu.Input_Stream([1], "in1", "DD", "Input: 1")
        in2     = gu.Input_Stream([2], "in2", "DD", "Input: 2")
        concat1 = gu.Concatenator('default', "concat1", "DD", "combine")
        add1    = gu.Simple_Adder(-5, "sub 5", "DD", "subtract 5")
        splt1   = gu.Splitter('default', "splt1", "DD", "split")
        add2    = gu.Simple_Adder(20, "add 20", "DD", "add 20")
        add3    = gu.Simple_Adder(25, "add 25", "DD", "add 25")
        eval1   = gu.Evaluator_1("eval1", "DD", "all > 10 ?")
        eval2   = gu.Evaluator_1("eval2", "DD", "all > 10 ?")
        mymap   = gu.Map(4,6)

        mymap.install_machine(in1,      [0,0], [gu.DOWN_RIGHT]);            
        mymap.install_machine(in2,      [1,0], [gu.RIGHT]);                 
        mymap.install_machine(concat1,  [1,1], [gu.RIGHT]);                 
        self.assertEqual(False, concat1.ready_input_count())
        mymap.install_machine(add1,     [1,2], [gu.RIGHT]);               
        mymap.install_machine(splt1,    [1,3], [gu.RIGHT, gu.DOWN_RIGHT]);  
        mymap.install_machine(add2,     [1,4], [gu.RIGHT]);                
        mymap.install_machine(add3,     [2,4], [gu.RIGHT]);                 
        mymap.install_machine(eval1,    [1,5], [gu.END]);                   
        mymap.install_machine(eval2,    [2,5], [gu.END]);           
        mymap.run_complex_route(elements=[[0,0],[1,0]])
        self.assertEqual(eval1.output_buffer['main'], [1])
        self.assertEqual(eval2.output_buffer['main'], [1])

    def test_ready_input_count_unit_test(self):
        concat = gu.Concatenator(mode='default', title_private="concat1", manufacturer="DD", title_public="concatenator")
        self.assertEqual(False, concat.ready_input_count())
        concat.input_buffer['main'].append(1)
        self.assertEqual(False, concat.ready_input_count())
        concat.input_buffer['aux'].append(3)
        self.assertEqual(True, concat.ready_input_count())


    def test_run_complex_route_endless_loop_safety_mechanism(self):
        mymap = gu.Map(3,3)
        mymap.run_complex_route([[1,2], [3,4]])

    def test_manual_route_with_splitters_and_concatenators(self):
        in1     = gu.Input_Stream([1], "in1", "DD", "Input: 1")
        in2     = gu.Input_Stream([2], "in2", "DD", "Input: 2")
        concat1 = gu.Concatenator('default', "concat1", "DD", "combine")
        add1    = gu.Simple_Adder(-5, "sub 5", "DD", "subtract 5")
        splt1   = gu.Splitter('default', "splt1", "DD", "split")
        add2    = gu.Simple_Adder(20, "add 20", "DD", "add 20")
        add3    = gu.Simple_Adder(25, "add 25", "DD", "add 25")
        eval1   = gu.Evaluator_1("eval1", "DD", "all > 10 ?")
        eval2   = gu.Evaluator_1("eval2", "DD", "all > 10 ?")
        mymap   = gu.Map(4,6)

        mymap.install_machine(in1,      [0,0], [gu.DOWN_RIGHT]);            obj_in1     = mymap.get_cell(0,0)['obj']
        mymap.install_machine(in2,      [1,0], [gu.RIGHT]);                 obj_in2     = mymap.get_cell(1,0)['obj']
        mymap.install_machine(concat1,  [1,1], [gu.RIGHT]);                 obj_concat1 = mymap.get_cell(1,1)['obj']
        self.assertEqual(False, concat1.ready_input_count())
        mymap.install_machine(add1,     [1,2], [gu.RIGHT]);                 obj_add1    = mymap.get_cell(1,2)['obj']
        mymap.install_machine(splt1,    [1,3], [gu.RIGHT, gu.DOWN_RIGHT]);  obj_splt1   = mymap.get_cell(1,3)['obj']
        mymap.install_machine(add2,     [1,4], [gu.RIGHT]);                 obj_add2    = mymap.get_cell(1,4)['obj']
        mymap.install_machine(add3,     [2,4], [gu.RIGHT]);                 obj_add3    = mymap.get_cell(2,4)['obj']
        mymap.install_machine(eval1,    [1,5], [gu.END]);                   obj_eval1   = mymap.get_cell(1,5)['obj']
        mymap.install_machine(eval2,    [2,5], [gu.END]);                   obj_eval2   = mymap.get_cell(2,5)['obj']

        gu.connect_and_run(obj_in1, concat1); gu.connect_and_run(obj_in2, concat1, 'main', 'aux')
        gu.connect_and_run(concat1, add1); gu.connect_and_run(add1, splt1)
        gu.connect_and_run(splt1, add2, 'main', 'main')
        gu.connect_and_run(splt1, add3, 'aux',  'main')
        gu.connect_and_run(add2, eval1); gu.connect_and_run(add3, eval2)
        eval1.run()
        eval2.run()

        self.assertEqual(concat1.input_buffer['main'], [1])
        self.assertEqual(concat1.input_buffer['aux'] , [2])
        self.assertEqual(add1.output_buffer['main'], [-4,-3])
        self.assertEqual(splt1.output_buffer['main'], [-4])
        self.assertEqual(splt1.output_buffer['aux'], [-3])
        self.assertEqual(add2.output_buffer['main'], [16])
        self.assertEqual(add3.output_buffer['main'], [22])
        self.assertEqual(eval1.output_buffer['main'], [1])
        self.assertEqual(eval2.output_buffer['main'], [1])

        self.assertEqual(True, obj_in1.ready_input_count())
        self.assertEqual(True, obj_in2.ready_input_count())
        self.assertEqual(True, concat1.ready_input_count())
        self.assertEqual(True, add1.ready_input_count())
        self.assertEqual(True, splt1.ready_input_count())
        self.assertEqual(True, add2.ready_input_count())
        self.assertEqual(True, add3.ready_input_count())
        self.assertEqual(True, eval1.ready_input_count())
        self.assertEqual(True, eval2.ready_input_count())
       

    def test_ingest_data_append_method(self):
        adder = gu.Simple_Adder(operand=1, title_private='adder1',
                                title_public='add 1', manufacturer='DD',)
        adder.input_buffer['main'] = [1,2,3]
        adder.ingest_data([1], channel='main', method='append')
        print(adder.input_buffer['main'])
        self.assertEqual(4, len(adder.input_buffer['main']))
        self.assertEqual([1,2,3,1], adder.input_buffer['main'])

    def test_machine_with_inverted_directions(self):
        splitter_1 = gu.Splitter(mode='default', title_private='spt_1', manufacturer='N/A',
                                 title_public='splitter', loud_debug=False)
        mymap = gu.Map(4, 4, loud_debug=False)
        mymap.install_machine(splitter_1, 
                                 [0,0], output_directions=[gu.DOWN, gu.DOWN_RIGHT, gu.RIGHT])
        temp_1 = mymap.grid[1][0]['input_directions']
        temp_2 = mymap.grid[1][1]['input_directions']
        temp_3 = mymap.grid[0][1]['input_directions']
        self.assertEqual(temp_1, [gu.UP])
        self.assertEqual(temp_2, [gu.UP_LEFT])
        self.assertEqual(temp_3, [gu.LEFT])

        with self.assertRaises(ValueError):
            mymap.install_machine(splitter_1, [2,0], output_directions=[gu.DOWN, gu.LEFT, gu.RIGHT])
    

    def test_helper_invert_direction(self):
        temp_a = gu.RIGHT
        temp_b = gu.invert_direction(temp_a)
        print(temp_b)
        self.assertEqual(temp_b, gu.LEFT)

        temp_c = [2,0]
        with self.assertRaises(ValueError):
            gu.invert_direction(temp_c)
    
    def test_unit_test_concatenator(self):
        concat = gu.Concatenator(title_private='concat_1', manufacturer='Siemens', mode='default', title_public='concatenator', loud_debug=False)
        concat.input_buffer['main'] = [1,2,3]
        concat.input_buffer['aux']  = [4,5,6,7]
        concat.run()
        temp = concat.output_buffer['main']
        self.assertEqual(temp, [1,2,3,4,5,6,7])
        self.assertEqual(len(temp), 7)

        concat.input_buffer['main'] = None
        concat.input_buffer['aux']  = [4,5,6,7]
        concat.output_buffer['main'] = []
        with self.assertRaises(ValueError):
            concat.run()
        temp = concat.output_buffer['main']

   
    def test_print_logic_for_evaluator(self):
        input_stream = gu.Input_Stream(input_data=[1,2,3,4,5], title_private="INPUT_STREAM", manufacturer="N/A", loud_debug=False)
        input_stream.output_buffer['main'] = [1,2,3,4,5]
        temp = input_stream.print_logic()
        self.assertIsInstance(temp, str)
        self.assertEqual(temp, '1, 2, 3, 4, 5')
        #print(f'\n\nInput Buffer.print_logic() = {temp}')

    def test_check_all_win_conditions(self):
        eval_1       = gu.Evaluator_1(title_private="EVAL_1", manufacturer='DD', loud_debug=False)
        eval_2       = gu.Evaluator_1(title_private="EVAL_2", manufacturer='DD', loud_debug=False)
        eval_3       = gu.Evaluator_1(title_private="EVAL_3", manufacturer='DD', loud_debug=False)
        eval_4       = gu.Evaluator_1(title_private="EVAL_4", manufacturer='DD', loud_debug=False)
        eval_5       = gu.Evaluator_1(title_private="EVAL_5", manufacturer='DD', loud_debug=False)
        mymap        = gu.Map(gu.GRID_SIZE["rows"], gu.GRID_SIZE["cols"], loud_debug=True)

        mymap.install_machine(eval_1, [0,0], output_directions=[gu.END])
        mymap.install_machine(eval_2, [1,1], output_directions=[gu.END])
        mymap.install_machine(eval_3, [2,2], output_directions=[gu.END])
        mymap.install_machine(eval_4, [0,3], output_directions=[gu.END])
        mymap.install_machine(eval_5, [3,3], output_directions=[gu.END])

        with self.assertRaises(ValueError):
            mymap.check_all_win_conditions()
        
        for robot in (eval_1, eval_2, eval_3, eval_4, eval_5):
            robot.output_buffer['main'] = [0]
        self.assertEqual(mymap.check_all_win_conditions(),0)

        for robot in (eval_1, eval_2, eval_3, eval_4, eval_5):
            robot.output_buffer['main'] = [1]
        self.assertEqual(mymap.check_all_win_conditions(),1)

        for robot in (eval_1, eval_2, eval_3):
            robot.output_buffer['main'] = [1]
        for robot in (eval_4, eval_5):
            robot.output_buffer['main'] = [0]
        self.assertEqual(mymap.check_all_win_conditions(),0)


    def test_unit_test_for_evaluator_successful_check(self):
        eval_1       = gu.Evaluator_1(title_private="EVAL_1", manufacturer='DD', loud_debug=False)
        mymap        = gu.Map(gu.GRID_SIZE["rows"], gu.GRID_SIZE["cols"], loud_debug=True)
        mymap.install_machine(eval_1, [1,3], output_directions=[gu.END])

        temp = mymap.get_obj_at_coordinates(row=1, col=3)
        self.assertIsNotNone(temp, "object evaluates to None")
        self.assertIsInstance(temp, gu.Evaluator, "object is not an Evaluator subclass")
        temp.output_buffer['main'] = None
        
        with self.assertRaises(ValueError):
            temp.check_success()

        temp.output_buffer['main'] = []
        with self.assertRaises(ValueError):
            temp.check_success()

        temp.output_buffer['main'] = [1,2]
        with self.assertRaises(ValueError):
            temp.check_success()

        temp.output_buffer['main'] = [2]
        with self.assertRaises(ValueError):
            temp.check_success()

        temp.output_buffer['main'] = [1]
        temp_output = temp.check_success()
        self.assertEqual(temp_output, 1)
        self.assertIsInstance(temp_output, int)

    
    def test_find_all_evaluators_in_grid(self):
        eval_1       = gu.Evaluator_1(title_private="EVAL_1", manufacturer='DD', loud_debug=False)
        eval_2       = gu.Evaluator_1(title_private="EVAL_2", manufacturer='DD', loud_debug=False)
        eval_3       = gu.Evaluator_1(title_private="EVAL_3", manufacturer='DD', loud_debug=False)
        eval_4       = gu.Evaluator_1(title_private="EVAL_4", manufacturer='DD', loud_debug=False)
        eval_5       = gu.Evaluator_1(title_private="EVAL_5", manufacturer='DD', loud_debug=False)
        mymap        = gu.Map(gu.GRID_SIZE["rows"], gu.GRID_SIZE["cols"], loud_debug=True)

        mymap.install_machine(eval_1, [0,0], output_directions=[gu.END])
        mymap.install_machine(eval_2, [1,1], output_directions=[gu.END])
        mymap.install_machine(eval_3, [2,2], output_directions=[gu.END])
        mymap.install_machine(eval_4, [0,3], output_directions=[gu.END])
        mymap.install_machine(eval_5, [3,3], output_directions=[gu.END])

        temp = mymap.search_grid(gu.is_evaluator)
        self.assertEqual(len(temp), 5)


    def test_run_simple_route(self):
        adder_1      = gu.Simple_Adder(operand = 1,            title_private="ADDER_1",      manufacturer="DD",  loud_debug=False)
        adder_2      = gu.Simple_Adder(operand = 3,            title_private="ADDER_2",      manufacturer="DD",  loud_debug=False)
        adder_3      = gu.Simple_Adder(operand = 6,            title_private="ADDER_3",      manufacturer="DD",  loud_debug=False)
        input_stream = gu.Input_Stream(input_data=[1,2,6,4,2], title_private="INPUT_STREAM", manufacturer="N/A", loud_debug=False)
        eval_1       = gu.Evaluator_1(                         title_private="EVAL_1",       manufacturer='DD',  loud_debug=False)
        mymap        = gu.Map(gu.GRID_SIZE["rows"], gu.GRID_SIZE["cols"], loud_debug=True)

        mymap.install_machine(input_stream, [0,0], output_directions=[gu.DOWN])
        mymap.install_machine(adder_1,      [1,0], output_directions=[gu.UP_RIGHT])
        mymap.install_machine(adder_2,      [0,1], output_directions=[gu.DOWN_RIGHT])
        mymap.install_machine(adder_3,      [1,2], output_directions=[gu.RIGHT])
        mymap.install_machine(eval_1,       [1,3], output_directions=[gu.END])
        mymap.run_simple_route()
        output = mymap.get_cell(1,3)['obj'].output_buffer['main']
        self.assertEqual(output, [1])
    
    def test_exception_on_non_default_mode(self):
        with self.assertRaises(ValueError):
            my_splitter = gu.Splitter('special', 'test', 'test', False)

    def test_even_len_input_returns_valid_output(self):    
        my_splitter = gu.Splitter('default', 'test', 'test', False)
        my_splitter.ingest_data([1,2,3,4], channel='main', method='replace')
        my_splitter.run()
        temp_main = my_splitter.get_output('main')
        temp_aux  = my_splitter.get_output('aux')
        self.assertEqual(len(temp_main), len(temp_aux))
        self.assertEqual(temp_main, [1,2])
        self.assertEqual(temp_aux, [3,4])
        self.assertEqual(my_splitter.input_buffer['main'], temp_main + temp_aux)

    def test_odd_len_output_returns_valid_output(self):
        my_splitter = gu.Splitter('default', 'test', 'test', False)
        my_splitter.ingest_data([1,2,3,4,5], channel='main', method='replace')
        my_splitter.run()
        temp_main = my_splitter.get_output('main')
        temp_aux  = my_splitter.get_output('aux')
        self.assertEqual(len(temp_main), len(temp_aux))
        self.assertEqual(temp_main, [1,2,3])
        self.assertEqual(temp_aux, [4,5,5])



if __name__ == "__main__":
    unittest.main()