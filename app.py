from gaji import generate_slip_gaji_pdf

# setelah form disubmit
if submitted:
    data = {
        'nama': nama,
        'alamat': alamat,
        'telp': telp,
        'divisi': divisi,
        'jabatan': jabatan,
        'bank': bank,
        'rekening': rekening,
        'periode': periode,
        'gaji_pokok': gaji_pokok,
        'tunj_kin': tunj_kin,
        'tunj_makan': tunj_makan,
        'tunj_lembur': tunj_lembur,
        'tunj_jabatan': tunj_jabatan,
        'pph21': pph21,
        'bpjs_kes': bpjs_kes,
        'bpjs_kerja': bpjs_kerja,
        'hutang1': hutang1,
        'hutang2': hutang2,
    }

    pdf = generate_slip_gaji_pdf(data)
    st.download_button("Download PDF", data=pdf, file_name=f"Slip Gaji {nama}.pdf", mime="application/pdf")
