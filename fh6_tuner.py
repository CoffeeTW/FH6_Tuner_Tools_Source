from __future__ import annotations
import customtkinter as ctk
from tkinter import messagebox
from fh6_core import TuneInput, calculate_tune, format_tune_text

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

class TunerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('FH6 車輛調校工具')
        self.geometry('1120x720')
        self.minsize(900, 620)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_left()
        self._build_right()

    def _build_left(self):
        p = ctk.CTkFrame(self, width=310, corner_radius=0)
        p.grid(row=0, column=0, sticky='nsew')
        p.grid_propagate(False)
        ctk.CTkLabel(p, text='FH6 TUNER', font=ctk.CTkFont(size=28, weight='bold')).pack(pady=(24, 18))
        self.drive = self._combo(p, '驅動方式', ['AWD','RWD','FWD'], 'AWD')
        self.goal = self._combo(p, '用途', ['公路平衡','公路極速','越野','拉力','甩尾'], '公路平衡')
        self.tire = self._combo(p, '輪胎', ['原廠','街道','運動','半熱熔','光頭胎','越野'], '半熱熔')
        self.weight = self._entry(p, '車重（kg）', '1400')
        self.front = self._entry(p, '前軸重量（%）', '55')
        self.power = self._entry(p, '馬力（hp）', '500')
        ctk.CTkButton(p, text='計算調校', height=46, command=self.calculate).pack(fill='x', padx=22, pady=(24,8))
        ctk.CTkButton(p, text='重設', fg_color='transparent', border_width=1, command=self.reset).pack(fill='x', padx=22)

    def _combo(self, parent, label, values, default):
        ctk.CTkLabel(parent, text=label, anchor='w').pack(fill='x', padx=22, pady=(8,3))
        w = ctk.CTkComboBox(parent, values=values)
        w.set(default)
        w.pack(fill='x', padx=22)
        return w

    def _entry(self, parent, label, default):
        ctk.CTkLabel(parent, text=label, anchor='w').pack(fill='x', padx=22, pady=(8,3))
        w = ctk.CTkEntry(parent)
        w.insert(0, default)
        w.pack(fill='x', padx=22)
        return w

    def _build_right(self):
        p = ctk.CTkFrame(self, corner_radius=0, fg_color='#0a0a0a')
        p.grid(row=0, column=1, sticky='nsew')
        p.grid_rowconfigure(1, weight=1)
        p.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(p, text='建議調校值', font=ctk.CTkFont(size=24, weight='bold'), anchor='w').grid(row=0,column=0,sticky='ew',padx=28,pady=(24,12))
        self.output = ctk.CTkTextbox(p, font=ctk.CTkFont(size=16), wrap='word')
        self.output.grid(row=1,column=0,sticky='nsew',padx=28,pady=(0,24))
        self.output.insert('1.0','輸入車輛資料後按「計算調校」。')

    def calculate(self):
        try:
            inp = TuneInput(self.drive.get(), float(self.weight.get()), float(self.front.get()), float(self.power.get()), self.goal.get(), self.tire.get())
            result = calculate_tune(inp)
        except ValueError:
            messagebox.showerror('輸入錯誤','車重、前軸重量與馬力必須是數字。')
            return
        self.output.delete('1.0','end')
        self.output.insert('1.0', format_tune_text(result))

    def reset(self):
        for e,v in [(self.weight,'1400'),(self.front,'55'),(self.power,'500')]:
            e.delete(0,'end')
            e.insert(0,v)
        self.drive.set('AWD')
        self.goal.set('公路平衡')
        self.tire.set('半熱熔')
        self.output.delete('1.0','end')
        self.output.insert('1.0','輸入車輛資料後按「計算調校」。')

if __name__ == '__main__':
    TunerApp().mainloop()
