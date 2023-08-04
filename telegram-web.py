import time, pandas, dotenv, os, logging, sys, datetime

from browser_instance import meu_browser
from selenium.webdriver.remote.errorhandler import InvalidElementStateException

dotenv.load_dotenv('config.env')
logging.basicConfig(
    level=logging.WARNING,
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s: %(message)s'
)


def salvar_excel(df, nome_do_arquivo):
    try:
        logging.warning('Salvando o arquivo, não encerre agora para não corromper...')
        time.sleep(3)
        with pandas.ExcelWriter(nome_do_arquivo, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        logging.warning("Arquivo Salvo com sucesso!")
        time.sleep(3)
        return True
    except PermissionError:
        input("Arquivo está aberto, feche para salvar o registro do LOG (Enter para prosseguir)")
        return False


def automatiza_telegram(driver, fone, name, mensagem) -> str:
    """
    Returns:
        "mensagem do log"
    """
    driver.visit('https://web.telegram.org/a/')
    time.sleep(1)

    logging.warning("expandindo opçoes")
    # btn_sandwich = driver.find_by_xpath('//button[@title="Abrir menu"]')
    btn_sandwich = driver.find_by_xpath('//button[@title="Open menu"]')
    btn_sandwich.click()
    time.sleep(1)

    logging.warning("Clicando em contatos")
    # contacts = driver.find_by_text('Contatos')
    contacts = driver.find_by_text('Contacts')
    contacts.click()
    time.sleep(1)

    logging.warning("Adicionar novo contatos")
    # new_contacts = driver.find_by_xpath('//button[@aria-label="Novo Contato"]')
    new_contacts = driver.find_by_xpath('//button[@aria-label="Create New Contact"]')
    new_contacts.click()
    time.sleep(1)

    logging.warning("Preenchendo número")
    # phone_number = driver.find_by_xpath('//input[@aria-label="Número de Telefone"]')
    phone_number = driver.find_by_xpath('//input[@aria-label="Phone Number"]')
    phone_number.fill(str(fone))
    time.sleep(1)

    logging.warning("Adicionar nome")
    # first_name = driver.find_by_xpath('//input[@aria-label="Nome (obrigatório)"]')
    first_name = driver.find_by_xpath('//input[@aria-label="First name (required)"]')
    first_name.fill(name)
    time.sleep(1)

    logging.warning("Clicando em pronto")
    # done = driver.find_by_text('Pronto')
    done = driver.find_by_text('Done')
    done.click()
    time.sleep(1)

    encontrou_user = driver.is_element_present_by_xpath(
        '//div[@class="messages-layout"]//div[@class="info"]//h3', wait_time=5
        )
    
    logging.warning(f"Encontrou chat: {encontrou_user}")
    msg = "NÃO ENCONTROU USUARIO NO TELEGRAM"
    if encontrou_user:
        msg = "ENCONTROU USUARIO NO TELEGRAM MAS NÃO ENVIOU MENSAGEM"
        timeout_count = 0
        while True:
            try:
                mensagem_livre = driver.is_element_present_by_xpath("//div[@aria-label='Message']", wait_time=5)
                if mensagem_livre:
                    driver.driver.find_element('xpath', '//div[@aria-label="Message"]').send_keys(mensagem)
                    break
                else:
                    driver.reload()
                    time.sleep(3)
            except InvalidElementStateException: # espera o elemento estar liberado para click
                driver.reload()
                time.sleep(3)
            finally:
                timeout_count += 1
                if timeout_count > 10:
                    break

        send_message = driver.find_by_xpath('//button[@aria-label="Send Message"]')
        send_message.click()
        time.sleep(1)
        msg = "ENCONTROU USUARIO NO TELEGRAM E ENVIOU MENSAGEM"
    
    return msg
    

nome_do_arquivo = os.getenv("NOME_DO_EXCEL")
try:
    df = pandas.read_excel(nome_do_arquivo)
except FileNotFoundError:
    nome_do_arquivo = input(f"Arquivo {nome_do_arquivo} não encontrado, digite o nome do excel para continuar: ")
    try: 
        df = pandas.read_excel(nome_do_arquivo)
    except FileNotFoundError:
        input("ERROOOOO!! arquivo não encontrado (lembre-se de acrescentar .xlsx no final do nome do arquivo). reinicie o executável")
        sys.exit()

df = df.fillna("") # tratar NAN para evitar corromper o excel

driver = meu_browser()
driver.visit('https://web.telegram.org/a/')
input('Após escanear o QRCODE tecle "enter"')
df.to_excel(f"BKP-{datetime.datetime.now().strftime('%d%H%M%S')}-{nome_do_arquivo}", engine="openpyxl" , index=False)

tentativas_de_disparo = 0
for index in df.index:
    coluna_log_esta_vazia = pandas.isna(df['LOG'][index])
    if coluna_log_esta_vazia == False:
        coluna_log_esta_vazia = len(df['LOG'][index]) <= 1

    if coluna_log_esta_vazia:
        tentativas_de_disparo += 1
        name = df['NOME'][index]
        fone = df['TELEFONE'][index]
        mensagem = df['MENSAGEM'][index]
        
        logging.warning(f"Tentando adicionar e enviar mensagem para {name} ({fone})")

        msg = automatiza_telegram(driver, fone, name, mensagem)
        hr_log = datetime.datetime.now().strftime("%d-%m-%Y às %H:%M:%S")

        logging.warning(msg)

        df.loc[index, 'LOG'] = msg
        df.loc[index, 'DATA'] = hr_log

        if tentativas_de_disparo % 10 == 0:
            while True:
                if salvar_excel(df, nome_do_arquivo):
                    break


        time.sleep(1)
    if tentativas_de_disparo >= 100:
        input("já chegou no limite recomendado de 100 números... conecte uma nova conta para evitar erros")
        while True:
            if salvar_excel(df, nome_do_arquivo):
                break
        driver.quit()
        sys.exit()

while True:
    if salvar_excel(df, nome_do_arquivo):
        break
driver.quit()
input("Processo finalizado. (Enter para fechar)")