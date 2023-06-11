import openai
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import base64

# Set up the API key
openai.api_key = "YOUR_API_KEY"

# Create a function to perform named entity recognition
def perform_ner(input_text, text_widget, model="davinci", max_tokens=50, n=1, temperature=0.5):
    # Perform named entity recognition on the input text
    result = openai.Completion.create(
        engine=model,
        prompt="What entities are mentioned in the following text:\n\n" + input_text,
        max_tokens=max_tokens,
        n=n,
        stop=None,
        temperature=temperature
    )
    entities = result.choices[0].text

    # Display the named entities in a text widget
    text_widget.configure(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, entities)
    text_widget.configure(state="disabled")

# Create a function to perform image recognition
def perform_image_recognition(file_path, text_widget, model="image-alpha-001"):
    # Open the image file and resize it
    image = Image.open(file_path)
    image.thumbnail((256, 256))

    # Convert the image to base64
    with open(file_path, "rb") as file:
        image_base64 = base64.b64encode(file.read()).decode()

    # Perform image recognition on the image
    result = openai.Image.create(
        prompt="What is in this image?",
        image=image_base64,
        model=model,
        n=1,
        size="512x512"
    )
    concepts = result.output_text

    # Display the recognized concepts in a text widget
    text_widget.configure(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, concepts)
    text_widget.configure(state="disabled")

# Create a GUI window
root = tk.Tk()
root.title("Named Entity and Image Recognition")

# Create a label to explain the options
options_label = tk.Label(root, text="Choose an option to perform recognition:")
options_label.pack()

# Create a frame for the options
options_frame = tk.Frame(root)
options_frame.pack()

# Create a radio button to choose text option
input_type_var = tk.StringVar(value="text")
text_radio = tk.Radiobutton(options_frame, text="Text", variable=input_type_var, value="text")
text_radio.pack(side="left")

# Create a text box for the user to enter text
text_entry = tk.Text(options_frame, height=10, width=50)
text_entry.pack(side="left")

# Create a radio button to choose file option
file_radio = tk.Radiobutton(options_frame, text="File", variable=input_type_var, value="file")
file_radio.pack(side="left")

# Create a button to browse for a local file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Image files", "*.jpg;*.jpeg;*.png")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)
    if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
        # Display the image in a label widget
        image = Image.open(file_path)
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

file_button = tk.Button(options_frame, text="Browse", command=b
file_button = tk.Button(options_frame, text="Browse", command=browse_file)
file_button.pack(side="left")

# Create an entry to display the chosen file path
file_entry = tk.Entry(options_frame, width=50)
file_entry.pack(side="left")

# Create a button to perform the recognition
button = tk.Button(root, text="Perform Recognition")
button.pack()

# Create a label widget to display the image
image_label = tk.Label(root)
image_label.pack()

# Create a text widget to display the recognized entities or concepts
text_widget = tk.Text(root, state="disabled", wrap="word")
text_widget.pack()

# Bind the button to perform the selected recognition
def perform_recognition():
    input_type = input_type_var.get()
    if input_type == "text":
        input_text = text_entry.get("1.0", tk.END).strip()
        if input_text:
            perform_ner(input_text, text_widget, model=model_var.get(), max_tokens=max_tokens_var.get(),
                        n=n_var.get(), temperature=temperature_var.get())
    elif input_type == "file":
        file_path = file_entry.get()
        if file_path and os.path.isfile(file_path):
            if file_path.lower().endswith(".txt"):
                with open(file_path, "r") as file:
                    input_text = file.read().strip()
                perform_ner(input_text, text_widget, model=model_var.get(), max_tokens=max_tokens_var.get(),
                            n=n_var.get(), temperature=temperature_var.get())
            elif file_path.lower().endswith((".jpg", ".jpeg", ".png")):
                perform_image_recognition(file_path, text_widget, model=model_var.get())

button.config(command=perform_recognition)

# Create a frame for the configuration options
config_frame = tk.LabelFrame(root, text="Configuration Options")
config_frame.pack()

# Create a dropdown to choose the language model for NER
model_var = tk.StringVar(value="davinci")
model_label = tk.Label(config_frame, text="Choose a language model for NER:")
model_label.pack()
model_dropdown = tk.OptionMenu(config_frame, model_var, "davinci", "curie", "babbage", "ada")
model_dropdown.pack()

# Create a spinbox to set the maximum number of tokens for NER
max_tokens_var = tk.IntVar(value=50)
max_tokens_label = tk.Label(config_frame, text="Set the maximum number of tokens for NER:")
max_tokens_label.pack()
max_tokens_spinbox = tk.Spinbox(config_frame, from_=1, to=1000, increment=1, textvariable=max_tokens_var)
max_tokens_spinbox.pack()

# Create a spinbox to set the number of completions for NER
n_var = tk.IntVar(value=1)
n_label = tk.Label(config_frame, text="Set the number of completions for NER:")
n_label.pack()
n_spinbox = tk.Spinbox(config_frame, from_=1, to=10, increment=1, textvariable=n_var)
n_spinbox.pack()

# Create a scale to set the temperature for NER
temperature_var = tk.DoubleVar(value=0.5)
temperature_label = tk.Label(config_frame, text="Set the temperature for NER:")
temperature_label.pack()
temperature_scale = tk.Scale(config_frame, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=200,
                             variable=temperature_var)
temperature_scale.pack()

root.mainloop()