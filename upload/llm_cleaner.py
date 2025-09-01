from typing import List, Dict
import re


def parse_llm_text(text: str) -> List[Dict]:
    sections = []

    # Split into main sections using ## headings
    main_sections = re.findall(
        r"## (.*?)\n\n(.*?)(?=\n## |\Z)", text, re.DOTALL)

    for section_title, section_body in main_sections:
        # If the section contains subsections with ### (like Detailed Results)
        subsections = re.findall(
            r"### (.*?)\n(.*?)(?=\n### |\Z)", section_body, re.DOTALL)

        if subsections:
            for sub_title, sub_body in subsections:
                tests = extract_tests(sub_body)
                sections.append({
                    "name": f"{section_title.strip()} - {sub_title.strip()}",
                    "tests": tests,
                    "interpretation": None
                })
        else:
            # If no subsections, treat the section as plain text or abnormal/summary/recommendations
            tests = extract_tests(section_body)
            sections.append({
                "name": section_title.strip(),
                "tests": tests,
                "interpretation": section_body.strip() if not tests else None
            })

    return sections


def extract_tests(section_text: str) -> List[Dict]:
    test_lines = re.findall(
        r"- \*\*(.+?)\*\*:(.+?)\((.*?)\) - \*\*(.*?)\*\*",
        section_text,
        re.DOTALL
    )
    tests = []
    for name, value_unit, ref_range, status in test_lines:
        value_unit = value_unit.strip()
        if " " in value_unit:
            value, unit = value_unit.split(" ", 1)
        else:
            value, unit = value_unit, ""
        tests.append({
            "name": name.strip(),
            "value": value.strip(),
            "unit": unit.strip(),
            "referenceRange": ref_range.strip().replace("normal range:", "").strip(),
            "description": "",
            "status": status.strip()
        })
    return tests
