import math
import os
import secrets
import string
from math import sqrt
from pathlib import Path
from tkinter import Tk, filedialog
import random as r
from math import gcd as bltin_gcd


class ChoiceHandler:
    # Konstruktor
    def __init__(self):
        self.public_key1 = None
        self.public_key2 = None
        self.private_key = None
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
        self.menu_public_key_selection = {
            1: 'Secure-random',
            2: 'Vlastní',
            3: 'Exit',
        }
        self.menu_options_keep_going = {
            1: 'Ano',
            2: 'Ne (exit)',
        }

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
                self.select_public_key_gen()
            elif option == 2:
                self.decryptMode = True
            elif option == 3:
                print('Program ukončen.')
                exit()
            else:
                print('Špatný výběr. Vložte číslo mezi 1 až 3.')

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
            print(self.parsedMessage[0:100].decode(), "\n\t ... (", len(self.parsedMessage.decode()) - 100,
                  ") dalších znaků.")
        else:
            print(self.parsedMessage.decode())
        print("\n--------- KONEC ZPRÁVY ---------\n")

    def parse_input_text_from_user(self):
        temp = str(self.get_input_text_from_user())
        self.parsedMessage = str.encode(temp)

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
            print(self.parsedMessage[0:100].decode(), "\n\t ... (", len(self.parsedMessage.decode()) - 100,
                  ") dalších znaků.")
        else:
            print("\nVložená zpráva k zašifrování: \n")
            print("--------- ZAČÁTEK ZPRÁVY ---------\n")
            print(self.parsedMessage.decode())

        print("\n--------- KONEC ZPRÁVY ---------\n")

    def parse_input_file_for_encryption(self):
        while self.filename is None or self.filename == '':
            print("Nevybraný soubor. Vyberte soubor znovu.")
            self.open_file_text()

        if os.path.isfile(self.filename):
            temp = Path(self.filename).read_text()
        else:
            return

        self.parsedMessage = str.encode(temp)

    def generate_partial_key(self):
        partial_key = self.public_key1 ** self.private_key
        partial_key = partial_key % self.public_key2
        return partial_key

    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r ** self.private_key
        full_key = full_key % self.public_key2
        self.full_key = full_key
        return full_key

    def encrypt_message(self):
        encrypted_message = ""
        key = self.full_key
        for c in self.parsedMessage:
            encrypted_message += chr(ord(c) + key)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c) - key)
        return decrypted_message

    def select_public_key_gen(self):
        while self.public_key1 is None or self.public_key2 is None:
            self.print_menu_public_key_selection()
            option = ''
            try:
                option = int(input('Zvolte způsob zadání 1. a 2. veřejného klíče: '))
            except:
                print('Špatný výběr. Zkuste to znovu.')
            if option == 1:
                self.public_key_random()
            elif option == 2:
                self.public_key_1_by_user()
                self.public_key_2_by_user()
            elif option == 3:
                print('Program ukončen.')
                exit()
            else:
                print('Špatný výběr. Vložte číslo mezi 1 až 3.')

    def print_menu_public_key_selection(self):
        for key in self.menu_public_key_selection.keys():
            print(key, '--', self.menu_public_key_selection[key])

    def public_key_random(self):
            primes = [2]
            for a in range(3, 10000):
                sqrta = sqrt(a+1)
                for i in primes:
                    if a % i == 0:
                        break
                    if i >= sqrta:
                        primes.append(a)
                        break

            self.public_key1 = r.choice(primes)
            self.public_key2 = r.choice(primes)

    def public_key_1_by_user(self):
        while self.public_key1 is None:
            temp = input("Vložte veřejný klíč 1")
            if not str.isnumeric(temp):
                print("Vložte pouze číslice.")
            elif not self.is_prime(int(temp)):
                print("Vložte prvočíslo.")
            else:
                self.public_key1 = temp

    def public_key_2_by_user(self):
        while self.public_key2 is None:
            temp = input("Vložte P: ")
            if not str.isnumeric(temp):
                print("Vložte pouze číslice.")
            elif not self.is_prime(int(temp)):
                print("Vložte prvočíslo.")
            else:
                self.public_key2 = temp

    def secret_key_by_user(self):
        temp = ""
        while len(temp) != 16 or not str.isascii(temp):
            temp = input("Vložte skrytý klíč 1")
            if len(temp) != 16:
                print("Vložený počet znaků: ", len(temp))
                print("Vložili jste nevhodný počet znaků. Inicializační vektor musí mít délku 16 znaků")
            elif not str.isascii(temp):
                print("Vložili jste inicializační vektor s diakritikou. Použijte znaky ASCII.")
            else:
                self.iv = temp

    def primRoots(self, modulo):
        required_set = {num for num in range(1, modulo) if bltin_gcd(num, modulo)}
        return r.choice([g for g in range(1, modulo) if required_set == {pow(g, powers, modulo)
                                                                for powers in range(1, modulo)}])

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

if __name__ == '__main__':
    ch = ChoiceHandler()
    print(ch.primRoots(23))
    ch.start()