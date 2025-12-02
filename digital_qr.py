import qrcode
import cv2
import json
from datetime import datetime
import os

OUTPUT = "outputs"
os.makedirs(OUTPUT, exist_ok=True)

def save_qr(data, prefix):
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(OUTPUT, filename)
    qrcode.make(data).save(path)
    print("QR Created:", path)

# ---------------- USECASES ----------------
def url_qr(): save_qr(input("URL: "), "url")

def text_qr(): save_qr(input("Enter text: "), "text")

def vcard_qr():
    name = input("Name: "); phone = input("Phone: "); email = input("Email: ")
    v = f"BEGIN:VCARD\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
    save_qr(v, "vcard")

def pdf_qr(): save_qr(input("PDF path or URL: "), "pdf")

def wifi_qr():
    ssid = input("SSID: "); pwd = input("Password: "); sec = input("Security(WPA/WEP): ") or "WPA"
    save_qr(f"WIFI:T:{sec};S:{ssid};P:{pwd};;", "wifi")

def payment_qr(): save_qr(input("UPI/Stripe/PayPal URL: "), "payment")

def product_qr():
    d = {"name": input("Product:"), "manual": input("Manual URL:")}
    save_qr(json.dumps(d), "product")

def login_qr():
    token = os.urandom(5).hex()
    save_qr(json.dumps({"login_token": token}), "login")

def event_qr():
    d = {"event": input("Event:"), "name": input("Name:"), "seat": input("Seat:"), "id": input("Ticket ID:")}
    save_qr(json.dumps(d), "event")

def api_qr(): save_qr(input("API URL on scan:"), "api")

def dynamic_qr():
    short = input("Short code: "); url = input("Redirect URL: ")
    db = "dynamic.json"
    m = json.loads(open(db).read()) if os.path.exists(db) else {}
    m[short] = url; open(db, "w").write(json.dumps(m, indent=2))
    save_qr("DYNAMIC:" + short, "dynamic")

def inventory_qr():
    d = {"id": input("Product ID:"), "name": input("Name:"), "qty": input("Qty:"), "price": input("Price:")}
    save_qr(json.dumps(d), "inventory")

# --------------- SCANNER -----------------
def scan_qr():
    img = cv2.imread(input("Image path: "))
    d, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    print("Scanned:", d if d else "No QR found")

#--------------- MENU -----------------
menu = [
    ("URL", url_qr),
    ("Text", text_qr),
    ("vCard", vcard_qr),
    ("PDF", pdf_qr),
    ("WiFi", wifi_qr),
    ("Payment", payment_qr),
    ("Product Manual", product_qr),
    ("Login Token", login_qr),
    ("Event Ticket", event_qr),
    ("QR → API", api_qr),
    ("Dynamic QR", dynamic_qr),
    ("Inventory", inventory_qr),
    ("Scan QR from Image", scan_qr),
]

while True:
    print("\n====== UNIVERSAL QR SYSTEM ======")
    for i,(n,_) in enumerate(menu,1):
        print(i, "-", n)
    print("0 - Exit")
    ch = input("Select: ")
    if ch=="0": break
    if ch.isdigit() and 1 <= int(ch) <= len(menu):
        menu[int(ch)-1][1]()
    else: print("Invalid")
