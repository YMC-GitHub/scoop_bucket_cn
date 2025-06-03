import os
import json
from pathlib import Path

def info_status(msg_body, status):
    msg_success = "✅"
    msg_failed = "❌"
    msg_warn = "ℹ️"

    if status == 0:
        print(f"{msg_success} {msg_body}")
    elif status == 1:
        print(f"{msg_failed} {msg_body}")
    else:
        print(f"{msg_warn} {msg_body}")

def check_result(msg_body, flag_exit):
    status = 0
    try:
        # Normally you'd put the operation you're checking here
        pass
    except Exception:
        status = 1

    if status == 0:
        info_status(msg_body, 0)
    else:
        info_status(msg_body, 1)
        if flag_exit:
            exit(1)

def msg_padd(msg, msg_max_len=60):
    msg_len = len(msg)
    msg_fill_length = (msg_max_len - msg_len + 2) // 2
    msg_padding = '-' * msg_fill_length
    padded_msg = f"{msg_padding} {msg} {msg_padding}"
    return padded_msg[:msg_max_len]

def info_step(msg):
    print(f"\n{msg_padd(msg)}")

def get_json_files(bucket_dir="bucket"):
    """Get all JSON files from bucket directory"""
    try:
        json_files = [f for f in Path(bucket_dir).glob("*.json")]
        info_status(f"Found {len(json_files)} JSON files in {bucket_dir}", 0)
        return json_files
    except Exception as e:
        info_status(f"Error reading JSON files: {str(e)}", 1)
        return []

def read_descriptions(json_files):
    """Read descriptions from JSON files"""
    descriptions = []
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                filename = json_file.stem
                description = data.get("description", "No description available")
                descriptions.append(f"- `{filename}` - {description}")
        except Exception as e:
            info_status(f"Error reading {json_file}: {str(e)}", 1)
            descriptions.append(f"- `{json_file.stem}` - Error reading file")

    return sorted(descriptions)

def update_readme(descriptions, template_path="template.README.md", output_path="README.md"):
    """Update README.md using template"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        content = "\n".join(descriptions)
        updated_readme = template.replace("<!-- apps-desc-here -->", content)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(updated_readme)

        info_status(f"Successfully updated {output_path}", 0)
    except Exception as e:
        info_status(f"Error updating README: {str(e)}", 1)

def run():
    info_step("Starting README Update Process")

    # Step 1: Get JSON files
    info_step("Finding JSON Files")
    json_files = get_json_files()
    if not json_files:
        check_result("No JSON files found to process", True)

    # Step 2: Read descriptions
    info_step("Reading Descriptions")
    descriptions = read_descriptions(json_files)

    # Step 3: Update README
    info_step("Updating README.md")
    update_readme(descriptions)

    info_step("Process Completed")

if __name__ == "__main__":
    run()
