﻿import tkinter as tk
class StringChooser(tk.Frame):
    def __init__(self, root, name, defaultValue, OnChange, maxLength):
        super().__init__(root)
        self.value = tk.StringVar()
        self.value.set(defaultValue)
        self.maxLength = maxLength
        self.value.trace("w", lambda name, index, mode: self.changeValueText())
        self.OnChange = OnChange
        tk.Label(self,text=name).grid(row=0,columnspan=4)
        tk.Entry(self,textvariable=self.value).grid(row=1,columnspan=4)

    def changeValueText(self):
        success = len(self.value.get()) < self.maxLength
        if success:
            self.OnChange(self.value.get())
        else:
            self.value.set(self.value.get()[:maxLength])
        
    def changeValue(self, amount):
        success, value = tryGetFloat(self.value.get())
        if success:
            value += amount
            self.value.set(str(value))
