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
    return msg_padd(msg, 60)


def get_page_content():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://ghproxy.link/")
        print(f"Title: {page.title()}")

        # get page content
        print(f"Content: \n{page.content()}")

        # save page content
        # with open("scripts/page_content.html", "w") as f:
        #     f.write(page.content())

        # save page body
        with open("scripts/page_body.html", "w") as f:
            f.write(page.locator("body").inner_html())

        # save page body text
        # with open("scripts/page_body_text.txt", "w") as f:
        #     f.write(page.locator("body").inner_text())

        page.screenshot(path="scripts/screenshot.png")
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
        if 'green-text' in status.get('class', []):
            domain = div.find('div', class_='domain-name').find('a').get('href')
            available_domains.append(domain)

    return available_domains

def save_domain(domains:list[str],file_name:str="scripts/ghproxy-url-latest.txt"):
    if len(domains) > 0:
        with open(file_name, "w") as f:
            f.write(domains[0])

# read old available domain from "scripts/ghproxy-url.txt"
# if the new available domain is not the same as the old one,
# save the new one to "scripts/ghproxy-url.txt"
# read *.json files in bucket and replace the old domain with the new one

def run():
    # step_name="get page content"
    # info_step(step_name)
    # get_page_content()

    step_name="get available domains"
    info_step(step_name)
    domains = get_available_domains()
    print("Available domains:",domains)


    step_name="save the first available domain"
    info_step(step_name)
    # save the first domain to a file when exists
    save_domain(domains,"scripts/ghproxy-url-latest.txt")

if __name__ == "__main__":
    run()
