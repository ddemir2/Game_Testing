'''
Version 1.0
Tired Bison
'''

import game_utils as gu

if __name__ == "__main__":
    adder_1      = gu.Simple_Adder(operand = 1,  title="Adder 1", manufacturer="DD", loud_debug=False)
    adder_2      = gu.Simple_Adder(operand = 2,  title="Adder 2", manufacturer="DD", loud_debug=False)
    adder_3      = gu.Simple_Adder(operand = 3, title="Adder 3", manufacturer="DD", loud_debug=False)
    input_stream = gu.Input_Stream([1,2,3,4,5], "Input Stream", "N/A", loud_debug=False)
    eval_1       = gu.Evaluator_1(title="eval_1", manufacturer='DD', loud_debug=False)
    mymap        = gu.Map(GRID_SIZE_LOCAL = gu.GRID_SIZE)

    mymap.install_machine(input_stream, [0,0], output_directions=[gu.RIGHT])
    mymap.install_machine(adder_1, [0,1], output_directions=[gu.DOWN])
    mymap.install_machine(adder_2, [1,1], output_directions=[gu.RIGHT])
    mymap.install_machine(adder_3, [1,2], output_directions=[gu.RIGHT])
    mymap.install_machine(eval_1,  [1,3], output_directions=[gu.NONE])
    

    current_row = 0
    current_col = 0
    temp = mymap.grid[current_row][current_col]["obj"].run()
    direction = mymap.grid[current_row][current_col]["output_directions"][0]
    destination_row, destination_col = [x + y for x, y in zip([current_row, current_col], direction)]
    mymap.grid[destination_row][destination_col]["obj"].ingest_data(data=temp, method="replace")

    current_row = 0; current_col = 1
    temp = mymap.grid[current_row][current_col]["obj"].run()
    direction = mymap.grid[current_row][current_col]["output_directions"][0]
    destination_row, destination_col = [x + y for x, y in zip([current_row, current_col], direction)]
    mymap.grid[destination_row][destination_col]["obj"].ingest_data(data=temp, method="replace")

    current_row = 1; current_col = 1
    temp = mymap.grid[current_row][current_col]["obj"].run()
    direction = mymap.grid[current_row][current_col]["output_directions"][0]
    destination_row, destination_col = [x + y for x, y in zip([current_row, current_col], direction)]
    mymap.grid[destination_row][destination_col]["obj"].ingest_data(data=temp, method="replace")

    current_row = 1; current_col = 2
    temp = mymap.grid[current_row][current_col]["obj"].run()
    direction = mymap.grid[current_row][current_col]["output_directions"][0]
    destination_row, destination_col = [x + y for x, y in zip([current_row, current_col], direction)]
    mymap.grid[destination_row][destination_col]["obj"].ingest_data(data=temp, method="replace")

    current_row = 1; current_col = 3
    outcome = mymap.grid[current_row][current_col]["obj"].run()

    

    end_game = False
    menu_choice = 0
    machine_change = 0

    while not end_game:
        mymap.print_grid()

        current_row = 0
        current_col = 0
        temp = mymap.grid[current_row][current_col]["obj"].run()
        direction = mymap.grid[current_row][current_col]["output_directions"][0]
        destination_row, destination_col = [x + y for x, y in zip([current_row, current_col], direction)]
        mymap.grid[destination_row][destination_col]["obj"].ingest_data(data=temp, method="replace")

        current_row = 0; current_col = 1
        temp = mymap.grid[current_row][current_col]["obj"].run()
        direction = mymap.grid[current_row][current_col]["output_directions"][0]
        destination_row, destination_col = [x + y for x, y in zip([current_row, current_col], direction)]
        mymap.grid[destination_row][destination_col]["obj"].ingest_data(data=temp, method="replace")

        current_row = 1; current_col = 1
        temp = mymap.grid[current_row][current_col]["obj"].run()
        direction = mymap.grid[current_row][current_col]["output_directions"][0]
        destination_row, destination_col = [x + y for x, y in zip([current_row, current_col], direction)]
        mymap.grid[destination_row][destination_col]["obj"].ingest_data(data=temp, method="replace")

        current_row = 1; current_col = 2
        temp = mymap.grid[current_row][current_col]["obj"].run()
        direction = mymap.grid[current_row][current_col]["output_directions"][0]
        destination_row, destination_col = [x + y for x, y in zip([current_row, current_col], direction)]
        mymap.grid[destination_row][destination_col]["obj"].ingest_data(data=temp, method="replace")

        current_row = 1; current_col = 3
        outcome = mymap.grid[current_row][current_col]["obj"].run()

        if outcome:
            end_game = True
            print("You passed level 1")
        else:
            print(f"\n-----------------------")
            print(f"Change a machine to achieve the goal [ALL OUTPUT STREAM ITEMS MUST BE > 10]:")
            print(f"\t1) Adder A: +1    |   Location: [0,1]")
            print(f"\t2) Adder A: +2    |   Location: [1,1]")
            print(f"\t3) Adder A: +3   |   Location: [1,2]")
            # Reset choices so the user is prompted each loop iteration
            menu_choice = 0
            machine_change = 0
            while menu_choice not in [1,2,3]:
                try:
                    print(f"Type your choice here: ")
                    menu_choice = int(input())
                except ValueError:
                    menu_choice = 0
            while machine_change not in range(1,999):
                try:
                    print(f"To which value would you like to change the adder? Type your answer here:")
                    machine_change = int(input())
                except ValueError:
                    machine_change = 0
            if menu_choice == 1:
                mymap.grid[0][1]["obj"].update_operand(machine_change) 
            elif menu_choice == 2:
                mymap.grid[1][1]["obj"].update_operand(machine_change)
            elif menu_choice == 3:
                mymap.grid[1][2]["obj"].update_operand(machine_change)
            else:
                raise ValueError("Unknown Game State")
