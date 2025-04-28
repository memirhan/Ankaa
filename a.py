# Tek Genel sıralama ile haftalık soru sayısı ekle kaldı. küçük nüanslarda yapıldı
# genel sıralamanın butonları filan yapılcak
# Haftalık soru sayısı ekle yapıldı incele yapılcak

from PyQt5 import QtWidgets, QtCore, QtGui
import platform
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.student_buttons = []
        self.setWindowTitle("Anasayfa")
        #self.showFullScreen()
        self.setStyleSheet("background-color: #2c2f33; color: white;")
        self.create_database()

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.main_page = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.main_page)

        # Sayfaları yönetmek için QStackedWidget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.layout.addWidget(self.stacked_widget)        

        self.label = QtWidgets.QLabel("HOŞGELDİNİZ")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(self.label)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.main_layout.addWidget(self.scroll_area)

        self.ogrencilerim_button = QtWidgets.QPushButton("ÖĞRENCİLERİM")
        self.ogrencilerim_button.setStyleSheet(
            "background-color: #40444B; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            "border: 2px solid #7289da;"
        )
        self.main_layout.addWidget(self.ogrencilerim_button)

        self.ogrencilerim_button.clicked.connect(self.ogrenci_page)

        self.haftalık_deneme_sonucu = QtWidgets.QPushButton("DENEMELER")
        self.haftalık_deneme_sonucu.setStyleSheet(
            "background-color: #3F51B5; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
        )
        self.main_layout.addWidget(self.haftalık_deneme_sonucu)
        # self.ogrencilerim_button.clicked.connect(self.ogrenci_page)

        self.sorun_bildir = QtWidgets.QPushButton("Sorun Bildir")
        self.sorun_bildir.setStyleSheet(
            "background-color: #FF7F00; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
        )

        #ff4747
        self.main_layout.addWidget(self.sorun_bildir)
        self.sorun_bildir.clicked.connect(self.sorun_bildir_func)

        self.kapat_button = QtWidgets.QPushButton("Uygulamayı Kapat")
        self.kapat_button.setStyleSheet(
            "background-color: #FF4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
        )

        #ff4747
        self.main_layout.addWidget(self.kapat_button)
        self.kapat_button.clicked.connect(self.kapat)

        self.students = []
        self.row = 0
        self.col = 0

        self.main_page.setLayout(self.main_layout)
        self.stacked_widget.addWidget(self.main_page)

        # Öğrenci detay sayfası
        self.ogrencilerim_page = QtWidgets.QWidget()
        self.ogrencilerim_layout = QtWidgets.QVBoxLayout(self.ogrencilerim_page)

        # Grid layout'u öğrenci sayfasına ekle
        self.student_grid_layout = QtWidgets.QGridLayout()  # Burada doğru sırayı izliyoruz
        self.ogrencilerim_layout.addLayout(self.student_grid_layout)

        # Bu labelı boşluk bırakmak için kullanıyoruz biraz acemice
        self.ogrencilerim_bosluk = QtWidgets.QLabel("")
        self.ogrencilerim_bosluk.setAlignment(QtCore.Qt.AlignCenter)
        self.ogrencilerim_bosluk.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.ogrencilerim_layout.addWidget(self.ogrencilerim_bosluk)

        self.ogrenci_ekle_buton = QtWidgets.QPushButton("Öğrenci Ekle")
        self.ogrenci_ekle_buton.setStyleSheet(
            "background-color: #00aaff; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
        )
        self.ogrenci_ekle_buton.clicked.connect(self.add_student)
        self.ogrencilerim_layout.addWidget(self.ogrenci_ekle_buton)

        # GERİ BUTON
        self.back_button = QtWidgets.QPushButton("Geri Dön")
        self.back_button.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
        )
        self.back_button.clicked.connect(self.handle_back_button)
        self.ogrencilerim_layout.addWidget(self.back_button)

        self.ogrencilerim_page.setLayout(self.ogrencilerim_layout)
        self.stacked_widget.addWidget(self.ogrencilerim_page)

        # Öğrenci Detay Sayfası
        self.ogrencim_page = QtWidgets.QWidget()
        self.ogrencim_layout = QtWidgets.QVBoxLayout(self.ogrencim_page)

        self.deneme_gor_page = QtWidgets.QWidget()
        self.deneme_gor_layout = QtWidgets.QVBoxLayout(self.deneme_gor_page)

        self.ders_denemesi_page = QtWidgets.QWidget()
        self.ders_denemesi_layout = QtWidgets.QVBoxLayout(self.ders_denemesi_page)

        self.ders_denemesi_ekle_page = QtWidgets.QWidget()
        self.ders_denemesi_ekle_layout = QtWidgets.QVBoxLayout(self.ders_denemesi_ekle_page)

        self.ders_denemesi_gor_one_page = QtWidgets.QWidget()
        self.ders_denemesi_gor_one_layout = QtWidgets.QVBoxLayout(self.ders_denemesi_gor_one_page)

        self.ders_denemesi_gor_table_page = QtWidgets.QWidget()
        self.ders_denemesi_gor_table_layout = QtWidgets.QVBoxLayout(self.ders_denemesi_gor_table_page)

        self.haftalik_soru_ekle_one_page = QtWidgets.QWidget()
        self.haftalik_soru_ekle_one_layout = QtWidgets.QVBoxLayout(self.haftalik_soru_ekle_one_page)

        self.haftalik_soru_ekle_two_page = QtWidgets.QWidget()
        self.haftalik_soru_ekle_two_layout = QtWidgets.QVBoxLayout(self.haftalik_soru_ekle_two_page)

        self.haftalik_soru_ekle_dersler_page = QtWidgets.QWidget()
        self.haftalik_soru_ekle_dersler_layout = QtWidgets.QVBoxLayout(self.haftalik_soru_ekle_dersler_page)

        self.haftalik_soru_incele_one_page = QtWidgets.QWidget()
        self.haftalik_soru_incele_one_layout = QtWidgets.QVBoxLayout(self.haftalik_soru_incele_one_page)

        self.haftalik_soru_incele_two_page = QtWidgets.QWidget()
        self.haftalik_soru_incele_two_layout = QtWidgets.QVBoxLayout(self.haftalik_soru_incele_two_page)

        

        self.student_name_label = QtWidgets.QLabel("")
        self.student_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.ogrencim_layout.addWidget(self.student_name_label)    

        self.ogrencim_page.setLayout(self.ogrencim_layout)
        self.deneme_gor_page.setLayout(self.deneme_gor_layout)
        self.ders_denemesi_page.setLayout(self.ders_denemesi_layout)
        self.ders_denemesi_ekle_page.setLayout(self.ders_denemesi_ekle_layout)
        self.ders_denemesi_gor_one_page.setLayout(self.ders_denemesi_gor_one_layout)
        self.ders_denemesi_gor_table_page.setLayout(self.ders_denemesi_gor_table_layout)
        self.haftalik_soru_ekle_one_page.setLayout(self.haftalik_soru_ekle_one_layout)
        self.haftalik_soru_ekle_two_page.setLayout(self.haftalik_soru_ekle_two_layout)
        self.haftalik_soru_ekle_dersler_page.setLayout(self.haftalik_soru_ekle_dersler_layout)
        self.haftalik_soru_incele_one_page.setLayout(self.haftalik_soru_incele_one_layout)
        self.haftalik_soru_incele_two_page.setLayout(self.haftalik_soru_incele_two_layout)

        # Stacked a ekle
        self.stacked_widget.addWidget(self.ogrencim_page)
        self.stacked_widget.addWidget(self.deneme_gor_page)
        self.stacked_widget.addWidget(self.ders_denemesi_page)
        self.stacked_widget.addWidget(self.ders_denemesi_ekle_page)
        self.stacked_widget.addWidget(self.ders_denemesi_gor_one_page)
        self.stacked_widget.addWidget(self.ders_denemesi_gor_table_page)
        self.stacked_widget.addWidget(self.haftalik_soru_ekle_one_page)
        self.stacked_widget.addWidget(self.haftalik_soru_ekle_two_page)
        self.stacked_widget.addWidget(self.haftalik_soru_ekle_dersler_page)
        self.stacked_widget.addWidget(self.haftalik_soru_incele_one_page)
        self.stacked_widget.addWidget(self.haftalik_soru_incele_two_page)

        
        self.load_students()

    def kapat(self):
        yanit = QMessageBox.question(
            self,
            "Çıkış Onayı",
            "Uygulamayı kapatmak istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if yanit == QMessageBox.Yes:
            self.close()

    def handle_back_button(self):
        current_page = self.stacked_widget.currentWidget()
        if current_page == self.ogrencilerim_page:
            self.stacked_widget.setCurrentWidget(self.main_page)

        elif current_page == self.ogrencim_page:
            self.stacked_widget.setCurrentWidget(self.ogrencilerim_page)

        elif current_page == self.deneme_gor_page:
            self.stacked_widget.setCurrentWidget(self.ogrencim_page)

        elif current_page == self.ders_denemesi_page:
            self.stacked_widget.setCurrentWidget(self.ogrencim_page)

        elif current_page == self.ders_denemesi_ekle_page:
            self.stacked_widget.setCurrentWidget(self.ders_denemesi_page)

        elif current_page == self.ders_denemesi_gor_one_page:
            self.stacked_widget.setCurrentWidget(self.ders_denemesi_page)

        elif current_page == self.ders_denemesi_gor_table_page:
            self.stacked_widget.setCurrentWidget(self.ders_denemesi_gor_one_page)

        elif current_page == self.haftalik_soru_ekle_one_page:
            self.stacked_widget.setCurrentWidget(self.ogrencim_page)

        elif current_page == self.haftalik_soru_ekle_two_page:
            self.stacked_widget.setCurrentWidget(self.haftalik_soru_ekle_one_page)

        elif current_page == self.haftalik_soru_ekle_dersler_page:
            self.stacked_widget.setCurrentWidget(self.haftalik_soru_ekle_two_page)
            
        else:
            self.stacked_widget.setCurrentWidget(self.main_page)

    def sorun_bildir_func(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Sorun Bildir")
        dialog.setFixedSize(500, 350)  # Pencere boyutunu genişlet

        form_layout = QtWidgets.QFormLayout()

        self.konu = QtWidgets.QLineEdit(dialog)
        self.konu.setPlaceholderText("Konu giriniz...")
        self.konu.setFixedHeight(35)
        self.konu.setFixedWidth(450)

        self.mesaj = QtWidgets.QTextEdit(dialog)  # Daha büyük mesaj alanı
        self.mesaj.setPlaceholderText("Sorununuzu buraya yazınız...")
        self.mesaj.setFixedHeight(180)
        self.mesaj.setFixedWidth(450)

        gonder_button = QtWidgets.QPushButton("Gönder", dialog)
        gonder_button.setStyleSheet("background-color: #ff4747; color: white; padding: 10px; border-radius: 5px;")
        gonder_button.setFixedWidth(100)
        gonder_button.clicked.connect(lambda: self.mail_gonder(dialog))  # Butona tıklanınca mail gönder

        # Butonu ortalamak için QHBoxLayout kullan
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(gonder_button)
        button_layout.addStretch()

        form_layout.addRow("Konu:", self.konu)
        form_layout.addRow("Mesaj:", self.mesaj)

        # Layout'u dikey olarak ayarla
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)  # Butonu ortalamış olduk

        dialog.setLayout(main_layout)
        dialog.exec_()

    def mail_gonder(self, dialog):
        subject = self.konu.text()
        message = self.mesaj.toPlainText()

        if not subject or not message:
            QtWidgets.QMessageBox.warning(self, "Hata", "Konu ve mesaj alanları boş bırakılamaz!")
            return

        senderMail = "pdrappykfl@gmail.com"
        senderPassword = "ieja nsjy dwlx wzhm"  # Gmail uygulama şifren buraya gelecek
        toMail = "memirhansumer@gmail.com"

        try:
            # **Platform Bilgilerini Al**
            platform_bilgisi = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"

            # **IP Adresini Al, Hata Olursa Pas Geç**
            try:
                ip_adresi = requests.get('https://api64.ipify.org', timeout=5).text  
            except Exception:
                ip_adresi = "IP alınamadı"  # Eğer hata olursa, pas geçip boş bırak

            msg = MIMEMultipart()
            msg['From'] = senderMail
            msg['To'] = toMail
            msg['Subject'] = subject

            # **HTML Mail Şablonu**
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; background-color: white; padding: 20px; border-radius: 8px; 
                            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; text-align: center;">📩 Yeni Sorun Bildirimi</h2>
                    <hr style="border: none; height: 1px; background-color: #ddd;">
                    <p><strong>📌 Konu:</strong> {subject}</p>
                    <p><strong>📜 Mesaj:</strong></p>
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 5px solid #ff4747;">
                        {message}
                    </div>
                    <hr style="border: none; height: 1px; background-color: #ddd;">
                    <p><strong>💻 Platform:</strong> {platform_bilgisi}</p>
                    <p><strong>🌍 IP Adresi:</strong> {ip_adresi}</p>
                    <hr style="border: none; height: 1px; background-color: #ddd;">
                    <p style="text-align: center; color: #777; font-size: 12px;">
                        Bu e-posta Ankaa Kitap Kafe tarafından otomatik olarak gönderilmiştir.
                    </p>
                </div>
            </body>
            </html>
            """

            msg.attach(MIMEText(html_content, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(senderMail, senderPassword)
            server.sendmail(senderMail, toMail, msg.as_string())
            server.quit()

            QtWidgets.QMessageBox.information(self, "Başarılı", "Sorununuz başarıyla gönderildi!")
            dialog.accept()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", "Mail gönderilemedi!\nİnternet Bağlantınızı Kontrol Ediniz")

    def ogrenci_page(self):
        self.stacked_widget.setCurrentWidget(self.ogrencilerim_page)

    def add_student(self):
        self.cursor.execute("SELECT COUNT(*) FROM students")
        student_count = self.cursor.fetchone()[0]

        if student_count >= 100:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Öğrenci sayısı 100 oldu! Lütfen geliştirici ile iletişime geçin.")
            return
        
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Öğrenci Ekle")

        form_layout = QtWidgets.QFormLayout(dialog)

        name_input = QtWidgets.QLineEdit(dialog)
        last_name_input = QtWidgets.QLineEdit(dialog)
        class_input = QtWidgets.QLineEdit(dialog)

        form_layout.addRow("Öğrenci Adı:", name_input)
        form_layout.addRow("Öğrenci Soyadı:", last_name_input)
        form_layout.addRow("Öğrenci Sınıfı:", class_input)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, dialog)
        form_layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            name = name_input.text()
            last_name = last_name_input.text()
            student_class = class_input.text()

            if name and last_name and student_class:
                self.create_student_button(name, last_name, student_class)
                self.save_to_database(name, last_name, student_class)
            else:
                QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")

    def save_to_database(self, name, last_name, student_class):
        self.cursor.execute("INSERT INTO students (name, last_name, student_class) VALUES (?, ?, ?)",
                            (name, last_name, student_class))
        self.conn.commit()

    def create_database(self):
        self.conn = sqlite3.connect("db/veritabani.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # Öğrenci tablosu
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                last_name TEXT,
                                student_class TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sinav_sonuclari (
                                id INTEGER PRIMARY KEY,
                                ogrenci_id INTEGER,
                                sinav_ismi TEXT,
                                sinav_tarihi TEXT,
                                turkce_d INTEGER,
                                turkce_y INTEGER,
                                turkce_b INTEGER,
                                sosyal_d INTEGER,
                                sosyal_y INTEGER,
                                sosyal_b INTEGER,
                                din_d INTEGER,
                                din_y INTEGER,
                                din_b INTEGER,
                                ingilizce_d INTEGER,
                                ingilizce_y INTEGER,
                                ingilizce_b INTEGER,
                                matematik_d INTEGER,
                                matematik_y INTEGER,
                                matematik_b INTEGER,
                                fen_d INTEGER,
                                fen_y INTEGER,
                                fen_b INTEGER,
                                FOREIGN KEY (ogrenci_id) REFERENCES students(id) ON DELETE CASCADE)''')   
             
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ders_denemeleri (
                                id INTEGER PRIMARY KEY,
                                ogrenci_id INTEGER,
                                ders_id INTEGER,
                                ders_ismi TEXT,
                                sinav_ismi TEXT,
                                dogru_sayisi INTEGER,
                                yanlis_sayisi INTEGER,
                                bos_sayisi INTEGER,
                                FOREIGN KEY (ogrenci_id) REFERENCES students(id) ON DELETE CASCADE)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS haftalik_soru (
                                id INTEGER PRIMARY KEY,
                                ogrenci_id INTEGER,
                                ders_id INTEGER,
                                ders_ismi TEXT,
                                ay TEXT,
                                hafta TEXT,
                                dogru_sayisi INTEGER,
                                yanlis_sayisi INTEGER,
                                bos_sayisi INTEGER,
                                FOREIGN KEY (ogrenci_id) REFERENCES students(id) ON DELETE CASCADE)''')
    
                
        self.conn.commit()

    def create_student_button(self, name, last_name, student_class):
        full_name = f"{name} {last_name} - {student_class}"
        button = QtWidgets.QPushButton(full_name)
        button.setStyleSheet(
            "background-color: #7289da; border-radius: 10px; padding: 10px;"
            "font-size: 14px; color: white;"
        )
        button.clicked.connect(lambda: self.show_student_page(name,))
        self.student_grid_layout.addWidget(button, self.row, self.col)
        self.students.append(button)

        if self.col == 0 and self.row > 0:
            self.student_grid_layout.setRowMinimumHeight(self.row - 1, 20)

        self.col += 1
        if self.col >= 10:
            self.col = 0
            self.row += 1

    def load_students(self):
        # **Önce eski öğrenci butonlarını temizle**
        for i in reversed(range(self.student_grid_layout.count())):
            widget = self.student_grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # **Güncellenmiş öğrenci listesini al**
        self.cursor.execute("SELECT id, name, last_name, student_class FROM students")
        students = self.cursor.fetchall()

        self.row, self.col = 0, 0  # Yeni düzen başlat
        for student_id, name, last_name, student_class in students:
            self.create_student_button(name, last_name, student_class)

    def deneme_sonucu_ekle(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Yeni Deneme Sonucu Ekle")

        form_layout = QtWidgets.QFormLayout(dialog)

        deneme_isim = QtWidgets.QLineEdit(dialog)
        deneme_tarihi = QtWidgets.QLineEdit(dialog)

        turkce_d = QtWidgets.QLineEdit(dialog)
        turkce_y = QtWidgets.QLineEdit(dialog)
        turkce_b = QtWidgets.QLineEdit(dialog)
        
        sosyal_d = QtWidgets.QLineEdit(dialog)
        sosyal_y = QtWidgets.QLineEdit(dialog)
        sosyal_b = QtWidgets.QLineEdit(dialog)

        din_d = QtWidgets.QLineEdit(dialog)
        din_y = QtWidgets.QLineEdit(dialog)
        din_b = QtWidgets.QLineEdit(dialog)
        
        ingilizce_d = QtWidgets.QLineEdit(dialog)
        ingilizce_y = QtWidgets.QLineEdit(dialog)
        ingilizce_b = QtWidgets.QLineEdit(dialog)

        matematik_d = QtWidgets.QLineEdit(dialog)
        matematik_y = QtWidgets.QLineEdit(dialog)
        matematik_b = QtWidgets.QLineEdit(dialog)

        fen_d = QtWidgets.QLineEdit(dialog)
        fen_y = QtWidgets.QLineEdit(dialog)
        fen_b = QtWidgets.QLineEdit(dialog)
        
        form_layout.addRow("Deneme İsmi:", deneme_isim)
        form_layout.addRow("Deneme Tarihi:", deneme_tarihi)

        form_layout.addRow("Türkçe Doğru:", turkce_d)
        form_layout.addRow("Türkçe Yanlış:", turkce_y)
        form_layout.addRow("Türkçe Boş:", turkce_b)

        form_layout.addRow("Sosyal Doğru:", sosyal_d)
        form_layout.addRow("Sosyal Yanlış:", sosyal_y)
        form_layout.addRow("Sosyal Boş:", sosyal_b)

        form_layout.addRow("Din Doğru:", din_d)
        form_layout.addRow("Din Yanlış:", din_y)
        form_layout.addRow("Din Boş:", din_b)

        form_layout.addRow("İngilizce Doğru:", ingilizce_d)
        form_layout.addRow("İngilizce Yanlış:", ingilizce_y)
        form_layout.addRow("İngilizce Boş:", ingilizce_b)

        form_layout.addRow("Matematik Doğru:", matematik_d)
        form_layout.addRow("Matematik Yanlış:", matematik_y)
        form_layout.addRow("Matematik Boş:", matematik_b)

        form_layout.addRow("Fen Doğru:", fen_d)
        form_layout.addRow("Fen Yanlış:", fen_y)
        form_layout.addRow("Fen Boş:", fen_b)


        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, dialog)
        form_layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            values = [
                deneme_isim.text(),
                deneme_tarihi.text(),
                turkce_d.text(), turkce_y.text(), turkce_b.text(),
                sosyal_d.text(), sosyal_y.text(), sosyal_b.text(),
                din_d.text(), din_y.text(), din_b.text(),
                ingilizce_d.text(), ingilizce_y.text(), ingilizce_b.text(),
                matematik_d.text(), matematik_y.text(), matematik_b.text(),
                fen_d.text(), fen_y.text(), fen_b.text()
            ]

            if all(values):  # Boş alan bırakılmaması için kontrol
                sinav_ismi, sinav_tarihi, *numeric_values = values  # İlk iki eleman sınav ismi ve tarihi, geri kalanı sayılar

                if not all(x.text().isdigit() for x in [turkce_d, turkce_y, turkce_b, sosyal_d, sosyal_y, sosyal_b, din_d, din_y, din_b, ingilizce_d, ingilizce_y, ingilizce_b, matematik_d, matematik_y, matematik_b, fen_d, fen_y, fen_b]):
                    QtWidgets.QMessageBox.warning(self, "Hata", "Doğru, Yanlış ve Boş sayıları sadece rakam olmalıdır!")
                    return  # Hata durumunda ekleme işlemini durdur


                ogrenci_id = self.current_student_id

                self.cursor.execute("""
                    INSERT INTO sinav_sonuclari (ogrenci_id, sinav_ismi, sinav_tarihi, turkce_d, turkce_y, turkce_b, sosyal_d, sosyal_y, sosyal_b, din_d, din_y, din_b, ingilizce_d, ingilizce_y, ingilizce_b, matematik_d, matematik_y, matematik_b, fen_d, fen_y, fen_b) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (ogrenci_id, sinav_ismi, sinav_tarihi, *map(int, numeric_values)))  # Sadece sayısal alanları int'e çevir
                self.conn.commit()

                ogrenci_ismi = self.get_name_with_suffix(self.isim)
                QtWidgets.QMessageBox.information(self, "Başarılı", "{} {} isimli denemesi eklendi".format(ogrenci_ismi, sinav_ismi))

            else:
                QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")

    def get_name_with_suffix(self, name):
        if name[-1].lower() in 'aeıioöuü':  # Son harfi ünlü harfse
            return name + "'nın"
        else:
            return name + "'in"

    def show_student_page(self, name):
        # Net Sayısı = Doğru Sayısı - (Yanlış Sayısı / 3)
        if hasattr(self, 'student_name_label') and self.student_name_label:
            self.student_name_label.deleteLater()
        
        if hasattr(self, 'deneme_ekle_buton') and self.deneme_ekle_buton:
            self.deneme_ekle_buton.deleteLater()

        if hasattr(self, 'deneme_sonucu_gor') and self.deneme_sonucu_gor:
            self.deneme_sonucu_gor.deleteLater()

        if hasattr(self, 'haftalik_soru_ekle') and self.haftalik_soru_ekle:
            self.haftalik_soru_ekle.deleteLater()

        if hasattr(self, 'haftalik_soru_incele') and self.haftalik_soru_incele:
            self.haftalik_soru_incele.deleteLater()

        if hasattr(self, 'ders_denemesi_button') and self.ders_denemesi_button:
            self.ders_denemesi_button.deleteLater()

        if hasattr(self, 'back_button_ogrencim') and self.back_button_ogrencim:
            self.back_button_ogrencim.deleteLater()

        if hasattr(self, 'ogrenci_sil_button') and self.ogrenci_sil_button:
            self.ogrenci_sil_button.deleteLater()
        
        self.cursor.execute("SELECT id FROM students WHERE name = ?", (name,)) # nameem sayesinde id yi alıyour
        result = self.cursor.fetchone()
        self.current_student_id = result[0]

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        if result:
            # Öğrencinin ismini bir QLabel olarak ekleyelim
            self.student_name_label = QtWidgets.QLabel(f"Merhaba, {name}!")
            self.student_name_label.setAlignment(QtCore.Qt.AlignCenter)
            self.student_name_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
            self.ogrencim_layout.addWidget(self.student_name_label)
            self.stacked_widget.setCurrentWidget(self.ogrencim_page)

            # DENEME EKLE
            self.deneme_ekle_buton = QtWidgets.QPushButton("Deneme Ekle")
            self.deneme_ekle_buton.setStyleSheet(
            "background-color: #4caf50; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
            self.deneme_ekle_buton.clicked.connect(self.deneme_sonucu_ekle)
            self.ogrencim_layout.addWidget(self.deneme_ekle_buton)
            ###############################

            # DENEME SONUCU GÖR
            self.deneme_sonucu_gor = QtWidgets.QPushButton("Deneme Sonucu Gör")
            self.deneme_sonucu_gor.setStyleSheet(
            "background-color: #FF6600; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
            self.deneme_sonucu_gor.clicked.connect(self.deneme_gor)
            self.ogrencim_layout.addWidget(self.deneme_sonucu_gor)
            ###############################

            # HAFTALIK SORU SAYISI EKLE
            self.haftalik_soru_ekle = QtWidgets.QPushButton("Haftalık Soru Sayısı Ekle")
            self.haftalik_soru_ekle.setStyleSheet(
            "background-color: #9B59B6; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
            self.haftalik_soru_ekle.clicked.connect(self.haftalik)
            self.ogrencim_layout.addWidget(self.haftalik_soru_ekle)
            ###############################

            # HAFTALIK SORU SAYISI GÖR
            self.haftalik_soru_incele = QtWidgets.QPushButton("Haftalık Soru Sayısını İncele")
            self.haftalik_soru_incele.setStyleSheet(
            "background-color: #AF7AC5; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
            self.haftalik_soru_incele.clicked.connect(self.haftalik_incele)
            self.ogrencim_layout.addWidget(self.haftalik_soru_incele)
            ###############################

            # DERS DENEMELERİ
            self.ders_denemesi_button = QtWidgets.QPushButton("Ders Denemeleri")
            self.ders_denemesi_button.setStyleSheet(
            "background-color: #DA70D6; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
            self.ders_denemesi_button.clicked.connect(self.ders_denemesi)
            self.ogrencim_layout.addWidget(self.ders_denemesi_button)
            ###############################

            self.ogrenci_sil_button = QtWidgets.QPushButton("Öğrenci Sil")
            self.ogrenci_sil_button.setStyleSheet(
            "background-color: #A52A2A; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
            self.ogrenci_sil_button.clicked.connect(self.ogrenci_sil)
            self.ogrencim_layout.addWidget(self.ogrenci_sil_button)

            self.back_button_ogrencim = QtWidgets.QPushButton("Geri Dön")
            self.back_button_ogrencim.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            )
            self.back_button_ogrencim.clicked.connect(self.handle_back_button)
            self.ogrencim_layout.addWidget(self.back_button_ogrencim)
            
        else:
            QtWidgets.QMessageBox.warning(self, "Hata", "Öğrenci bulunamadı.")
            
    def ogrenci_sil(self, name):

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]
        name = self.isim
        reply = QtWidgets.QMessageBox.question(
            self, "Öğrenci Sil", 
            f"{name} adlı öğrenciyi ve tüm ilişkili verilerini silmek istediğinizden emin misiniz?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:

                self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
                result2 = self.cursor.fetchone()
                self.isim = result2[0]

                name = self.isim

                print(name)
                print(f"Silme işlemi başlıyor: Öğrenci adı = {name}")

                self.cursor.execute("SELECT id FROM students WHERE name = ?", (name,))
                result = self.cursor.fetchone()
                

                print(f"SQL Sorgu Sonucu: {result}")  # Debug için eklenen satır

                if result is None:  # Eğer öğrenci bulunamazsa hata ver
                    QtWidgets.QMessageBox.warning(self, "Hata", f"{name} adlı öğrenci bulunamadı.")
                    return  

                self.current_student_id = result[0]
                print(f"Silinecek Öğrenci ID: {self.current_student_id}")

                self.cursor.execute("PRAGMA foreign_keys = ON;")

                self.cursor.execute("DELETE FROM ders_denemeleri WHERE ogrenci_id = ?", (self.current_student_id,))
                self.cursor.execute("DELETE FROM sinav_sonuclari WHERE ogrenci_id = ?", (self.current_student_id,))
                self.cursor.execute("DELETE FROM students WHERE id = ?", (self.current_student_id,))

                self.load_students()
                self.conn.commit()

                QtWidgets.QMessageBox.information(self, "Başarılı", f"{name} ve tüm ilişkili veriler silindi.")

                # Butonları temizle ve sayfayı güncelle
                # self.clear_student_buttons()
                # self.load_students()
                self.stacked_widget.setCurrentWidget(self.ogrencilerim_page)

            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Hata", f"Öğrenci silinirken hata oluştu: {str(e)}")

    def deneme_gor(self, ogrenci_id):
        ogrenci_id = self.current_student_id

        self.cursor.execute("""
            SELECT sinav_ismi, sinav_tarihi, turkce_d, turkce_y, turkce_b, sosyal_d, sosyal_y, sosyal_b, din_d, din_y, din_b, ingilizce_d, ingilizce_y, ingilizce_b, matematik_d, matematik_y, matematik_b, fen_d, fen_y, fen_b, id
            FROM sinav_sonuclari WHERE ogrenci_id = ?
        """, (ogrenci_id,))

        results = self.cursor.fetchall()

        if not results:
            QtWidgets.QMessageBox.information(self, "Bilgi", "Bu öğrencinin deneme sonucu yok.")
            return

        self.stacked_widget.setCurrentWidget(self.deneme_gor_page)

        if hasattr(self, 'student_name_label_deneme') and self.student_name_label_deneme:
            self.student_name_label_deneme.deleteLater()

        if hasattr(self, 'back_button_deneme') and self.back_button_deneme:
            self.back_button_deneme.deleteLater()

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        ogrenci_ismi = self.get_name_with_suffix(self.isim)

        self.student_name_label_deneme = QtWidgets.QLabel(f"{ogrenci_ismi} Deneme Sonuçları")
        self.student_name_label_deneme.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_deneme.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.deneme_gor_layout.addWidget(self.student_name_label_deneme)

        if hasattr(self, "exam_results_table"):
            self.deneme_gor_layout.removeWidget(self.exam_results_table)
            self.exam_results_table.deleteLater()

        def calculate_net(correct, wrong):
            # 3 yanlış = 1 doğruyu götürür, o yüzden (correct - wrong // 3)
            return correct - (wrong * 0.25)

        # QTableWidget oluştur
        self.exam_results_table = QtWidgets.QTableWidget()
        self.exam_results_table.setRowCount(len(results))
        self.exam_results_table.setColumnCount(10)  # Added extra column for delete button
        self.exam_results_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.exam_results_table.setHorizontalHeaderLabels(["Sınav İsmi", "Sınav Tarihi", "Türkçe", "Sosyal", "Din", "İngilizce", "Matematik", "Fen", "Net", "Sil"])
        self.exam_results_table.setStyleSheet("""
        QTableWidget {
            background-color: #2c2f33;
            color: white;
            font-size: 14px;
            border: none;
            gridline-color: #444;
            border-radius: 10px;
        }
        QTableWidget::item {
            padding: 10px;
            border-bottom: 1px solid #444;
        }
        QHeaderView::section {
            background-color: #2c2f33;
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
        }
        QTableWidget::horizontalHeader {
            background-color: #333;
        }
        QTableWidget::verticalHeader {
            background-color: #333;
        }
        """)

        # Verileri tabloya ekle
        for row_idx, result in enumerate(results):
            self.exam_results_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(result[0]))  # Sınav İsmi
            self.exam_results_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(result[1]))  # Sınav Tarihi

            # Türkçe
            turkce_text = f"{result[2]}D / {result[3]}Y / {result[4]}B"
            self.exam_results_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(turkce_text))

            # Sosyal
            sosyal_text = f"{result[5]}D / {result[6]}Y / {result[7]}B"
            self.exam_results_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(sosyal_text))

            # Din
            din_text = f"{result[8]}D / {result[9]}Y / {result[10]}B"
            self.exam_results_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(din_text))

            # İngilizce
            ingilizce_text = f"{result[11]}D / {result[12]}Y / {result[13]}B"
            self.exam_results_table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(ingilizce_text))

            # Matematik
            matematik_text = f"{result[14]}D / {result[15]}Y / {result[16]}B"
            self.exam_results_table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(matematik_text))

            # Fen
            fen_text = f"{result[17]}D / {result[18]}Y / {result[19]}B"
            self.exam_results_table.setItem(row_idx, 7, QtWidgets.QTableWidgetItem(fen_text))

            turkce_correct = result[2]
            turkce_wrong = result[3]

            sosyal_correct = result[5]
            sosyal_wrong = result[6]

            din_correct = result[8]
            din_wrong = result[9]

            ingilizce_correct = result[11]
            ingilizce_wrong = result[12]

            matematik_correct = result[14]
            matematik_wrong = result[15]

            fen_correct = result[17]
            fen_wrong = result[18]

            total_net = calculate_net(turkce_correct, turkce_wrong) + calculate_net(sosyal_correct, sosyal_wrong) + calculate_net(din_correct, din_wrong) + calculate_net(ingilizce_correct, ingilizce_wrong) + calculate_net(matematik_correct, matematik_wrong) + calculate_net(fen_correct, fen_wrong)
            net_item = QtWidgets.QTableWidgetItem(str(total_net))

            green_color = QtGui.QColor(46, 204, 113)
            red_color = QtGui.QColor(231, 76, 60)

            if total_net > 70:
                net_item.setForeground(QtGui.QBrush(green_color))
            
            else:
                net_item.setForeground(QtGui.QBrush(red_color))

            self.exam_results_table.setItem(row_idx, 8, net_item)

            delete_button = QtWidgets.QPushButton("Sil")
            delete_button.setFixedHeight(15)  # Yüksekliği 40px olarak ayarla
            delete_button.clicked.connect(lambda _, row_idx=row_idx, exam_id=result[14]: self.delete_exam_result(row_idx, exam_id))
            self.exam_results_table.setCellWidget(row_idx, 9, delete_button)
            delete_button.setStyleSheet("background-color: #ff4747")

        self.deneme_gor_layout.addWidget(self.exam_results_table)
        self.back_button_deneme = QtWidgets.QPushButton("Geri Dön")
        self.back_button_deneme.setStyleSheet(
        "background-color: #ff4747; border-radius: 10px; padding: 10px;"
        "font-size: 16px; color: white;"
        )
        self.deneme_gor_layout.addWidget(self.back_button_deneme)
        self.back_button_deneme.clicked.connect(self.handle_back_button)

    def delete_exam_result(self, row_idx, exam_id):
        # Show a confirmation dialog before deleting
        reply = QtWidgets.QMessageBox.question(self, 'Silme Onayı', 'Bu denemeyi silmek istediğinizden emin misiniz?', 
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # Delete the record from the database
            self.cursor.execute("DELETE FROM sinav_sonuclari WHERE id = ?", (exam_id,))
            self.conn.commit()

            self.exam_results_table.removeRow(row_idx)

            if self.exam_results_table.rowCount() == 0:
                QtWidgets.QMessageBox.information(self, "Bilgi", "Tüm denemeler silindi.")
                self.stacked_widget.setCurrentWidget(self.ogrencim_page)
                
            else:
                self.exam_results_table.viewport().update()  # Force update the table view

    def ders_denemesi(self):
    # Önceki widget'ları kaldırmak için
        
        if hasattr(self, 'student_name_label_ders_denemesi') and self.student_name_label_ders_denemesi:
            self.student_name_label_ders_denemesi.deleteLater()

        if hasattr(self, 'ders_denemesi_ekle_button') and self.ders_denemesi_ekle_button:
            self.ders_denemesi_ekle_button.deleteLater()

        if hasattr(self, 'ders_denemesi_gor_button') and self.ders_denemesi_gor_button:
            self.ders_denemesi_gor_button.deleteLater()

        if hasattr(self, 'back_button_ders_denemesi') and self.back_button_ders_denemesi:
            self.back_button_ders_denemesi.deleteLater()

        # Öğrencinin ismini alalım
        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        ogrenci_ismi = self.get_name_with_suffix(self.isim)

        # Yeni bir QLabel ekleyelim
        self.student_name_label_ders_denemesi = QtWidgets.QLabel(f"{ogrenci_ismi} İçin Hangi İşlemi Yapıcaksınız ?")
        self.student_name_label_ders_denemesi.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_ders_denemesi.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.ders_denemesi_layout.addWidget(self.student_name_label_ders_denemesi)
        
        # Sayfayı güncelleyelim
        self.stacked_widget.setCurrentWidget(self.ders_denemesi_page)

        # DENEME EKLE
        self.ders_denemesi_ekle_button = QtWidgets.QPushButton("Deneme Ekle")
        self.ders_denemesi_ekle_button.setStyleSheet(
            "background-color: #4caf50; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
        )
        self.ders_denemesi_ekle_button.clicked.connect(self.ders_denemesi_ekle)
        self.ders_denemesi_layout.addWidget(self.ders_denemesi_ekle_button)

        ###############################

        # DENEME SONUCU GÖR
        self.ders_denemesi_gor_button = QtWidgets.QPushButton("Deneme Sonucu Gör")
        self.ders_denemesi_gor_button.setStyleSheet(
            "background-color: #FF6600; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
        )
        self.ders_denemesi_gor_button.clicked.connect(self.ders_denemesi_gor)
        self.ders_denemesi_layout.addWidget(self.ders_denemesi_gor_button)

        ###############################

        # Geri Dön butonu
        self.back_button_ders_denemesi = QtWidgets.QPushButton("Geri Dön")
        self.back_button_ders_denemesi.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
        )
        self.back_button_ders_denemesi.clicked.connect(self.handle_back_button)
        self.ders_denemesi_layout.addWidget(self.back_button_ders_denemesi)

    def ders_denemesi_ekle(self):
        if hasattr(self, 'student_name_label_ders_denemesi_ekle') and self.student_name_label_ders_denemesi_ekle:
            self.student_name_label_ders_denemesi_ekle.deleteLater()
        
        if hasattr(self, 'matematik_button') and self.matematik_button:
            self.matematik_button.deleteLater()

        if hasattr(self, 'fen_button') and self.fen_button:
            self.fen_button.deleteLater()

        if hasattr(self, 'turkce_button') and self.turkce_button:
            self.turkce_button.deleteLater()

        if hasattr(self, 'sosyal_button') and self.sosyal_button:
            self.sosyal_button.deleteLater()

        if hasattr(self, 'din_button') and self.din_button:
            self.din_button.deleteLater()

        if hasattr(self, 'ingilizce_button') and self.ingilizce_button:
            self.ingilizce_button.deleteLater()

        if hasattr(self, 'back_button_ders_denemesi_ekle') and self.back_button_ders_denemesi_ekle:
            self.back_button_ders_denemesi_ekle.deleteLater()
            

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        ogrenci_ismi = self.get_name_with_suffix(self.isim)

        self.student_name_label_ders_denemesi_ekle = QtWidgets.QLabel(f"{ogrenci_ismi} Hangi Ders Denemesini Ekliceksiniz ?")
        self.student_name_label_ders_denemesi_ekle.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_ders_denemesi_ekle.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.ders_denemesi_ekle_layout.addWidget(self.student_name_label_ders_denemesi_ekle)
        self.stacked_widget.setCurrentWidget(self.ders_denemesi_ekle_page)


        self.matematik_button = QtWidgets.QPushButton("Matematik")
        self.matematik_button.setStyleSheet(
            "background-color: #4caf50; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        self.matematik_button.clicked.connect(lambda: self.ders_denemesi_ekle_func(1, "Matematik"))
        self.ders_denemesi_ekle_layout.addWidget(self.matematik_button)
            ###############################

            # DENEME SONUCU GÖR
        self.fen_button = QtWidgets.QPushButton("Fen Bilgisi")
        self.fen_button.setStyleSheet(
            "background-color: #FF6600; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        self.fen_button.clicked.connect(lambda: self.ders_denemesi_ekle_func(2, "Fen Bilgisi"))
        self.ders_denemesi_ekle_layout.addWidget(self.fen_button)


        self.turkce_button = QtWidgets.QPushButton("Türkçe")
        self.turkce_button.setStyleSheet(
            "background-color: #9B59B6; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #9B59B6
        self.turkce_button.clicked.connect(lambda: self.ders_denemesi_ekle_func(3, "Türkçe"))
        self.ders_denemesi_ekle_layout.addWidget(self.turkce_button)
            ###############################
        
        self.sosyal_button = QtWidgets.QPushButton("Sosyal Bilgiler")
        self.sosyal_button.setStyleSheet(
            "background-color: #DA70D6; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #DA70D6
        self.sosyal_button.clicked.connect(lambda: self.ders_denemesi_ekle_func(4, "Sosyal Bilgiler"))
        self.ders_denemesi_ekle_layout.addWidget(self.sosyal_button)


        self.din_button = QtWidgets.QPushButton("Din Kültürü")
        self.din_button.setStyleSheet(
            "background-color: #F08080; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #DA70D6
        self.din_button.clicked.connect(lambda: self.ders_denemesi_ekle_func(5, "Din Kültürü"))
        self.ders_denemesi_ekle_layout.addWidget(self.din_button)
        
        self.ingilizce_button = QtWidgets.QPushButton("İngilizce")
        self.ingilizce_button.setStyleSheet(
            "background-color: #C2A1B3; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
        )
        self.ingilizce_button.clicked.connect(lambda: self.ders_denemesi_ekle_func(6, "İngilizce"))
        self.ders_denemesi_ekle_layout.addWidget(self.ingilizce_button)

        self.back_button_ders_denemesi_ekle = QtWidgets.QPushButton("Geri Dön")
        self.back_button_ders_denemesi_ekle.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            )
        self.back_button_ders_denemesi_ekle.clicked.connect(self.handle_back_button)
        self.ders_denemesi_ekle_layout.addWidget(self.back_button_ders_denemesi_ekle)

    def ders_denemesi_ekle_func(self, ders_id, ders_adi):
    # Yeni bir dialog penceresi oluşturuluyor
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"{ders_adi} - Yeni Deneme Sonucu Ekle")

        form_layout = QtWidgets.QFormLayout(dialog)

        # Ders adı QLabel olarak eklendi
        ders_adi_label = QtWidgets.QLabel(ders_adi, dialog)

        # Doğru, Yanlış ve Boş sayıları için giriş kutuları
        sinav_adi = QtWidgets.QLineEdit(dialog)
        dogru_sayisi = QtWidgets.QLineEdit(dialog)
        yanlis_sayisi = QtWidgets.QLineEdit(dialog)
        bos_sayisi = QtWidgets.QLineEdit(dialog)

        # Formu dolduruyoruz
        form_layout.addRow("Ders Adı:", ders_adi_label)
        form_layout.addRow("Sınav Adı:", sinav_adi)  # Ders adı QLabel olarak gösteriliyor
        form_layout.addRow("Doğru Sayısı:", dogru_sayisi)
        form_layout.addRow("Yanlış Sayısı:", yanlis_sayisi)
        form_layout.addRow("Boş Sayısı:", bos_sayisi)

        # OK ve Cancel butonları ekliyoruz
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, dialog)
        form_layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        # Dialog penceresini göster
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
    # Kullanıcıdan alınan verileri alıyoruz
            values = [
                ders_adi_label.text(),
                sinav_adi.text(),
                dogru_sayisi.text(),
                yanlis_sayisi.text(),
                bos_sayisi.text()
            ]

            # Eğer tüm alanlar doluysa veriyi işliyoruz
            if all(values):  # Boş alan bırakılmaması için kontrol
                ders_adi, sinav_adi, dogru, yanlis, bos = values  # Verileri ayırıyoruz

                # Sayısal veri kontrolü (sadece rakam girildiğinden emin olalım)
                if not (dogru.isdigit() and yanlis.isdigit() and bos.isdigit()):
                    QtWidgets.QMessageBox.warning(self, "Hata", "Doğru, Yanlış ve Boş sayıları sadece rakam olmalıdır!")
                    return  # Hata durumunda ekleme işlemini durdur

                # String verileri integer'a çevir
                dogru = int(dogru)
                yanlis = int(yanlis)
                bos = int(bos)

                ogrenci_id = self.current_student_id

                # Veritabanına ekleme
                self.cursor.execute("""
                    INSERT INTO ders_denemeleri (ogrenci_id, ders_id, ders_ismi, sinav_ismi, dogru_sayisi, yanlis_sayisi, bos_sayisi) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (ogrenci_id, ders_id, ders_adi, sinav_adi, dogru, yanlis, bos))  
                self.conn.commit()

                # Kullanıcıya mesaj
                ogrenci_ismi = self.get_name_with_suffix(self.isim)
                QtWidgets.QMessageBox.information(self, "Başarılı", f"{ogrenci_ismi} isimli öğrencinin {ders_adi} dersine ait denemesi başarıyla eklendi!")

            else:
                QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")            
            
    def ders_denemesi_gor(self):
        if hasattr(self, 'student_name_label_ders_denemesi_gor') and self.student_name_label_ders_denemesi_gor:
            self.student_name_label_ders_denemesi_gor.deleteLater()
        
        if hasattr(self, 'matematik_gor_button') and self.matematik_gor_button:
            self.matematik_gor_button.deleteLater()

        if hasattr(self, 'fen_gor_button') and self.fen_gor_button:
            self.fen_gor_button.deleteLater()

        if hasattr(self, 'turkce_gor_button') and self.turkce_gor_button:
            self.turkce_gor_button.deleteLater()

        if hasattr(self, 'sosyal_gor_button') and self.sosyal_gor_button:
            self.sosyal_gor_button.deleteLater()

        if hasattr(self, 'din_gor_button') and self.din_gor_button:
            self.din_gor_button.deleteLater()

        if hasattr(self, 'ingilizce_gor_button') and self.ingilizce_gor_button:
            self.ingilizce_gor_button.deleteLater()

        if hasattr(self, 'back_button_ders_denemesi_ekle') and self.back_button_ders_denemesi_ekle:
            self.back_button_ders_denemesi_ekle.deleteLater()
            

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        ogrenci_ismi = self.get_name_with_suffix(self.isim)

        self.student_name_label_ders_denemesi_gor = QtWidgets.QLabel(f"{ogrenci_ismi} Hangi Ders Denemesini İnceleyeceksiniz ?")
        self.student_name_label_ders_denemesi_gor.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_ders_denemesi_gor.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.ders_denemesi_gor_one_layout.addWidget(self.student_name_label_ders_denemesi_gor)
        self.stacked_widget.setCurrentWidget(self.ders_denemesi_gor_one_page)


        self.matematik_gor_button = QtWidgets.QPushButton("Matematik")
        self.matematik_gor_button.setStyleSheet(
            "background-color: #4caf50; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        self.matematik_gor_button.clicked.connect(lambda: self.ders_denemesi_gor_table("Matematik"))
        self.ders_denemesi_gor_one_layout.addWidget(self.matematik_gor_button)
            ###############################

            # DENEME SONUCU GÖR
        self.fen_gor_button = QtWidgets.QPushButton("Fen Bilgisi")
        self.fen_gor_button.setStyleSheet(
            "background-color: #FF6600; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        self.fen_gor_button.clicked.connect(lambda: self.ders_denemesi_gor_table("Fen Bilgisi"))
        self.ders_denemesi_gor_one_layout.addWidget(self.fen_gor_button)


        self.turkce_gor_button = QtWidgets.QPushButton("Türkçe")
        self.turkce_gor_button.setStyleSheet(
            "background-color: #9B59B6; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #9B59B6
        self.turkce_gor_button.clicked.connect(lambda: self.ders_denemesi_gor_table("Türkçe"))
        self.ders_denemesi_gor_one_layout.addWidget(self.turkce_gor_button)
            ###############################
        
        self.sosyal_gor_button = QtWidgets.QPushButton("Sosyal Bilgiler")
        self.sosyal_gor_button.setStyleSheet(
            "background-color: #DA70D6; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #DA70D6
        self.sosyal_gor_button.clicked.connect(lambda: self.ders_denemesi_gor_table("Sosyal Bilgiler"))
        self.ders_denemesi_gor_one_layout.addWidget(self.sosyal_gor_button)


        self.din_gor_button = QtWidgets.QPushButton("Din Kültürü")
        self.din_gor_button.setStyleSheet(
            "background-color: #F08080; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #DA70D6
        self.din_gor_button.clicked.connect(lambda: self.ders_denemesi_gor_table("Din Kültürü"))
        self.ders_denemesi_gor_one_layout.addWidget(self.din_gor_button)
        
        self.ingilizce_gor_button = QtWidgets.QPushButton("İngilizce")
        self.ingilizce_gor_button.setStyleSheet(
            "background-color: #C2A1B3; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
        )
        self.ingilizce_gor_button.clicked.connect(lambda: self.ders_denemesi_gor_table("İngilizce"))
        self.ders_denemesi_gor_one_layout.addWidget(self.ingilizce_gor_button)

        self.back_button_ders_denemesi_ekle = QtWidgets.QPushButton("Geri Dön")
        self.back_button_ders_denemesi_ekle.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            )
        self.back_button_ders_denemesi_ekle.clicked.connect(self.handle_back_button)
        self.ders_denemesi_gor_one_layout.addWidget(self.back_button_ders_denemesi_ekle)

    def ders_denemesi_gor_table(self, ders_ismi):

        if hasattr(self, 'student_name_label_ders_denemesi_gor_table') and self.student_name_label_ders_denemesi_gor_table:
            self.student_name_label_ders_denemesi_gor_table.setAlignment(QtCore.Qt.AlignCenter)
        
        ogrenci_id = self.current_student_id

        self.cursor.execute("""
        SELECT id, ders_ismi, sinav_ismi, dogru_sayisi, yanlis_sayisi, bos_sayisi
        FROM ders_denemeleri
        WHERE ogrenci_id = ? AND ders_ismi = ? """, (ogrenci_id, ders_ismi))

        results = self.cursor.fetchall()

        if not results:
            QtWidgets.QMessageBox.information(self, "Bilgi", f"{ders_ismi} dersine ait deneme sonucu yok.")
            return

        self.stacked_widget.setCurrentWidget(self.ders_denemesi_gor_table_page)

        # Önceki widget'ları temizle
        if hasattr(self, 'student_name_label_ders_denemesi_gor_table'):
            self.student_name_label_ders_denemesi_gor_table.deleteLater()

        if hasattr(self, 'back_button_ders_denemesi_gor_table'):
            self.back_button_ders_denemesi_gor_table.deleteLater()

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0] if result2 else "Bilinmeyen"

        ogrenci_ismi = self.get_name_with_suffix(self.isim)

        self.student_name_label_ders_denemesi_gor_table = QtWidgets.QLabel(f"{ogrenci_ismi} - {ders_ismi} Deneme Sonuçları")
        self.student_name_label_ders_denemesi_gor_table.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_ders_denemesi_gor_table.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.ders_denemesi_gor_table_layout.addWidget(self.student_name_label_ders_denemesi_gor_table)

        if hasattr(self, "exam_results_ders_denemesi_gor_table"):
            self.ders_denemesi_gor_table_layout.removeWidget(self.exam_results_ders_denemesi_gor_table)
            self.exam_results_ders_denemesi_gor_table.deleteLater()

        # QTableWidget oluştur
        self.exam_results_ders_denemesi_gor_table = QtWidgets.QTableWidget()
        self.exam_results_ders_denemesi_gor_table.setRowCount(len(results))
        self.exam_results_ders_denemesi_gor_table.setColumnCount(7)  # Puan sütunu eklendi
        self.exam_results_ders_denemesi_gor_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.exam_results_ders_denemesi_gor_table.setHorizontalHeaderLabels(["Ders İsmi", "Sınav İsmi", "Doğru", "Yanlış", "Boş", "Puan", "Sil"])

        # Stil ayarları
        self.exam_results_ders_denemesi_gor_table.setStyleSheet("""
        QTableWidget {
            background-color: #2c2f33;
            color: white;
            font-size: 14px;
            border: none;
            gridline-color: #444;
            border-radius: 10px;
        }
        QTableWidget::item {
            padding: 10px;
            border-bottom: 1px solid #444;
        }
        QHeaderView::section {
            background-color: #2c2f33;
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
        }
        """)

        for row_idx, result in enumerate(results):
            exam_id, ders_ismi, sinav_ismi, dogru_sayisi, yanlis_sayisi, bos_sayisi = result

            dogru_sayisi = int(dogru_sayisi)
            yanlis_sayisi = int(yanlis_sayisi)
            bos_sayisi = int(bos_sayisi)

            # Net hesaplama (3 yanlış 1 doğruyu götürür)
            net_sayisi = dogru_sayisi - (yanlis_sayisi * 0.25)

            # Toplam soru sayısı
            toplam_soru = dogru_sayisi + yanlis_sayisi + bos_sayisi

            # Puanı 100 üzerinden ölçeklendirme
            if toplam_soru > 0:
                puan = round((net_sayisi / toplam_soru) * 100, 2)
            else:
                puan = 0  # Hiç soru çözülmemişse puan 0

            self.exam_results_ders_denemesi_gor_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(ders_ismi))
            self.exam_results_ders_denemesi_gor_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(sinav_ismi))
            self.exam_results_ders_denemesi_gor_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(f"{dogru_sayisi}D"))
            self.exam_results_ders_denemesi_gor_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(f"{yanlis_sayisi}Y"))
            self.exam_results_ders_denemesi_gor_table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(f"{bos_sayisi}B"))
            
            puan_item = QtWidgets.QTableWidgetItem(str(puan))

            green_color = QtGui.QColor(46, 204, 113)
            red_color = QtGui.QColor(231, 76, 60)

            if puan > 80:
                puan_item.setForeground(QtGui.QBrush(green_color))
            
            else:
                puan_item.setForeground(QtGui.QBrush(red_color))

            self.exam_results_ders_denemesi_gor_table.setItem(row_idx, 5, puan_item)

            delete_button = QtWidgets.QPushButton("Sil")
            delete_button.setFixedHeight(15)  # Yüksekliği 40px olarak ayarla
            delete_button.clicked.connect(lambda _, row_idx=row_idx, exam_id=exam_id: self.delete_ders_denemesi(row_idx, exam_id))
            self.exam_results_ders_denemesi_gor_table.setCellWidget(row_idx, 8, delete_button)
            delete_button.setStyleSheet("background-color: #ff4747")

            self.exam_results_ders_denemesi_gor_table.setCellWidget(row_idx, 6, delete_button)  # Sil butonu son sütunana

        self.ders_denemesi_gor_table_layout.addWidget(self.exam_results_ders_denemesi_gor_table)

        # Geri dön butonu
        self.back_button_ders_denemesi_gor_table = QtWidgets.QPushButton("Geri Dön")
        self.back_button_ders_denemesi_gor_table.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px; font-size: 16px; color: white;"
        )
        self.ders_denemesi_gor_table_layout.addWidget(self.back_button_ders_denemesi_gor_table)
        self.back_button_ders_denemesi_gor_table.clicked.connect(self.handle_back_button)

    def delete_ders_denemesi(self, row_idx, exam_id):
    # Show a confirmation dialog before deleting
        reply = QtWidgets.QMessageBox.question(self, 'Silme Onayı', 'Bu denemeyi silmek istediğinizden emin misiniz?', 
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # Delete the record from the database
            self.cursor.execute("DELETE FROM ders_denemeleri WHERE id = ?", (exam_id,))
            self.conn.commit()

            # Remove the row from the table
            self.exam_results_ders_denemesi_gor_table.removeRow(row_idx)

            # If the table is empty, show a message and navigate to the previous page
            if self.exam_results_ders_denemesi_gor_table.rowCount() == 0:
                QtWidgets.QMessageBox.information(self, "Bilgi", "Tüm denemeler silindi.")
                self.stacked_widget.setCurrentWidget(self.ders_denemesi_gor_one_page)  # Go back page

            else:
                # Force table view update
                self.exam_results_ders_denemesi_gor_table.viewport().update()

    def haftalik(self):
        if hasattr(self, 'student_name_label_haftalik_soru') and self.student_name_label_haftalik_soru:
            self.student_name_label_haftalik_soru.deleteLater()
        
        if hasattr(self, 'ocak_buton') and self.ocak_buton:
            self.ocak_buton.deleteLater()

        if hasattr(self, 'subat_buton') and self.subat_buton:
            self.subat_buton.deleteLater()

        if hasattr(self, 'mart_buton') and self.mart_buton:
            self.mart_buton.deleteLater()

        if hasattr(self, 'nisan_buton') and self.nisan_buton:
            self.nisan_buton.deleteLater()

        if hasattr(self, 'mayis_buton') and self.mayis_buton:
            self.mayis_buton.deleteLater()

        if hasattr(self, 'haziran_buton') and self.haziran_buton:
            self.haziran_buton.deleteLater()

        if hasattr(self, 'temmuz_buton') and self.temmuz_buton:
            self.temmuz_buton.deleteLater()

        if hasattr(self, 'agustos_buton') and self.agustos_buton:
            self.agustos_buton.deleteLater()

        if hasattr(self, 'eylul_buton') and self.eylul_buton:
            self.eylul_buton.deleteLater()

        if hasattr(self, 'ekim_buton') and self.ekim_buton:
            self.ekim_buton.deleteLater()

        if hasattr(self, 'kasim_buton') and self.kasim_buton:
            self.kasim_buton.deleteLater()

        if hasattr(self, 'aralik_buton') and self.aralik_buton:
            self.aralik_buton.deleteLater()

        if hasattr(self, 'back_button_haftalik_soru_ekle') and self.back_button_haftalik_soru_ekle:
            self.back_button_haftalik_soru_ekle.deleteLater()

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        self.cursor.execute("SELECT id FROM students WHERE name = ?", (self.isim,)) # nameem sayesinde id yi alıyour
        result = self.cursor.fetchone()
        self.current_student_id = result[0]
        print(self.current_student_id)

        ogrenci_ismi = self.get_name_with_suffix(self.isim)

        self.student_name_label_haftalik_soru = QtWidgets.QLabel(f"{ogrenci_ismi} Haftalık Soru Sayısını Ekle")
        self.student_name_label_haftalik_soru.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_haftalik_soru.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.haftalik_soru_ekle_one_layout.addWidget(self.student_name_label_haftalik_soru)
        self.stacked_widget.setCurrentWidget(self.haftalik_soru_ekle_one_page)

        self.ocak_buton = self.create_button("Ocak", lambda: self.haftalik_two("ocak"), "#5DADE2")
        self.haftalik_soru_ekle_one_layout.addWidget(self.ocak_buton)
        
        self.subat_buton = self.create_button("Şubat", lambda: self.haftalik_two("subat"), "#AF7AC5")
        self.haftalik_soru_ekle_one_layout.addWidget(self.subat_buton)
        
        self.mart_buton = self.create_button("Mart", lambda: self.haftalik_two("mart"), "#58D68D")
        self.haftalik_soru_ekle_one_layout.addWidget(self.mart_buton)
        
        self.nisan_buton = self.create_button("Nisan", lambda: self.haftalik_two("nisan"), "#F4D03F")
        self.haftalik_soru_ekle_one_layout.addWidget(self.nisan_buton)
        
        self.mayis_buton = self.create_button("Mayıs", lambda: self.haftalik_two("mayis"), "#45B39D")
        self.haftalik_soru_ekle_one_layout.addWidget(self.mayis_buton)

        self.haziran_buton = self.create_button("Haziran", lambda: self.haftalik_two("haziran"), "#F1948A")
        self.haftalik_soru_ekle_one_layout.addWidget(self.haziran_buton)

        self.temmuz_buton = self.create_button("Temmuz", lambda: self.haftalik_two("temmuz"), "#EC7063")
        self.haftalik_soru_ekle_one_layout.addWidget(self.temmuz_buton)

        self.agustos_buton = self.create_button("Ağustos", lambda: self.haftalik_two("agustos"), "#F39C12")
        self.haftalik_soru_ekle_one_layout.addWidget(self.agustos_buton)

        self.eylul_buton = self.create_button("Eylül", lambda: self.haftalik_two("eylul"), "#DC7633")
        self.haftalik_soru_ekle_one_layout.addWidget(self.eylul_buton)

        self.ekim_buton = self.create_button("Ekim", lambda: self.haftalik_two("ekim"), "#D35400")
        self.haftalik_soru_ekle_one_layout.addWidget(self.ekim_buton)

        self.kasim_buton = self.create_button("Kasım", lambda: self.haftalik_two("kasim"), "#873600")
        self.haftalik_soru_ekle_one_layout.addWidget(self.kasim_buton)

        self.aralik_buton = self.create_button("Aralık", lambda: self.haftalik_two("aralik"), "#7FB3D5")
        self.haftalik_soru_ekle_one_layout.addWidget(self.aralik_buton)

        self.back_button_haftalik_soru_ekle = QtWidgets.QPushButton("Geri Dön")
        self.back_button_haftalik_soru_ekle.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            )
        self.back_button_haftalik_soru_ekle.clicked.connect(self.handle_back_button)
        self.haftalik_soru_ekle_one_layout.addWidget(self.back_button_haftalik_soru_ekle)

    def haftalik_two(self, ay):
        if hasattr(self, 'student_name_label_haftalik_soru_two') and self.student_name_label_haftalik_soru_two:
            self.student_name_label_haftalik_soru_two.deleteLater()
        
        if hasattr(self, 'birinci_hafta') and self.birinci_hafta:
            self.birinci_hafta.deleteLater()

        if hasattr(self, 'ikinci_hafta') and self.ikinci_hafta:
            self.ikinci_hafta.deleteLater()

        if hasattr(self, 'ucuncu_hafta') and self.ucuncu_hafta:
            self.ucuncu_hafta.deleteLater()

        if hasattr(self, 'dorduncu_hafta') and self.dorduncu_hafta:
            self.dorduncu_hafta.deleteLater()

        if hasattr(self, 'back_button_haftalik_soru_ekle_two') and self.back_button_haftalik_soru_ekle_two:
            self.back_button_haftalik_soru_ekle_two.deleteLater()

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        self.cursor.execute("SELECT id FROM students WHERE name = ?", (self.isim,)) # nameem sayesinde id yi alıyour
        result = self.cursor.fetchone()
        self.current_student_id = result[0]
        print(self.current_student_id)

        ogrenci_ismi = self.get_name_with_suffix(self.isim)
        self.selected_month = ay

        self.student_name_label_haftalik_soru_two = QtWidgets.QLabel(f"{ogrenci_ismi} Kaçıncı Haftaya Ekliceksiniz ?")
        self.student_name_label_haftalik_soru_two.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_haftalik_soru_two.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.haftalik_soru_ekle_two_layout.addWidget(self.student_name_label_haftalik_soru_two)
        self.stacked_widget.setCurrentWidget(self.haftalik_soru_ekle_two_page)

        self.birinci_hafta = self.create_button("Birinci Hafta", lambda: self.haftalik_dersler("birinci"), "#5DADE2")
        self.haftalik_soru_ekle_two_layout.addWidget(self.birinci_hafta)
        
        self.ikinci_hafta = self.create_button("İkinci Hafta", lambda: self.haftalik_dersler("ikinci"), "#AF7AC5")
        self.haftalik_soru_ekle_two_layout.addWidget(self.ikinci_hafta)
        
        self.ucuncu_hafta = self.create_button("Üçüncü Hafta", lambda: self.haftalik_dersler("ucuncu"), "#58D68D")
        self.haftalik_soru_ekle_two_layout.addWidget(self.ucuncu_hafta)
        
        self.dorduncu_hafta = self.create_button("Dördüncü Hafta", lambda: self.haftalik_dersler("dorduncu"), "#F4D03F")
        self.haftalik_soru_ekle_two_layout.addWidget(self.dorduncu_hafta)

        self.back_button_haftalik_soru_ekle_two = QtWidgets.QPushButton("Geri Dön")
        self.back_button_haftalik_soru_ekle_two.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            )
        self.back_button_haftalik_soru_ekle_two.clicked.connect(self.handle_back_button)
        self.haftalik_soru_ekle_two_layout.addWidget(self.back_button_haftalik_soru_ekle_two)

    def haftalik_dersler(self, hafta):
        if hasattr(self, 'student_name_label_ders_denemesi_ekle_dersler') and self.student_name_label_ders_denemesi_ekle_dersler:
            self.student_name_label_ders_denemesi_ekle_dersler.deleteLater()
    
        if hasattr(self, 'matematik_button') and self.matematik_button:
            self.matematik_button.deleteLater()

        if hasattr(self, 'fen_button') and self.fen_button:
            self.fen_button.deleteLater()

        if hasattr(self, 'turkce_button') and self.turkce_button:
            self.turkce_button.deleteLater()

        if hasattr(self, 'sosyal_button') and self.sosyal_button:
            self.sosyal_button.deleteLater()

        if hasattr(self, 'din_button') and self.din_button:
            self.din_button.deleteLater()

        if hasattr(self, 'ingilizce_button') and self.ingilizce_button:
            self.ingilizce_button.deleteLater()

        if hasattr(self, 'back_button_ders_denemesi_ekle') and self.back_button_ders_denemesi_ekle:
            self.back_button_ders_denemesi_ekle.deleteLater()
            
        self.selected_week = hafta

        print(self.selected_week)
        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        ogrenci_ismi = self.get_name_with_suffix(self.isim)

        self.student_name_label_ders_denemesi_ekle_dersler = QtWidgets.QLabel(f"{ogrenci_ismi} Hangi Derse Ekliceksiniz ?")
        self.student_name_label_ders_denemesi_ekle_dersler.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_ders_denemesi_ekle_dersler.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.haftalik_soru_ekle_dersler_layout.addWidget(self.student_name_label_ders_denemesi_ekle_dersler)
        self.stacked_widget.setCurrentWidget(self.haftalik_soru_ekle_dersler_page)

        self.matematik_button = QtWidgets.QPushButton("Matematik")
        self.matematik_button.setStyleSheet(
            "background-color: #4caf50; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        self.matematik_button.clicked.connect(lambda: self.haftalik_soru_ekle_func(1, "Matematik"))
        self.haftalik_soru_ekle_dersler_layout.addWidget(self.matematik_button)
            ###############################

            # DENEME SONUCU GÖR
        self.fen_button = QtWidgets.QPushButton("Fen Bilgisi")
        self.fen_button.setStyleSheet(
            "background-color: #FF6600; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        self.fen_button.clicked.connect(lambda: self.haftalik_soru_ekle_func(2, "Fen Bilgisi"))
        self.haftalik_soru_ekle_dersler_layout.addWidget(self.fen_button)

        self.turkce_button = QtWidgets.QPushButton("Türkçe")
        self.turkce_button.setStyleSheet(
            "background-color: #9B59B6; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #9B59B6
        self.turkce_button.clicked.connect(lambda: self.haftalik_soru_ekle_func(3, "Türkçe"))
        self.haftalik_soru_ekle_dersler_layout.addWidget(self.turkce_button)
            ###############################
        
        self.sosyal_button = QtWidgets.QPushButton("Sosyal Bilgiler")
        self.sosyal_button.setStyleSheet(
            "background-color: #DA70D6; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #DA70D6
        self.sosyal_button.clicked.connect(lambda: self.haftalik_soru_ekle_func(4, "Sosyal Bilgiler"))
        self.haftalik_soru_ekle_dersler_layout.addWidget(self.sosyal_button)


        self.din_button = QtWidgets.QPushButton("Din Kültürü")
        self.din_button.setStyleSheet(
            "background-color: #F08080; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
            )
        
        #DA70D6
        self.din_button.clicked.connect(lambda: self.haftalik_soru_ekle_func(5, "Din Kültürü"))
        self.haftalik_soru_ekle_dersler_layout.addWidget(self.din_button)
        
        self.ingilizce_button = QtWidgets.QPushButton("İngilizce")
        self.ingilizce_button.setStyleSheet(
            "background-color: #C2A1B3; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: black; color: #ffffff"
        )
        self.ingilizce_button.clicked.connect(lambda: self.haftalik_soru_ekle_func(6, "İngilizce"))
        self.haftalik_soru_ekle_dersler_layout.addWidget(self.ingilizce_button)

        self.back_button_ders_denemesi_ekle = QtWidgets.QPushButton("Geri Dön")
        self.back_button_ders_denemesi_ekle.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            )
        self.back_button_ders_denemesi_ekle.clicked.connect(self.handle_back_button)
        self.haftalik_soru_ekle_dersler_layout.addWidget(self.back_button_ders_denemesi_ekle)

    def haftalik_soru_ekle_func(self, ders_id, ders_adi):
    # Yeni bir dialog penceresi oluşturuluyor
        
        ay = self.selected_month
        hafta = self.selected_week
        
        edited_ay = ""
        edited_hafta = ""

        if ay == "ocak":
            edited_ay = "Ocak"

        elif ay == "subat":
            edited_ay = "Şubat"

        elif ay == "mart":
            edited_ay = "Mart"

        elif ay == "nisan":
            edited_ay = "Nisan"

        elif ay == "mayis":
            edited_ay = "Mayıs"

        elif ay == "haziran":
            edited_ay = "Haziran"

        elif ay == "temmuz":
            edited_ay = "Temmuz"

        elif ay == "agustos":
            edited_ay = "Ağustos"

        elif ay == "eylul":
            edited_ay = "Eylül"

        elif ay == "ekim":
            edited_ay = "Ekim"

        elif ay == "kasim":
            edited_ay = "Kasım"

        elif ay == "aralik":
            edited_ay = "Aralık"

        else:
            edited_ay = ay

        if hafta == "birinci":
            edited_hafta = "birinci"

        elif hafta == "ikinci":
            edited_hafta = "ikinci"

        elif hafta == "ucuncu":
            edited_hafta = "üçüncü"

        elif hafta == "dorduncu":
            edited_hafta = "dördüncü"

        else:
            edited_hafta = hafta

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"{ders_adi} - Yeni Deneme Sonucu Ekle")

        form_layout = QtWidgets.QFormLayout(dialog)

        # Ders adı QLabel olarak eklendi
        ders_adi_label = QtWidgets.QLabel(ders_adi, dialog)
        ay_label = QtWidgets.QLabel(edited_ay, dialog)

        if edited_hafta == "ikinci":
            hafta_label = QtWidgets.QLabel("İkinci", dialog)

        else:
            hafta_label = QtWidgets.QLabel(edited_hafta.capitalize(), dialog)


        # Doğru, Yanlış ve Boş sayıları için giriş kutuları
        dogru_sayisi = QtWidgets.QLineEdit(dialog)
        yanlis_sayisi = QtWidgets.QLineEdit(dialog)
        bos_sayisi = QtWidgets.QLineEdit(dialog)

        # Formu dolduruyoruz
        form_layout.addRow("Ay:", ay_label)
        form_layout.addRow("Hafta:", hafta_label)
        form_layout.addRow("Ders Adı:", ders_adi_label)
        form_layout.addRow("Doğru Sayısı:", dogru_sayisi)
        form_layout.addRow("Yanlış Sayısı:", yanlis_sayisi)
        form_layout.addRow("Boş Sayısı:", bos_sayisi)

        # OK ve Cancel butonları ekliyoruz
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, dialog)
        form_layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        # Dialog penceresini göster
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
    # Kullanıcıdan alınan verileri alıyoruz
            values = [
                ders_adi_label.text(),
                dogru_sayisi.text(),
                yanlis_sayisi.text(),
                bos_sayisi.text()
            ]

            # Eğer tüm alanlar doluysa veriyi işliyoruz
            if all(values):  # Boş alan bırakılmaması için kontrol
                ders_adi, dogru, yanlis, bos = values  # Verileri ayırıyoruz

                # Sayısal veri kontrolü (sadece rakam girildiğinden emin olalım)
                if not (dogru.isdigit() and yanlis.isdigit() and bos.isdigit()):
                    QtWidgets.QMessageBox.warning(self, "Hata", "Doğru, Yanlış ve Boş sayıları sadece rakam olmalıdır!")
                    return  # Hata durumunda ekleme işlemini durdur

                # String verileri integer'a çevir
                dogru = int(dogru)
                yanlis = int(yanlis)
                bos = int(bos)

                ogrenci_id = self.current_student_id

                # Veritabanına ekleme
                self.cursor.execute("""
                    INSERT INTO haftalik_soru (ogrenci_id, ders_id, ders_ismi, ay, hafta, dogru_sayisi, yanlis_sayisi, bos_sayisi) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (ogrenci_id, ders_id, ders_adi, ay, hafta, dogru, yanlis, bos))  
                self.conn.commit()

                ogrenci_ismi = self.get_name_with_suffix(self.isim)
                print("##", edited_ay)
                QtWidgets.QMessageBox.information(self, "Başarılı", f"{ogrenci_ismi} isimli öğrencinin {ders_adi} dersinin {edited_ay} ayının {edited_hafta} haftasına ait soru sayısı başarıyla eklendi!")

            else:
                QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.") 

    def haftalik_incele(self):
        if hasattr(self, 'student_name_label_haftalik_soru') and self.student_name_label_haftalik_soru:
            self.student_name_label_haftalik_soru.deleteLater()
        
        if hasattr(self, 'ocak_buton') and self.ocak_buton:
            self.ocak_buton.deleteLater()

        if hasattr(self, 'subat_buton') and self.subat_buton:
            self.subat_buton.deleteLater()

        if hasattr(self, 'mart_buton') and self.mart_buton:
            self.mart_buton.deleteLater()

        if hasattr(self, 'nisan_buton') and self.nisan_buton:
            self.nisan_buton.deleteLater()

        if hasattr(self, 'mayis_buton') and self.mayis_buton:
            self.mayis_buton.deleteLater()

        if hasattr(self, 'haziran_buton') and self.haziran_buton:
            self.haziran_buton.deleteLater()

        if hasattr(self, 'temmuz_buton') and self.temmuz_buton:
            self.temmuz_buton.deleteLater()

        if hasattr(self, 'agustos_buton') and self.agustos_buton:
            self.agustos_buton.deleteLater()

        if hasattr(self, 'eylul_buton') and self.eylul_buton:
            self.eylul_buton.deleteLater()

        if hasattr(self, 'ekim_buton') and self.ekim_buton:
            self.ekim_buton.deleteLater()

        if hasattr(self, 'kasim_buton') and self.kasim_buton:
            self.kasim_buton.deleteLater()

        if hasattr(self, 'aralik_buton') and self.aralik_buton:
            self.aralik_buton.deleteLater()

        if hasattr(self, 'back_button_haftalik_soru_ekle') and self.back_button_haftalik_soru_ekle:
            self.back_button_haftalik_soru_ekle.deleteLater()

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        self.cursor.execute("SELECT id FROM students WHERE name = ?", (self.isim,)) # nameem sayesinde id yi alıyour
        result = self.cursor.fetchone()
        self.current_student_id = result[0]
        print(self.current_student_id)

        ogrenci_ismi = self.get_name_with_suffix(self.isim)

        self.student_name_label_haftalik_soru = QtWidgets.QLabel(f"{ogrenci_ismi} Haftalık Soru Sayısını İncele")
        self.student_name_label_haftalik_soru.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_haftalik_soru.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.haftalik_soru_incele_one_layout.addWidget(self.student_name_label_haftalik_soru)
        self.stacked_widget.setCurrentWidget(self.haftalik_soru_incele_one_page)

        self.ocak_buton = self.create_button("Ocak", lambda: self.haftalik_incele_two("ocak"), "#5DADE2")
        self.haftalik_soru_incele_one_layout.addWidget(self.ocak_buton)
        
        self.subat_buton = self.create_button("Şubat", lambda: self.haftalik_incele_two("subat"), "#AF7AC5")
        self.haftalik_soru_incele_one_layout.addWidget(self.subat_buton)
        
        self.mart_buton = self.create_button("Mart", lambda: self.haftalik_incele_two("mart"), "#58D68D")
        self.haftalik_soru_incele_one_layout.addWidget(self.mart_buton)
        
        self.nisan_buton = self.create_button("Nisan", lambda: self.haftalik_incele_two("nisan"), "#F4D03F")
        self.haftalik_soru_incele_one_layout.addWidget(self.nisan_buton)
        
        self.mayis_buton = self.create_button("Mayıs", lambda: self.haftalik_incele_two("mayis"), "#45B39D")
        self.haftalik_soru_incele_one_layout.addWidget(self.mayis_buton)

        self.haziran_buton = self.create_button("Haziran", lambda: self.haftalik_incele_two("haziran"), "#F1948A")
        self.haftalik_soru_incele_one_layout.addWidget(self.haziran_buton)

        self.temmuz_buton = self.create_button("Temmuz", lambda: self.haftalik_incele_two("temmuz"), "#EC7063")
        self.haftalik_soru_incele_one_layout.addWidget(self.temmuz_buton)

        self.agustos_buton = self.create_button("Ağustos", lambda: self.haftalik_incele_two("agustos"), "#F39C12")
        self.haftalik_soru_incele_one_layout.addWidget(self.agustos_buton)

        self.eylul_buton = self.create_button("Eylül", lambda: self.haftalik_incele_two("eylul"), "#DC7633")
        self.haftalik_soru_incele_one_layout.addWidget(self.eylul_buton)

        self.ekim_buton = self.create_button("Ekim", lambda: self.haftalik_incele_two("ekim"), "#D35400")
        self.haftalik_soru_incele_one_layout.addWidget(self.ekim_buton)

        self.kasim_buton = self.create_button("Kasım", lambda: self.haftalik_incele_two("kasim"), "#873600")
        self.haftalik_soru_incele_one_layout.addWidget(self.kasim_buton)

        self.aralik_buton = self.create_button("Aralık", lambda: self.haftalik_incele_two("aralik"), "#7FB3D5")
        self.haftalik_soru_incele_one_layout.addWidget(self.aralik_buton)

        self.back_button_haftalik_soru_ekle = QtWidgets.QPushButton("Geri Dön")
        self.back_button_haftalik_soru_ekle.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            )
        self.back_button_haftalik_soru_ekle.clicked.connect(self.handle_back_button)
        self.haftalik_soru_incele_one_layout.addWidget(self.back_button_haftalik_soru_ekle)

    def haftalik_incele_two(self, ay):
        if hasattr(self, 'student_name_label_haftalik_soru_two') and self.student_name_label_haftalik_soru_two:
            self.student_name_label_haftalik_soru_two.deleteLater()
        
        if hasattr(self, 'birinci_hafta') and self.birinci_hafta:
            self.birinci_hafta.deleteLater()

        if hasattr(self, 'ikinci_hafta') and self.ikinci_hafta:
            self.ikinci_hafta.deleteLater()

        if hasattr(self, 'ucuncu_hafta') and self.ucuncu_hafta:
            self.ucuncu_hafta.deleteLater()

        if hasattr(self, 'dorduncu_hafta') and self.dorduncu_hafta:
            self.dorduncu_hafta.deleteLater()

        if hasattr(self, 'back_button_haftalik_soru_ekle_two') and self.back_button_haftalik_soru_ekle_two:
            self.back_button_haftalik_soru_ekle_two.deleteLater()

        self.cursor.execute("SELECT name FROM students WHERE id = ?", (self.current_student_id,))
        result2 = self.cursor.fetchone()
        self.isim = result2[0]

        self.cursor.execute("SELECT id FROM students WHERE name = ?", (self.isim,)) # nameem sayesinde id yi alıyour
        result = self.cursor.fetchone()
        self.current_student_id = result[0]
        print(self.current_student_id)

        ogrenci_ismi = self.get_name_with_suffix(self.isim)
        self.selected_month = ay

        self.student_name_label_haftalik_soru_two = QtWidgets.QLabel(f"{ogrenci_ismi} Kaçıncı Haftaya Ekliceksiniz ?")
        self.student_name_label_haftalik_soru_two.setAlignment(QtCore.Qt.AlignCenter)
        self.student_name_label_haftalik_soru_two.setStyleSheet("font-size: 24px; font-weight: bold; color: #7289da;")
        self.haftalik_soru_incele_two_layout.addWidget(self.student_name_label_haftalik_soru_two)
        self.stacked_widget.setCurrentWidget(self.haftalik_soru_incele_two_page)

        self.birinci_hafta = self.create_button("Birinci Hafta", lambda: self.haftalik_dersler("birinci"), "#5DADE2")
        self.haftalik_soru_incele_two_layout.addWidget(self.birinci_hafta)
        
        self.ikinci_hafta = self.create_button("İkinci Hafta", lambda: self.haftalik_dersler("ikinci"), "#AF7AC5")
        self.haftalik_soru_incele_two_layout.addWidget(self.ikinci_hafta)
        
        self.ucuncu_hafta = self.create_button("Üçüncü Hafta", lambda: self.haftalik_dersler("ucuncu"), "#58D68D")
        self.haftalik_soru_incele_two_layout.addWidget(self.ucuncu_hafta)
        
        self.dorduncu_hafta = self.create_button("Dördüncü Hafta", lambda: self.haftalik_dersler("dorduncu"), "#F4D03F")
        self.haftalik_soru_incele_two_layout.addWidget(self.dorduncu_hafta)

        self.back_button_haftalik_soru_ekle_two = QtWidgets.QPushButton("Geri Dön")
        self.back_button_haftalik_soru_ekle_two.setStyleSheet(
            "background-color: #ff4747; border-radius: 10px; padding: 10px;"
            "font-size: 16px; color: white;"
            )
        self.back_button_haftalik_soru_ekle_two.clicked.connect(self.handle_back_button)
        self.haftalik_soru_incele_two_layout.addWidget(self.back_button_haftalik_soru_ekle_two)

    def create_button(self, text, callback, color):
            btn = QtWidgets.QPushButton(text)
            btn.setStyleSheet(
                f"background-color: {color}; border-radius: 10px; padding: 10px; font-size: 16px; color: white;"
            )
            btn.clicked.connect(callback)
            return btn

#derse tıkladığında soru sayısını gör yapılcak

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
