
import math
import os
from pathlib import Path
from tkinter import Tk, filedialog
import random as r
from math import gcd as bltin_gcd

class ChoiceHandler:
    # Konstruktor
    def __init__(self):
        self.is_picked = None
        self.prime_p = None
        self.prim_root_g = None
        self.private_key1 = None
        self.private_key2 = None
        self.full_key = None
        self.decryptFilename = None
        self.filename = None
        self.decryptMode = None
        self.encryptMode = None
        self.mode = None
        self.parsedMessage = None
        self.menu_options_cypher_selection = {
            1: 'Zašifrovat',
            2: 'Dešifrovat',
            3: 'Exit',
        }
        self.menu_options_input_message = {
            1: 'Textový řetězec',
            2: 'Soubor (*.txt)',
            3: 'Exit',
        }
        self.menu_p_q_selection = {
            1: 'Náhodně',
            2: 'Vlastní',
            3: 'Exit',
        }
        self.menu_options_keep_going = {
            1: 'Ano',
            2: 'Ne (exit)',
        }

    def restart_app(self):
        self.prime_p = None
        self.prim_root_g = None
        self.private_key1 = None
        self.private_key2 = None
        self.full_key = None
        self.decryptFilename = None
        self.filename = None
        self.decryptMode = None
        self.encryptMode = None
        self.mode = None
        self.parsedMessage = None
        self.is_picked = None
        ch.start()

    def keep_going(self):
        if self.encryptMode or self.decryptMode:
            while True:
                self.print_menu_keep_going()
                option = ''
                try:
                    option = int(input('Přejete si pokračovat?: '))
                except:
                    print('Špatný výběr. Zkuste to znovu.')
                if option == 1:
                    self.restart_app()
                elif option == 2:
                    exit()
                else:
                    print('Špatný výběr. Vložte číslo mezi 1 až 2.')

    def print_menu_keep_going(self):
        for key in self.menu_options_keep_going.keys():
            print(key, '--', self.menu_options_keep_going[key])

    def start(self):
        while self.encryptMode is None or self.decryptMode is None:
            self.print_menu_cypher_selection()
            option = ''
            try:
                option = int(input('Vyberte, jestli chcete šifrovat nebo dešifrovat: '))
            except:
                print('Špatný výběr. Zkuste to znovu.')
            if option == 1:
                self.encryptMode = True
                self.select_input()
                self.select_p_g_key_gen()
                self.secret_key_by_user1()
                self.secret_key_by_user2()
                self.calculate_public_keys()
                self.encrypt_message()
                self.keep_going()
            elif option == 2:
                self.decryptMode = True
                self.input_key()
                self.parse_input_file_for_decryption()
                self.decrypt_message()
                self.keep_going()
            elif option == 3:
                print('Program ukončen.')
                exit()
            else:
                print('Špatný výběr. Vložte číslo mezi 1 až 3.')

    def parse_input_file_for_decryption(self):
        self.open_file_text()
        while self.filename == '':
            print("Nevybraný soubor. Vyberte soubor znovu.")
            self.open_file_text()

        f = open(self.filename, "r", encoding="utf-8")
        self.parsedMessage = f.read()

    def print_menu_cypher_selection(self):
        for key in self.menu_options_cypher_selection.keys():
            print(key, '--', self.menu_options_cypher_selection[key])

    def select_input(self):
        if self.encryptMode:
            while self.parsedMessage is None:
                self.print_menu_input_msg()
                option = ''
                try:
                    option = int(input('Vyberte, jestli chcete zašifrovat řetězec, nebo textový soubor: '))
                except:
                    print('Špatný výběr. Zkuste to znovu.')
                if option == 1:
                    self.show_input_text()
                elif option == 2:
                    self.show_input_file_as_text()
                elif option == 3:
                    print('Program ukončen.')
                    exit()
                else:
                    print('Špatný výběr. Vložte číslo mezi 1 až 3.')
        if self.decryptMode:
            self.open_file_text()
            print("Načtěte soubor, který chcete dešifrovat.")

    def print_menu_input_msg(self):
        for key in self.menu_options_input_message.keys():
            print(key, '--', self.menu_options_input_message[key])

    def show_input_text(self):
        self.parse_input_text_from_user()
        print("\nVložená zpráva k zašifrování: \n")
        print("--------- ZAČÁTEK ZPRÁVY ---------\n")
        if len(self.parsedMessage) > 100:
            print(self.parsedMessage[0:100], "\n\t ... (", len(self.parsedMessage) - 100,
                  ") dalších znaků.")
        else:
            print(self.parsedMessage)
        print("\n--------- KONEC ZPRÁVY ---------\n")

    def parse_input_text_from_user(self):
        temp = str(self.get_input_text_from_user())
        self.parsedMessage = temp

    def get_input_text_from_user(self):
        input_msg = input("Vložte zprávu k zašifrování: ")
        return input_msg

    def open_file_text(self):
        window = Tk()
        window.wm_attributes('-topmost', 1)
        window.withdraw()
        try:
            self.filename = filedialog.askopenfilename(parent=window,
                                                       title="Vyberte textový soubor",
                                                       filetypes=(("Text files", "*.txt"),))
            return self.filename
        except:
            print("Zvolte soubor!")
            return

    def show_input_file_as_text(self):
        self.parse_input_file_for_encryption()
        if len(self.parsedMessage) > 100:
            print("Zpráva je příliš dlouhá. Výpis prvních 100 znaků: ")
            print("--------- ZAČÁTEK ZPRÁVY ---------\n")
            print(self.parsedMessage[0:100], "\n\t ... (", len(self.parsedMessage) - 100,
                  ") dalších znaků.")
        else:
            print("\nVložená zpráva k zašifrování: \n")
            print("--------- ZAČÁTEK ZPRÁVY ---------\n")
            print(self.parsedMessage)

        print("\n--------- KONEC ZPRÁVY ---------\n")

    def parse_input_file_for_encryption(self):
        while self.filename is None or self.filename == '':
            print("Nevybraný soubor. Vyberte soubor znovu.")
            self.open_file_text()

        if os.path.isfile(self.filename):
            temp = Path(self.filename).read_text('utf-8')
        else:
            return

        self.parsedMessage = temp

    def encrypt_message(self):

        encrypted_message = ""
        key = self.full_key
        for c in self.parsedMessage:
            encrypted_message += chr(ord(c) + key)

        file_out = open("encrypted.txt", "w", encoding="utf-8")
        file_out.write(encrypted_message)
        file_out.close()

        return encrypted_message

    def decrypt_message(self):
        decrypted_message = ""
        key = int(self.full_key)
        for c in self.parsedMessage:
            decrypted_message += chr(ord(c) - key)

        with open('decrypted.txt', 'w', encoding="utf-8") as f:
            f.write(decrypted_message)

        if len(decrypted_message) >= 100:
            print("Dešifrovaná zpráva je příliš dlouhá. Výpis prvních 100 znaků: ")
            print("--------- ZAČÁTEK ZPRÁVY ---------\n")
            print(decrypted_message[0:100], "\n\t ... (", len(decrypted_message) - 100,
                  ") dalších znaků.")
        else:
            print("\nDešifrovaný text: \n")
            print("--------- ZAČÁTEK ZPRÁVY ---------\n")
            print(decrypted_message)

        print("\n--------- KONEC ZPRÁVY ---------\n")
        print("\n Dešifrovaný soubor uložen jako: decrypted.txt\n")
        with open('decrypted.txt', 'w') as f:
            f.write(decrypted_message)

        return decrypted_message

    def select_p_g_key_gen(self):
        while self.prime_p is None or self.prim_root_g is None:
            self.print_menu_p_g_selection()
            option = ''
            try:
                option = int(input('Zvolte způsob zadání 1. a 2. veřejného klíče: '))
            except:
                print('Špatný výběr. Zkuste to znovu.')
            if option == 1:
                self.p_g_random()
                self.is_picked = False
            elif option == 2:
                self.prime_p_by_user()
                self.primitive_root_g_by_user()
                self.is_picked = True
            elif option == 3:
                print('Program ukončen.')
                exit()
            else:
                print('Špatný výběr. Vložte číslo mezi 1 až 3.')

    def print_menu_p_g_selection(self):
        for key in self.menu_p_q_selection.keys():
            print(key, '--', self.menu_p_q_selection[key])

    def p_g_random(self):
        out = list()
        sieve = [True] * (2000 + 1)
        for p in range(2, 2000 + 1):
            if sieve[p] and sieve[p] % 2 == 1:
                out.append(p)
                for i in range(p, 2000 + 1, p):
                    sieve[i] = False

        self.prime_p = r.choice(out)
        self.prim_root_g = r.choice(self.prim_roots(self.prime_p))
        print("Prvočíslo p: ", self.prime_p, "Číslo g: ", self.prim_root_g)

    def prime_p_by_user(self):
        while self.prime_p is None:
            temp = input("Vložte p: ")
            if not str.isnumeric(temp):
                print("Vložte pouze číslice.")
            elif not self.is_prime(int(temp)):
                print("Vložte prvočíslo.")
            else:
                self.prime_p = int(temp)

    def primitive_root_g_by_user(self):
        while self.prim_root_g is None:
            temp = input("Vložte g: ")
            if not str.isnumeric(temp):
                print("Vložte pouze číslice.")
            elif int(temp) not in self.prim_roots(int(self.prime_p)):
                print("Číslo g není primitivním kořenem modulo p. Napište jedno z následujících čísel: ")
                print(self.prim_roots(int(self.prime_p)))
            else:
                self.prim_root_g = int(temp)

    def secret_key_by_user1(self):
        while self.private_key1 is None:
            temp = input("Vložte tajný mocnitel 1: ")
            if not str.isnumeric(temp):
                print("Vložte pouze číslice.")
            else:
                self.private_key1 = int(temp)

    def secret_key_by_user2(self):
        while self.private_key2 is None:
            temp = input("Vložte tajný mocnitel 2: ")
            if not str.isnumeric(temp):
                print("Vložte pouze číslice.")
            else:
                self.private_key2 = int(temp)

    def prim_roots(self, modulo):
        required_set = {num for num in range(1, modulo) if bltin_gcd(num, modulo)}
        ret = [g for g in range(1, modulo) if required_set == {pow(g, powers, modulo)
                                                                for powers in range(1, modulo)}]

        return ret

    def is_prime(self, n):
        if n == 2:
            return True
        if n % 2 == 0 or n <= 1:
            return False

        sqr = int(math.sqrt(n)) + 1

        for divisor in range(3, sqr, 2):
            if n % divisor == 0:
                return False
        return True

    def calculate_public_keys(self):
        A = self.prim_root_g ** self.private_key1 % self.prime_p
        B = self.prim_root_g ** self.private_key2 % self.prime_p
        s1 = B ** self.private_key1 % self.prime_p
        s2 = A ** self.private_key2 % self.prime_p

        if s1 == s2:
            self.full_key = s1
            print("\n ---------- SIMULACE PŘENOSU ---------- ")
            if self.is_picked:
                print("\n Vložili jste prvočíslo p a primitivní kořen modulo p - g: ", "[ p = ", self.prime_p, ", g = ", self.prim_root_g,"]")
            elif not self.is_picked:
                print("\n Náhodně jste vygenerovali prvočíslo g a primitivní kořen modulo p - g: ", "[ p = ", self.prime_p, ", g = ", self.prim_root_g,"]")
            print("\n Vložili jste tajné mocnitele: ", "[ x = ", self.private_key1, ", y = ", self.private_key2,"]")
            print("\n Proběhl výpočet a sdílení veřejných klíčů obou stran: ", "[ A = ", A, ", B = ", B,"]")
            print("\n Obě strany si vypočítaly tajný klíč následujícím postupem: ")
            print("\n Strana 1: ", "s1 = ", "B^x % p")
            print("\n Strana 1: ", "s1 = ", B, "^", self.private_key1, "%", self.prime_p, " = ", s1)
            print("\n Strana 2: ", "s2 = ", "A^y % p")
            print("\n Strana 2: ", "s2 = ", A, "^", self.private_key2, "%", self.prime_p, " = ", s2)
            print("\n ----------------------------------------------------")
            print("\n Oběma stranám vyšel stejný tajný klíč použitý k zašifrování: ", "[ s1 = ", s1, " s2 = ", s2,"]")
            print("\n ----------------------------------------------------")
            print("\n\n Zpráva byla zašifrovaná a uložena jako encrypted.txt.\n")
        else:
            print("Něco se pokazilo.")

    def input_key(self):
        while self.full_key is None:
            self.full_key = input("Vložte tajný klíč použitý k zašifrování: ")

if __name__ == '__main__':
    print("\n##----------------------- INFORMACE O PROGRAMU -----------------------##\n"
          "\nProgram slouží k zašifrování libovolného textu ze vstupu uživatele či z textového souboru s příponou .txt."
          "\nProgram simuluje výměnu klíčů pomocí algoritmu Diffie-Hellman."
          "\nUživatel buď vybírá prvočíslo p a primitivní kořen modula p - g, nebo je program náhodně generuje."
          "\nV případě výběru náhodného generování, program sám generuje náhodné prvočíslo v intervalu 1-2000."
          "\nPokud uživatel zadá číslo g ručně, ale zvolí nevhodně, program sám vygeneruje nabídku čísel g, které jsou přijatelné pro zvolené prvočíslo p."
          "\nUživatel dále zvolí tajné číslo x a tajné číslo y, tedy mocnitele."
          "\nProběhne simulace a názorná ukázka výpočtu veřejných klíčů A a B."
          "\nNa konci simulace proběhne taktéž výpočet tajného klíče. Ten se nikde neukládá, uživatel si jej musí zapamatovat."
          "\nK dešifrování je potřeba zvolit soubor se zašifrovaným textem a vložit tajný kód, který byl použitý k zašifrování tohoto textu."
          "\nPokud je zadaný klíč nesprávný, pak výsledný dešifrovaný řetězec nebude dávat smysl."
          "\nZašifrovaný text se ukládá do souboru encrypted.txt ve složce s programem."
          "\nDešifrovaný text se ukládá do souboru decrypted.txt ve složce s programem.\n")
    ch = ChoiceHandler()
    ch.start()