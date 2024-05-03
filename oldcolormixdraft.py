import tkinter as tk
class ColorPicker(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Pick a Color")
        self.callback = callback
        self.colors = ["#000000", "#FAFA33", "#0047AB", "#90EE90", "#FFFFFF", "#FF0000", "#006400", "#E97451", "#CB9D06", "#003153", "#E34234", "#FFA700"]

        self.create_buttons()

    def create_buttons(self):
        for color in self.colors:
            button = tk.Button(self, bg=color, width=3, command=lambda c=color: self.callback(c))
            button.pack(side=tk.LEFT, padx=5, pady=5)

class ColorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Color Chooser App")
        self.geometry("400x200")

        self.color1 = "#ff0000"  # Initial color for color1
        self.color2 = "#0000ff"  # Initial color for color2

        self.canvas = tk.Canvas(self, width=200, height=200)
        self.canvas.pack(side=tk.LEFT, padx=10)

        self.color1_circle = self.canvas.create_oval(50, 50, 150, 150, fill=self.color1, outline='black', width=2)
        self.color2_circle = self.canvas.create_oval(250, 50, 350, 150, fill=self.color2, outline='black', width=2)

        self.canvas.tag_bind(self.color1_circle, "<Button-1>", lambda event: self.pick_color1())
        self.canvas.tag_bind(self.color2_circle, "<Button-1>", lambda event: self.pick_color2())

    def pick_color1(self):
        self.show_color_dialog(self.set_color1)

    def pick_color2(self):
        self.show_color_dialog(self.set_color2)

    def set_color1(self, color):
        self.color1 = color
        self.canvas.itemconfig(self.color1_circle, fill=self.color1)

    def set_color2(self, color):
        self.color2 = color
        self.canvas.itemconfig(self.color2_circle, fill=self.color2)

    def show_color_dialog(self, callback):
        dialog = ColorPicker(self, callback)

if __name__ == "__main__":
    app = ColorApp()
    app.mainloop()
