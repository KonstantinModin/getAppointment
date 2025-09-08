import time
from playwright.sync_api import sync_playwright
from notifications import playAlert

url = 'https://sige.gva.es/qsige/citaprevia.justicia/#/es/home?uuid=01E4-33B69-2883-5B9B8'

def checkWebsite():
    res = False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)

            # Solicitar cita previa
            page.click("body > app-root > div > div.col-12.d-flex.flex-column.align-items-center > div.col-11.col-xl-9.ng-star-inserted > home > div.col-12.d-flex.flex-column.pt-4.ng-star-inserted > div > div:nth-child(1)")

            # REGISTRO CIVIL EXCLUSIVO ALICANTE
            page.click("text=REGISTRO CIVIL EXCLUSIVO ALICANTE")

            # CP JURA DE NACIONALIDAD
            page.click("text=CP JURA DE NACIONALIDAD")

            # Siguiente
            page.click("text=Siguiente")

            if page.is_visible("text=No hay horas disponibles"):
                time.sleep(5) 
                browser.close()
            else:
                playAlert()
                print("✅ Appointment available!")
                time.sleep(5000000000)
                res = True
    except Exception as e:
        print(f"Something went wrong: {e}")

    finally:
        return res

