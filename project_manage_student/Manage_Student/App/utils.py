from flask import Flask, send_file
import pandas as pd
import os
from App import form


def export_excel(data,year_learn):

    df = pd.DataFrame(data)

    # 2. Tạo thư mục lưu file
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    # 3. Tạo tên file duy nhất
    file_name = f"DataStudentHistory-{year_learn}.xlsx"
    file_path = os.path.join(upload_folder, file_name)

    # 4. Ghi dữ liệu vào file
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # 5. Trả file về client
    return send_file(
        file_path,
        as_attachment=True,
        download_name="export.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

