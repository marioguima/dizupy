from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import schedule
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from datetime import datetime, time
from random import randint
import json

INSTA_LINK = "https://www.instagram.com/"
DIZU_LINK = "https://dizu.com.br/login"
PAINEL_CONECTAR = "https://dizu.com.br/painel/conectar"

# XPATH DIZU
xDIZU_USUARIO = "//*[@id='login']"
xDIZU_SENHA = "//*[@id='senha']"
xDIZU_BTN_ACESSAR = "//*[contains(@class, 'bg-orange')]"
xDIZU_SELECT_INSTAGRAM = "//*[@id='instagram_id']"
xDIZU_BTN_INICIAR_TAREFA = "//*[@id='iniciarTarefas']"
xDIZU_BOXE_USER = "//*[contains(@class, 'box_user')]"
xDIZU_BTN_VER_LINK = "//*[@id='conectar_step_4']"
xDIZU_BTN_CONFIRMAR = "//*[@id='conectar_step_5']"
xDIZU_SEM_TAREFA = "//p[contains(text(), 'não existem tarefas disponíveis no momento')]"

# XPATH INSTAGRAM
xINSTA_USUARIO = "//*[@name='username']"
xINSTA_SENHA = "//*[@name='password']"
xINSTA_BTN_ENTRAR = "//*[contains(@class, 'L3NKy')]"

xINSTA_BTN_NAO_ATIVAR_NOTIFICACAO = "//button[contains(text(), 'Agora não')]"
xINSTA_ICONE_PERFIL = "//*[contains(@class, '_47KiJ')]//*[contains(@class, '_2dbep')]"
xINSTA_SAIR = "//div[text()='Sair']"

xINSTA_BTN_SEGUIR = "//button[text()='Seguir']"


# def wait_for(condition_function):
#     start_time = time.time()
#     while time.time() < start_time + 3:
#         if condition_function():
#             return True
#         else:
#             time.sleep(0.1)
#     raise Exception(
#         'Timeout waiting for {}'.format(condition_function.**name**)
#     )


# class wait_for_page_load(object):
#     def __init__(self, browser):
#         self.browser = browser

#     def __enter__(self):
#         self.old_page = self.browser.find_element_by_tag_name('html')

#     def page_has_loaded(self):
#         new_page = self.browser.find_element_by_tag_name('html')
#         return new_page.id != self.old_page.id

#     def __exit__(self, *_):
#         wait_for(self.page_has_loaded)


class Dizu:
    def __init__(self):
        self.driver = self._setup_driver()

    @staticmethod
    def _setup_driver():
        chrome_options = Options()
        chrome_options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        chrome_options.add_argument('lang=pt-br')
        chrome_options.add_argument(
            f'--user-data-dir=C:\\Users\\mario\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 8')
        chrome_options.add_argument("disable-infobars")

        driver = webdriver.Chrome(
            chrome_options=chrome_options, executable_path=os.path.dirname(os.path.realpath(__file__)) + '\\chromedriver.exe')
        driver.maximize_window()
        return driver

    def _get_element(self, xpath, attempts=5, _count=0):
        try:
            element = self.driver.find_element_by_xpath(xpath)
            # print('Found element!')
            return element
        except Exception as e:
            if _count < attempts:
                sleep(1)
                # print(f'Attempt {_count}')
                self._get_element(
                    xpath, attempts=attempts, _count=_count+1)
            else:
                print("Element not found")

    def _click(self, xpath):
        el = self._get_element(xpath)
        el.click()

    def _send_keys(self, xpath, message):
        el = self._get_element(xpath)
        el.send_keys(message)

    def hasXpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False

    def conectarGanharInstagram(self):
        with open(os.path.join('data', 'accounts.json'), 'r') as json_file:
            self.accounts = json.load(json_file)
        for accountDizu in self.accounts:
            self.loginDizu(accountDizu['dizu'].username,
                           accountDizu['dizu'].password)
            for accountInstagram in accountDizu:
                self.loginInstagram(accountInstagram.username,
                                    accountInstagram.password)
                self.selecionarPerfilInstagram(accountInstagram.username)
                self.executarTarefaSeguir()

    def loginDizu(self, usuario, senha):
        self.driver.get(DIZU_LINK)

        wait = WebDriverWait(self.driver, 10)

        # usuario
        wait.until(EC.visibility_of_element_located((By.XPATH, xDIZU_USUARIO)))
        self._send_keys(xDIZU_USUARIO, usuario)

        # senha
        wait.until(EC.visibility_of_element_located((By.XPATH, xDIZU_SENHA)))
        self._send_keys(xDIZU_SENHA, senha)

        self._click(xDIZU_BTN_ACESSAR)

    def loginInstagram(self, usuario, senha):
        wait = WebDriverWait(self.driver, 10)

        # Store the ID of the original window
        original_window = self.driver.current_window_handle

        # Opens a new tab and switches to new tab
        self.driver.execute_script("window.open('" + INSTA_LINK + "')")

        # Wait for the new window or tab
        wait.until(EC.number_of_windows_to_be(2))

        # Loop through until we find a new window handle
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

        # carrega instagram
        # self.driver.get(INSTA_LINK)

        if self.hasXpath(xINSTA_BTN_NAO_ATIVAR_NOTIFICACAO):
            self._click(xINSTA_BTN_NAO_ATIVAR_NOTIFICACAO)

            if not self.hasXpath("//*[contains(@alt, '" + usuario + "')]"):
                self._click(xINSTA_ICONE_PERFIL)

                sleep(1)

                self._click(xINSTA_SAIR)

                # usuario
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, xINSTA_USUARIO)))

        # só vai logar se a conta logada anteriormente for diferente
        if self.hasXpath(xINSTA_USUARIO):
            # usuario
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, xINSTA_USUARIO)))
            self._send_keys(xINSTA_USUARIO, usuario)

            # senha
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, xINSTA_SENHA)))
            self._send_keys(xINSTA_SENHA, senha)

            # logar
            self._click(xINSTA_BTN_ENTRAR)

        # aguardar carregar
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@alt, '" + usuario + "')]")))

        # FECHAR A ABA
        self.driver.close()

        # Switch back to the old tab or window
        self.driver.switch_to.window(original_window)

    def selecionarPerfilInstagram(self, perfil):
        self.driver.get(PAINEL_CONECTAR)

        # SELECIONAR CONTA DO INSTAGRAM
        self.driver.find_element_by_xpath(
            xDIZU_SELECT_INSTAGRAM + "/option[text()='" + perfil + "']").click()

        # INICIAR TAREFA
        self._click(xDIZU_BTN_INICIAR_TAREFA)

    def executarTarefaSeguir(self):
        wait = WebDriverWait(self.driver, 10)
        try:
            # AGUARDA O BOX DO USUÁRIO PARA SEGUIR
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, xDIZU_BOXE_USER)))

            # Store the ID of the original window
            original_window = self.driver.current_window_handle

            # BOTÃO PARA O LINK DO INSTAGRAM
            self._click(xDIZU_BTN_VER_LINK)

            # Wait for the new window or tab
            wait.until(EC.number_of_windows_to_be(2))

            # Loop through until we find a new window handle
            for window_handle in self.driver.window_handles:
                if window_handle != original_window:
                    self.driver.switch_to.window(window_handle)
                    break

            # AGUARDA O BOTÃO DE SEGUIR
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, xINSTA_BTN_SEGUIR)))

            # SEGUIR
            self._click(xINSTA_BTN_SEGUIR)

            # FECHAR A ABA
            self.driver.close()

            # Switch back to the old tab or window
            self.driver.switch_to.window(original_window)

            # AGUARDA O BOTÃO CONFIRMAR
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, xDIZU_BTN_CONFIRMAR)))

            # CONFIRMAR DEPOIS DE SEGUIR
            self._click(xDIZU_BTN_CONFIRMAR)

            # interagir devager
            sleep(randint(5, 10))
        finally:
            if self.hasXpath(xDIZU_BOXE_USER):
                self.executarTarefaSeguir()

    def end(self):
        sleep(5)
        self.driver.close()


dizu = Dizu()
dizu.loginDizu('marioguimaemail01@gmail.com', '*Mcsg2408')
dizu.loginInstagram('biancaamaralbr', '*Bibiamaral')
dizu.selecionarPerfilInstagram('biancaamaralbr')


# def in_between(now, start, end):
#     if start <= end:
#         return start <= now < end
#     else:  # over midnight e.g., 23:30-04:15
#         return start <= now or now < end

dizu.executarTarefaSeguir()
# if __name__ == "__main__":
#     # if in_between(datetime.now().time(), time(9), time(22)):
#     #     dizu.executarTarefaSeguir()

#     schedule.every().day.at("10:30").do(dizu.conectarGanharInstagram)
#     schedule.every().day.at("13:00").do(dizu.conectarGanharInstagram)
#     schedule.every().day.at("18:00").do(dizu.conectarGanharInstagram)
#     schedule.every().day.at("22:00").do(dizu.conectarGanharInstagram)

#     while True:
#         schedule.run_pending()
#         sleep(1)

dizu.end()
