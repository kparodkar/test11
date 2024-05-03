import tkinter as tk
import random
from tkinter import colorchooser
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import random
import numpy as np 
import matplotlib.pyplot as plt


def mix_colors(color1, color2, percent1, percent2):
    # Check if color strings are empty
    if not color1 or not color2:
        return "#000000"  # Return black if either color is not provided

    # Convert percentages to ratios
    total_percent = percent1 + percent2
    ratio1 = percent1 / total_percent
    ratio2 = percent2 / total_percent

    # Extract RGB values from color strings
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    # Interpolate RGB values based on the ratios
    r = int(r1 * ratio1 + r2 * ratio2)
    g = int(g1 * ratio1 + g2 * ratio2)
    b = int(b1 * ratio1 + b2 * ratio2)

    # Convert interpolated RGB values to hexadecimal format
    mixed_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

    return mixed_color

def pick_color1():
    # Open color chooser dialog and update color1 entry
    chosen_color = colorchooser.askcolor()[1]
    color1_entry.delete(0, tk.END)
    color1_entry.insert(0, chosen_color)
    update_color()

def pick_color2():
    # Open color chooser dialog and update color2 entry
    chosen_color = colorchooser.askcolor()[1]
    color2_entry.delete(0, tk.END)
    color2_entry.insert(0, chosen_color)
    update_color()

def use_mixed_color_as_color1():
    # Get the current mixed color and set it as color1
    mixed_color = mixed_color_label.cget("bg")
    color1_entry.delete(0, tk.END)
    color1_entry.insert(0, mixed_color)
    update_color()

def update_color(event=None):
    # Get the color mixing parameters from the entry fields
    color1 = color1_entry.get()
    color2 = color2_entry.get()
    percent1 = float(percent1_entry.get())
    percent2 = float(percent2_entry.get())

    # Mix the colors
    mixed_color = mix_colors(color1, color2, percent1, percent2)

    # Update the background color of the label to display the mixed color
    mixed_color_label.config(bg=mixed_color)

    # Update color boxes next to color labels
    color_box1.config(bg=color1)
    color_box2.config(bg=color2)

def generate_random_color():
    # Generate random RGB values
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Convert RGB to hexadecimal format
    random_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

    return random_color

def update_target_color():
    # Generate a random color
    random_color = generate_random_color()

    # Update the color box background color
    color_box.config(bg=random_color)

def choose_custom_color():
    # Open a color chooser dialog
    color = colorchooser.askcolor()[1]
    if color:
        canvas.config(bg=color)

def clear_canvas():
    # Clear the canvas by deleting all items
    canvas.delete("all")
    canvas.config(bg="white")

def submit_action():
    # Get the target color from the color box
    target_color = color_box.cget('bg')

    # Get the canvas color
    canvas_color = canvas.cget('bg')

    # Convert target color from hexadecimal to sRGBColor
    r_target, g_target, b_target = tuple(int(target_color[i:i+2], 16) for i in (1, 3, 5))
    color1_rgb = sRGBColor(r_target / 255, g_target / 255, b_target / 255)

    # Convert canvas color from hexadecimal to sRGBColor
    r_canvas, g_canvas, b_canvas = tuple(int(canvas_color[i:i+2], 16) for i in (1, 3, 5))
    color2_rgb = sRGBColor(r_canvas / 255, g_canvas / 255, b_canvas / 255)

    # Convert from sRGB to Lab Color Space
    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)

    # Calculate the Euclidean distance between LAB color coordinates
    delta_l = color1_lab.lab_l - color2_lab.lab_l
    delta_a = color1_lab.lab_a - color2_lab.lab_a
    delta_b = color1_lab.lab_b - color2_lab.lab_b
    color_distance = np.sqrt(delta_l**2 + delta_a**2 + delta_b**2)

    # Calculate color similarity percentage
    max_distance = np.sqrt(100**2 + 100**2 + 100**2)  # Maximum possible distance in LAB color space
    similarity_percentage = ((max_distance - color_distance) / max_distance) * 100

    # Plot the colors
    plt.figure(figsize=(8, 4))

    # Plot color 1 (target color)
    plt.subplot(1, 2, 1)
    plt.imshow([[color1_rgb.get_value_tuple()]], extent=(0, 1, 0, 1))
    plt.axis('off')

    # Plot color 2 (canvas color)
    plt.subplot(1, 2, 2)
    plt.imshow([[color2_rgb.get_value_tuple()]], extent=(0, 1, 0, 1))
    plt.axis('off')

    plt.tight_layout()

    # Print color distance and similarity percentage
    print("Color 1 (RGB):", color1_rgb.get_value_tuple())
    print("Color 2 (RGB):", color2_rgb.get_value_tuple())
    print("Color Distance:", color_distance)
    print("Color Similarity Percentage:", similarity_percentage)

    plt.show()

def update_canvas_color(event):
    # Update canvas color to the mixed color
    canvas.config(bg=mixed_color_label.cget("bg"))

# Create the main window
root = tk.Tk()
root.title("Color Mixing")

# Styling
root.configure(bg="#f0f0f0")  # Set background color

# Label for "Target color:"
target_label = tk.Label(root, text="Target color:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
target_label.grid(row=0, column=0, padx=10, pady=5)

# Color box to display the generated color
color_box = tk.Label(root, bg="white", width=10, height=2)
color_box.grid(row=1, column=0, padx=10, pady=5)

# Frame for canvas with border
canvas_frame = tk.Frame(root, bg="black", bd=2)
canvas_frame.grid(row=2, column=0, padx=10, pady=5)
# Canvas for drawing/painting
canvas = tk.Canvas(canvas_frame, bg="white", width=300, height=200)
canvas.pack()

# Button to manually update the color
update_button = tk.Button(root, text="Update Target Color", command=update_target_color, bg="#009688", fg="white", font=("Helvetica", 10, "bold"))
update_button.grid(row=3, column=0, padx=(100,0), pady=(5,0), sticky='n')

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_action, bg="#009688", fg="white", font=("Helvetica", 10, "bold"))
submit_button.grid(row=8, column=3,columnspan=2, padx=(130,0), pady=5)

# Button to choose custom color
choose_color_button = tk.Button(root, text="Choose Color", command=choose_custom_color, bg="#009688", fg="white", font=("Helvetica", 10, "bold"))
choose_color_button.grid(row=2, column=1, padx=10, pady=5, sticky='nw')

# Button to clear canvas
clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas, bg="#009688", fg="white", font=("Helvetica", 10, "bold"))
clear_button.grid(row=3, column=0, padx=10, pady=5, sticky='nw')

# Color mixing section
color1_label = tk.Label(root, text="Color 1:", bg="#f0f0f0", fg="#333", font=("Helvetica", 10))
color1_label.grid(row=2, column=1, padx=10, pady=(0,100), sticky="w")
color_box1 = tk.Label(root, bg="white", width=3, height=1, bd=1, relief="solid")
color_box1.grid(row=2, column=1, padx=(50,0), pady=(0,100))

color1_entry = tk.Entry(root)
color1_entry.grid(row=2, column=2, padx=10, pady=(0,100))
color1_button = tk.Button(root, text="Pick Color", command=pick_color1, bg="#009688", fg="white", font=("Helvetica", 10, "bold"))
color1_button.grid(row=2, column=3, padx=10, pady=(0,110))

color2_label = tk.Label(root, text="Color 2:", bg="#f0f0f0", fg="#333", font=("Helvetica", 10))
color2_label.grid(row=2, column=1, padx=10, pady=(0,40), sticky="w")
color_box2 = tk.Label(root, bg="white", width=3, height=1, bd=1, relief="solid")
color_box2.grid(row=2, column=1, padx=(50,0), pady=(0,40))

color2_entry = tk.Entry(root)
color2_entry.grid(row=2, column=2, padx=10, pady=(0,40))
color2_button = tk.Button(root, text="Pick Color", command=pick_color2, bg="#009688", fg="white", font=("Helvetica", 10, "bold"))
color2_button.grid(row=2, column=3, padx=10, pady=(0,40))

percent1_label = tk.Label(root, text="Percent 1:", bg="#f0f0f0", fg="#333", font=("Helvetica", 10))
percent1_label.grid(row=2, column=1, padx=(10,0), pady=(40,20), sticky="w")
percent1_entry = tk.Entry(root)
percent1_entry.grid(row=2, column=2, padx=(0,0), pady=(40,20))
percent1_entry.insert(0, "50")  # Default value for percent 1

percent2_label = tk.Label(root, text="Percent 2:", bg="#f0f0f0", fg="#333", font=("Helvetica", 10))
percent2_label.grid(row=2, column=1, padx=(10,0),pady=(100,20), sticky="w")
percent2_entry = tk.Entry(root)
percent2_entry.grid(row=2, column=2, padx=(0,0), pady=(100,20))
percent2_entry.insert(0, "50")  # Default value for percent 2

mixed_color_label = tk.Label(root, text="Mixed Color", width=20, height=5, bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
mixed_color_label.grid(row=3, column=1,columnspan=2, padx=10, pady=20)

update_button = tk.Button(root, text="Update mixed color", command=update_color, bg="#009688", fg="white", font=("Helvetica", 10, "bold"))
update_button.grid(row=8, column=2, columnspan=2,padx=(100,0), pady=5)

use_mixed_color_button = tk.Button(root, text="Use Mixed Color as Color1", command=use_mixed_color_as_color1, bg="#009688", fg="white", font=("Helvetica", 10, "bold"))
use_mixed_color_button.grid(row=8, column=1, columnspan=2, pady=5)

# Bind click event to mixed color label
mixed_color_label.bind("<Button-1>", update_canvas_color)

# Initially update the color
update_target_color()

root.mainloop()