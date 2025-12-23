import json

# =========================
# CONFIG
# =========================
INPUT_JSON = "college_documents_updated.json"
OUTPUT_JSON = "engineering_invalid_courses.json"
TARGET_DEPARTMENT = "Engineering And Technology"


# =========================
# LOAD JSON
# =========================
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    colleges = json.load(f)


# =========================
# FILTER INVALID COURSES
# =========================
invalid_colleges = []

for college in colleges:
    department = college.get("department")

    if not department:
        continue

    if department.get("name") != TARGET_DEPARTMENT:
        continue

    if college.get("is_approved_course") is False:
        invalid_colleges.append(college)


# =========================
# SAVE JSON
# =========================
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(invalid_colleges, f, indent=2, ensure_ascii=False)


print("✅ Export completed")
print(f"📄 Invalid Engineering courses saved to: {OUTPUT_JSON}")
print(f"🔢 Total invalid colleges: {len(invalid_colleges)}")
