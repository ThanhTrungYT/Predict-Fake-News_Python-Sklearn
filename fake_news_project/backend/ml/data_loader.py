import pandas as pd
from pathlib import Path
import json


def load_data_from_folder(folder_path, split_name=""):
    texts = []
    sources = []
    labels = []

    print(f"Đang load {split_name} từ: {folder_path}")

    for class_name in ['Fake', 'Real']:
        class_dir = Path(folder_path) / class_name

        if not class_dir.exists():
            print(f"⚠️ Không tìm thấy thư mục: {class_dir}")
            continue

        # label: Fake = 0, Real = 1
        label = 0 if class_name == "Fake" else 1

        file_count = 0

        for file_path in class_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # ⚠️ JSON của bạn là dạng list
                    if isinstance(data, list):
                        data = data[0]

                    # ===== LẤY DỮ LIỆU =====
                    title = data.get("title", "")
                    content = data.get("maintext", "")
                    source = data.get("source_domain", "")

                    # ===== COMBINE TEXT =====
                    text = (title + " " + content).strip()

                    # ===== VALID DATA =====
                    if text:
                        texts.append(text)
                        sources.append(source)
                        labels.append(label)
                        file_count += 1

            except Exception as e:
                print(f"❌ Lỗi đọc file {file_path.name}: {e}")

        print(f"   → {class_name}: {file_count} files")

    # ===== TẠO DATAFRAME =====
    df = pd.DataFrame({
        'text': texts,
        'source': sources,
        'label': labels
    })

    print(f"✅ Load {split_name} xong: {len(df)} mẫu\n")

    return df