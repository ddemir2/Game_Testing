'''
Version 1.5
Ice Fox
Additional UI Improvements; change machine mechanic implemented
'''

import game_utils as gu
import game_ui as gui

if __name__ == "__main__":
    adder_1      = gu.Simple_Adder(operand = 1,            title_private="ADDER_1",      manufacturer="DD",  title_public='Adder',          loud_debug=False)
    adder_2      = gu.Simple_Adder(operand = 3,            title_private="ADDER_2",      manufacturer="DD",  title_public='Adder',          loud_debug=False)
    adder_3      = gu.Simple_Adder(operand = 6,            title_private="ADDER_3",      manufacturer="DD",  title_public= 'Adder',         loud_debug=False)
    input_stream = gu.Input_Stream(input_data=[1,2,6,4,2], title_private="INPUT_STREAM", manufacturer="N/A", title_public='Input',          loud_debug=False)
    eval_1       = gu.Evaluator_1(                         title_private="EVAL_1",       manufacturer='DD',  title_public='Output',  loud_debug=False)
    mymap        = gu.Map(gu.GRID_SIZE["rows"], gu.GRID_SIZE["cols"], loud_debug=True)

    mymap.install_machine(input_stream, [0,0], output_directions=[gu.DOWN])
    mymap.install_machine(adder_1,      [1,0], output_directions=[gu.UP_RIGHT])
    mymap.install_machine(adder_2,      [0,1], output_directions=[gu.DOWN_RIGHT])
    mymap.install_machine(adder_3,      [1,2], output_directions=[gu.RIGHT])
    mymap.install_machine(eval_1,       [1,3], output_directions=[gu.END])

    root = gui.ctk.CTk()
    root.title("Game Board GUI")
    root.geometry("1000x700")
    root.minsize(800, 600)
    app = gui.GUI(root, mymap)
    mymap.run_simple_route()
    root.mainloop()
