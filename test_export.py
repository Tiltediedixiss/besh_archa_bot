from data.excel_exporter import excel_exporter

if __name__ == "__main__":
    path = excel_exporter.export_user_progress("_test.xlsx")
    print("EXPORTED:", path)
