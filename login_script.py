import time
from playwright.sync_api import sync_playwright, TimeoutError

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    print("Navigating to sign-in page...")
    page.goto("https://stg.proquro.ai/sign-in?redirect=%2Fcompany-admin%2Fdashboard")
    page.wait_for_load_state('networkidle')
    
    print("Clicking 'Securely Login With Email'...")
    try:
        # The button is actually an anchor tag
        login_btn = page.locator('a:has-text("Securely Login With Email")')
        login_btn.click()
        page.wait_for_load_state('networkidle')
        print("Navigated to auth page.")
    except Exception as e:
        print("Could not click initial login button:", e)
        page.screenshot(path="error_step1.png")
    
    print("Looking for input fields...")
    try:
        # Try to find email input on the Auth0/login page
        email_input = page.locator('input[type="email"], input[name="email"], input[name="username"]')
        email_input.first.fill('mobpark@yopmail.com')
        print("Filled email.")
        
        # Try to find password input
        password_input = page.locator('input[type="password"], input[name="password"]')
        password_input.first.fill('Avromandal12345@')
        print("Filled password.")
        
        # Try to find submit button
        submit_button = page.locator('button[type="submit"], button:has-text("Continue"), button:has-text("Sign in"), button:has-text("Login")')
        submit_button.first.click()
        print("Clicked submit button.")
        
        # Wait for navigation back to dashboard
        print("Waiting for dashboard to load...")
        page.wait_for_url("**/company-admin/dashboard", timeout=20000)
        page.wait_for_load_state('networkidle')
        
        print("Successfully logged in!")
        page.screenshot(path="dashboard_success.png")
        print("Screenshot saved to dashboard_success.png")
        
        with open("dashboard_success.html", "w", encoding="utf-8") as f:
            f.write(page.content())
            
    except TimeoutError:
        print("Timed out. Current URL:", page.url)
        page.screenshot(path="error_timeout.png")
        with open("error_timeout.html", "w", encoding="utf-8") as f:
            f.write(page.content())
    except Exception as e:
        print("An error occurred:", str(e))
        page.screenshot(path="error_general.png")
        with open("error_general.html", "w", encoding="utf-8") as f:
            f.write(page.content())
    
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
