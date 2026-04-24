import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import threading
from processor import enhance_image

# Set appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ImageEnhancerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Image Enhancer & Watermark Remover")
        self.geometry("1100x800")

        # Variables
        self.input_dir = tk.StringVar(value=os.path.abspath("originals"))
        self.output_dir = tk.StringVar(value=os.path.abspath("enhanced"))
        self.remove_watermark = tk.BooleanVar(value=True)
        self.removal_method = tk.StringVar(value="crop")
        self.image_list = []
        self.selected_image = None
        self.preview_img = None

        self.setup_gui()
        self.load_images()

    def setup_gui(self):
        # Configure grid layout (1x2)
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main Preview
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Image Enhancer", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input Dir Selection
        self.btn_input = ctk.CTkButton(self.sidebar_frame, text="Select Input Folder", command=self.select_input_dir)
        self.btn_input.grid(row=1, column=0, padx=20, pady=10)

        self.lbl_input = ctk.CTkLabel(self.sidebar_frame, textvariable=self.input_dir, wraplength=200, font=ctk.CTkFont(size=10))
        self.lbl_input.grid(row=2, column=0, padx=20, pady=0)

        # Image Listbox
        self.image_scrollable_frame = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="Originals")
        self.image_scrollable_frame.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
        self.image_buttons = []

        # Options Frame
        self.options_frame = ctk.CTkFrame(self.sidebar_frame)
        self.options_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        self.check_watermark = ctk.CTkCheckBox(self.options_frame, text="Remove Watermark", variable=self.remove_watermark)
        self.check_watermark.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.lbl_method = ctk.CTkLabel(self.options_frame, text="Method:", font=ctk.CTkFont(size=12))
        self.lbl_method.grid(row=1, column=0, padx=10, pady=0, sticky="w")

        self.radio_crop = ctk.CTkRadioButton(self.options_frame, text="Crop (Best)", variable=self.removal_method, value="crop")
        self.radio_crop.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.radio_inpaint = ctk.CTkRadioButton(self.options_frame, text="Inpaint", variable=self.removal_method, value="inpaint")
        self.radio_inpaint.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        # Output Dir Selection
        self.btn_output = ctk.CTkButton(self.sidebar_frame, text="Select Output Folder", command=self.select_output_dir)
        self.btn_output.grid(row=6, column=0, padx=20, pady=10)

        # --- Main Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Preview Image
        self.preview_label = ctk.CTkLabel(self.main_frame, text="Select an image to preview", fg_color="#1a1a1a")
        self.preview_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Controls at Bottom
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.control_frame.grid_columnconfigure(0, weight=1)

        self.btn_enhance = ctk.CTkButton(self.control_frame, text="Enhance & Upscale (4K)", command=self.start_enhancement, 
                                          height=40, font=ctk.CTkFont(size=14, weight="bold"), fg_color="#2b719e")
        self.btn_enhance.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self.control_frame, text="Ready", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, padx=20, pady=(0, 10))

    def select_input_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.input_dir.set(dir_path)
            self.load_images()

    def select_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.set(dir_path)

    def load_images(self):
        for btn in self.image_buttons:
            btn.destroy()
        self.image_buttons = []

        path = self.input_dir.get()
        if not os.path.exists(path):
            return

        files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        files.sort()
        self.image_list = files

        for i, filename in enumerate(files):
            btn = ctk.CTkButton(self.image_scrollable_frame, text=filename, anchor="w", fg_color="transparent", 
                                text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                command=lambda f=filename: self.show_preview(f))
            btn.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            self.image_buttons.append(btn)

        if files:
            self.show_preview(files[0])

    def show_preview(self, filename):
        self.selected_image = filename
        img_path = os.path.join(self.input_dir.get(), filename)
        
        # Load for preview
        img = Image.open(img_path)
        
        # Calculate size for preview box
        preview_w = self.preview_label.winfo_width()
        preview_h = self.preview_label.winfo_height()
        if preview_w < 100: preview_w = 600
        if preview_h < 100: preview_h = 400

        # We don't need to manually resize the PIL image for CTkImage if we specify the size
        # but let's keep the aspect ratio logic
        w, h = img.size
        ratio = min(preview_w/w, preview_h/h)
        new_size = (int(w * ratio), int(h * ratio))

        # Use CTkImage for better rendering in CustomTkinter
        self.preview_ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=new_size)
        
        self.preview_label.configure(image=self.preview_ctk_img, text="")
        self.status_label.configure(text=f"Selected: {filename}")

    def start_enhancement(self):
        if not self.selected_image:
            messagebox.showwarning("Warning", "No image selected!")
            return

        threading.Thread(target=self.process_image, daemon=True).start()

    def process_image(self):
        try:
            self.btn_enhance.configure(state="disabled", text="Processing...")
            self.status_label.configure(text=f"Enhancing {self.selected_image}...")

            input_path = os.path.join(self.input_dir.get(), self.selected_image)
            output_filename = f"enhanced_{self.selected_image}"
            output_path = os.path.join(self.output_dir.get(), output_filename)

            enhance_image(
                input_path, 
                output_path, 
                remove_watermark=self.remove_watermark.get(),
                removal_method=self.removal_method.get()
            )

            self.after(0, lambda: self.finish_enhancement(output_path))
        except Exception as e:
            self.after(0, lambda e=e: messagebox.showerror("Error", f"Enhancement failed: {str(e)}"))
            self.after(0, lambda: self.btn_enhance.configure(state="normal", text="Enhance & Upscale (4K)"))

    def finish_enhancement(self, output_path):
        self.btn_enhance.configure(state="normal", text="Enhance & Upscale (4K)")
        self.status_label.configure(text=f"Success! Saved to {os.path.basename(output_path)}")
        messagebox.showinfo("Success", f"Image enhanced and saved to:\n{output_path}")

if __name__ == "__main__":
    app = ImageEnhancerApp()
    app.mainloop()
