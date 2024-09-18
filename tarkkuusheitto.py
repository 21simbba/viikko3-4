import tkinter as tk
import random
import pygame

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Kernest ja Maalitaulu")

        # Asetetaan ikkunan koko
        self.root.geometry("1440x1080")

        # Alustetaan pygame ääniä varten
        pygame.mixer.init()
        self.throw_sound = pygame.mixer.Sound("mixkit-quick-rope-throw-730.mp3")  # Tomaatin heittoääni
        self.hit_sound = pygame.mixer.Sound("mixkit-soft-quick-punch-2151.wav")  # Osumaääni
        self.win_sound = pygame.mixer.Sound("mixkit-video-game-win-2016.wav")  # Pelin loppuääni

        # Luodaan Canvas ikkunaan
        self.canvas = tk.Canvas(self.root, width=1200, height=600)
        self.canvas.pack()

        # Ladataan kuvat
        self.kernest_img = tk.PhotoImage(file="kerne.png")
        self.ernesti_img = tk.PhotoImage(file="erne.png")
        self.target_img = tk.PhotoImage(file="maalitaulu.png")
        self.tomato_img = tk.PhotoImage(file="tomaatti.png")

        # Piirretään maalitaulu keskelle (vakiosijainti)
        self.target_x = 600
        self.target_y = 300
        self.canvas.create_image(self.target_x, self.target_y, image=self.target_img)

        # Piirretään Kernest satunnaiseen sijaintiin vasemmalle
        self.kernest_x = random.randint(50, 150)
        self.kernest_y = random.randint(50, 550)
        self.kernest = self.canvas.create_image(self.kernest_x, self.kernest_y, image=self.kernest_img, anchor=tk.NW)

        # Alustetaan osumalaskuri
        self.hit_data = {"Kernest": 0, "Ernesti": 0}

        # Piirretään painike Ernestin siirtämiselle oikealle
        self.move_ernest_button = tk.Button(self.root, text="Sijoita Ernesti oikeaan reunaan", command=self.move_ernesti)
        self.move_ernest_button.pack()

        # Heittopainikkeet Ernestille ja Kernestille
        self.throw_ernest_button = tk.Button(self.root, text="Heitä tomaatti Ernestiltä", command=self.throw_tomato_from_ernest)
        self.throw_ernest_button.pack()

        self.throw_kernest_button = tk.Button(self.root, text="Heitä tomaatti Kernestiltä", command=self.throw_tomato_from_kernest)
        self.throw_kernest_button.pack()

        # Näyttöruutu osumien määrälle
        self.kernest_hits_label = tk.Label(self.root, text="Kernestin osumat: 0", font=("Arial", 16))
        self.kernest_hits_label.pack()

        self.ernesti_hits_label = tk.Label(self.root, text="Ernestin osumat: 0", font=("Arial", 16))
        self.ernesti_hits_label.pack()

        # Reset-painike tulosten nollaamiseen
        self.reset_button = tk.Button(self.root, text="Nollaa tulokset", command=self.reset_scores)
        self.reset_button.pack()

    def move_ernesti(self):
        # Siirrä Ernesti oikeaan reunaan satunnaiseen paikkaan
        self.ernesti_x = random.randint(900, 1100)
        self.ernesti_y = random.randint(50, 550)
        if hasattr(self, 'ernesti'):
            self.canvas.coords(self.ernesti, self.ernesti_x, self.ernesti_y)
        else:
            self.ernesti = self.canvas.create_image(self.ernesti_x, self.ernesti_y, image=self.ernesti_img, anchor=tk.NW)

    def animate_tomato(self, tomato, start_x, start_y, end_x, step=0, thrower=""):
        # Lasketaan uudet koordinaatit (x-akselilla ja lisätään pieni kaari)
        new_x = start_x + step * (end_x - start_x) / 100
        new_y = start_y - 10 * step * (1 - step / 100)  # Y-akselin kaari

        # Päivitetään tomaatin sijainti
        self.canvas.coords(tomato, new_x, new_y)

        # Jatketaan animaatiota kunnes step = 100
        if step < 100:
            self.root.after(10, self.animate_tomato, tomato, start_x, start_y, end_x, step + 1, thrower)
        else:
            self.canvas.delete(tomato)
            self.check_hit(thrower)

    def throw_tomato(self, start_x, start_y, thrower):
        # Luo tomaatti alkukoordinaatteihin
        tomato = self.canvas.create_image(start_x, start_y, image=self.tomato_img)

        # Toista tomaatin heittoääni
        self.throw_sound.play()

        # Aloitetaan animaatio, tomaatti lentää vaakasuorassa kohti maalitaulua
        self.animate_tomato(tomato, start_x, start_y, self.target_x, thrower=thrower)

    def throw_tomato_from_ernest(self):
        # Käynnistä tomaattiheitto Ernestiltä
        self.throw_tomato(self.ernesti_x + 50, self.ernesti_y + 50, "Ernesti")

    def throw_tomato_from_kernest(self):
        # Käynnistä tomaattiheitto Kernestiltä
        self.throw_tomato(self.kernest_x + 50, self.kernest_y + 50, "Kernest")

    def check_hit(self, thrower):
        # Käytetään satunnaislukua osuman tarkistamiseen (esim. 30% mahdollisuus osua)
        hit_chance = random.random()
        if hit_chance <= 0.3:
            self.hit_data[thrower] += 1
            print(f"{thrower} osui! Osumia yhteensä: {self.hit_data[thrower]}")
            self.hit_sound.play()
            self.update_hit_labels()
            self.check_winner()
        else:
            print(f"{thrower} ei osunut.")

    def update_hit_labels(self):
        # Päivitä näytössä olevat osumien määrät
        self.kernest_hits_label.config(text=f"Kernestin osumat: {self.hit_data['Kernest']}")
        self.ernesti_hits_label.config(text=f"Ernestin osumat: {self.hit_data['Ernesti']}")

    def reset_scores(self):
        # Nollaa osumatiedot
        self.hit_data = {"Kernest": 0, "Ernesti": 0}

        # Päivitä laskurin näyttöruutu
        self.update_hit_labels()

        print("Tulokset nollattu.")

    def check_winner(self):
        # Tarkista onko ero osumissa kaksi, jolloin toinen saa heittää toista
        if abs(self.hit_data["Kernest"] - self.hit_data["Ernesti"]) >= 2:
            if self.hit_data["Kernest"] > self.hit_data["Ernesti"]:
                print("Kernest saa heittää Ernestiä!")
                self.throw_tomato(self.kernest_x + 50, self.kernest_y + 50, "Kernest")
            else:
                print("Ernesti saa heittää Kernestiä!")
                self.throw_tomato(self.ernesti_x + 50, self.ernesti_y + 50, "Ernesti")

            # Jos osuma syntyy, peli päättyy
            if random.random() <= 0.3:  # Osuman todennäköisyys vastustajaan on 30%
                self.win_sound.play()
                print("Peli päättyi, voittaja on se, joka osui vastustajaan!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
