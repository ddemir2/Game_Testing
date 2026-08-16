

import unittest

import Game_Testing.game_utils as gu
import Game_Testing.game_ui as gui

class Splitter_Test(unittest.TestCase):
    def test_run_simple_route(self):
        adder_1      = gu.Simple_Adder(operand = 1,            title="ADDER_1",      manufacturer="DD",  loud_debug=False)
        adder_2      = gu.Simple_Adder(operand = 3,            title="ADDER_2",      manufacturer="DD",  loud_debug=False)
        adder_3      = gu.Simple_Adder(operand = 6,            title="ADDER_3",      manufacturer="DD",  loud_debug=False)
        input_stream = gu.Input_Stream(input_data=[1,2,6,4,2], title="INPUT_STREAM", manufacturer="N/A", loud_debug=False)
        eval_1       = gu.Evaluator_1(                         title="EVAL_1",       manufacturer='DD',  loud_debug=False)
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