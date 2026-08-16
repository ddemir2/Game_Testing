import tkinter as tk
import customtkinter as ctk
import Game_Testing.game_utils as gu

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

CELL_WIDTH = 140
CELL_HEIGHT = 90

ARROW_ANCHORS = {
    tuple(gu.UP)         : (0.5, 0.01, "n", "\u2191"),
    tuple(gu.DOWN)       : (0.5, 0.99, "s", "\u2193"),
    tuple(gu.LEFT)       : (0.01, 0.5, "w", "\u2190"),
    tuple(gu.RIGHT)      : (0.99, 0.5, "e", "\u2192"),
    tuple(gu.UP_LEFT)    : (0.01, 0.01, "nw", "\u2196"),
    tuple(gu.UP_RIGHT)   : (0.99, 0.01, "ne", "\u2197"),
    tuple(gu.DOWN_LEFT)  : (0.01, 0.99, "sw", "\u2199"),
    tuple(gu.DOWN_RIGHT) : (0.99, 0.99, "se", "\u2198"),
}


class GUI:
    def __init__(self, root, game_map):
        self.root = root
        self.game_map = game_map

        self.root.rowconfigure(0, weight=8)
        self.root.rowconfigure(1, weight=2)
        self.root.columnconfigure(0, weight=1)

        self.top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="nsew")

        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure(0, weight=7)
        self.top_frame.columnconfigure(1, weight=3)

        self.cell_frame = ctk.CTkFrame(self.top_frame)
        self.cell_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.info_panel = ctk.CTkFrame(self.top_frame)
        self.info_panel.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)

        self.status_var = tk.StringVar(value="Click a machine cell")
        self.status_label = ctk.CTkLabel(self.top_frame, textvariable=self.status_var, anchor="w")
        self.status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.control_frame = ctk.CTkFrame(self.top_frame)
        self.control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.bottom_panel = ctk.CTkFrame(self.root)
        self.bottom_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.cell_boxes = {}
        self.cell_labels = {}
        self.cell_arrows = {}
        self.selected_cell = None

        self.build_controls()
        self.build_board()

    def build_controls(self):
        run_button = ctk.CTkButton(self.control_frame, text="Run Simple Route", command=self.run_route)
        refresh_button = ctk.CTkButton(self.control_frame, text="Refresh Board", command=self.refresh_board)

        run_button.pack(side="left", padx=5, pady=5)
        refresh_button.pack(side="left", padx=5, pady=5)

    def build_board(self):
        for widget in self.cell_frame.winfo_children():
            widget.destroy()

        self.cell_boxes = {}
        self.cell_labels = {}
        self.cell_arrows = {}
        self.selected_cell = None

        for row in range(self.game_map.rows):
            self.cell_frame.rowconfigure(row, weight=1)
            for col in range(self.game_map.cols):
                self.cell_frame.columnconfigure(col, weight=1)
                cell = self.game_map.get_cell(row, col)

                box = ctk.CTkFrame(
                    self.cell_frame,
                    width=CELL_WIDTH,
                    height=CELL_HEIGHT,
                    fg_color="black",
                    corner_radius=6,
                )
                box.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
                box.grid_propagate(False)
                box.rowconfigure(0, weight=1)
                box.columnconfigure(0, weight=1)

                if cell["status"] == "empty":
                    label = ctk.CTkLabel(box, text="", text_color="white")
                    label.grid(row=0, column=0, sticky="nsew")
                else:
                    label = ctk.CTkLabel(
                        box,
                        text=cell["obj"].title,
                        text_color="white",
                    )
                    label.grid(row=0, column=0, sticky="nsew")
                    label.bind("<Button-1>", lambda e, r=row, c=col: self.on_cell_click(r, c))

                    directions = cell.get("output_directions", [])
                    arrow_labels = []
                    for direction in directions:
                        anchor_info = ARROW_ANCHORS.get(tuple(direction))
                        if anchor_info is None:
                            continue
                        relx, rely, anchor, glyph = anchor_info
                        arrow_label = ctk.CTkLabel(
                            box,
                            text=glyph,
                            text_color="yellow",
                            font=ctk.CTkFont(size=20, weight="bold"),
                            fg_color="transparent",
                        )
                        arrow_label.place(relx=relx, rely=rely, anchor=anchor)
                        arrow_label.bind("<Button-1>", lambda e, r=row, c=col: self.on_cell_click(r, c))
                        arrow_labels.append(arrow_label)

                    box.bind("<Button-1>", lambda e, r=row, c=col: self.on_cell_click(r, c))

                self.cell_boxes[(row, col)] = box
                self.cell_labels[(row, col)] = label
                self.cell_arrows[(row, col)] = arrow_labels

    def on_cell_click(self, row, col):
        cell = self.game_map.get_cell(row, col)

        if self.selected_cell is not None and self.selected_cell in self.cell_boxes:
            self.cell_boxes[self.selected_cell].configure(fg_color="black")
            if self.selected_cell in self.cell_labels:
                self.cell_labels[self.selected_cell].configure(text_color="white")
            for arrow_label in self.cell_arrows.get(self.selected_cell, []):
                arrow_label.configure(text_color="yellow")

        if cell["status"] == "empty":
            self.selected_cell = None
            self.status_var.set(f"Cell ({row},{col}) is empty")
            return

        self.selected_cell = (row, col)
        self.cell_boxes[(row, col)].configure(fg_color="gold")
        if (row, col) in self.cell_labels:
            self.cell_labels[(row, col)].configure(text_color="black")
        for arrow_label in self.cell_arrows.get((row, col), []):
            arrow_label.configure(text_color="black")

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
