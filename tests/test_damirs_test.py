

import unittest

import game_utils as gu
import game_ui as gui

class General_Test(unittest.TestCase):
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