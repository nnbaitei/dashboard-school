import json
import urllib.request



school_url = "https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json"
with urllib.request.urlopen(school_url) as url:
    sdata = json.loads(url.read().decode())

thai_url = "https://raw.githubusercontent.com/chingchai/OpenGISData-Thailand/master/provinces.geojson"
with urllib.request.urlopen(thai_url) as url:
    jdata = json.loads(url.read().decode())


# สร้าง dictionary สำหรับเก็บข้อมูลจาก file1 โดยใช้ schools_province เป็น key
file1_dict = {item['schools_province']: item for item in sdata}

# วนลูปใน features ของ file2 เพื่อตรวจสอบ schools_province และเพิ่ม student จาก file1 ลงใน properties ของ feature ที่ match
for feature in jdata['features']:
    if 'properties' in feature and 'pro_th' in feature['properties']:
        pro_th = feature['properties']['pro_th']
        if pro_th in file1_dict:
            file1_data = file1_dict[pro_th]
            feature['properties']['student'] = file1_data

# เขียนข้อมูลที่แก้ไขแล้วออกไปเป็นไฟล์ JSON ใหม่
with open('merged_file.json', 'w', encoding='utf-8') as file:
    json.dump(jdata, file, indent=4, ensure_ascii=False)

