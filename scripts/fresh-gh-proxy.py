import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

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
    status = 0  # In Python, we'd typically use try/except instead of checking $?
    try:
        # Normally you'd put the operation you're checking here
        pass
    except Exception:
        status = 1

    if status == 0:
        info_status(msg_body, 0)
    else:
        info_status(msg_body, 1)
        if flag_exit == 0:
            exit(1)

def msg_padd(msg, msg_max_len):
    msg_len = len(msg)
    msg_fill_length = (msg_max_len - msg_len + 2) // 2
    msg_padding = '-' * msg_fill_length
    padded_msg = f"{msg_padding}-{msg}-{msg_padding}"
    return padded_msg[:msg_max_len]

def info_step(msg):
    print(msg_padd(msg, 60))

def get_page_content():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://ghproxy.link/")
        print(f"Title: {page.title()}")

        # Save page content
        with open("scripts/page_content.html", "w", encoding='utf-8') as f:
            f.write(page.content())

        page.screenshot(path="scripts/page_screenshot.png")
        browser.close()

def get_available_domains():
    # Read the HTML content from file
    with open('scripts/page_content.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all domain status divs
    domain_divs = soup.find_all('div', class_='domain-status')

    available_domains = []
    for div in domain_divs:
        # Check if domain is available (green-text status)
        status = div.find('div', class_='status-text')
        if status and 'green-text' in status.get('class', []):
            domain_name = div.find('div', class_='domain-name')
            if domain_name:
                link = domain_name.find('a')
                if link:
                    available_domains.append(link.get('href', '').strip())
                else:
                    # Fallback to text content if no <a> tag
                    available_domains.append(domain_name.get_text(strip=True))

    return available_domains

def read_old_domain(file_path="scripts/ghproxy-url.txt"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_domain(domain: str, file_path="scripts/ghproxy-url.txt"):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(domain)

def update_json_files(old_domain, new_domain, bucket_path="bucket"):
    if not old_domain or not new_domain or old_domain == new_domain:
        return False

    updated_files = 0
    for root, _, files in os.walk(bucket_path):
        for file in files:
            if file.endswith('.json'):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if old_domain in content:
                        new_content = content.replace(old_domain, new_domain)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        updated_files += 1
                        info_status(f"Updated {file_path}", 0)
                except Exception as e:
                    info_status(f"Failed to update {file_path}: {str(e)}", 1)

    return updated_files > 0

def run():
    # Step 1: Get page content
    step_name = "Fetching page content"
    info_step(step_name)
    get_page_content()

    # Step 2: Get available domains
    step_name = "Extracting available domains"
    info_step(step_name)
    domains = get_available_domains()


    if not domains:
        info_status("No available domains found", 1)
        exit(1)
    else:
        print("Available domains:", domains)


    new_domain = domains[0]

    # Step 3: Read old domain
    step_name = "Checking old domain"
    info_step(step_name)
    old_domain = read_old_domain()
    print(f"Old domain: {old_domain}")
    print(f"New domain: {new_domain}")

    # Step 4: Save new domain if different
    if old_domain != new_domain:
        step_name = "Updating domain reference"
        info_step(step_name)
        save_domain(new_domain)
        info_status(f"Saved new domain: {new_domain}", 0)

        # Step 5: Update JSON files
        step_name = "Updating JSON files in bucket"
        info_step(step_name)
        if update_json_files(old_domain, new_domain):
            info_status("JSON files updated successfully", 0)
        else:
            info_status("No JSON files needed updating", 2)
    else:
        info_status("Domain unchanged, no updates needed", 2)

if __name__ == "__main__":
    run()
