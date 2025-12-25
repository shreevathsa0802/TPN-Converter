import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from converter import TwoPortConverter

class TPNConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("TPN - Two-Port Converter")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e3a5f')
        
        self.converter = TwoPortConverter()
        self.param_type = tk.StringVar(value="Z")
        self.entries = {}
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="TPN Converter", 
                        font=('Arial', 24, 'bold'),
                        bg='#1e3a5f', fg='white')
        title.pack(pady=10)
        
        subtitle = tk.Label(self.root, text="Two-Port Network Parameter Converter",
                          font=('Arial', 12),
                          bg='#1e3a5f', fg='#a0c8ff')
        subtitle.pack()
        
        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Input Parameters",
                                   bg='#2c4a7a', fg='white',
                                   font=('Arial', 12, 'bold'))
        input_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Parameter Type Selection
        type_frame = tk.Frame(input_frame, bg='#2c4a7a')
        type_frame.pack(pady=10)
        
        tk.Label(type_frame, text="Select Type:", 
                bg='#2c4a7a', fg='white').pack(side='left', padx=5)
        
        for ptype in ['Z', 'Y', 'H', 'ABCD', 'G']:
            tk.Radiobutton(type_frame, text=ptype, variable=self.param_type,
                          value=ptype, bg='#2c4a7a', fg='white',
                          command=self.update_labels).pack(side='left', padx=5)
        
        # Matrix Input Grid
        matrix_frame = tk.Frame(input_frame, bg='#2c4a7a')
        matrix_frame.pack(pady=20)
        
        for i in range(2):
            for j in range(2):
                cell_frame = tk.Frame(matrix_frame, bg='#2c4a7a')
                cell_frame.grid(row=i, column=j, padx=20, pady=10)
                
                label = tk.Label(cell_frame, text=f"Z{i+1}{j+1}",
                                font=('Arial', 12, 'bold'),
                                bg='#2c4a7a', fg='#4a90e2')
                label.pack()
                
                # Real part
                tk.Label(cell_frame, text="Real:", 
                        bg='#2c4a7a', fg='white').pack()
                real_entry = tk.Entry(cell_frame, width=15,
                                     bg='#1a2d4a', fg='white')
                real_entry.pack()
                
                # Imaginary part
                tk.Label(cell_frame, text="Imag:", 
                        bg='#2c4a7a', fg='white').pack()
                imag_entry = tk.Entry(cell_frame, width=15,
                                     bg='#1a2d4a', fg='white')
                imag_entry.pack()
                
                self.entries[f'{i}{j}'] = {'real': real_entry, 'imag': imag_entry}
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg='#2c4a7a')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="CONVERT", command=self.convert,
                 bg='#3a7ca5', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="CLEAR", command=self.clear,
                 bg='#d9534f', fg='white', font=('Arial', 12),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="EXAMPLE", command=self.load_example,
                 bg='#5bc0de', fg='white', font=('Arial', 12),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        # Results Frame
        results_frame = tk.LabelFrame(self.root, text="Results",
                                     bg='#2c4a7a', fg='white',
                                     font=('Arial', 12, 'bold'))
        results_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     bg='#1a2d4a',
                                                     fg='white',
                                                     font=('Consolas', 11))
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def update_labels(self):
        ptype = self.param_type.get()
        for i in range(2):
            for j in range(2):
                cell_frame = self.entries[f'{i}{j}']['real'].master
                label = cell_frame.winfo_children()[0]
                label.config(text=f"{ptype}{i+1}{j+1}")
    
    def convert(self):
        try:
            # Get matrix from entries
            matrix = np.zeros((2, 2), dtype=complex)
            for i in range(2):
                for j in range(2):
                    real_val = float(self.entries[f'{i}{j}']['real'].get() or 0)
                    imag_val = float(self.entries[f'{i}{j}']['imag'].get() or 0)
                    matrix[i, j] = complex(real_val, imag_val)
            
            # Convert
            ptype = self.param_type.get()
            self.converter.set_parameters(ptype, matrix)
            
            # Display results
            results = f"{'='*50}\n"
            results += "CONVERSION RESULTS\n"
            results += f"{'='*50}\n\n"
            results += self.converter.get_formatted_results()
            
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert('1.0', results)
            
            messagebox.showinfo("Success", "Conversion completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def clear(self):
        for entry in self.entries.values():
            entry['real'].delete(0, tk.END)
            entry['imag'].delete(0, tk.END)
        self.results_text.delete('1.0', tk.END)
    
    def load_example(self):
        example = [[10+5j, 2-3j], [2+1j, 8-2j]]
        for i in range(2):
            for j in range(2):
                val = example[i][j]
                self.entries[f'{i}{j}']['real'].delete(0, tk.END)
                self.entries[f'{i}{j}']['imag'].delete(0, tk.END)
                self.entries[f'{i}{j}']['real'].insert(0, str(val.real))
                self.entries[f'{i}{j}']['imag'].insert(0, str(val.imag))

def main():
    root = tk.Tk()
    app = TPNConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
