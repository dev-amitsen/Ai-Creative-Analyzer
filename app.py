import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import json
import re
import threading
from google import genai

# --- Configuration Management ---
CONFIG_FILE = "config.json"

def save_api_key(api_key):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": api_key}, f)

def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("api_key")
            except: return None
    return None

# --- UI Theme Settings ---
ctk.set_appearance_mode("light") 
MAIN_BLUE = "#0069d9"
HOVER_BLUE = "#0056b3"
CORNER_RADIUS = 6 

# --- Setup Popup Window ---
class ApiKeyPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("System Configuration")
        self.geometry("420x340")
        self.attributes("-topmost", True)
        self.grab_set() 
        
        ctk.CTkLabel(self, text="Ai Creative Analyzer", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 10))
        ctk.CTkLabel(self, text="Please enter your Gemini API Key:", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=5)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter API Key...", width=320, height=40, corner_radius=CORNER_RADIUS, show="*")
        self.entry.pack(pady=15)
        self.entry.focus_set()

        self.save_btn = ctk.CTkButton(self, text="Verify Credentials", font=ctk.CTkFont(size=14, weight="bold"), fg_color=MAIN_BLUE, hover_color=HOVER_BLUE, height=45, corner_radius=CORNER_RADIUS, command=self.start_verification)
        self.save_btn.pack(pady=20)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_verification(self):
        key = self.entry.get().strip()
        if not key: return
        self.save_btn.configure(state="disabled", text="Verifying...")
        threading.Thread(target=self.verify_key, args=(key,), daemon=True).start()

    def verify_key(self, key):
        try:
            test_client = genai.Client(api_key=key)
            test_client.models.list(config={'page_size': 1})
            save_api_key(key)
            self.after(0, lambda: self.master.finalize_setup(key))
            self.after(0, self.destroy)
        except:
            self.after(0, lambda: messagebox.showerror("Error", "Invalid API Key. Please try again."))
            self.after(0, lambda: self.save_btn.configure(state="normal", text="Verify Credentials"))

    def on_closing(self): self.master.destroy()

# --- Main Application ---
class CreativeAnalyzer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ai Creative Analyzer")
        self.geometry("1150x800")
        self.image_path = None
        self.client = None

        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()
        self.check_api_key()

    def check_api_key(self):
        key = load_api_key()
        if not key:
            self.withdraw()
            self.after(100, lambda: ApiKeyPopup(self))
        else: self.finalize_setup(key)

    def finalize_setup(self, key):
        self.client = genai.Client(api_key=key)
        self.deiconify()

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=350, corner_radius=0, fg_color="#f8f9fa")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0)

        ctk.CTkLabel(self.sidebar, text="Ai Creative Analyzer", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(40, 20))
        
        self.upload_btn = ctk.CTkButton(self.sidebar, text="Select Image", font=ctk.CTkFont(size=14, weight="bold"), fg_color=MAIN_BLUE, hover_color=HOVER_BLUE, corner_radius=CORNER_RADIUS, height=40, command=self.upload_image)
        self.upload_btn.pack(pady=10, padx=40, fill="x")

        self.preview_label = ctk.CTkLabel(self.sidebar, text="No Preview Available", width=280, height=280, fg_color="#e9ecef", corner_radius=CORNER_RADIUS)
        self.preview_label.pack(pady=20, padx=30)

        self.analyze_btn = ctk.CTkButton(self.sidebar, text="Run Analysis", font=ctk.CTkFont(size=14, weight="bold"), state="disabled", fg_color="#b0b0b0", hover_color="#b0b0b0", text_color="white", height=45, corner_radius=CORNER_RADIUS, command=self.start_analysis_thread)
        self.analyze_btn.pack(pady=10, padx=40, fill="x")

        self.progress = ctk.CTkProgressBar(self.sidebar, orientation="horizontal", mode="indeterminate", height=10)
        
        self.reset_btn = ctk.CTkLabel(self.sidebar, text="Reset API Key", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray", cursor="hand2")
        self.reset_btn.pack(side="bottom", pady=30)
        self.reset_btn.bind("<Enter>", lambda e: self.reset_btn.configure(font=ctk.CTkFont(size=12, weight="bold", underline=True)))
        self.reset_btn.bind("<Leave>", lambda e: self.reset_btn.configure(font=ctk.CTkFont(size=12, weight="bold", underline=False)))
        self.reset_btn.bind("<Button-1>", lambda e: self.reset_key())

        # Content Area
        self.content_area = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=0)

        self.status_label = ctk.CTkLabel(self.content_area, text="System Ready", font=ctk.CTkFont(size=13, weight="bold"), text_color="#6c757d")
        self.status_label.pack(pady=(30, 5))

        self.results_area = ctk.CTkTextbox(self.content_area, font=ctk.CTkFont(size=15), corner_radius=CORNER_RADIUS, border_width=1, border_color="#dee2e6")
        self.results_area.pack(pady=20, padx=40, fill="both", expand=True)

        self.copy_btn = ctk.CTkButton(self.content_area, text="Copy Report", font=ctk.CTkFont(size=13, weight="bold"), fg_color="transparent", border_width=1, border_color=MAIN_BLUE, text_color=MAIN_BLUE, hover_color="#eef6ff", corner_radius=CORNER_RADIUS, command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=(0, 40))

    def upload_image(self):
        file = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if file:
            self.image_path = file
            img_data = Image.open(file)
            self.ctk_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(280, 280))
            self.preview_label.configure(image=self.ctk_img, text="")
            self.analyze_btn.configure(state="normal", fg_color="#10b981", hover_color="#059669")

    def start_analysis_thread(self):
        self.status_label.configure(text="ANALYSIS IN PROGRESS...")
        self.analyze_btn.configure(state="disabled")
        self.results_area.delete("1.0", tk.END)
        self.progress.pack(pady=10, padx=40, fill="x")
        self.progress.start()
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        try:
            img = Image.open(self.image_path)
            prompt = """Analyze this social media post. Respond strictly in JSON:
            {"spelling and grammar": "accuracy feedback", "design": "layout feedback", "hierarchy": "visual flow feedback", "engagement": "suitability feedback", "suggestions": ["s1", "s2", "s3"]}"""
            
            response = self.client.models.generate_content(model="gemini-2.5-flash", contents=[prompt, img])
            data = json.loads(re.sub(r'```json|```', '', response.text).strip())
            
            output = f"TEXT AUDIT:\n{data['spelling and grammar']}\n\nDESIGN COMPOSITION:\n{data['design']}\n\n"
            output += f"VISUAL FLOW:\n{data['hierarchy']}\n\nPLATFORM POTENTIAL:\n{data['engagement']}\n\n"
            output += "STRATEGIC SUGGESTIONS:\n" + "\n".join([f"  • {s}" for s in data['suggestions']])

            self.after(0, lambda: self.results_area.insert("1.0", output))
            self.after(0, lambda: self.status_label.configure(text="ANALYSIS SUCCESSFUL"))
            
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                # Specific friendly message for Quota errors
                quota_msg = "Rate Limit Reached: You're using the free tier too fast! Please wait 30-60 seconds before trying again."
                self.after(0, lambda: messagebox.showinfo("System Cooldown", quota_msg))
                self.after(0, lambda: self.status_label.configure(text="COOLDOWN REQUIRED"))
            else:
                self.after(0, lambda msg=err_msg: messagebox.showerror("Error", f"Process Failed: {msg}"))
                self.after(0, lambda: self.status_label.configure(text="SYSTEM ERROR"))
        finally:
            self.after(0, self.stop_progress)

    def stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.analyze_btn.configure(state="normal", fg_color="#10b981", hover_color="#059669")

    def copy_to_clipboard(self):
        content = self.results_area.get("1.0", tk.END).strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            messagebox.showinfo("System", "Report copied to clipboard.")

    def reset_key(self):
        if messagebox.askyesno("Reset", "Delete configuration and restart?"):
            if os.path.exists(CONFIG_FILE): os.remove(CONFIG_FILE)
            self.destroy()
            os.system('python "' + __file__ + '"')

if __name__ == "__main__":
    CreativeAnalyzer().mainloop()