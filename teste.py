import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import mysql.connector

# Caminho para o driver do Chrome
driver_path = 'chromedriver.exe'

# Configura as opções do Chrome
chrome_options = Options()
chrome_options.headless = False  # Executa o Chrome em modo não headless

# Inicializa o navegador Chrome
service = Service(driver_path)
chrome_driver = webdriver.Chrome(service=service, options=chrome_options)

# Abre o link desejado
url = 'https://www.oi.com.br/minha-oi/102busca/'
chrome_driver.get(url)



try:
    # Localiza o campo de input de nome e digita o nome desejado
    campo_input = chrome_driver.find_element(By.ID, 'input-nome-razao-social')
    campo_input.send_keys('...')
except Exception as e:
    print("Erro ao inserir nome no campo input", str(e))

try:
    # Localiza e clica no elemento <div> para abrir as opções de estado
    div_elements = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-gzVnrw.ikAvuQ'))
    )

    if len(div_elements) >= 1:
        div_element = div_elements[0]
        div_element.click()
    else:
        raise Exception("Não foi possível encontrar o elemento <div> para abrir os estados")
except Exception as e:
    print("Erro ao localizar e clicar no campo para abrir os estados", str(e))

try:
    # Localiza o elemento <div> para digitar "PR"
    div_elements = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-gzVnrw.ikAvuQ'))
    )

    if len(div_elements) >= 1:
        div_element = div_elements[0]
        input_element = div_element.find_element(By.CSS_SELECTOR, 'input.itemSelected')
        input_element.clear()
        input_element.send_keys('PR')
    else:
        raise Exception("Não foi possível encontrar o elemento <div> para digitar PR")
except Exception as e:
    print("Erro ao digitar PR", str(e))

try:
   
    button_element = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.options > button[value="PR"]'))
    )
    action = ActionChains(chrome_driver)
    action.move_to_element(button_element).click().perform()
except Exception as e:
    print("Erro ao clicar no botão PR", str(e))

try:
   
    span_element = chrome_driver.find_element(By.CSS_SELECTOR, 'span.styled__Arrow-sc-tuh5ii-0.kpukzj.arrow')
    action = ActionChains(chrome_driver)
    action.move_to_element(span_element).click().perform()
except Exception as e:
    print("Erro ao localizar e clicar no campo para abrir as cidades", str(e))

try:
    # Localiza o elemento <div> para digitar "Curitiba"
    div_elements = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-gzVnrw.ikAvuQ'))
    )

    if len(div_elements) >= 2:
        div_element = div_elements[1]
        input_element = div_element.find_element(By.CSS_SELECTOR, 'input.itemSelected')
        input_element.clear()
        input_element.send_keys('Curitiba')
    else:
        raise Exception("Não foi possível encontrar o segundo elemento <div> para digitar Curitiba")
except Exception as e:
    print("Erro ao digitar Curitiba", str(e))

try:
    # Localiza e clica no <button> com o valor "Curitiba"
    button_element = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@value="Curitiba"]'))
    )
    button_element.click()
except Exception as e:
    print("Erro ao clicar no botão Curitiba", str(e))


# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = 'mypassword'
db_name = 'mytable'

# Cria a conexão com o banco de dados
db_connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

def inserir_dados(nome, telefone, endereco):
    # Cria o cursor para executar as consultas
    cursor = db_connection.cursor()

    # Prepara a consulta SQL
    sql = "INSERT INTO loremardois (nome, telefone, endereco) VALUES (%s, %s, %s)"
    values = (nome, telefone, endereco)

    try:
        # Executa a consulta SQL
        cursor.execute(sql, values)

        # Faz o commit da transação
        db_connection.commit()
        print("Dados inseridos com sucesso!")
    except Exception as e:
        # Reverte a transação em caso de erro
        db_connection.rollback()
        print("Erro ao inserir os dados:", str(e))


def extrair_nomes():
    try:
        elementos_resultado = WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.content-result'))
        )

        if elementos_resultado:
            print('A busca foi realizada com sucesso!')
            print('Nomes encontrados:')
            for elemento in elementos_resultado:
                nome = elemento.find_element(By.CSS_SELECTOR, 'h1.titulo-result').text
                info_resultados = elemento.find_elements(By.CSS_SELECTOR, 'p.texto-result')
                telefone = info_resultados[0].text.strip()[15:]
                endereco = info_resultados[1].text.strip()[10:]
                print(nome, telefone, endereco)

                # Insere os dados no banco de dados
                inserir_dados(nome, telefone, endereco)
        else:
            print('Nenhum nome encontrado.')
    except Exception as e:
        print("Erro ao aguardar o carregamento da página de resultados", str(e))

try:
    # Aguarda a presença dos elementos necessários
    WebDriverWait(chrome_driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.content-result'))
    )

    while True:
        # Extrai nomes da página atual
        extrair_nomes()

        try:
            # Tenta localizar todos os botões com o seletor CSS do botão "Próximo"
            proximo_buttons = chrome_driver.find_elements(By.CSS_SELECTOR, 'button.styled__Button-sc-6mz6kj-0.enBOZc.btn-navegacao')

            # Verifica se há mais de um botão "Próximo"
            if len(proximo_buttons) >= 2:
                # Seleciona o segundo botão "Próximo"
                proximo_button = proximo_buttons[1]
            elif len(proximo_buttons) == 1:
                # Seleciona o único botão "Próximo" encontrado
                proximo_button = proximo_buttons[0]
            else:
                # Sai do loop se nenhum botão "Próximo" for encontrado
                break

            # Clica no botão "Próximo"
            proximo_button.click()
        except Exception:
            break  # Sai do loop se o botão "Próximo" não estiver mais presente

except Exception as e:
    print("Erro ao carregar os elementos e realizar o scraping", str(e))
    traceback.print_exc()

# Fecha o navegador
chrome_driver.quit()

# Fecha a conexão com o banco de dados
db_connection.close()