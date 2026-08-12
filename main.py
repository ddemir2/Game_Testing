'''
Version 1.2
Resting Squirrel
Refactors and basic GUI
'''

import game_utils as gu
import game_ui as gui

if __name__ == "__main__":
    adder_1      = gu.Simple_Adder(operand = 1,            title="ADDER_1",      manufacturer="DD",  loud_debug=False)
    adder_2      = gu.Simple_Adder(operand = 3,            title="ADDER_2",      manufacturer="DD",  loud_debug=False)
    adder_3      = gu.Simple_Adder(operand = 6,            title="ADDER_3",      manufacturer="DD",  loud_debug=False)
    input_stream = gu.Input_Stream(input_data=[1,2,6,4,2], title="INPUT_STREAM", manufacturer="N/A", loud_debug=False)
    eval_1       = gu.Evaluator_1(                         title="EVAL_1",       manufacturer='DD',  loud_debug=False)
    mymap        = gu.Map(gu.GRID_SIZE["rows"], gu.GRID_SIZE["cols"], loud_debug=True)

    mymap.install_machine(input_stream, [0,0], output_directions=[gu.DOWN])
    mymap.install_machine(adder_1,      [1,0], output_directions=[gu.RIGHT])
    mymap.install_machine(adder_2,      [1,1], output_directions=[gu.RIGHT])
    mymap.install_machine(adder_3,      [1,2], output_directions=[gu.RIGHT])
    mymap.install_machine(eval_1,       [1,3], output_directions=[gu.END])

    root = gui.tk.Tk()
    root.title("Game Board GUI")
    app = gui.GUI(root, mymap)
    root.mainloop()
