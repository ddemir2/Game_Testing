import tkinter as tk
import customtkinter as ctk
import game_utils as gu

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

CELL_WIDTH = 140
CELL_HEIGHT = 90
CELL_DEFAULT_COLOR = "#1f6aa5"

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

        self.cell_frame = ctk.CTkFrame(self.top_frame, width=700, height=500, fg_color="transparent")
        self.cell_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.cell_frame.grid_propagate(False)

        self.info_panel = ctk.CTkFrame(self.top_frame, width=250, height=500)
        self.info_panel.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)
        self.info_panel.grid_propagate(False)
        self.info_panel.pack_propagate(False)

        self.status_var = tk.StringVar(value="(Nothing Selected)")
        self.status_label = ctk.CTkLabel(
            self.info_panel,
            textvariable=self.status_var,
            anchor="nw",
            justify="left",
            wraplength=230,
            font=ctk.CTkFont(family="Courier New", size=16),
        )
        self.status_label.pack(side="top", fill="x", padx=10, pady=10)

        self.edit_machine_button = ctk.CTkButton(
            self.info_panel,
            text="Edit Machine",
            command=self.on_edit_machine,
        )

        self.control_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.bottom_panel = ctk.CTkFrame(self.root)
        self.bottom_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.cell_boxes = {}
        self.cell_labels = {}
        self.cell_arrows = {}
        self.selected_cell = None
        self.tooltip_window = None

        self.build_controls()
        self.build_board()

    def build_controls(self):
        refresh_button = ctk.CTkButton(self.control_frame, text="Unselect All", command=self.refresh_board)

        refresh_button.pack(side="left", padx=5, pady=5)

    def build_board(self):
        self.hide_tooltip()
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
                    fg_color=CELL_DEFAULT_COLOR,
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
                        text=cell["obj"].title_public + f'\n' + cell["obj"].print_logic(),
                        text_color="white",
                    )
                    label.grid(row=0, column=0, sticky="nsew")
                    label.bind("<Button-1>", lambda e, r=row, c=col: self.on_cell_click(r, c))
                    label.bind("<Enter>", lambda e, r=row, c=col: self.show_tooltip(r, c))
                    label.bind("<Leave>", lambda e: self.hide_tooltip())

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
                    box.bind("<Enter>", lambda e, r=row, c=col: self.show_tooltip(r, c))
                    box.bind("<Leave>", lambda e: self.hide_tooltip())

                self.cell_boxes[(row, col)] = box
                self.cell_labels[(row, col)] = label
                self.cell_arrows[(row, col)] = arrow_labels

    def on_cell_click(self, row, col):
        cell = self.game_map.get_cell(row, col)

        if self.selected_cell is not None and self.selected_cell in self.cell_boxes:
            self.cell_boxes[self.selected_cell].configure(fg_color=CELL_DEFAULT_COLOR)
            if self.selected_cell in self.cell_labels:
                self.cell_labels[self.selected_cell].configure(text_color="white")
            for arrow_label in self.cell_arrows.get(self.selected_cell, []):
                arrow_label.configure(text_color="yellow")

        if cell["status"] == "empty":
            self.selected_cell = None
            self.status_var.set(f"Cell ({row},{col}) is empty")
            self.edit_machine_button.place_forget()
            return

        self.selected_cell = (row, col)
        self.cell_boxes[(row, col)].configure(fg_color="gold")
        if (row, col) in self.cell_labels:
            self.cell_labels[(row, col)].configure(text_color="black")
        for arrow_label in self.cell_arrows.get((row, col), []):
            arrow_label.configure(text_color="black")

        obj = cell["obj"]
        title_private = getattr(obj, "title_private", "Unknown")
        logic = obj.print_logic() if hasattr(obj, "print_logic") else ""
        inputs = obj.input_buffer.get("main", []) if hasattr(obj, "input_buffer") else []
        outputs = obj.output_buffer.get("main", []) if hasattr(obj, "output_buffer") else []
        directions = cell.get("output_directions", [])

        self.status_var.set(
            f"Cell ({row},{col}): {title_private} | logic={logic} | in={inputs} | out={outputs} | dirs={directions}"
        )

        self.edit_machine_button.place(relx=0.5, rely=0.75, anchor="center")

    def on_edit_machine(self):
        if self.selected_cell is None:
            return
        row, col = self.selected_cell
        self.status_var.set(f"Edit Machine clicked for cell ({row},{col})")

        self.root.update_idletasks()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()

        dialog_width = int(root_width * 0.25)
        dialog_height = int(root_height * 0.25)
        dialog_x = root_x + (root_width - dialog_width) // 2
        dialog_y = root_y + (root_height - dialog_height) // 2

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Machine")
        dialog.geometry(f"{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}")
        dialog.configure(background="white", highlightthickness=8, highlightbackground="black", highlightcolor="black")
        dialog.transient(self.root)
        dialog.grab_set()

        obj = self.game_map.get_cell(row, col)["obj"]

        if isinstance(obj, gu.Simple_Adder):
            self.build_simple_adder_dialog(dialog, obj)

    def build_simple_adder_dialog(self, dialog, obj):
        operand_var = tk.IntVar(value=obj.operand)

        operand_label = tk.Label(
            dialog,
            textvariable=operand_var,
            background="white",
            font=("Courier New", 24),
        )
        operand_label.pack(pady=20)

        button_frame = tk.Frame(dialog, background="white")
        button_frame.pack(pady=10)

        def increment():
            operand_var.set(operand_var.get() + 1)

        def decrement():
            operand_var.set(operand_var.get() - 1)

        minus_button = tk.Button(button_frame, text="-", command=decrement, width=5)
        minus_button.pack(side="left", padx=10)

        plus_button = tk.Button(button_frame, text="+", command=increment, width=5)
        plus_button.pack(side="left", padx=10)

        def update():
            obj.modify_object(operand_var.get())
            dialog.destroy()
            self.run_route()

        update_button = tk.Button(dialog, text="Update", command=update)
        update_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def show_tooltip(self, row, col):
        cell = self.game_map.get_cell(row, col)
        if cell["status"] == "empty":
            return

        obj = cell["obj"]
        title_private = getattr(obj, "title_private", "Unknown")
        logic = obj.print_logic() if hasattr(obj, "print_logic") else ""
        inputs = obj.input_buffer.get("main", []) if hasattr(obj, "input_buffer") else []
        outputs = obj.output_buffer.get("main", []) if hasattr(obj, "output_buffer") else []
        directions = cell.get("output_directions", [])
        text = f"Cell ({row},{col}): {title_private} | logic={logic} | in={inputs} | out={outputs} | dirs={directions}"

        self.hide_tooltip()

        box = self.cell_boxes.get((row, col))
        if box is None:
            return

        box_x = box.winfo_rootx() - self.top_frame.winfo_rootx() + 15
        box_y = box.winfo_rooty() - self.top_frame.winfo_rooty() + box.winfo_height() - 15

        button_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        border_color = button_color[1] if ctk.get_appearance_mode() == "Dark" else button_color[0]

        self.tooltip_window = tk.Label(
            self.top_frame,
            text=text,
            background="#2b2b2b",
            foreground="white",
            padx=8,
            pady=4,
            justify="left",
            anchor="n",
            wraplength=400,
            height=12,
            highlightthickness=6,
            highlightbackground=border_color,
            highlightcolor=border_color,
        )
        self.tooltip_window.place(x=box_x, y=box_y)
        self.tooltip_window.lift()

    def hide_tooltip(self):
        if self.tooltip_window is not None:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def refresh_board(self):
        self.build_board()
        self.status_var.set("(Nothing Selected)")
        self.edit_machine_button.place_forget()

    def run_route(self):
        try:
            self.game_map.run_simple_route()
            self.refresh_board()
            self.status_var.set("Route run completed")
        except Exception as exc:
            self.status_var.set(f"Run failed: {exc}")
