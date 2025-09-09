import time
from playwright.sync_api import sync_playwright
from notifications import playAlert
from datetime import datetime

url = 'https://sige.gva.es/qsige/citaprevia.justicia/#/es/home?uuid=01E4-33B69-2883-5B9B8'

name = "Anastasia"
surname = "Modina"
nie = "Y3501060Z"
email = "modinaspain@gmail.com"
phone = "640702535"

# name = "Jorge"
# surname = "Navarro"
# nie = "Y3501060Z"
# email = "jornavarro@gmail.com"
# phone = "641712531"

def checkWebsite():
    # return alternativeCheck()
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
            time.sleep(5) 

            if page.is_visible("text=No hay horas disponibles"):
                time.sleep(5) 
                browser.close()
            else:
                now = datetime.now()
                now_str = now.strftime("%H:%M")
                print(f"[{now_str}] ✅ Appointment available, trying to book it!")
                bookAppointment(page)
                time.sleep(5000000000)
                res = True
    except Exception as e:
        print(f"Something went wrong: {e}")

    finally:
        return res


def alternativeCheck():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        # Solicitar cita previa
        page.click("body > app-root > div > div.col-12.d-flex.flex-column.align-items-center > div.col-11.col-xl-9.ng-star-inserted > home > div.col-12.d-flex.flex-column.pt-4.ng-star-inserted > div > div:nth-child(1)")

        page.click("text=REGISTRO CIVIL GANDIA")
        page.click("text=CP EXPEDICION DE CERTIFICADOS")
        page.click("text=Siguiente")
        time.sleep(5) 
        if page.is_visible("text=No hay horas disponibles"):
            print("❌ No hay horas disponibles!")
            time.sleep(10) 
            browser.close()
            return False
        else:
            now = datetime.now()
            now_str = now.strftime("%H:%M")
            print(f"[{now_str}] ✅ Appointment available, trying to book it!")
            bookAppointment(page)
            time.sleep(5000000000)
    
def bookAppointment(page):
    time.sleep(1)
    # possible_times - list of strings representing time from 06:00 to 20:00, with interval of 5 minutes
    # possible_times = [f"{hour}:{minute:02d}" for hour in range(6, 20) for minute in range(0, 60, 5)]

    # print(possible_times)
    
    # for t in possible_times:
        # print(f"Checking {t}")
        # if page.is_visible(f"text={t}"):
            # page.click(f"text={t}")
    page.click("#cdk-step-content-0-1 > div.col-12.d-flex.justify-content-center.mb-4.ng-star-inserted > div > calendar-step > div > div:nth-child(2) > slots > div > div.col-12.d-flex.slots-container.flex-wrap.p-1.ng-star-inserted > div")
    time.sleep(5)
    print('clicking next button')
    page.click("#cdk-step-content-0-1 > div.col-12.d-flex.justify-content-between.mb-4.ng-star-inserted > button > span.p-button-label")
    time.sleep(2)
    page.fill("input[name='name']", name)
    time.sleep(2)
    page.fill("input[name='surname']", surname)
    time.sleep(2)
    page.click(".p-dropdown.p-component")
    time.sleep(2)
    page.click("text=NIE")
    time.sleep(2)
    # Clear field first, then type character by character to help with validation
    page.click("input[placeholder='Introduzca el documento']")
    page.fill("input[placeholder='Introduzca el documento']", "")  # Clear first
    page.type("input[placeholder='Introduzca el documento']", nie, delay=100)
    time.sleep(2)
    page.fill("input[placeholder='Introduzca el email']", email)
    time.sleep(2)
    page.fill("input[placeholder='Introduzca el teléfono']", phone)
    time.sleep(2)
    page.check("input[inputid='privacyCheck']")
    time.sleep(2)
    # Try multiple strategies to click Confirmar button
    try:
        # Strategy 2: Click button element specifically 
        page.click("button:has-text('Confirmar')", force=True)
        print("✅ Clicked Confirmar (button selector)")
    except:
        try:
            # Strategy 3: Scroll into view first
            page.scroll_into_view_if_needed("text=Confirmar")
            time.sleep(1)
            page.click("text=Confirmar", force=True)
            print("✅ Clicked Confirmar (after scroll)")
        except:
            # Strategy 4: JavaScript click as last resort
            page.evaluate("""
                const buttons = document.querySelectorAll('button');
                for(let btn of buttons) {
                    if(btn.textContent.includes('Confirmar')) {
                        btn.click();
                        break;
                    }
                }
            """)
            print("✅ Clicked Confirmar (JavaScript)")
            time.sleep(1)
    print("end")
    playAlert()
    time.sleep(2000000)
    

