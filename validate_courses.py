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

    # Replace & with AND
    text = text.replace("&", "AND")

    # Fix spelling mistakes
    text = re.sub(r"SCEINCE|SCINCE", "SCIENCE", text)

    # Handle Artificial Intelligence & Data Science variations
    if (
        "ARTIFICIAL" in text
        and "INTELLIGENCE" in text
        and "DATA" in text
        and "SCIENCE" in text
    ):
        return "ARTIFICIALINTELLIGENCEANDDATASCIENCE"

    # Extract content inside brackets if present
    bracket_match = re.search(r"\((.*?)\)", text)
    if bracket_match:
        text = bracket_match.group(1)

    # Remove degree prefixes
    text = re.sub(
        r"\b(B\.?TECH|BTECH|B\.?E|BE|BACHELOR OF TECHNOLOGY|BACHELOR OF ENGINEERING)\b",
        "",
        text
    )

    # Normalize ENGG to ENGINEERING
    text = re.sub(r"\bENGG\.?\b", "ENGINEERING", text)

    # Normalize Computer Science alone
    if "COMPUTER" in text and "SCIENCE" in text and "ENGINEERING" not in text:
        text = "COMPUTER SCIENCE"

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

print(f"✅ Loaded {len(approved_courses)} approved courses")


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

    # EXACT department match (NO normalization)
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

print("✅ Engineering & Technology courses validated successfully")
print(f"📄 Output file: {OUTPUT_JSON_FILE}")
