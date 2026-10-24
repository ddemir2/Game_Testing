import unittest

import game_utils as gu
import game_ui as gui
from collections import deque

class General_Test(unittest.TestCase):
    def test_third_output_channel_unit_testing(self):
        mach1 = gu.Machine(title_private="mach1", config="DD", title_public="Machine")
        with self.assertRaises(ValueError):
            mach1.get_output(channel='main')
        mach1.output_channels['main'] = [5]; mach1.output_channels['aux_1'] = [6]; mach1.output_channels['aux_2'] = [7]
        self.assertEqual(mach1.get_output('aux_2'), [7])

    def test_ingest_data_unit_testing(self):
        mech = gu.Machine("a", {}, "b")
        mech.ingest_data([1,2,3,4,5])
        self.assertEqual(mech.input_buffer, [1,2,3,4,5])

        mech.ingest_data([6,7,8], method='replace')
        self.assertEqual(mech.input_buffer, [6,7,8])

        mech2 = gu.Machine("a", {}, "b"); 
        mech2.ingest_data([1,2,3,4,5], method='append')
        self.assertEqual(mech2.input_buffer, [1,2,3,4,5])
        mech2.ingest_data([9,8], method='append')
        self.assertEqual(mech2.input_buffer, [1,2,3,4,5,9,8])


    def test_evaluator_base_class_unit_testing(self):
        myconfig = {'truth_statement' : [12,14,15]}
        eval1 = gu.Evaluator("d", myconfig, "a");
        with self.assertRaises(ValueError): eval1.run()
        with self.assertRaises(ValueError): eval1.check_success()
        eval1.input_buffer = [14,12]; eval1.run()
        self.assertEqual(eval1.check_success(), False)
        eval1.ingest_data(data=[15], method='append')
        eval1.run()
        self.assertEqual(eval1.check_success(), True)

    def test_print_logic_unit_testing(self):
        myconfig = {'truth_statement' : None, 'logic_text' : 'contains 12,14, and 15'}
        in1   = gu.Input_Stream([6,7,8],"d", myconfig,"d")
        eval1 = gu.Evaluator(title_private='d', config=myconfig, title_public='e')
        
        temp_eval = eval1.print_logic()
        temp_in   = in1.print_logic()
        self.assertEqual('contains 12,14, and 15', temp_eval)
        self.assertEqual('6, 7, 8', temp_in)


    def test_input_stream_unit_testing(self):
        myconfig = {'truth_statement' : None, 'logic_text' : '1, 2, 3'}
        in1 = gu.Input_Stream(input_data=[1,2,3], title_private='d', config=myconfig, title_public='e')
        with self.assertRaises(ValueError):
            in2 = gu.Input_Stream(input_data=[], title_private='d', config=myconfig, title_public='e')
        in1.run()
        self.assertEqual(in1.get_output(channel='main'), [1,2,3])


    def test_map_unit_testing(self):
        TEST_NUM = 7
        myconfig = {'truth_statement' : None, 'logic_text' : '1, 2, 3'}
        in1 = gu.Input_Stream(input_data=[1,2,3], title_private='d', config=myconfig, title_public='d')
        mymap = gu.Map(TEST_NUM, TEST_NUM)

        with self.assertRaises(TypeError): mymap = gu.Map(True, TEST_NUM)
        with self.assertRaises(ValueError): mymap = gu.Map(-1, TEST_NUM) 
        with self.assertRaises(ValueError): mymap = gu.Map(0, TEST_NUM) 

    def test_in_bounds_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(TEST_NUM, TEST_NUM)
        self.assertEqual(False, mymap.is_in_bounds(row = -1, col = 2))
        self.assertEqual(False, mymap.is_in_bounds(row = 7, col = 2))
        self.assertEqual(False, mymap.is_in_bounds(row = 3, col = 12))
        self.assertEqual(True, mymap.is_in_bounds(row = 2, col = 4))

    def test_get_cell(self):
        TEST_NUM = 7
        mymap = gu.Map(TEST_NUM, TEST_NUM)
        myconfig = {'truth_statement' : None, 'logic_text' : '1, 2, 3'}
        in1 = gu.Input_Stream(input_data=[1,2,3], title_private='d', config=myconfig, title_public='e')
        mymap.grid[1][1]['obj'] = in1; mymap.grid[1][1]['status'] = 'occupied'  

        self.assertEqual(mymap.get_cell(0,3), gu.CELL_TEMPLATE)
        self.assertNotEqual(mymap.get_cell(1,1), gu.CELL_TEMPLATE)
        self.assertEqual(mymap.get_cell(1,1)['status'], 'occupied')
        self.assertIsInstance(mymap.get_cell(1,1)['obj'], gu.Input_Stream)
        with self.assertRaises(KeyError): mymap.get_cell(-1,0)
        with self.assertRaises(KeyError): mymap.get_cell(7,2)
        with self.assertRaises(KeyError): mymap.get_cell(4,12)

    def test_is_in_bounds(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        statements = all([mymap.is_in_bounds(0,0), mymap.is_in_bounds(6,0), not mymap.is_in_bounds(-1,0), not mymap.is_in_bounds(TEST_NUM,0)])
        self.assertEqual(statements, True)

    def test_is_empty_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1 = gu.Input_Stream([4,5,6], 'd', {}, 'd');   in2 = gu.Input_Stream([10,11,12], 'd', {}, 'd')
        mymap.get_cell(0,0)['obj'] = in1;   mymap.get_cell(0,0)['status'] ='occupied'
        mymap.get_cell(1,0)['obj'] = in2;
        mymap.get_cell(2,0)['status'] = 'occupied'

        self.assertEqual(mymap.is_empty(0,0), False)
        self.assertEqual(mymap.is_empty(0,1), True)
        with self.assertRaises(LookupError): mymap.is_empty(1,0)
        with self.assertRaises(LookupError): mymap.is_empty(2,0)

    def test_install_machine_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1 = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        in2 = gu.Input_Stream([9,10,11], 'e', {}, 'e');
        mymap.install_machine(obj=in2, install_location=[3,0], output_directions=[gu.DOWN])

        with self.assertRaises(IndexError): mymap.install_machine(obj=in1, install_location=[-1,0], output_directions=[gu.RIGHT])
        with self.assertRaises(TypeError): mymap.install_machine(obj=in1, install_location=[0,0], output_directions=gu.RIGHT)
        with self.assertRaises(TypeError): mymap.install_machine(obj=in1, install_location=[0,0], output_directions=[1,2])        
        with self.assertRaises(TypeError): mymap.install_machine(obj=in1, install_location=[0,0], output_directions=None)
        with self.assertRaises(PermissionError): mymap.install_machine(obj=in1, install_location=[3,0], output_directions=[gu.LEFT])

    def test_get_obj_at_coordinates_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1 = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        mymap.install_machine(in1, [2,2], output_directions=[gu.RIGHT])
        temp = mymap.get_obj_at_coordinates(row=2, col=2)
        
        self.assertIsInstance(temp, gu.Input_Stream)
        self.assertIsSubclass(type(temp), gu.Machine)

    def test_get_status_at_coordinates_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1 = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        mymap.install_machine(in1, [2,2], output_directions=[gu.RIGHT])
        mymap.get_cell(row=0, col=0)['status'] = 'lol'
        temp_1 = mymap.get_status_at_coordinates(row=2, col=2)
        temp_2 = mymap.get_status_at_coordinates(row=1, col=1)

        with self.assertRaises(KeyError): mymap.get_status_at_coordinates(0,0)
        self.assertEqual(temp_1, 'occupied')
        self.assertEqual(temp_2, 'empty')

    def test_get_output_directions_at_coordinates_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1 = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        mymap.install_machine(in1, [2,2], output_directions=[gu.RIGHT, gu.DOWN, gu.DOWN_RIGHT])
        mymap.get_cell(row=0, col=0)['status'] = 'lol'
        temp_1 = mymap.get_status_at_coordinates(row=2, col=2)
        temp_2 = mymap.get_status_at_coordinates(row=1, col=1)

        with self.assertRaises(KeyError): mymap.get_status_at_coordinates(0,0)
        self.assertEqual(temp_1, 'occupied')
        self.assertEqual(temp_2, 'empty')

    def test_iter_cells_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1 = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        mymap.install_machine(in1, [1,1], output_directions=[gu.RIGHT])
        yield_result = list(mymap.iter_cells())
        obj_list = []
        for tuple in yield_result:
            obj_list.append(tuple[2]['obj'])
        machine = [x for x in obj_list if x][0]
        none_list = [x for x in obj_list if not x]

        self.assertEqual(len(obj_list), TEST_NUM ** 2)
        self.assertIs(machine, in1)
        self.assertEqual(len(none_list), (TEST_NUM ** 2)-1)

    def test_search_grid_unit_testing(self):
        foo = lambda x: type(x) == gu.Input_Stream
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1   = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        in2   = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        eval1 = gu.Evaluator("d", {}, "d")

        mymap.install_machine(in1, [1,1], output_directions=[gu.RIGHT]) 
        temp = mymap.search_grid(foo)
        self.assertEqual(len(temp), 1)
        self.assertEqual(temp[0], [1,1])

        mymap.install_machine(in2, [3,3], output_directions=[gu.DOWN]) 
        temp2 = mymap.search_grid(foo)
        self.assertEqual(len(temp2), 2)
        self.assertEqual(temp2, [[1,1],[3,3]])

        mymap.install_machine(obj=eval1, install_location=[4,4], output_directions=[gu.DOWN])
        temp3 = mymap.search_grid(foo)
        self.assertEqual(len(temp3), 2)
        self.assertEqual(temp3, [[1,1],[3,3]])

    def test_is_functions_unit_testing(self):
        in1     = gu.Input_Stream([1,2], "d", {}, "d")
        eval1   = gu.Evaluator("d", {}, "d")
        self.assertEqual(gu.is_input_stream(in1), True)
        self.assertEqual(gu.is_input_stream(eval1), False)
        self.assertEqual(gu.is_evaluator(eval1), True)
        
    def test_clear_cell_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1   = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        self.assertEqual(mymap.get_cell(0,0), gu.CELL_TEMPLATE)   
        mymap.install_machine(obj=in1, install_location=[0,0], output_directions=[gu.RIGHT])
        self.assertEqual(mymap.get_cell(0,0)['status'], 'occupied')
        self.assertIs(in1, mymap.get_cell(0,0)['obj'])
        mymap.clear_cell(0,0)
        self.assertEqual(mymap.get_cell(0,0), gu.CELL_TEMPLATE)   

    def test_pipe_unit_testing(self):
        TEST_NUM = 7
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        pipe  = gu.Input_Stream([4,5,6], 'd', {}, 'd');
        mymap.install_machine(pipe, [0,0], [gu.RIGHT])
        temp = mymap.get_obj_at_coordinates(0,0)
        temp.input_buffer = [1,2,3]

        self.assertEqual(len(temp.output_channels), 1)
        self.assertEqual(temp.output_channels['main'], [])
        temp.run()
        self.assertEqual(len(temp.output_channels['main']), 3)
        self.assertEqual(temp.output_channels['main'], [1,2,3])

    def test_connect_and_run_unit_testing(self):
        in1 = gu.Input_Stream([1,2,3],'d',{},'d')
        p1  = gu.Pipe('d',{},'d')
        m1 = gu.Machine('d',{},'d')

        with self.assertRaises(ValueError):
            gu.connect_and_run(in1, 'main', None)
            gu.connect_and_run(in1, '', p1)
            gu.connect_and_run(None, 'main', p1)
        with self.assertRaises(TypeError):
            gu.connect_and_run(m1, 'main', p1)
            gu.connect_and_run(in1, 'main', m1)
        with self.assertRaises(KeyError):
            gu.connect_and_run(in1, 'aux_4', p1)

        gu.connect_and_run(in1, 'main', p1)
        self.assertEqual(p1.input_buffer, [1,2,3])
        gu.connect_and_run(in1, 'main', p1)
        self.assertEqual(p1.input_buffer, [1,2,3,1,2,3])

    def test_connect_and_run_at_coordinates(self):
        TEST_NUM = 7
        mymap = gu.Map(TEST_NUM, TEST_NUM)
        in1 = gu.Input_Stream([1,2,3],'d',{},'d'); mymap.install_machine(in1, [1,0], [gu.RIGHT])
        p1  = gu.Pipe('d',{},'d'); mymap.install_machine(p1, [1,1], [gu.DOWN])

        mymap.connect_and_run_at_coordinates([1,0], 'main', [1,1])
        self.assertEqual(p1.input_buffer, [1,2,3])

        with self.assertRaises(KeyError):
            mymap.connect_and_run_at_coordinates(None, 'main', [1,1])
        with self.assertRaises(KeyError):
            mymap.connect_and_run_at_coordinates([1,0], 'main', None)
        with self.assertRaises(TypeError):
            mymap.connect_and_run_at_coordinates(["g",0], 'main', [1,1])
        with self.assertRaises(KeyError):
            mymap.connect_and_run_at_coordinates((1,0), 'main', [1,1])
        with self.assertRaises(KeyError):
            mymap.connect_and_run_at_coordinates([1,0,5], 'main', [2])
        with self.assertRaises(LookupError):
            mymap.connect_and_run_at_coordinates([5,0], 'main', [1,1])
        with self.assertRaises(LookupError):
            mymap.connect_and_run_at_coordinates([6,0], 'main', [6,4])

    def test_ready_to_run_unit_testing(self):
        pipe1 = gu.Pipe('d',{},'d',False)
        self.assertEqual(pipe1.ready_to_run(), False)
        pipe1.input_buffer = [1,2,3]
        self.assertEqual(pipe1.ready_to_run(), True)
        pipe1.input_buffer = None
        self.assertEqual(pipe1.ready_to_run(), False)

    def test_naive_splitter_unit_testing(self):
        splitter1 = gu.Naive_Splitter('d',{},'d',False)
        splitter1.ingest_data([1,2,3,4,5])
        splitter1.run()
        self.assertEqual(splitter1.output_channels['main'], [1,2,3])
        self.assertEqual(splitter1.output_channels['aux_1'], [4,5,5])



    def test_naive_run_integration_testing(self):
        TEST_NUM = 4
        eval_config1 = {'truth_statement' : [4,5,6]}
        eval_config2 = {'truth_statement' : [7,8,8]}
        mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        in1  = gu.Input_Stream([4,5,6,7,8], 'in1', {}, 'in1', False);
        sp1 = gu.Naive_Splitter('d',{},'d',False)
        pi1  = gu.Pipe('d', {}, 'd')
        pi2  = gu.Pipe('d', {}, 'd')
        pi3  = gu.Pipe('d', {}, 'd')
        ev1  = gu.Evaluator('eval1', eval_config1, 'eval1', False)
        ev2  = gu.Evaluator('eval2', eval_config2, 'eval2', False)

        mymap.install_machine(in1, [0,0], [gu.RIGHT])
        mymap.install_machine(sp1, [0,1], [gu.RIGHT, gu.DOWN])
        mymap.install_machine(pi1, [1,1], [gu.RIGHT])
        mymap.install_machine(pi2, [0,2], [gu.RIGHT])
        mymap.install_machine(pi3, [1,2], [gu.RIGHT])
        mymap.install_machine(ev1, [0,3], [gu.END])
        mymap.install_machine(ev2, [1,3], [gu.END])

        mymap.run_complex_route([[0, 0]])
        self.assertEqual(ev1.check_success(), 1)
        self.assertEqual(ev2.check_success(), 1)







    #def test_run_complex_route_unit_testing(self):
     #   TEST_NUM = 4
      #  eval_config = {'truth_statement' : [4,5,6]}
       # mymap = gu.Map(rows=TEST_NUM, cols=TEST_NUM)
        #in1  = gu.Input_Stream([4,5,6], 'in1', {}, 'in1', False);
        #pi1  = gu.Pipe('d', {}, 'd')
       # pi2  = gu.Pipe('d', {}, 'd')
        #ev1  = gu.Evaluator('eval1', eval_config, 'eval1', False)
        #mymap.install_machine(in1, [1,0], [gu.RIGHT])
        #mymap.install_machine(pi1, [1,1], [gu.RIGHT])
        #mymap.install_machine(pi2, [1,2], [gu.RIGHT])
        #mymap.install_machine(ev1, [1,3], [gu.RIGHT])
        #mymap.run_complex_route([[1,0]])
        #self.assertEqual(ev1.check_success(), 1)

if __name__ == "__main__":
    unittest.main()