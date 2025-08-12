CRAWLER_STATE_FILE = "crawler_state_file.json"
FILES_DIRECTORY="files"
CRAWLED_DATA_FILE="crawled_data.jsonl"

# Indexer
REVERSE_INDEX_FILE = "inverted_index.json"
DOCS_FILE = "documents.json"

STOP_WORDS = set([
    "a", "an", "the", "and", "or", "but", "if", "while", "is", "are", "was", "were", "in", "on", "for", "to", "of",
    "at", "by", "with", "as", "it", "this", "that", "these", "those", "i", "you", "he", "she", "they", "we", "me",
    "my", "your", "our", "their", "his", "her", "its", "be", "been", "being", "do", "does", "did", "will", "would",
    "can", "could", "should", "shall", "not"
])

FILE_EXTENSIONS = [
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico',

    # Documents
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.odt', '.ods', '.odp', '.rtf', '.txt', '.md', '.csv', '.tsv',

    # Archives & Compressed
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso',

    # Audio
    '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma',

    # Video
    '.mp4', '.avi', '.mov', '.wmv', '.mkv', '.webm', '.flv', '.m4v',

    # Code & Markup
    '.css', '.js', '.jsx', '.ts', '.tsx',
    '.py', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs',
    '.json', '.xml', '.yml', '.yaml', '.sh', '.bat', '.pl', 'ps'

    # Fonts
    '.ttf', '.otf', '.woff', '.woff2',

    # Executables & Binaries
    '.exe', '.msi', '.apk', '.bin', '.dll', '.deb', '.rpm',

    # Database
    '.sql', '.db', '.sqlite', '.mdb', '.accdb',

    # Others
    '.log', '.conf', '.ini', '.bak', '.tmp'
]

LANGUAGE_CODES =  [
    'af',  # Afrikaans
    'am',  # Amharic
    'ar',  # Arabic
    'az',  # Azerbaijani
    'be',  # Belarusian
    'bg',  # Bulgarian
    'bn',  # Bengali
    'bs',  # Bosnian
    'ca',  # Catalan
    'ceb', # Cebuano
    'cs',  # Czech
    'cy',  # Welsh
    'da',  # Danish
    'de',  # German
    'dv',  # Divehi
    'el',  # Greek
    'en',  # English
    'eo',  # Esperanto
    'es',  # Spanish
    'et',  # Estonian
    'eu',  # Basque
    'fa',  # Persian
    'fi',  # Finnish
    'fr',  # French
    'fy',  # Frisian
    'ga',  # Irish
    'gd',  # Scots Gaelic
    'gl',  # Galician
    'gu',  # Gujarati
    'ha',  # Hausa
    'haw', # Hawaiian
    'he',  # Hebrew
    'hi',  # Hindi
    'hmn', # Hmong
    'hr',  # Croatian
    'ht',  # Haitian Creole
    'hu',  # Hungarian
    'hy',  # Armenian
    'id',  # Indonesian
    'ig',  # Igbo
    'is',  # Icelandic
    'it',  # Italian
    'ja',  # Japanese
    'jv',  # Javanese
    'ka',  # Georgian
    'kk',  # Kazakh
    'km',  # Khmer
    'kn',  # Kannada
    'ko',  # Korean
    'ku',  # Kurdish (Kurmanji)
    'ky',  # Kyrgyz
    'la',  # Latin
    'lb',  # Luxembourgish
    'lo',  # Lao
    'lt',  # Lithuanian
    'lv',  # Latvian
    'mg',  # Malagasy
    'mi',  # Maori
    'mk',  # Macedonian
    'ml',  # Malayalam
    'mn',  # Mongolian
    'mr',  # Marathi
    'ms',  # Malay
    'mt',  # Maltese
    'my',  # Burmese
    'ne',  # Nepali
    'nl',  # Dutch
    'no',  # Norwegian
    'ny',  # Chichewa
    'pa',  # Punjabi
    'pl',  # Polish
    'ps',  # Pashto
    'pt',  # Portuguese
    'ro',  # Romanian
    'ru',  # Russian
    'rw',  # Kinyarwanda
    'sd',  # Sindhi
    'si',  # Sinhala
    'sk',  # Slovak
    'sl',  # Slovenian
    'sm',  # Samoan
    'sn',  # Shona
    'so',  # Somali
    'sq',  # Albanian
    'sr',  # Serbian
    'st',  # Sesotho
    'su',  # Sundanese
    'sv',  # Swedish
    'sw',  # Swahili
    'ta',  # Tamil
    'te',  # Telugu
    'tg',  # Tajik
    'th',  # Thai
    'tk',  # Turkmen
    'tl',  # Tagalog (Filipino)
    'tr',  # Turkish
    'tt',  # Tatar
    'ug',  # Uyghur
    'uk',  # Ukrainian
    'ur',  # Urdu
    'uz',  # Uzbek
    'vi',  # Vietnamese
    'xh',  # Xhosa
    'yi',  # Yiddish
    'yo',  # Yoruba
    'zh',  # Chinese (Simplified)
    'zh-TW', # Chinese (Traditional)
    'zu'   # Zulu
]


SEEDS = [
    # Wikipedia and Informational
    "https://en.wikipedia.org/wiki/Web_crawler",
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://simple.wikipedia.org/wiki/Main_Page",

    # Tech & Programming
    "https://www.python.org/",
    "https://developer.mozilla.org/",
    "https://stackoverflow.com/",
    "https://github.com/explore",
    "https://gitlab.com/",
    "https://pypi.org/",
    "https://npmjs.com/",
    "https://www.geeksforgeeks.org/",
    "https://www.freecodecamp.org/",
    "https://dev.to/",
    "https://realpython.com/",
    "https://towardsdatascience.com/",

    # News & Media
    "https://www.bbc.com/",
    "https://www.cnn.com/",
    "https://www.nytimes.com/",
    "https://www.theguardian.com/international",
    "https://news.ycombinator.com/",
    "https://www.reuters.com/",
    "https://apnews.com/",

    # Education & Science
    "https://arxiv.org/",
    "https://www.khanacademy.org/",
    "https://ocw.mit.edu/",
    "https://www.coursera.org/",
    "https://www.edx.org/",
    "https://plato.stanford.edu/",

    # Tech Companies
    "https://google.com",
    "https://openai.com/",
    "https://microsoft.com/",
    "https://apple.com/",
    "https://meta.com/",
    "https://amazon.com/",
    "https://vercel.com/",
    "https://cloudflare.com/",

    # Personal / Portfolio (examples)
    "https://github.com/Razamindset",
    "https://myportfolio-mu-coral.vercel.app/",
    "https://github.com/Ali-Raza764",
    "https://github.com/tensorflow/",
    "https://github.com/pytorch/",

    # Academic
    "https://www.nature.com/",
    "https://www.sciencedirect.com/",
    "https://www.jstor.org/",
    "https://www.nasa.gov/",

    # Blogs and Articles
    "https://paulgraham.com/",
    "https://seths.blog/",
    "https://waitbutwhy.com/",
    "https://xkcd.com/",

    # Social / Discussion
    "https://reddit.com/",
    "https://medium.com/",
    "https://quora.com/",
    "https://producthunt.com/",
    "https://lobste.rs/",
    "https://simple.wikipedia.org/wiki/List_of_countries",
    "https://www.britannica.com/topic/list-of-games-2072482",
    "https://pakaf.com/mcq/pakistan-general-knowledge-mcqs/",
]