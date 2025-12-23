import json
import re
from collections import defaultdict

# =========================
# CONFIG
# =========================
INPUT_JSON = "engineering_invalid_courses.json"
OUTPUT_JSON = "course_wise_count.json"


# =========================
# NORMALIZE COURSE
# =========================
def normalize_course(text):
    if not text:
        return ""
    text = text.upper().strip()
    text = re.sub(r"\s+", " ", text)
    return text


# =========================
# LOAD DATA
# =========================
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    colleges = json.load(f)


# =========================
# COUNT COURSES
# =========================
course_counter = defaultdict(int)
course_original_name = {}

for college in colleges:
    department = college.get("department")
    if not department:
        continue

    course = department.get("course")
    if not course:
        continue

    normalized = normalize_course(course)

    course_counter[normalized] += 1

    # store first readable version
    if normalized not in course_original_name:
        course_original_name[normalized] = course.strip()


# =========================
# BUILD OUTPUT
# =========================
result = []

for norm_course, count in sorted(course_counter.items()):
    result.append({
        "course": course_original_name[norm_course],
        "count": count
    })


# =========================
# SAVE JSON
# =========================
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)


print("✅ Course count generated successfully")
print(f"📄 Output file: {OUTPUT_JSON}")
print(f"🔢 Total unique courses: {len(result)}")
