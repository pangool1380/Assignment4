import tkinter as tk
from tkinter import messagebox
import requests

API_DELETE_ENDPOINT = "http://127.0.0.1:5000/cars/"

class DeleteCarPopup(tk.Frame):
    """ Popup Frame to Delete a Book """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        # The Delete Point Form Widgets
        tk.Label(self, text="Car ID:").grid(row=2, column=1)
        self._car_id = tk.Entry(self)
        self._car_id.grid(row=2, column=2)
        tk.Button(self, text="Submit", command=self._submit_cb).grid(row=3, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(row=3, column=2)

    def _submit_cb(self):
        """ Submit the Delete Book """
        data = {}
        data['car_id'] = self._car_id.get()

        response = requests.delete(API_DELETE_ENDPOINT + data['car_id'])
        if response.status_code == 200:
            messagebox.showinfo("Success", "Car Deleted")
            self._close_cb()
        else:
            messagebox.showerror("Error", "Car Not Deleted")
            self._close_cb()
