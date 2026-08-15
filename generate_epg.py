import datetime

def generate_xmltv():
    # Define a rough estimated schedule loop for 24 hours
    # Format: (start_hour, start_minute, duration_hours, title, desc)
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
    
    start_date = datetime.date.today()
    xml_lines = []
    xml_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml_lines.append('<!DOCTYPE tv SYSTEM "xmltv.dtd">')
    xml_lines.append('<tv generator-info-name="GMS-EPG-Github-Action">')
    xml_lines.append('  <channel id="GMS.Channel.TV">')
    xml_lines.append('    <display-name lang="id">GMS Channel TV</display-name>')
    xml_lines.append('  </channel>')
    
    # Generate for 7 days
    for i in range(7):
        current_day = start_date + datetime.timedelta(days=i)
        for start_h, start_m, duration, title, desc in daily_slots:
            # Construct start time
            start_dt = datetime.datetime.combine(current_day, datetime.time(start_h, start_m))
            end_dt = start_dt + datetime.timedelta(hours=duration)
            
            start_str = start_dt.strftime("%Y%m%d%H%M%S") + " +0700"
            end_str = end_dt.strftime("%Y%m%d%H%M%S") + " +0700"
            
            xml_lines.append(f'  <programme start="{start_str}" stop="{end_str}" channel="GMS.Channel.TV">')
            xml_lines.append(f'    <title lang="id">{title}</title>')
            xml_lines.append(f'    <desc lang="id">{desc}</desc>')
            xml_lines.append('  </programme>')
            
    xml_lines.append('</tv>')
    
    with open("gms_channel_epg.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))
    print("EPG successfully generated!")

if __name__ == "__main__":
    generate_xmltv()
