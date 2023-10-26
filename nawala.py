from datetime import datetime
import requests
import time

BOT_TOKEN = "6374582132:AAEMjw8CO2YRLNvEAl0VSzZ9AXTvaU9u96A"
CHAT_ID = "-823196726"
LINK_URL = "https://kaconkalus.site/checker/Link.txt"

def check_nawala_domain(url):
    try:
        response = requests.get(url)
        if any(text in response.text for text in ["This site can’t be reached", "Situs ini tidak dapat dijangkau", "SITUS DIBLOKIR"]):
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return True

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    return response.json()

def main():
    output_file = "Nawala.txt"
    interval_minutes = 15 # Interval waktu dalam menit

    while True:
        try:
            response = requests.get(LINK_URL)
            domain_list = response.text.splitlines()
        except requests.exceptions.RequestException:
            print("Gagal mendapatkan daftar domain dari URL.")
            domain_list = []

        nawala_domains = []

        for domain in domain_list:
            domain = domain.strip()
            if domain.startswith("http://") or domain.startswith("https://"):
                url = domain
            else:
                url = "https://" + domain

            if check_nawala_domain(url):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nawala_domains.append(f"{domain} | {timestamp}")

        if nawala_domains:
            message = "\n".join(nawala_domains)
            send_telegram_message(message)

        with open(output_file, "a") as nawala_file:
            nawala_file.write("==================================\n")
            nawala_file.write("----------------------------------\n\n")

            for domain in nawala_domains:
                nawala_file.write(f"{domain}\n")

            nawala_file.write("\n==================================\n")

        print("Pengecekan Selesai! Domain terkena nawala telah disimpan dan pesan telah dikirim.")

        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    main()
