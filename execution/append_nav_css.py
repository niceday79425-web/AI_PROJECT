import os

CSS_APPEND = """
/* Glassmorphism Navigation Bar */
.glass-nav {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 999px;
    padding: 0.5rem 1rem;
    margin: 1rem auto 3rem;
    max-width: fit-content;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
.glass-nav a {
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.5rem 1.25rem;
    border-radius: 999px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.glass-nav a:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
}
.glass-nav a.active {
    background: var(--primary-gradient);
    color: #fff;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.nav-card[href*="learn"] i {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    -webkit-background-clip: text;
    background-clip: text;
}
"""

style_path = r"d:\AI_PROJECT\css\style.css"
with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

if ".glass-nav" not in content:
    with open(style_path, "a", encoding="utf-8") as f:
        f.write(CSS_APPEND)
    print("CSS successfully appended to style.css")
else:
    print("CSS already exists in style.css")
