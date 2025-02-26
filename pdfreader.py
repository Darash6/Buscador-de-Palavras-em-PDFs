import os
import fitz  # PyMuPDF
import sys
import subprocess
import webbrowser
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QListWidget, QLabel, QMessageBox, QInputDialog, QProgressBar, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

CONFIG_FILE = "config.json"
PASSWORD = "darash6"  # Senha fixa para alterar a pasta


def save_config(folder_path):
    """Salva a pasta escolhida no arquivo de configuração."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"folder_path": folder_path}, f)


def load_config():
    """Carrega a pasta salva no arquivo de configuração, se existir."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("folder_path", "")
    return ""


def find_word_in_pdf(pdf_path, keyword):
    """Procura a palavra-chave dentro do PDF e retorna as páginas onde foi encontrada."""
    try:
        doc = fitz.open(pdf_path)
        pages_found = [page_number + 1 for page_number in range(len(doc))
                       if doc[page_number].search_for(keyword)]
        return (pdf_path, pages_found) if pages_found else None
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")
        return None


class PDFSearchThread(QThread):
    """Thread para buscar palavras-chave nos PDFs, evitando travamentos na UI."""
    progress_updated = pyqtSignal(int)
    search_finished = pyqtSignal(list)

    def __init__(self, folder_path, keyword):
        super().__init__()
        self.folder_path = folder_path
        self.keyword = keyword
        self.found_files = []

    def run(self):
        """Executa a busca paralelamente."""
        pdf_files = [os.path.join(root, file)
                     for root, _, files in os.walk(self.folder_path)
                     for file in files if file.endswith(".pdf")]

        total_pdfs = len(pdf_files)
        if total_pdfs == 0:
            self.search_finished.emit([])
            return

        results = []
        for i, pdf in enumerate(pdf_files):
            res = find_word_in_pdf(pdf, self.keyword)
            if res:
                results.append(res)
            progress = int(((i + 1) / total_pdfs) * 100)
            self.progress_updated.emit(progress)

        self.found_files = results
        self.search_finished.emit(self.found_files)


class PDFSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        # Carregar pasta salva ou definir padrão
        self.folder_path = load_config() or r"C:\Users\SeuUsuario\Documents\PDFs"

        self.init_ui()
        self.found_files = []

    def init_ui(self):
        """Cria a interface gráfica."""
        self.setWindowIcon(QIcon(r"C:\Users\darash\PycharmProjects\PythonProject\logoempresa.ico"))
        self.setWindowTitle("Buscador de Palavras em PDFs")
        self.setGeometry(200, 200, 600, 500)

        layout = QVBoxLayout()

        self.label_folder = QLabel(f"Pasta Atual: {self.folder_path}", self)
        layout.addWidget(self.label_folder)

        self.btn_change_folder = QPushButton("Alterar Pasta", self)
        self.btn_change_folder.clicked.connect(self.request_password)
        layout.addWidget(self.btn_change_folder)

        self.label_keyword = QLabel("Digite a palavra-chave:", self)
        layout.addWidget(self.label_keyword)

        self.input_keyword = QLineEdit(self)
        layout.addWidget(self.input_keyword)

        self.btn_search = QPushButton("Buscar nos PDFs", self)
        self.btn_search.clicked.connect(self.search_pdfs)
        layout.addWidget(self.btn_search)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.results_list = QListWidget(self)
        self.results_list.itemClicked.connect(self.open_pdf)
        layout.addWidget(self.results_list)

        self.setLayout(layout)

    def request_password(self):
        """Solicita a senha antes de permitir alterar a pasta."""
        password, ok = QInputDialog.getText(self, "Autenticação", "Digite a senha:", QLineEdit.Password)

        if ok and password == PASSWORD:
            self.change_folder()
        else:
            QMessageBox.warning(self, "Erro", "Senha incorreta! A pasta não foi alterada.")

    def change_folder(self):
        """Permite alterar a pasta dos PDFs e salva a nova escolha."""
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Nova Pasta")
        if folder:
            self.folder_path = folder
            save_config(folder)
            self.label_folder.setText(f"Pasta Atual: {self.folder_path}")

    def search_pdfs(self):
        """Inicia a busca de palavras-chave nos PDFs usando uma thread."""
        keyword = self.input_keyword.text().strip()
        if not keyword:
            QMessageBox.warning(self, "Erro", "Digite uma palavra-chave!")
            return

        self.results_list.clear()
        self.progress_bar.setValue(0)

        self.search_thread = PDFSearchThread(self.folder_path, keyword)
        self.search_thread.search_finished.connect(self.display_results)
        self.search_thread.progress_updated.connect(self.update_progress_bar)
        self.search_thread.start()

    def update_progress_bar(self, value):
        """Atualiza a barra de progresso."""
        self.progress_bar.setValue(value)

    def display_results(self, found_files):
        """Exibe os resultados após a busca."""
        self.found_files = found_files
        if not self.found_files:
            QMessageBox.information(self, "Resultado", "Nenhum PDF contém essa palavra.")
            return

        for pdf_path, pages in self.found_files:
            pages_str = ", ".join(map(str, pages))
            self.results_list.addItem(f"{pdf_path} (Páginas: {pages_str})")

    def open_pdf(self, item):
        """Abre o PDF na página escolhida pelo usuário."""
        index = self.results_list.row(item)
        pdf_path, pages = self.found_files[index]

        if len(pages) > 1:
            page, ok = QInputDialog.getItem(
                self, "Escolher Página", "Selecione a página para abrir:",
                [str(p) for p in pages], 0, False
            )
            if not ok:
                return
            first_page = int(page)
        else:
            first_page = pages[0]

        acrobat_paths = [
            r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
            r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"
        ]

        acrobat_found = False
        for acrobat in acrobat_paths:
            if os.path.exists(acrobat):
                subprocess.Popen([acrobat, f'/A', f'page={first_page}', pdf_path], shell=True)
                acrobat_found = True
                break

        if not acrobat_found:
            resposta = QMessageBox.question(
                self, "Adobe não encontrado",
                "Adobe Acrobat não foi encontrado. Deseja abrir no navegador?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )

            if resposta == QMessageBox.Yes:
                self.open_pdf_in_browser(pdf_path, first_page)

    def open_pdf_in_browser(self, pdf_path, page):
        """Abre o PDF na página correta no navegador."""
        pdf_path = pdf_path.replace("\\", "/")
        url = f"file:///{pdf_path}#page={page}"
        webbrowser.open(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFSearchApp()
    window.show()
    sys.exit(app.exec_())
