import datetime
import os

def generate_xmltv():
    # Daftar susunan acara asli milik Anda
    daily_slots = [
        (0, 0, 2, "Menara Doa Malam", "Saat teduh dan doa malam bersama GMS Church."),
        (2, 0, 3, "Pujian & Penyembahan", "Lagu-lagu pujian dan penyembahan non-stop GMS Worship."),
        (5, 0, 1, "Saat Teduh Fajar", "Renungan firman Tuhan dan doa memulai hari."),
        (6, 0, 2, "Eagle Kidz & Voltage", "Ibadah dan pengajaran firman kreatif untuk anak-anak dan remaja."),
        (8, 0, 2, "GMS Sunday Service (Replay)", "Siaran ulang ibadah umum mingguan Gereja Mawar Sharon."),
        (10, 0, 2, "Khotbah Ps. Philip Mantofa", "Seri pengajaran Alkitab dan pesan rohani mendalam oleh Pastor Philip Mantofa."),
        (12, 0, 2, "GMS Worship Session", "Dokumenter, klip musik, dan kesaksian di balik lagu-lagu GMS Worship."),
        (14, 0, 2, "Army of God Youth", "Ibadah pemuda dan remaja dengan pesan yang relevan bagi generasi muda."),
        (16, 0, 2, "GMS Sunday Service (Replay)", "Siaran ulang ibadah umum mingguan Gereja Mawar Sharon."),
        (18, 0, 2, "Khotbah Ps. Philip Mantofa", "Seri pengajaran Alkitab dan pesan rohani mendalam oleh Pastor Philip Mantofa."),
        (20, 0, 2, "Talkshow & Conference Snippets", "Bincang-bincang rohani dan cuplikan seminar/konferensi GMS."),
        (22, 0, 2, "Menara Doa Malam", "Saat teduh dan doa malam bersama GMS Church.")
    ]
    
    # 1. Deteksi otomatis lokasi file guide.xml hasil grab Node.js
    xml_path = 'public/guide.xml'
    if not os.path.exists(xml_path):
        xml_path = '../public/guide.xml'  # Keluar satu folder jika dijalankan dari my-config

    if not os.path.exists(xml_path):
        print(f"Error: Berkas target guide.xml tidak ditemukan!")
        return

    # 2. Baca seluruh isi konten file guide.xml asli
    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # 3. Buat baris teks XML baru khusus untuk saluran dan jadwal GMS
    gms_lines = []
    
    # Tambahkan channel GMS jika belum terdaftar di dalam berkas asli
    if 'id="GMS.Channel.TV"' not in xml_content:
        gms_lines.append('  <channel id="GMS.Channel.TV">')
        gms_lines.append('    <display-name lang="id">GMS Channel TV</display-name>')
        gms_lines.append('  </channel>')
    
    # Generate otomatis mengikuti rentang 3 hari agar sinkron dengan parameter workflow Anda
    start_date = datetime.date.today()
    for i in range(3):
        current_day = start_date + datetime.timedelta(days=i)
        for start_h, start_m, duration, title, desc in daily_slots:
            start_dt = datetime.datetime.combine(current_day, datetime.time(start_h, start_m))
            end_dt = start_dt + datetime.timedelta(hours=duration)
            
            start_str = start_dt.strftime("%Y%m%d%H%M%S") + " +0700"
            end_str = end_dt.strftime("%Y%m%d%H%M%S") + " +0700"
            
            gms_lines.append(f'  <programme start="{start_str}" stop="{end_str}" channel="GMS.Channel.TV">')
            gms_lines.append(f'    <title lang="id">{title}</title>')
            gms_lines.append(f'    <desc lang="id">{desc}</desc>')
            gms_lines.append('  </programme>')

    # 4. Cari posisi tag penutup </tv> lalu sisipkan jadwal GMS tepat sebelum tag tersebut
    gms_injection_text = "\n".join(gms_lines) + "\n"
    if "</tv>" in xml_content:
        # Ganti tag penutup </tv> dengan gabungan teks jadwal baru + tag penutup kembali
        updated_xml_content = xml_content.replace("</tv>", gms_injection_text + "</tv>")
    else:
        print("Error: Tag penutup </tv> tidak ditemukan di berkas asli!")
        return

    # 5. Tulis ulang hasil penggabungan ke dalam berkas public/guide.xml
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(updated_xml_content)
        
    print("Jadwal GMS Channel sukses disuntikkan ke dalam berkas gabungan guide.xml!")

if __name__ == "__main__":
    generate_xmltv()
