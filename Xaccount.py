from package import install_package,google_chrome,kill_chrome_process
install_package("bs4")

def time_now():
    from datetime import datetime
    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    return now.strftime("%H:%M:%S:%f")[:-3]

def click_simple(button,driver):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    try:
        # Convertir l'élément BeautifulSoup en sélecteur CSS
        css_selector = ''
        # Récupérer les noms de classes de l'élément
        classes = button.attrs.get('class', [])

        # Construire le sélecteur CSS en utilisant les classes
        if classes:
            css_selector = '.' + '.'.join(classes)
        else:
            # Si l'élément n'a pas de classes, essayer de générer un sélecteur plus générique
            tag = button.name
            id_ = button.attrs.get('id', '')
            if id_:
                css_selector = f'{tag}#{id_}'
            else:
                css_selector = tag
        # Attendre que l'élément soit visible
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        
        # Cliquer sur l'élément
        element.click()
        
        # Attendre un peu pour voir l'action effectuée (optionnel)
        driver.implicitly_wait(5)
        
        print(f"{time_now()} : Le bouton a été cliqué avec succès.")
        return True
    except Exception as e:
        print(f"{time_now()} : Une erreur s'est produite: {e}")
        return False
        
def button_txt_fils(driver,button_locator, target_text, target_locator):
    from bs4 import BeautifulSoup
    import time
    # Nombre maximum de tentatives
    max_attempts = 10
    # Attendre 1 seconde entre chaque tentative
    delay = 1
    # Boucle pour rechercher l'élément
    attempts = 0
    button_found = None
    button = None
    while button is None and attempts < max_attempts:
            
        # Récupérer le contenu HTML de la page
        html_content = driver.page_source
        # Créer un objet BeautifulSoup à partir du contenu HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Rechercher tous les boutons correspondant au localisateur
        buttons = soup.select(button_locator)
        
        # Incrémenter le nombre de tentatives
        attempts += 1
        
        # Parcourir les boutons
        for button in buttons:
            # Rechercher les éléments <span> dans les éléments enfants du bouton
            span_elements = button.select(target_locator)
            for span_element in span_elements:
                if span_element.text == target_text:
                    button_found = button
            
        # Attendre 1 seconde avant la prochaine tentative
        if attempts < max_attempts and button_found is None:
            print(f"{time_now()} : Élément non trouvé, nouvelle tentative dans", delay, "seconde(s)...")
            time.sleep(delay)
    # Vérifier si l'élément a été trouvé
    if button_found:
         print(f"{time_now()} : Élément <{button_locator}> avec fils {target_locator} contient le texte {target_text} a été trouvé.")
         return button_found        
    else:
        print(f"{time_now()} : L'élément <{button_locator}> avec fils {target_locator} contient le texte {target_text} n'a pas été trouvé après", max_attempts, "tentatives.")
        return False
        
def input_field(driver,tag,attribu,attr_value,txt):
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException

    try:

        # Trouver l'élément input avec l'attribut autocomplete="username"
        username_input = driver.find_element(By.CSS_SELECTOR, f'{tag}[{attribu}="{attr_value}"]')

        # Remplir le champ avec le texte "txt"
        username_input.send_keys(f"{txt}")

        print(f"{time_now()} : Champ rempli avec succès.")
        return True
    except NoSuchElementException as e:
        print(f"{time_now()} : Erreur : Aucun élément <{tag}> avec l'attribut '{attribu}={attr_value}' n'a été trouvé.")
        return False


def click_button(driver,tag,attribu,attr_value):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

    try:
        # Trouver l'élément bouton
        button = driver.find_element(By.CSS_SELECTOR, f"{tag}[{attribu}='{attr_value}']")
        # Attendre que l'élément soit cliquable
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"{tag}[{attribu}='{attr_value}']")))

        # Cliquer sur l'élément bouton
        button.click()
        print(f"{time_now()} : Élément <{tag}> avec l'attribut {attribu}='{attr_value}' cliqué avec succès.")
        return True
    except TimeoutException:
        print(f"{time_now()} : Délai d'attente dépassé pour que l'élément devienne cliquable.")
        return False
    except ElementClickInterceptedException:
        print(f"{time_now()} : Un autre élément a intercepté le clic sur le bouton.")
        return False
    except NoSuchElementException:
        print(f"{time_now()} : L'élément bouton n'a pas été trouvé sur la page.")
        return False
    except Exception as e:
        print(f"{time_now()} : Une erreur s'est produite : {e}")
        return False
        
def find_tag(driver,tag,attribu,attr_value):
    from bs4 import BeautifulSoup
    import time
    # Nombre maximum de tentatives
    max_attempts = 10
    # "button"
    # "aria-label"
    # "Follow @ARABPNEWS"
    # Attendre 1 seconde entre chaque tentative
    delay = 1

    # Boucle pour rechercher l'élément
    attempts = 0
    button = None
    while button is None and attempts < max_attempts:
            
        # Récupérer le contenu HTML de la page
        html_content = driver.page_source
        # Créer un objet BeautifulSoup à partir du contenu HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Rechercher l'élément <button> avec l'attribut attribu=attr_value
        button = soup.find(tag, {attribu: attr_value})
        
        # Incrémenter le nombre de tentatives
        attempts += 1

        # Attendre 1 seconde avant la prochaine tentative
        if attempts < max_attempts and button is None:
            print(f"{time_now()} : Élément non trouvé, nouvelle tentative dans", delay, "seconde(s)...")
            time.sleep(delay)
    # Vérifier si l'élément a été trouvé
    if button:
         print(f"{time_now()} : Élément <{tag}> avec l'attribut {attribu}='{attr_value}' a été trouvé.")       
         return True        
    else:
        print(f"{time_now()} : L'élément <{tag}> avec l'attribut {attribu}='{attr_value}' n'a pas été trouvé après", max_attempts, "tentatives.")
        return False


def open_logout(driver):
    url = "https://x.com/i/flow/login?redirect_after_login=%2Fhome"
    print(f"{time_now()} : 1-Go to logout X Page")
    driver.get(url)
    return driver
 
# def log_stat(driver):
#     print("2-Check X home Page")
#     if find_tag(driver,"a","data-testid","SideNav_NewTweet_Button"):
#         return True, "2-X home Page Ok"
#     else:
#         return False, "2-X Not Login"

# def find_logout(driver):
#     print("2-Trouver logout")
#     driver = open_logout(driver)
#     if find_tag(driver,"button","data-testid","confirmationSheetConfirm"):
#         return True, "2-Bouton log out Trouve"
#     else :
#         return False, "2-Bouton log out Pas Trouve"
        
# def click_logout(driver):
#     print("3-click sur bouton log out")
#     if click_button(driver,"button","data-testid","confirmationSheetConfirm"):
#         return True,"3-Bouton log out clicke"
#     else :
#         return False, "3-Bouton log out Pas Trouve"
        
def find_loginButton(driver):
    print(f"{time_now()} : Trouver Sign in")
    if find_tag(driver,"a","data-testid","loginButton"):
        print(f"{time_now()} : Bouton Sign in Trouve")
        return True
    else :
        print(f"{time_now()} : Bouton Sign in Pas Trouve")
        return False 
        
def click_loginButton(driver):
    print(f"{time_now()} : Click Sign in")
    if  click_button(driver,"a","data-testid","loginButton"):
        print(f"{time_now()} : 4-Bouton Sign in Clicke")
        return True
    else :
        print(f"{time_now()} : Bouton Sign in Pas Clicke")
        return False
    
def find_username(driver):
    print(f"{time_now()} : 3-Trouver username") 
    if find_tag(driver,"input","autocomplete","username"):
        return True, "3-Champ username Trouve"
    else :
        return False, "3-Champ username Pas Trouve"
        
def username_stat(driver,user):
    print(f"{time_now()} : 4-Remplir username")
    if input_field(driver,"input","autocomplete","username",user):
        return True, "4-Champ username rempli"  
    else :
        return False, "4-Champ username Pas rempli"
        
          
def find_Next(driver):
    print(f"{time_now()} : 5-Trouver button Next")
    if button_txt_fils(driver,"button", "Next", "span"):
        return True, "5-Button Next Trouve"    
    else :
        return False, "5-Button Next Pas Trouve"
        
            
def click_Next(driver):
    print(f"{time_now()} : 6-Click Button Next")
    button_Next = button_txt_fils(driver,"button", "Next", "span")
    if button_Next:
        if click_simple(button_Next,driver):
            return True, "6-Button Next Click" 
        else :
            return False, "6-Button Next Pas Click"
    else :
        return False, "6-Button Next Pas Trouve"       
       
def find_password(driver):
    print(f"{time_now()} : 7-Trouver Champ password") 
    if find_tag(driver,"input","autocomplete","current-password"):
        return True,  "7-Champ password Trouve"  
    else :
        return False, "7-Champ password Pas Trouve"
        
       
def input_password(driver,passwd):
    print(f"{time_now()} : 8-Remplir password")
    if input_field(driver,"input","autocomplete","current-password",passwd):
        return True, "8-Champ password rempli"
    else :
        return False, "8-Champ password Pas rempli"
        
def find_Login(driver):
    print(f"{time_now()} : 9-Trouver button Log in")
    if button_txt_fils(driver,"button", "Log in", "span"):
        return True, "9-Button Log in Trouve"  
    else :
        return False, "9-Button Log in Pas Trouve"
                
def click_Login(driver):
    print(f"{time_now()} : 10-Button Log in Click")
    button_Login = button_txt_fils(driver,"button", "Log in", "span")
    if button_Login:
        if click_simple(button_Login,driver):
            return True, "10-Button Log in Click"
        else:
            return False, "10-Button Log in Pas Click"
    else :
        return False, "10-Button Log in Pas Trouve"
            
def home_x(driver):
    print(f"{time_now()} : 11-Go to X home")
    print(f"{time_now()} : Check : The account being added is already logged in.")
    if find_tag(driver,"button","data-testid","confirmationSheetConfirm"):
        click_button(driver,"button","data-testid","confirmationSheetConfirm")
    print(f"{time_now()} : Check : Post")
    if find_tag(driver,"a","data-testid","SideNav_NewTweet_Button"):
        return True, "11-X home Page"
    else :
        return False, "11-X Not login In home Page"

# Liste des fonctions dans l'ordre    
conditions = [ 
        find_username,#(driver)-1
        username_stat,#(driver,user)-2
        find_Next,#(driver)-3
        click_Next,#(driver)-4      
        find_password,#(driver)-5       
        input_password,#(driver,passwd)-6       
        find_Login,#(driver)-7                
        click_Login,#(driver)-8            
        home_x #(driver)-9
    ]

def change_account(driver, user, passwd):
    for index in range(0 , len(conditions)):
        print(f"{time_now()} : Calling condition {index + 1}")
        if index == 1: 
            result, message = conditions[index](driver, user)
        elif index == 5: 
            result, message = conditions[index](driver, passwd)
        else:
            result, message = conditions[index](driver)
        print(f"{time_now()} : {message}")
        if not result:
            break
    return result
    
def get_profile_link(driver):
    from bs4 import BeautifulSoup
    if find_tag(driver,"a","aria-label","Profile"):
        # Récupérer le contenu HTML de la page
        html_content = driver.page_source
        # Créer un objet BeautifulSoup à partir du contenu HTML
        soup = BeautifulSoup(html_content, "html.parser")
        current_url = driver.current_url
        profile_element = soup.find("a", {"aria-label": "Profile"})
        if "href" in profile_element.attrs:
            profile = profile_element["href"]
            print(f"{time_now()} : Profile {profile[1:]} login.")
            return profile[1:]
        else:
            print(f"{time_now()} : No Profile.")
            return None
    else:
        print(f"{time_now()} : No Profile.")
        return None
    
def click_switch(driver, button_tag, button_aria_label, button_text, timeout=10):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import StaleElementReferenceException,TimeoutException, NoSuchElementException
    from selenium import webdriver
    try:
        # Trouver l'élément bouton
        button = driver.find_element(By.CSS_SELECTOR, f"{button_tag}[{button_aria_label}='{button_text}']")

        # Attendre que l'élément soit cliquable
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"{button_tag}[{button_aria_label}='{button_text}']")))

        # Cliquer sur l'élément bouton
        button.click()
        return True
    except StaleElementReferenceException:
        print(f"{time_now()} : l'élément est devenu obsolète, essayez de le retrouver ")
        return False
    except TimeoutException:
        print(f"{time_now()} : Délai d'attente dépassé pour que l'élément devienne cliquable.")
        return False
    except NoSuchElementException:
        print(f"{time_now()} : L'élément bouton n'a pas été trouvé sur la page.")
        return False
    except Exception as e:
        print(f"{time_now()} : Une erreur s'est produite : {e}")
        return False

        
def Account_cible(driver,profile):
    attr_value = f"Switch to @{profile}"
    if find_tag(driver,"button","aria-label",attr_value):
        print(f"{time_now()} : button Switch to Profile Found.")
        if click_switch(driver,"button","aria-label",attr_value):
            print(f"{time_now()} : button Switch to Profile Clicked.")
            return True
        else:
            print(f"{time_now()} : button Switch to Profile not Clicked.")
            return False
    else:
        print(f"{time_now()} : No button Switch to Profile.")
        return False

    
def Account_menu(driver):
    if get_profile_link(driver):
        if find_tag(driver,"button","aria-label","Account menu"):
            print(f"{time_now()} : button Account menu Found.")
            f"{time_now()} : button Account menu Found."
            if click_button(driver,"button","aria-label","Account menu"):
                print(f"{time_now()} : button Account menu Clicked.")
                return True
            else:
                print(f"{time_now()} : button Account menu not Clicked.")
                return False
        else:
            print(f"{time_now()} : button Account menu not Found.")
            return False            
    else:
        print(f"{time_now()} : No Profile.")
        return False

def account(driver):
    import time
    while True:
        kill_chrome_process()
        url = "https://x.com/home"
        print(f"{time_now()} : Go to X home")
        driver = google_chrome(url)    
        passwd = "123456789@Az"
        print(f"{time_now()} : Check Profile.")
        profile_link = get_profile_link(driver)
        user ="yassingaza24"
        skip = True
        result = False
        if profile_link:
            print(f"{time_now()} : Profile Exist")
            if profile_link == user:
                user = "JDownTiflet2024"
            if Account_menu(driver):
                print(f"{time_now()} : Profile button Found")
                if Account_cible(driver,user):
                    print(f"{time_now()} : account switch success")
                    attempts = 0
                    while get_profile_link(driver) != user and attempts < 10:
                        attempts += 1
                        print(f"{time_now()} : nouvelle tentative de switch account dans une seconde(s)...")
                        time.sleep(1)
                    if get_profile_link(driver) == user:
                        skip = False
                        result = True
        else:
            print(f"{time_now()} : Aucun profil n'a été trouvé.")
        if skip:
            open_logout(driver)    
            print(f"{time_now()} : Go to Profile {user}")    
            result = change_account(driver,user,passwd)
        if not result:
            find = find_loginButton(driver)
            loginButton = click_loginButton(driver)
            if loginButton and loginButton:
               change_account(driver,user,passwd) 
        if profile_link != get_profile_link(driver):
            return driver
        
if __name__ == "__main__":
    url = "https://x.com/home"
    driver = google_chrome(url)
    driver = account(driver)
