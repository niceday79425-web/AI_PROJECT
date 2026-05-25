import os
import re
from layout_fix import process_file

if __name__ == '__main__':
    fort_path = 'fortune.html'
    if os.path.exists(fort_path):
        process_file(
            fort_path,
            r'<section class="card fortune-card">.*?</section>',
            r'<section[^>]*margin-top: 4rem[^>]*>.*?</section>'
        )
