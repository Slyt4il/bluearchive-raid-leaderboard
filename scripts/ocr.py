import easyocr
import os
import re
import cv2

raw_data_dir = "raw_data\S44_Hieronymus_Urban"
file_set = set()

reader = easyocr.Reader(['en'])
reader_ja = easyocr.Reader(['ja'])
reader_ch_tra = easyocr.Reader(['ch_tra'])
reader_ko = easyocr.Reader(['ko'])
reader_th = easyocr.Reader(['th'])

def read_names(roi):
    names = []
    names.append(reader.readtext(roi, detail=1))
    names.append(reader_ja.readtext(roi, detail=1))
    names.append(reader_ch_tra.readtext(roi, detail=1))
    names.append(reader_ko.readtext(roi, detail=1))
    names.append(reader_th.readtext(roi, detail=1))

    max_confidence = 0
    max_name = ''
    for name in names:
        if not name:
            continue
        confidence = name[0][2]
        if confidence > max_confidence:
            max_name = name[0][1]
            max_confidence = confidence

    return re.sub(r'[\[<!,*)@#%(&$_?.^:;\'">\]]', '', max_name)

def extract_info(im, roi):
    result = reader.readtext(im, paragraph=False ,detail=0)
    name_result = read_names(roi)

    rank = re.search(r'([\d,oO]+)', result[0])
    rank = rank.group(1).replace('o', '0').replace('O', '0') if rank else '???'

    difficulty = re.search(r'(Normal|Hard|Very Hard|Hardcore|Extreme|Insane|Torment).*', result[1])
    difficulty = difficulty.group(1) if difficulty else '???'

    score_idx = 1
    score = re.search(r'([\d,]+)', result[score_idx])
    if score:
        score = score.group(1).replace(',', '')
    else:
        score_idx += 1
        score = re.search(r'([\d,]+)', result[score_idx])
        score = score.group(1).replace(',', '') if score else '???'

    level = re.search(r'Lv.(\d+)', result[-1])
    level = level.group(1) if level else '???'

    name = name_result if name_result else '???'

    return rank, difficulty, score, name, level

for root, dirs, files in os.walk(raw_data_dir):
    for fileName in files:
        file_set.add( os.path.join( root[len(raw_data_dir):], fileName))

extracted_data = []
count = 0
for file in file_set:
    count += 1
    print(f"File {count}/{len(file_set)}".ljust(50), end='\r')
    im = cv2.imread(os.path.join(raw_data_dir, file))
    name_roi = im[85:118, 0:226]
    rank, difficulty, score, name, level = extract_info(im, name_roi)
    extracted_data.append([rank, difficulty, score, name, level])

extracted_data = sorted(extracted_data, key=lambda x: int(x[0]))

with open("S44_Hieronymus_Urban_ASIA_TOP10000.csv", "w", encoding='utf-8') as csv_file:
    csv_file.write("Rank,Difficulty,Score,Name,Level\n")
    for line in extracted_data:
        rank = line[0]
        difficulty = line[1]
        score = line[2]
        name = line[3]
        level = line[4]
        
        csv_file.write(f"{rank},{difficulty},{score},{name},{level}\n")

print("CSV file has been created.")
