import json
import pandas as pd
import re

# =========================
# CONFIG
# =========================
COLLEGE_JSON_FILE = "college_documents.json"
NOMENCLATURE_EXCEL_FILE = "Approved_Nomenclature_of_Courses.xlsx"
OUTPUT_JSON_FILE = "college_documents_updated.json"

EXCEL_COLUMN_NAME = "Approved Nomenclature of Courses"
TARGET_DEPARTMENT = "Engineering And Technology"


# =========================
# NORMALIZE COURSE ONLY
# =========================
def normalize_course(text):
    if not text:
        return ""

    text = text.upper()

    # Replace common abbreviations / symbols
    text = re.sub(r"\bENGG\b|\bENGG\.\b", "ENGINEERING", text)
    text = text.replace("&", "AND")

    # Remove all non-alphanumeric characters
    text = re.sub(r"[^A-Z0-9]", "", text)

    return text


# =========================
# LOAD APPROVED COURSES
# =========================
df = pd.read_excel(NOMENCLATURE_EXCEL_FILE)

approved_courses = {
    normalize_course(course)
    for course in df[EXCEL_COLUMN_NAME].dropna()
}


# =========================
# LOAD COLLEGE DATA
# =========================
with open(COLLEGE_JSON_FILE, "r", encoding="utf-8") as f:
    colleges = json.load(f)


# =========================
# PROCESS ONLY ENGINEERING
# =========================
for college in colleges:
    department = college.get("department")

    if not department:
        continue

    # EXACT department match (as requested)
    if department.get("name") != TARGET_DEPARTMENT:
        continue

    course_name = department.get("course", "")
    normalized_course = normalize_course(course_name)

    # Write field ONLY for Engineering
    college["is_approved_course"] = normalized_course in approved_courses


# =========================
# SAVE OUTPUT
# =========================
with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(colleges, f, indent=2, ensure_ascii=False)

print("✅ Engineering & Technology courses validated with improved normalization")


# import json
# import pandas as pd
# import re

# # =========================
# # CONFIG
# # =========================
# COLLEGE_JSON_FILE = "college_documents.json"
# NOMENCLATURE_EXCEL_FILE = "Approved_Nomenclature_of_Courses.xlsx"
# OUTPUT_JSON_FILE = "college_documents_updated.json"

# EXCEL_COLUMN_NAME = "Approved Nomenclature of Courses"
# TARGET_DEPARTMENT = "ENGINEERING AND TECHNOLOGY"


# # =========================
# # NORMALIZATION
# # =========================
# def normalize_course(text):
#     if not text:
#         return ""
#     text = text.upper()
#     text = re.sub(r"[^A-Z0-9]", "", text)  # remove spaces, hyphens, symbols
#     return text


# # =========================
# # LOAD APPROVED COURSES
# # =========================
# df = pd.read_excel(NOMENCLATURE_EXCEL_FILE)

# approved_courses = set(
#     normalize_course(course)
#     for course in df[EXCEL_COLUMN_NAME].dropna()
# )

# print(f"✅ Loaded {len(approved_courses)} approved courses")


# # =========================
# # LOAD COLLEGE DATA
# # =========================
# with open(COLLEGE_JSON_FILE, "r", encoding="utf-8") as f:
#     colleges = json.load(f)


# # =========================
# # PROCESS COLLEGES
# # =========================
# for college in colleges:
#     department = college.get("department", {})

#     dept_name = department.get("name", "").upper().strip()
#     course_name = department.get("course", "")

#     normalized_course = normalize_course(course_name)

#     # Default
#     college["is_approved_course"] = False

#     if dept_name == TARGET_DEPARTMENT and normalized_course:
#         if normalized_course in approved_courses:
#             college["is_approved_course"] = True


# # =========================
# # SAVE OUTPUT
# # =========================
# with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
#     json.dump(colleges, f, indent=2, ensure_ascii=False)

# print("🎯 Course validation completed")
# print(f"📄 Output saved as: {OUTPUT_JSON_FILE}")
