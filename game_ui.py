import tkinter as tk
import game_utils as gu

class GUI:
    def __init__(self, root, game_map):
        self.root = root
        self.game_map = game_map

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.cell_frame = tk.Frame(self.root, padx=10, pady=10)
        self.cell_frame.grid(row=0, column=0, sticky="nsew")

        self.status_var = tk.StringVar(value="Click a machine cell")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w")
        self.status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.control_frame = tk.Frame(self.root, padx=10, pady=10)
        self.control_frame.grid(row=1, column=0, sticky="ew")

        self.build_controls()
        self.build_board()

    def build_controls(self):
        run_button = tk.Button(self.control_frame, text="Run Simple Route", command=self.run_route)
        refresh_button = tk.Button(self.control_frame, text="Refresh Board", command=self.refresh_board)

        run_button.pack(side="left", padx=5)
        refresh_button.pack(side="left")

    def build_board(self):
        for widget in self.cell_frame.winfo_children():
            widget.destroy()

        for row in range(self.game_map.rows):
            self.cell_frame.rowconfigure(row, weight=1)
            for col in range(self.game_map.cols):
                cell = self.game_map.get_cell(row, col)
                if cell["status"] == "empty":
                    widget = tk.Label(
                        self.cell_frame,
                        text="",
                        relief="groove",
                        borderwidth=1,
                        width=14,
                        height=6,
                        bg="white"
                    )
                else:
                    widget = tk.Button(
                        self.cell_frame,
                        text=cell["obj"].title,
                        relief="raised",
                        borderwidth=2,
                        width=14,
                        height=6,
                        command=lambda r=row, c=col: self.on_cell_click(r, c)
                    )

                widget.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                self.cell_frame.columnconfigure(col, weight=1)

    def on_cell_click(self, row, col):
        cell = self.game_map.get_cell(row, col)
        if cell["status"] == "empty":
            self.status_var.set(f"Cell ({row},{col}) is empty")
            return

        obj = cell["obj"]
        title = getattr(obj, "title", "Unknown")
        logic = obj.print_logic() if hasattr(obj, "print_logic") else ""
        inputs = obj.input_buffer.get("main", []) if hasattr(obj, "input_buffer") else []
        outputs = obj.output_buffer.get("main", []) if hasattr(obj, "output_buffer") else []
        directions = cell.get("output_directions", [])

        self.status_var.set(
            f"Cell ({row},{col}): {title} | logic={logic} | in={inputs} | out={outputs} | dirs={directions}"
        )

    def refresh_board(self):
        self.build_board()
        self.status_var.set("Board refreshed")

    def run_route(self):
        try:
            self.game_map.run_simple_route()
            self.refresh_board()
            self.status_var.set("Route run completed")
        except Exception as exc:
            self.status_var.set(f"Run failed: {exc}")
