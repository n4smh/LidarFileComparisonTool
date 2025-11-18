import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from tkinter.ttk import *
from pathlib import Path
from tkcalendar import DateEntry
from datetime import datetime, time, timedelta
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import numpy as np


class AppABC(tk.Frame):

    def __init__(self, main_window):

        super().__init__(main_window)

        self.valid_dfs = False
        self.valid_selected_date_range = True

        self.r_squared = ""
        self.date_range_start = datetime.today()
        self.date_range_end = datetime.today()

        self.date_format_string = "%Y-%m-%d"
        self.datetime_format_string = "%Y-%m-%d %H:%M"
        self.intersection_df = pd.DataFrame()

        self.temp_path = Path.joinpath(Path.cwd(), "temp_data")
        self.create_temp_dir(self.temp_path)

        self.main_window = main_window
        self.main_window.title("App")

        self.reference_frame = Frame(padding=10)
        self.target_frame = Frame(padding=10)
        self.date_frame = Frame(padding=10)

        self.data_vals = {
            "reference": {
                "file_path": "",
                "temp_file_path": "",
                "selected_height": StringVar(master=self.reference_frame),
                "choices": ["Select Option"],
                "created_info": "",
                "latitude": "",
                "longitude": "",
                "elevation": "",
                "calm_threshold": "",
                "included_flags": "",
                "excluded_flags": "",
                "df": pd.DataFrame(),
                "min": "",
                "max": "",
            },
            "target": {
                "file_path": "",
                "temp_file_path": "",
                "selected_height": StringVar(master=self.target_frame),
                "choices": ["Select Option"],
                "created_info": "",
                "latitude": "",
                "longitude": "",
                "elevation": "",
                "calm_threshold": "",
                "included_flags": "",
                "excluded_flags": "",
                "df": pd.DataFrame(),
                "min": "",
                "max": "",
            },
        }

        self.data_vals["reference"]["selected_height"].set(
            self.data_vals["reference"]["choices"][0]
        )

        self.data_vals["target"]["selected_height"].set(
            self.data_vals["target"]["choices"][0]
        )

    def create_ui(self):

        self.ui_vals = {
            "reference": {
                "select_label": Label(
                    master=self.reference_frame, text="Reference file: "
                ),
                "select_button": Button(
                    master=self.reference_frame,
                    text="Select",
                    command=lambda: self.select_file("reference"),
                ),
                "file_name_label": Label(
                    master=self.reference_frame,
                    text="File name: ",
                ),
                "file_name_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "select_height": OptionMenu(
                    self.reference_frame,
                    self.data_vals["reference"]["selected_height"],
                    *self.data_vals["reference"]["choices"],
                    command=lambda value: self.clear_plot_details()
                ),
                "created_info_label": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "created_info_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "latitude_label": Label(
                    master=self.reference_frame,
                    text="Latitude: ",
                ),
                "latitude_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "longitude_label": Label(
                    master=self.reference_frame,
                    text="Longitude: ",
                ),
                "longitude_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "elevation_label": Label(
                    master=self.reference_frame,
                    text="Elevation: ",
                ),
                "elevation_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "calm_threshold_label": Label(
                    master=self.reference_frame,
                    text="Calm threshold: ",
                ),
                "calm_threshold_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "included_flags_label": Label(
                    master=self.reference_frame,
                    text="Included flags: ",
                ),
                "included_flags_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "excluded_flags_label": Label(
                    master=self.reference_frame,
                    text="Excluded flags: ",
                ),
                "excluded_flags_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "min_label": Label(
                    master=self.reference_frame,
                    text="Min value: ",
                ),
                "min_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
                "max_label": Label(
                    master=self.reference_frame,
                    text="Max value:",
                ),
                "max_value": Label(
                    master=self.reference_frame,
                    text="",
                ),
            },
            "target": {
                "select_label": Label(master=self.target_frame, text="Target file: "),
                "select_button": Button(
                    master=self.target_frame,
                    text="Select",
                    command=lambda: self.select_file("target"),
                ),
                "file_name_label": Label(
                    master=self.target_frame,
                    text="File name: ",
                ),
                "file_name_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "select_height": OptionMenu(
                    self.target_frame,
                    self.data_vals["target"]["selected_height"],
                    *self.data_vals["target"]["choices"],
                    command=lambda value: self.clear_plot_details()
                ),
                "created_info_label": Label(
                    master=self.target_frame,
                    text="",
                ),
                "created_info_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "latitude_label": Label(
                    master=self.target_frame,
                    text="Latitude: ",
                ),
                "latitude_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "longitude_label": Label(
                    master=self.target_frame,
                    text="Longitude: ",
                ),
                "longitude_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "elevation_label": Label(
                    master=self.target_frame,
                    text="Elevation: ",
                ),
                "elevation_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "calm_threshold_label": Label(
                    master=self.target_frame,
                    text="Calm threshold: ",
                ),
                "calm_threshold_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "included_flags_label": Label(
                    master=self.target_frame,
                    text="Included flags: ",
                ),
                "included_flags_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "excluded_flags_label": Label(
                    master=self.target_frame,
                    text="Excluded flags: ",
                ),
                "excluded_flags_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "min_label": Label(
                    master=self.target_frame,
                    text="Min value: ",
                ),
                "min_value": Label(
                    master=self.target_frame,
                    text="",
                ),
                "max_label": Label(
                    master=self.target_frame,
                    text="Max value:",
                ),
                "max_value": Label(
                    master=self.target_frame,
                    text="",
                ),
            },
        }

        self.cal_start_value = datetime.today().date()
        self.cal_start_label = Label(
            master=self.date_frame,
            text="Start date: ",
        )
        self.cal_start = DateEntry(
            self.date_frame,
            date_pattern="yyyy-mm-dd",
            selectmode="day",
            firstweekday="sunday",
            mindate=self.date_range_start,
            maxdate=self.date_range_end,
            state="disabled",
        )
        self.cal_start.bind("<<DateEntrySelected>>", self.cal_selected)

        self.cal_end_value = datetime.today().date()
        self.cal_end_label = Label(
            master=self.date_frame,
            text="End date: ",
        )
        self.cal_end = DateEntry(
            self.date_frame,
            date_pattern="yyyy-mm-dd",
            selectmode="day",
            firstweekday="sunday",
            mindate=self.date_range_start,
            maxdate=self.date_range_end,
            state="disabled",
        )
        self.cal_end.bind("<<DateEntrySelected>>", self.cal_selected)

        self.plot_button = Button(
            master=self.date_frame,
            text="Plot",
            command=lambda: self.plot(),
        )

        self.r_squared_label = Label(
            master=self.date_frame,
            text="R^2: ",
        )
        self.r_squared_value = Label(
            master=self.date_frame,
            text="",
        )

        self.reference_frame.grid(row=1, column=1, sticky="w")
        self.target_frame.grid(row=1, column=2, sticky="w")
        self.date_frame.grid(row=2, column=1, sticky="w")

        # reference frame
        self.ui_vals["reference"]["select_label"].grid(row=1, column=1, sticky="w")
        self.ui_vals["reference"]["select_button"].grid(row=1, column=2, sticky="w")
        self.ui_vals["reference"]["file_name_label"].grid(row=2, column=1, sticky="w")
        self.ui_vals["reference"]["file_name_value"].grid(row=2, column=2, sticky="w")
        self.ui_vals["reference"]["select_height"].grid(
            row=3, column=2, sticky="w", pady="5"
        )
        self.ui_vals["reference"]["created_info_label"].grid(
            row=4, column=1, sticky="w", pady="2"
        )
        self.ui_vals["reference"]["created_info_value"].grid(
            row=4, column=2, sticky="w", pady="2"
        )
        self.ui_vals["reference"]["latitude_label"].grid(row=5, column=1, sticky="w")
        self.ui_vals["reference"]["latitude_value"].grid(row=5, column=2, sticky="w")
        self.ui_vals["reference"]["longitude_label"].grid(row=6, column=1, sticky="w")
        self.ui_vals["reference"]["longitude_value"].grid(row=6, column=2, sticky="w")
        self.ui_vals["reference"]["elevation_label"].grid(row=7, column=1, sticky="w")
        self.ui_vals["reference"]["elevation_value"].grid(row=7, column=2, sticky="w")
        self.ui_vals["reference"]["calm_threshold_label"].grid(
            row=8, column=1, sticky="w"
        )
        self.ui_vals["reference"]["calm_threshold_value"].grid(
            row=8, column=2, sticky="w"
        )
        self.ui_vals["reference"]["included_flags_label"].grid(
            row=9, column=1, sticky="w"
        )
        self.ui_vals["reference"]["included_flags_value"].grid(
            row=9, column=2, sticky="w"
        )
        self.ui_vals["reference"]["excluded_flags_label"].grid(
            row=10, column=1, sticky="w"
        )
        self.ui_vals["reference"]["excluded_flags_value"].grid(
            row=10, column=2, sticky="w"
        )
        self.ui_vals["reference"]["min_label"].grid(row=11, column=1, sticky="w")
        self.ui_vals["reference"]["min_value"].grid(row=11, column=2, sticky="w")
        self.ui_vals["reference"]["max_label"].grid(row=12, column=1, sticky="w")
        self.ui_vals["reference"]["max_value"].grid(row=12, column=2, sticky="w")

        # target frame
        self.ui_vals["target"]["select_label"].grid(row=1, column=1, sticky="w")
        self.ui_vals["target"]["select_button"].grid(row=1, column=2, sticky="w")
        self.ui_vals["target"]["file_name_label"].grid(row=2, column=1, sticky="w")
        self.ui_vals["target"]["file_name_value"].grid(row=2, column=2, sticky="w")
        self.ui_vals["target"]["select_height"].grid(
            row=3, column=2, sticky="w", pady="5"
        )
        self.ui_vals["target"]["created_info_label"].grid(
            row=4, column=1, sticky="w", pady="2"
        )
        self.ui_vals["target"]["created_info_value"].grid(
            row=4, column=2, sticky="w", pady="2"
        )
        self.ui_vals["target"]["latitude_label"].grid(row=5, column=1, sticky="w")
        self.ui_vals["target"]["latitude_value"].grid(row=5, column=2, sticky="w")
        self.ui_vals["target"]["longitude_label"].grid(row=6, column=1, sticky="w")
        self.ui_vals["target"]["longitude_value"].grid(row=6, column=2, sticky="w")
        self.ui_vals["target"]["elevation_label"].grid(row=7, column=1, sticky="w")
        self.ui_vals["target"]["elevation_value"].grid(row=7, column=2, sticky="w")
        self.ui_vals["target"]["calm_threshold_label"].grid(row=8, column=1, sticky="w")
        self.ui_vals["target"]["calm_threshold_value"].grid(row=8, column=2, sticky="w")
        self.ui_vals["target"]["included_flags_label"].grid(row=9, column=1, sticky="w")
        self.ui_vals["target"]["included_flags_value"].grid(row=9, column=2, sticky="w")
        self.ui_vals["target"]["excluded_flags_label"].grid(
            row=10, column=1, sticky="w"
        )
        self.ui_vals["target"]["excluded_flags_value"].grid(
            row=10, column=2, sticky="w"
        )
        self.ui_vals["target"]["min_label"].grid(row=11, column=1, sticky="w")
        self.ui_vals["target"]["min_value"].grid(row=11, column=2, sticky="w")
        self.ui_vals["target"]["max_label"].grid(row=12, column=1, sticky="w")
        self.ui_vals["target"]["max_value"].grid(row=12, column=2, sticky="w")

        # data frame
        self.cal_start_label.grid(row=1, column=1, sticky="w", pady="2")
        self.cal_start.grid(row=1, column=2, sticky="w", pady="2")
        self.cal_end_label.grid(row=2, column=1, sticky="w", pady="2")
        self.cal_end.grid(row=2, column=2, sticky="w", pady="2")
        self.plot_button.grid(row=1, column=3, sticky="w", pady="2")
        self.r_squared_label.grid(row=3, column=1, sticky="w", pady="2")
        self.r_squared_value.grid(row=3, column=2, sticky="w", pady="2")

    def select_file(self, type):

        file_path = filedialog.askopenfilename(title="Select {} file".format(type))

        if not file_path or not self.parse_file_data(type, file_path):
            messagebox.showerror("Error", "Select valid {} file".format(type))
            self.clear_data(type)

        self.update_ui(type)

    def clear_data(self, type):
        self.data_vals[type]["file_path"] = ""
        self.data_vals[type]["temp_file_path"] = ""
        self.data_vals[type]["created_info"] = ""
        self.data_vals[type]["latitude"] = ""
        self.data_vals[type]["longitude"] = ""
        self.data_vals[type]["elevation"] = ""
        self.data_vals[type]["calm_threshold"] = ""
        self.data_vals[type]["included_flags"] = ""
        self.data_vals[type]["excluded_flags"] = ""

        self.clear_plot_details()

        self.data_vals[type]["df"] = pd.DataFrame()
        self.intersection_df = pd.DataFrame()

        self.data_vals[type]["choices"] = ["Select Option"]
        self.data_vals[type]["selected_height"].set(self.data_vals[type]["choices"][0])

        self.date_range_start = datetime.today()
        self.date_range_end = datetime.today()

        self.valid_dfs = False

    def clear_plot_details(self):
        self.data_vals["reference"]["min"] = ""
        self.data_vals["reference"]["max"] = ""

        self.data_vals["target"]["min"] = ""
        self.data_vals["target"]["max"] = ""

        self.r_squared = ""

        self.update_ui_plot_details()

    def update_ui(self, type):

        self.ui_vals[type]["file_name_value"].config(
            text=self.file_name_from_path(self.data_vals[type]["file_path"])
        )
        self.ui_vals[type]["created_info_value"].config(
            text=self.data_vals[type]["created_info"]
        )
        self.ui_vals[type]["latitude_value"].config(
            text=self.data_vals[type]["latitude"]
        )
        self.ui_vals[type]["longitude_value"].config(
            text=self.data_vals[type]["longitude"]
        )
        self.ui_vals[type]["elevation_value"].config(
            text=self.data_vals[type]["elevation"]
        )
        self.ui_vals[type]["calm_threshold_value"].config(
            text=self.data_vals[type]["calm_threshold"]
        )
        self.ui_vals[type]["included_flags_value"].config(
            text=self.data_vals[type]["included_flags"]
        )
        self.ui_vals[type]["excluded_flags_value"].config(
            text=self.data_vals[type]["excluded_flags"]
        )

        self.ui_vals[type]["select_height"]["menu"].delete(0, "end")
        for choice in self.data_vals[type]["choices"]:
            self.ui_vals[type]["select_height"]["menu"].add_command(
                label=choice,
                command=tk._setit(
                    self.data_vals[type]["selected_height"],
                    choice,
                    lambda value: self.clear_plot_details(),
                ),
            )

        self.validate_date_range()

    def update_ui_plot_details(self):
        self.ui_vals["reference"]["min_value"].config(
            text=self.data_vals["reference"]["min"]
        )
        self.ui_vals["reference"]["max_value"].config(
            text=self.data_vals["reference"]["max"]
        )

        self.ui_vals["target"]["min_value"].config(text=self.data_vals["target"]["min"])
        self.ui_vals["target"]["max_value"].config(text=self.data_vals["target"]["max"])

        self.r_squared_value.config(text=self.r_squared)

    def validate_date_range(self):
        if self.date_range_start > self.date_range_end:
            self.valid_selected_date_range = False

            messagebox.showerror(
                "Error",
                "Invalid date range.\n\nStart: {}\n\nEnd: {}\n\nResetting to today.".format(
                    self.date_range_start, self.date_range_end
                ),
            )

            self.date_range_start = datetime.today()
            self.date_range_end = datetime.today()

        else:
            self.valid_selected_date_range = True

        self.cal_start.config(
            mindate=self.date_range_start,
            maxdate=self.date_range_end,
            state=(
                "normal"
                if self.valid_selected_date_range and self.valid_dfs
                else "disabled"
            ),
        )

        self.cal_end.config(
            mindate=self.date_range_start,
            maxdate=self.date_range_end,
            state=(
                "normal"
                if self.valid_selected_date_range and self.valid_dfs
                else "disabled"
            ),
        )

        self.cal_start.set_date(self.date_range_start)
        self.cal_end.set_date(self.date_range_end)

    def validate_selected_date_range(self):
        if self.cal_start_value > self.cal_end_value:
            self.valid_selected_date_range = False
            messagebox.showerror(
                "Error",
                "Invalid selected date range.\n\nStart: {}\n\nEnd: {}".format(
                    self.cal_start_value, self.cal_end_value
                ),
            )
        else:
            self.valid_selected_date_range = True

    def cal_selected(self, event):
        self.cal_start_value = self.cal_start.get_date()
        self.cal_end_value = self.cal_end.get_date()

        self.validate_selected_date_range()

        self.clear_plot_details()

    def file_name_from_path(self, file_path):
        filename_with_ext = Path(file_path).name
        filename_chopped = filename_with_ext[:30]

        if filename_with_ext != filename_chopped:
            filename_chopped += "..."

        return filename_chopped

    def create_temp_dir(self, path):

        if Path.is_dir(path):
            self.rmdir(path)

        Path.mkdir(path)

    def rmdir(self, directory):
        directory = Path(directory)
        for item in directory.iterdir():
            if item.is_dir():
                self.rmdir(item)
            else:
                item.unlink()
        directory.rmdir()

    def parse_file_data(self, type, source_path):
        method_response = True

        try:
            self.data_vals[type]["file_path"] = source_path

            temp_file_path = Path.joinpath(self.temp_path, Path(source_path).name)
            self.data_vals[type]["temp_file_path"] = temp_file_path

            input_file = open(source_path, "r", encoding="windows-1252")
            output_file = open(temp_file_path, "w", encoding="windows-1252")

            self.data_vals[type]["created_info"] = input_file.readline().strip()

            input_file.readline()

            self.data_vals[type]["latitude"] = (
                input_file.readline().strip().replace("Latitude =", "").strip()
            )
            self.data_vals[type]["longitude"] = (
                input_file.readline().strip().replace("Longitude =", "").strip()
            )
            self.data_vals[type]["elevation"] = (
                input_file.readline().strip().replace("Elevation =", "").strip()
            )
            self.data_vals[type]["calm_threshold"] = (
                input_file.readline().strip().replace("Calm threshold =", "").strip()
            )

            input_file.readline()

            self.data_vals[type]["included_flags"] = (
                input_file.readline().strip().replace("Included flags:", "").strip()
            )
            self.data_vals[type]["excluded_flags"] = (
                input_file.readline().strip().replace("Excluded flags:", "").strip()
            )

            input_file.readline()
            input_file.readline()
            input_file.readline()

            while True:
                line = input_file.readline()

                output_file.write(line)
                if not line:
                    break

            self.data_vals[type]["df"] = pd.read_csv(
                self.data_vals[type]["temp_file_path"],
                delimiter="\t",
                encoding="windows-1252",
            )

            options = self.data_vals[type]["df"].columns.tolist()[1:]
            options = list(filter(lambda x: x.startswith("WS_"), options))

            self.data_vals[type]["choices"] = options
            self.data_vals[type]["selected_height"].set(
                self.data_vals[type]["choices"][0]
            )

            if (
                self.data_vals["reference"]["df"].empty
                or self.data_vals["target"]["df"].empty
            ):
                self.valid_dfs = False
                self.date_range_start = datetime.today()
                self.date_range_end = datetime.today()

            else:
                self.valid_dfs = True

                self.intersection_df = pd.merge(
                    self.data_vals["reference"]["df"],
                    self.data_vals["target"]["df"],
                    how="inner",
                    on=["Date/Time"],
                    validate="one_to_one",
                    suffixes=("_ref", "_tar"),
                )

                self.intersection_df["Date/Time_updated"] = pd.to_datetime(
                    self.intersection_df["Date/Time"],
                    format=self.datetime_format_string,
                )

                self.date_range_start = datetime.strptime(
                    self.intersection_df.iloc[0, 0], self.datetime_format_string
                )
                self.date_range_end = datetime.strptime(
                    self.intersection_df.iloc[-1, 0], self.datetime_format_string
                )

                self.cal_start_value = self.date_range_start
                self.cal_end_value = self.date_range_end

        except Exception as e:
            method_response = False

        return method_response

    def plot(self):

        if not self.valid_dfs:
            messagebox.showerror("Error", "Select both Reference & Target file")
            return False

        if not self.valid_selected_date_range:
            messagebox.showerror("Error", "Select valid date range")
            return False

        plot_cal_start_value = datetime.combine(self.cal_start_value, time(00, 00, 00))
        plot_cal_end_value = datetime.combine(self.cal_end_value, time(00, 00, 00))
        print("StartDate:", plot_cal_start_value)
        print("EndDate: ", plot_cal_end_value + timedelta(days=1))

        ref_column_name = self.data_vals["reference"]["selected_height"].get()
        tar_column_name = self.data_vals["target"]["selected_height"].get()

        if ref_column_name == tar_column_name:
            ref_column_name += "_ref"
            tar_column_name += "_tar"

        plot_df = self.intersection_df.filter(
            ["Date/Time_updated", ref_column_name, tar_column_name]
        )

        plot_df = plot_df[
            (plot_df["Date/Time_updated"] >= plot_cal_start_value)
            & (plot_df["Date/Time_updated"] < (plot_cal_end_value + timedelta(days=1)))
        ]

        plot_df = plot_df[
            (plot_df[ref_column_name] != 9999) & (plot_df[tar_column_name] != 9999)
        ]

        plot_df["Size_Column"] = 2
        plot_df["Color_Column"] = 100

        print(plot_df)
        self.calculate_r_squared(plot_df)

        plot_df.plot.scatter(
            x=ref_column_name,
            y=tar_column_name,
            s="Size_Column",
            c="Color_Column",
            title="My Scatter Plot",
            xlabel="Reference",
            ylabel="Target",
        )
        plt.show()

    def calculate_r_squared(self, plot_df):

        columns = plot_df.columns

        # Calculate R-squared
        self.r_squared = r2_score(plot_df[columns[1]], plot_df[columns[2]])

        self.data_vals["reference"]["min"] = plot_df[columns[1]].min()
        self.data_vals["reference"]["max"] = plot_df[columns[1]].max()
        self.data_vals["target"]["min"] = plot_df[columns[2]].min()
        self.data_vals["target"]["max"] = plot_df[columns[2]].max()

        self.update_ui_plot_details()


root = tk.Tk()
myapp = AppABC(root)
myapp.create_ui()
myapp.mainloop()
