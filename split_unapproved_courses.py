import json

# =========================
# CONFIG
# =========================
INPUT_JSON = "college_documents_updated.json"
APPROVED_OUTPUT_JSON = "approved_colleges.json"
UNAPPROVED_OUTPUT_JSON = "unapproved_courses.json"


# =========================
# LOAD DATA
# =========================
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    colleges = json.load(f)


# =========================
# SPLIT DATA
# =========================
approved_colleges = []
unapproved_colleges = []

for college in colleges:
    if college.get("is_approved_course") is False:
        unapproved_colleges.append(college)
    else:
        approved_colleges.append(college)


# =========================
# SAVE APPROVED COLLEGES
# =========================
with open(APPROVED_OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(approved_colleges, f, indent=2, ensure_ascii=False)


# =========================
# SAVE UNAPPROVED COURSES
# =========================
with open(UNAPPROVED_OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(unapproved_colleges, f, indent=2, ensure_ascii=False)


print("✅ Splitting completed successfully")
print(f"✔ Approved colleges saved to: {APPROVED_OUTPUT_JSON}")
print(f"❌ Unapproved courses saved to: {UNAPPROVED_OUTPUT_JSON}")
print(f"🔢 Unapproved count: {len(unapproved_colleges)}")
