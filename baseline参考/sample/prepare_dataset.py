import pandas as pd
import argparse


def excel_to_csv(excel_file_path, csv_file_path):
    """
    Read an Excel file and save it as a CSV file.
    :param excel_file_path: Path to the Excel file
    :param csv_file_path: Path to save the CSV file
    """

    data = pd.read_excel(excel_file_path)
    data.to_csv(csv_file_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    excel_file = "../../data/数据字典.xlsx"
    csv_file = "../../data/数据字典.csv"
    excel_to_csv(excel_file, csv_file)
