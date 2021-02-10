#####pip install fpdf2

from fpdf import FPDF
import os
import platform
import subprocess
import datetime

class PDF(FPDF):
    last_page = False
    student_fee = False
    personalinfo = None

    def header(self):
        # Logo
        add_x = 0
        add_y = 0
        if self.cur_orientation == "P":
            add_x = 0
            add_y = 0
        else:
            add_x = 50
        
        self.set_draw_color(0, 1, 1)
        
    # Page footer
    def footer(self):
        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Página " + str(self.page_no()) + "/{nb}", 0, 0, "C")
        self.set_xy(-65, -20)
        if self.last_page:
            self.set_font("Arial", "I", 10)
            self.cell(0, 8, "BarSoft - barceloch@gmail.com  ", 0, 0, "L")


def show_doc(file_path):
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Linux":
            subprocess.call(["xdg-open", file_path])
    except:
        from kivymd.uix.snackbar import Snackbar

        Snackbar(text="Error abriendo archivo!", duration=1.5).show()

def generatePdf(total_details, reg_data, dir):

    # if dir is not provided then it will be saved at Documents Reciepts Folder
    if dir == None:
        if platform.system() == "Windows":
            documents = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Documentos")
            if not os.path.exists(documents + "/RegCEl_Pdf"):
                os.mkdir(documents + "/RegCEl_Pdf")
                dir = documents + "/RegCEl_Pdf"
            else:
                dir = documents + "/RegCEl_Pdf"
        elif platform.system() == "Linux":
            documents = os.path.join(os.path.join(os.path.expanduser("~")), "Documentos")
            if not os.path.exists(documents + "/RegCEl_Pdf"):
                os.mkdir(documents + "/RegCEl_Pdf")
                dir = documents + "/RegCEl_Pdf"
            else:
                dir = documents + "/RegCEl_Pdf"

    pdf = PDF("P", "mm", "A4")
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.ln(5)
    pdf.set_font("Times", "B", 15)
    pdf.cell(0, 5, "Registros", 0, 1, "C")

    pdf.ln(10)
    pdf.set_font("Times", "B", 12)

    pdf.ln(10)

    pdf.cell(
        188,
        9,
        "           Fecha            \
                    Hora                    \
                    Lectura                \
                    Consumo ",
        1,
    )
    pdf.ln(10)
    for reg in reg_data:
        pdf.cell(40, 10, reg["record_date"], 1, 0, "C")
        pdf.cell(60, 10, reg["record_time"], 1, 0, "C")
        pdf.cell(41, 10, reg["lectura"], 1, 0, "C")
        pdf.cell(47, 10, reg["consumo"], 1, 0, "C")
        pdf.ln(10)

    pdf.set_draw_color(0, 1, 1)

    pdf.multi_cell(
        0.0,
        7.0,
        "Comsumo Total: "
        + total_details["consumo_total"]
        + "                                                                              \
        Importe: "
        + total_details["importe"],
    )

    pdf.last_page = True


    file_name = (
        dir
        + "/"
        +"reg_"
        +f"{str(datetime.datetime.now())[:19]}"
        +".pdf"
        )

    try:
        pdf.output(file_name, "F")
        show_doc(file_name)
    except PermissionError:
        from kivymd.uix.snackbar import Snackbar

        Snackbar(text="PDF generado correctamente!", duration=3).show()


if __name__ == "__main__":

    reg_details = {
        "consumo_total": "150 Kw/h",
        "importe": "132.40$",

    }
    reg_data = [
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},        
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},
        {"fecha": "22/01/2021", "hora": "8:30 am", "lectura": "87400", "consumo": "123 kw/h",},       
    ]
    generatePdf(reg_details, reg_data, None)
