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
    
def time_now():
    from datetime import datetime
    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    return now.strftime("%H:%M:%S:%f")[:-3]

def get_post(driver):
    from bs4 import BeautifulSoup
    try:      
        # Récupérer le contenu HTML de la page
        html_content = driver.page_source

        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # Rechercher l'élément <span> contenant le texte spécifié
             
        if find_tag(driver,"div","data-testid","cellInnerDiv"):
            print(f"{time_now()} : Posts Trouve")
            posts = soup.find_all("div","data-testid","cellInnerDiv")
            if posts:
                print(f"{time_now()} : Posts Vide")
                return posts
            else:

        else :
            print(f"{time_now()} : Posts Pas Trouve")
            return False 
    except AttributeError:
        print(f"{time_now()} : Erreur : Impossible de trouver les Posts.")
        return False
    except Exception as e:
        print(f"{time_now()} : Une erreur inattendue s'est produite :", e)
        return False

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

