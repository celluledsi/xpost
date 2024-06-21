from package import install_package,google_chrome,init_chrome
from Xaccount import account
install_package("selenium")
install_package("bs4")


def time_now():
    from datetime import datetime
    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    return now.strftime("%H:%M:%S:%f")[:-3]
    
def find_element_by_css(driver, css_selector, max_attempts=10):
    import time
    from selenium import webdriver
    attempts = 0
    while attempts < max_attempts:
        try:
            element = driver.execute_script(f"return document.querySelector('{css_selector}');")
            if element:
                return True
            else:
                attempts += 1
                time.sleep(1)  # Attendre 1 seconde avant la prochaine tentative
        except:
            attempts += 1
            time.sleep(1)  # Attendre 1 seconde avant la prochaine tentative
    
    return False

def save_text_to_file(text, encoding="utf-8"):
    import os
    import subprocess
    from datetime import datetime
    """
    Enregistre le texte spécifié dans un fichier avec un nom basé sur la date et l'heure actuelles.
    
    Args:
        text (str): Le texte à enregistrer dans le fichier.
        encoding (str, optional): L'encodage à utiliser pour l'écriture du fichier. Par défaut, "utf-8".
    """
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    file_name = f"texte_{current_datetime}.txt"
    file_path = os.path.join(os.getcwd(), file_name)
    
    with open(file_path, "w", encoding=encoding) as file:
        file.write(text)
    subprocess.run(['explorer.exe', file_path])

def fetch_content(driver):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    if find_element_by_css(driver, 'div[aria-label="Home timeline"]'):  
        try:
            # Récupérer le contenu HTML de la page
            html_content = driver.page_source

            # Utiliser BeautifulSoup pour analyser le contenu HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Rechercher tous les éléments <span>
            span_elements = soup.find_all('span')

            # Vérifier si des éléments <span> ont été trouvés
            if not span_elements:
                print(f"{time_now()} : Aucun élément <span> n'a été trouvé.")
                return False
            else:
                # Afficher le texte de chaque élément <span>
                for index, span in enumerate(span_elements):
                    inner_html = ''.join(str(child) for child in span.children)
                    if "Account suspended" in inner_html:
                        print(f"{time_now()} : {inner_html}")
                        return True
        except Exception as e:
            print(f"{time_now()} : Erreur lors de la recherche des éléments <span>: {str(e)}")
            return False
        
def find_wrong(driver):
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException
    try:
        print(f"{time_now()} : find_wrong.")
        # Récupérer le contenu HTML de la page
        html_content = driver.page_source

        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # Rechercher l'élément <span> contenant le texte spécifié
        span_element = soup.find('span', string='Something went wrong. Try reloading.')

        if span_element:
            print(f"{time_now()} : Something went wrong.")
            driver.quit()
            return True  # Retourner True pour indiquer que l'erreur a été trouvée
        else:
            return False  # Retourner False pour indiquer que l'erreur n'a pas été trouvée

    except (NoSuchWindowException, NoSuchElementException):
        return False  # Retourner False pour indiquer que l'erreur n'a pas été trouvée

def get_post(driver):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.common.exceptions import NoSuchElementException
    wait = WebDriverWait(driver, 10)
    try:
        # Attendre que les éléments soient présents sur la page
        posts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))
        # Vérifier s'il y a au moins un post
        if posts:
            return posts
        else:
            return False
    except TimeoutException:
        print(f"{time_now()} : Délai d'attente dépassé, impossible de trouver les éléments.")
        return False
    except NoSuchElementException:
        print(f"{time_now()} : Impossible de trouver les éléments sur la page.")
        return False
    except StaleElementReferenceException:
        print(f"{time_now()} : Référence à un élément qui n'est plus présent sur la page.")
        return False
    except Exception as e:
        print(f"{time_now()} : Une erreur inattendue s'est produite : {e}")
        return False

def is_present(element, css_element):
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.by import By
    try:
        element.find_element(By.CSS_SELECTOR, css_element)
        return True
    except NoSuchElementException :
        return False
    except StaleElementReferenceException:
        return False
    
def get_last_article_time_element(last_article):
    from bs4 import BeautifulSoup
    try:
        # Extraire le HTML de l'élément
        html = last_article.get_attribute('outerHTML')
        
        # Utiliser BeautifulSoup pour analyser le HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Trouver l'élément enfant <time> avec l'attribut datetime
        time_element = soup.find('time', datetime=True)
        
        if time_element:
             # Récupérer l'élément parent de time_element
            parent_element = time_element.find_parent()
            
            # Récupérer la valeur de l'attribut 'href' si le parent est un lien <a>
            href_value = None
            if parent_element.name == 'a' and 'href' in parent_element.attrs:
                href_value = parent_element['href']
                
            return time_element, time_element['datetime'], href_value
        else:
            print(f"{time_now()} : last élément <time> avec l'attribut datetime n'a été trouvé.")
            return None, None, None
    except Exception:
        print(f"{time_now()} : Erreur lors de l'analyse de last élément")
        return None, None, None

def get_link(post,link_list):
    from selenium.webdriver.common.by import By
    link_count = 0
    last_element = False
    last_datetime = None
    for element in post:
        #print(element.get_attribute("innerHTML"))
        #print(element)
        # Appeler la fonction pour obtenir l'élément <time> et sa valeur datetime
        time_element, datetime_value, link = get_last_article_time_element(element)
        if time_element:
            #print(link)
            if [link, datetime_value] not in link_list:
                link_list.append([link, datetime_value])
                #print([link, datetime_value])
                last_datetime = datetime_value
                link_count += 1
        last_element = element
    print(f"{time_now()} : {last_datetime}")
    return link_count, link_list,last_element

def calculate_duration(link_list,days_threshold):
    from datetime import datetime, timezone
    # Récupérer la valeur de l'attribut "datetime"
    last_datetime_str = link_list[-1][1]
    # Convertir la valeur en objet datetime
    date_time = datetime.fromisoformat(last_datetime_str.replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
    #print(date_time)
    # Obtenir la date actuelle
    now = datetime.now(timezone.utc)
    # Calculer la durée
    duration = now - date_time
    if duration.days < days_threshold:
        return True
    else:
        return False
    
def scroll_end(driver):
    import time
    from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException
    try:
        from selenium.common.exceptions import NoSuchWindowException
        # Faire défiler l'élément dans la vue
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        # Attendre 5 secondes
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return False
    except (NoSuchWindowException, NoSuchElementException) as e:
        print(f"{time_now()} : Error scroll_end : {str(e)}")
        return True            

def get_tag_id(selenium_post):
    from bs4 import BeautifulSoup
    # Transformer l'élément Selenium en élément BeautifulSoup
    html = selenium_post.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    beautifulsoup_post = soup.find('*')

    # Extraire le tag et l'ID de l'élément BeautifulSoup
    tag_name = beautifulsoup_post.name
    element_id = beautifulsoup_post.get('id', None)

    return tag_name, element_id

def socialContext(driver, post):
    from selenium.common.exceptions import NoSuchElementException
    from bs4 import BeautifulSoup
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    try:
        tag_name = post.tag_name
        element_id = post.get_attribute("id")
    except NoSuchElementException:
        print(f"{time_now()} : L'élément post n'a pas été trouvé sur la page.")
        return False
    except Exception as e:
        print(f"{time_now()} : Une erreur s'est produite : {e}")
        return False
    beautifulsoup_post = soup.find(tag_name, id=element_id)
    # Récupérer le parent initial
    parent_element = beautifulsoup_post.parent
    # Remonter dans les parents jusqu'à trouver un élément "article" avec un attribut "aria-labelledby"
    while parent_element:
        tag_name = parent_element.name
        if tag_name == 'article' and parent_element.get_attribute('aria-labelledby'):
            print(f"{time_now()} : Parent article avec aria-labelledby trouvé.")
            return parent_element.find('span', {'data-testid': 'socialContext'}) is not None
        parent_element = parent_element.parent
    # Si aucun élément correspondant n'est trouvé, renvoyer None
    print(f"{time_now()} : Aucun élément parent article avec aria-labelledby n'a été trouvé.")
    return False
    
def save_links(url,link_list,file_path):
    with open(file_path, 'a') as file:
        for link, datetime_str in link_list:
            full_url = f"https://x.com{link}"
            print(f"Link: {full_url}")
            print(f"Datetime: {datetime_str}")
            print()
            file.write(full_url + '\n')
        file.write(datetime_str + '\n')
        file.write(f"X: {url}'\n'")

#scrapp chrome and extract urls
def scrap_compte(url,driver,file_path_save,days_threshold,index):
    link_list = []
    scroll_echec = False
    if fetch_content(driver):
        keep_going = False
        saving = False
    else:
        keep_going = True
        saving = True
    num_days = 10
    count_try = 0
    count_scroll = 0
    while keep_going:
        print(f"{time_now()} : get post")
        posts = get_post(driver)    
        if posts:
            print(f"{time_now()} : get links")
            link_count, link_list,post = get_link(posts,link_list)
            print(f"{time_now()} : count_link : {link_count}")
            if not post:
                print(f"{time_now()} : No end post")
                keep_going = False
            #for i, element in enumerate(link_list):
            #    print(f"Post numéro {i+1} : {element[0]} {element[1]}")
            if link_count > 0:
                count_try = 0
                print(f"{time_now()} : check calculate_duration")
                if calculate_duration(link_list,days_threshold):
                    print(f"{time_now()} : calculate_duration ok. scroll_end")
                    scroll_echec = scroll_end(driver)
                else:
                    print(f"{time_now()} : calculate_duration no. check socialContext")
                    if socialContext(driver,post):
                        print(f"{time_now()} : socialContext ok. scroll_end")
                        scroll_echec = scroll_end(driver)                
                    else:
                        print(f"{time_now()} : socialContext No. old post")
                        keep_going = False
            else :
                count_try += 1
                print(f"{time_now()} : count_try : {count_try}")
                if count_try < 10 :
                    print(f"{time_now()} : count_try ok. scroll_end")
                    scroll_echec = scroll_end(driver)      
                else:
                    print(f"{time_now()} : max try")
                    keep_going = False
        else:
            count_scroll += 1
            print(f"{time_now()} : count_scroll : {count_scroll}")
            if count_scroll < 10:
                print(f"{time_now()} : count_scroll ok. scroll_end")
                scroll_echec = scroll_end(driver)
            else:
                print(f"{time_now()} : End. Aucun posts")
                keep_going = False
        print(f"{time_now()} : Check wrong")
        wrong = find_wrong(driver)
        if wrong or scroll_echec:
            while wrong:
                print(f"{time_now()} : find wrong status : {wrong}")
                driver = account(url,driver)
                wrong = find_wrong(driver)
            print(f"{time_now()} : scroll_echec : {scroll_echec}")
            index -= 1
            saving = False
            keep_going = False
        
    ordre = index + 1 
    if saving:
        save_links(url,link_list,file_path_save)
    return ordre,driver
    
#extract url from filname 
def open_url(file_name,days_threshold):
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    import os
    import subprocess
    from datetime import datetime
    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    file_name_save = f"links_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    # Chemin du fichier dans le même répertoire que le script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_save = os.path.join(script_dir, file_name_save)
    # Chemin du fichier dans le même répertoire que le script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_open = os.path.join(script_dir, file_name)
    # Lecture des URLs à partir du fichier 'comptetwitter.txt'
    with open(file_path_open, 'r') as file:
        urls_to_check = file.readlines()
        urls_to_check = [url.strip() for url in urls_to_check]
    # Parcourir chaque URL et vérifier s'il y a une erreur
    index = 0
    driver = init_chrome()
    while index < len(urls_to_check):
        url = urls_to_check[index]
        try:    
            driver.get(url)
        except WebDriverException:
            driver = google_chrome(url)
        print(f"{time_now()} : Google Chrome : {url}")
        index,driver = scrap_compte(url,driver,file_path_save,days_threshold,index)
        
    subprocess.run(['explorer.exe', file_path_save])

days_threshold = 300           
file_name = 'comptetwitter.txt'            
open_url(file_name,days_threshold)        
print(f"{time_now()} : Goodbye!")

