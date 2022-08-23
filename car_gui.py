import tkinter as tk
import requests
from tkinter import messagebox
import datetime
from add_car_popup import AddCarPopup


API_DELETE_ENDPOINT = "http://127.0.0.1:5000/cars/"
API_ALL_ENDPOINT = "http://127.0.0.1:5000/cars/all"


class CarGui(tk.Frame):

    def __init__(self, master=None):
        """ Initializes the main frame """
        super().__init__(master)
        self.grid()
        self._create_widgets()

    def _create_widgets(self):
        """ Creates the main package management widgets """

        tk.Label(self, text="Cars List").grid(row=1, column=1)
        self._cars_listbox = tk.Listbox(self, width=100)
        self._cars_listbox.grid(row=2, column=0, columnspan=3)
        self._cars = []

        self._add = tk.Button(self, text="Add Car", command=self._add_car)
        self._add.grid(column=0, row=3)
        self._delete = tk.Button(self, text="Delete Car", command=self._delete_car)
        self._delete.grid(column=1, row=3)
        self._quit = tk.Button(self, text="Quit", command=self.master.destroy)
        self._quit.grid(column=2, row=3)

        self._get_cars()

    def _get_cars(self):
        """ Gets all car records from the backend """
        
        self._cars.clear()
        self._cars_listbox.delete(0, tk.END)


        response = requests.get(API_ALL_ENDPOINT)
        if response.status_code != 200:
            messagebox.showwarning("Warning", "Error getting cars from backend.")
            return

        for car in response.json():
            self._cars.append(car)
            self._cars_listbox.insert(tk.END, f"{car['make']} {car['model']}, {car['year']}, {car['price']} (Added: {car['timestamp']})")

            

    def _add_car(self):
        """ Add a car record to the backend """
		
        self._popup_win = tk.Toplevel()
        self._popup = AddCarPopup(self._popup_win, self._close_car_cb)

    def _close_car_cb(self):
        """ Closes the car popup """
        self._popup_win.destroy()
        self._get_cars()

    def _delete_car(self):
        """ Deletes a car record from the backend """
        selection = self._cars_listbox.curselection()

        if selection is None or len(selection) == 0:
            messagebox.showwarning("Warning", "No car selected to delete.")
            return

        car = self._cars[selection[0]]


        response = requests.delete(API_DELETE_ENDPOINT + str(car['id']))

        if response.status_code != 200:
            messagebox.showwarning("Warning", "Error deleting car from backend.")
            return

        self._get_cars()

root = tk.Tk()
app = CarGui(master=root)
app.mainloop()
