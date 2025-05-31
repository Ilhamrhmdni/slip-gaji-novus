def create_pdf_reportlab(data, nama_file):
    try:
        c = canvas.Canvas(nama_file, pagesize=letter)
        width, height = letter
        y_offset = height - 100

        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y_offset, "SLIP GAJI KARYAWAN")
        y_offset -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y_offset, f"Periode: {data['periode']}")
        y_offset -= 40

        # Logo
        logo_path = "novus_logo.png"
        logo_rgb_path = "novus_logo_rgb.png"
        convert_png_to_rgb(logo_path, logo_rgb_path)
        if os.path.exists(logo_rgb_path):
            c.drawImage(logo_rgb_path, 450, y_offset + 30, width=100, height=50)

        # Alamat Perusahaan
        c.setFont("Helvetica", 10)
        c.drawString(450, y_offset + 20, "NOVUS Stream Lab")
        c.drawString(450, y_offset + 5, "Jl. Wijaya Kusuma No. 1 Munggut")
        c.drawString(450, y_offset - 10, "Kec. Wungu, Kab. Malang")
        c.drawString(450, y_offset - 25, "Jawa Timur 63181")
        c.drawString(450, y_offset - 40, "Email: novustreamlab@gmail.com")

        y_offset -= 60

        # Data Pribadi
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_offset, "Data Pribadi")
        y_offset -= 20
        c.setFont("Helvetica", 10)
        for key, value in data["data_pribadi"].items():
            c.drawString(50, y_offset, f"{key}: {value}")
            y_offset -= 15
        y_offset -= 10

        # Data Bank
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_offset, "Data Bank")
        y_offset -= 20
        c.setFont("Helvetica", 10)
        for key, value in data["data_bank"].items():
            c.drawString(50, y_offset, f"{key}: {value}")
            y_offset -= 15
        y_offset -= 30

        # Tabel Penghasilan & Potongan
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_offset, "PENGHASILAN")
        c.drawString(300, y_offset, "POTONGAN")
        y_offset -= 20

        row_height = 15
        col_penghasilan_x = 50
        col_penghasilan_nilai_x = 200
        col_potongan_x = 300
        col_potongan_nilai_x = 450

        penghasilan = [
            ("Gaji Pokok", data["gaji_pokok"]),
            ("Tunjangan Kinerja", data["tunjangan_kinerja"]),
            ("Tunjangan Makan", data["tunjangan_makan"]),
            ("Tunjangan Overtime", data["tunjangan_overtime"]),
            ("Tunjangan Jabatan", data["tunjangan_jabatan"]),
            ("Total Penghasilan", data["total_penghasilan"]),
        ]
        potongan = [
            ("PPh 21", data["pph21"]),
            ("BPJS Kesehatan", data["bpjs_kesehatan"]),
            ("BPJS Ketenagakerjaan", data["bpjs_ketenagakerjaan"]),
            ("Tagihan Hutang", data["tagihan_hutang1"]),
            ("Tagihan Hutang", data["tagihan_hutang2"]),
            ("Total Potongan", data["total_potongan"]),
        ]

        for i in range(len(penghasilan)):
            c.setFont("Helvetica", 10)
            c.drawString(col_penghasilan_x, y_offset, str(penghasilan[i][0]))
            c.drawString(col_penghasilan_nilai_x, y_offset, format_rupiah(penghasilan[i][1]))

            c.drawString(col_potongan_x, y_offset, str(potongan[i][0]))
            c.drawString(col_potongan_nilai_x, y_offset, format_rupiah(potongan[i][1]))

            y_offset -= row_height

        # Pembayaran
        y_offset -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_offset, "Pembayaran:")
        c.drawString(200, y_offset, format_rupiah(data["pembayaran"]))
        y_offset -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y_offset, f"Terbilang: {terbilang_rupiah(data['pembayaran'])}")

        # Tanda Tangan
        y_offset -= 60
        c.setFont("Helvetica", 10)
        c.drawString(400, y_offset, "Mengetahui,")

        signature_path = "signature.png"
        signature_rgb_path = "signature_rgb.png"
        convert_png_to_rgb(signature_path, signature_rgb_path)

        if os.path.exists(signature_rgb_path):
            c.drawImage(signature_rgb_path, 450, y_offset - 50, width=50, height=50)
        else:
            c.drawString(450, y_offset - 50, "[TTD tidak ditemukan]")

        y_offset -= 70
        c.drawString(400, y_offset, "Septian Kurnia Armando")
        c.drawString(400, y_offset - 15, "Direktur")

        c.save()

        # Hapus file sementara
        for f in [logo_rgb_path, signature_rgb_path]:
            if os.path.exists(f):
                os.remove(f)

    except Exception as e:
        log_exception(e, "Gagal membuat PDF slip gaji")
        raise
