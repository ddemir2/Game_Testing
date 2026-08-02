'''
Version 1.1
Gurgling Rapids
Implemented run_simple_route
'''

import game_utils as gu

if __name__ == "__main__":
    adder_1      = gu.Simple_Adder(operand = 1,            title="ADDER_1",      manufacturer="DD",  loud_debug=False)
    adder_2      = gu.Simple_Adder(operand = 3,            title="ADDER_2",      manufacturer="DD",  loud_debug=False)
    adder_3      = gu.Simple_Adder(operand = 6,            title="ADDER_3",      manufacturer="DD",  loud_debug=False)
    input_stream = gu.Input_Stream(input_data=[1,2,3,4,5], title="INPUT_STREAM", manufacturer="N/A", loud_debug=False)
    eval_1       = gu.Evaluator_1(                         title="EVAL_1",       manufacturer='DD',  loud_debug=False)
    mymap        = gu.Map(GRID_SIZE_LOCAL = gu.GRID_SIZE, loud_debug=True)

    mymap.install_machine(input_stream, [0,0], output_directions=[gu.RIGHT])
    mymap.install_machine(adder_1,      [0,1], output_directions=[gu.DOWN])
    mymap.install_machine(adder_2,      [1,1], output_directions=[gu.RIGHT])
    mymap.install_machine(adder_3,      [1,2], output_directions=[gu.RIGHT])
    mymap.install_machine(eval_1,       [1,3], output_directions=[gu.END])


    mymap.run_simple_route()
    mymap.new_print_grid()
