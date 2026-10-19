import random
import urllib.request

COMMON_URL = ("https://raw.githubusercontent.com/first20hours/"
              "google-10000-english/master/google-10000-english-no-swears.txt")
DICT_URL = ("https://raw.githubusercontent.com/dwyl/"
            "english-words/master/words_alpha.txt")

MIN_LEN, MAX_LEN = 3, 5
TOP_N = 6000  # เอาเฉพาะคำที่ใช้บ่อยที่สุดกี่อันดับแรก

# คำที่ไม่อยากให้มีในเกม (เพิ่มเองได้เรื่อยๆ)
EXCLUDE = {
    "null", "reg", "info", "html", "http", "www", "com", "org", "net",
    "url", "usb", "cpu", "pdf", "jpg", "gif", "xml", "php", "css", "faq",
    "rss", "sql", "ftp", "dvd", "cds", "aol", "ebay", "yahoo", "msn",
    "gmt", "ref", "mac", "inc", "ltd", "llc", "eur", "usd", "ids", "est",
}


def download(url):
    return urllib.request.urlopen(url).read().decode("utf-8").splitlines()


common = [w.strip().lower() for w in download(COMMON_URL)][:TOP_N]
real_words = {w.strip().lower() for w in download(DICT_URL)}

words = sorted({w for w in common
                if MIN_LEN <= len(w) <= MAX_LEN
                and w.isalpha()
                and w in real_words
                and w not in EXCLUDE})

with open("words.txt", "w") as f:
    f.write("\n".join(words))

print(f"saved {len(words)} words to words.txt")
print("ตัวอย่าง:", ", ".join(random.sample(words, 40)))