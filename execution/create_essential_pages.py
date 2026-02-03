
# Script to create essential pages: Privacy Policy, About Us, Contact Us
import os

TEMPLATE_START = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | StockWise.ai</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header>
             <a href="/" class="logo">StockWise.ai</a>
        </header>
        <main style="max-width: 800px; margin: 4rem auto; min-height: 60vh;">
            <h1 style="margin-bottom: 2rem;">{title}</h1>
"""

TEMPLATE_END = """
        </main>
        <footer>
            <div class="footer-content">
                <p>&copy; 2026 StockWise.ai - Smart Dividend Investing</p>
                <!-- Links will be updated by another script -->
            </div>
        </footer>
    </div>
</body>
</html>
"""

PRIVACY_CONTENT = """
<p>At StockWise.ai, accessible from https://ai-project-1en.pages.dev/, one of our main priorities is the privacy of our visitors. This Privacy Policy document contains types of information that is collected and recorded by StockWise.ai and how we use it.</p>

<h2>Cookies and Web Beacons</h2>
<p>Like any other website, StockWise.ai uses "cookies". These cookies are used to store information including visitors' preferences, and the pages on the website that the visitor accessed or visited. The information is used to optimize the users' experience by customizing our web page content based on visitors' browser type and/or other information.</p>

<h2>Google DoubleClick DART Cookie</h2>
<p>Google is one of a third-party vendor on our site. It also uses cookies, known as DART cookies, to serve ads to our site visitors based upon their visit to www.website.com and other sites on the internet. However, visitors may choose to decline the use of DART cookies by visiting the Google ad and content network Privacy Policy at the following URL – <a href="https://policies.google.com/technologies/ads">https://policies.google.com/technologies/ads</a></p>

<h2>Privacy Policies</h2>
<p>You may consult this list to find the Privacy Policy for each of the advertising partners of StockWise.ai.</p>
<p>Third-party ad servers or ad networks uses technologies like cookies, JavaScript, or Web Beacons that are used in their respective advertisements and links that appear on StockWise.ai, which are sent directly to users' browser. They automatically receive your IP address when this occurs. These technologies are used to measure the effectiveness of their advertising campaigns and/or to personalize the advertising content that you see on websites that you visit.</p>
"""

ABOUT_CONTENT = """
<p>Welcome to StockWise.ai, your number one source for all things dividend investing. We're dedicated to pointing you to the very best of dividend stocks, with a focus on data accuracy, sustainability, and long-term growth.</p>
<p>Founded in 2026, StockWise.ai has come a long way from its beginnings. When we first started out, our passion for "echo-free financial data" drove us to start this project so that StockWise.ai can offer you the world's most advanced dividend grading system.</p>
<p>We serve customers all over the world, and are thrilled that we're able to turn our passion into our own website.</p>
<p>I hope you enjoy our products as much as we enjoy offering them to you. If you have any questions or comments, please don't hesitate to contact us.</p>
<p>Sincerely,<br>The StockWise Team</p>
"""

CONTACT_CONTENT = """
<p>We would love to hear from you!</p>
<p>If you have any questions about our site, advertising, or anything else, please feel free to reach out.</p>

<div style="background: var(--card-bg); padding: 2rem; border-radius: 12px; margin-top: 2rem; border: 1px solid var(--border-color);">
    <h3>Email Us</h3>
    <p style="font-size: 1.2rem; color: var(--accent-blue);">support@stockwise.ai</p>
    <p style="margin-top: 1rem; color: var(--text-secondary);">We aim to respond to all inquiries within 24-48 hours.</p>
</div>
"""

def create_page(filename, title, content):
    full_html = TEMPLATE_START.format(title=title) + content + TEMPLATE_END
    filepath = os.path.join("d:\\AI_PROJECT", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"[CREATED] {filepath}")

def main():
    create_page("privacy.html", "Privacy Policy", PRIVACY_CONTENT)
    create_page("about.html", "About Us", ABOUT_CONTENT)
    create_page("contact.html", "Contact Us", CONTACT_CONTENT)

if __name__ == "__main__":
    main()
