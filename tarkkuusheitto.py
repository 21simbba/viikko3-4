import tkinter as tk
import random
import pygame

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Kernest ja maalitaulu")

        # Asetetaan ikkunan koko
        self.root.geometry("1440x1080")

        # Luodaan Canvas (piirustusalusta) ikkunaan
        self.canvas = tk.Canvas(self.root, width=1200, height=600)
        self.canvas.pack()

        # Lataa Kernestin ja Ernestin kuvat
        self.kernest_img = tk.PhotoImage(file="kerne.png")
        self.ernesti_img = tk.PhotoImage(file="erne.png")

        # Lataa maalitaulun kuva
        self.target_img = tk.PhotoImage(file="maalitaulu.png")
        
        # Lataa tomaatin ja splatin kuvat
        self.tomato_img = tk.PhotoImage(file="tomaatti.png")
        self.splat_img = tk.PhotoImage(file="splat.png")

        # Piirretään maalitaulu (keskelle) x = 600, y = 300
        self.target_x = 600
        self.target_y = 300
        self.canvas.create_image(self.target_x, self.target_y, image=self.target_img)

        # Maalitaulun y-akselin osuma-alue laajennettuna (+-50 pikseliä)
        self.target_hitbox_min_y = self.target_y - 50
        self.target_hitbox_max_y = self.target_y + 50

        # Piirretään Kernestin kuva vasempaan reunaan satunnaiseen sijaintiin
        self.kernest_x = random.randint(50, 150)
        self.kernest_y = random.randint(50, 550)  # Laajennettu y-akselin alue
        self.kernest = self.canvas.create_image(self.kernest_x, self.kernest_y, image=self.kernest_img, anchor=tk.NW)

        # Piirretään Ernestin kuva oikeaan reunaan satunnaiseen sijaintiin
        self.ernesti_x = random.randint(900, 1100)
        self.ernesti_y = random.randint(50, 550)  # Laajennettu y-akselin alue
        self.ernesti = self.canvas.create_image(self.ernesti_x, self.ernesti_y, image=self.ernesti_img, anchor=tk.NW)

        # Alustetaan pygame ääniä varten
        pygame.mixer.init()
        self.throw_sound = pygame.mixer.Sound("mixkit-quick-rope-throw-730.mp3")  # Käytä pygame.mixer.Sound lyhyille äänille
        self.hit_sound = pygame.mixer.Sound("mixkit-soft-quick-punch-2151.wav")  # Ääni osumalle

        # Sanakirja osumatietojen tallentamiseksi
        self.hit_data = {"Kernest": 0, "Ernesti": 0}

        # Luodaan osumalaskuri-alue maalitaulun yläpuolelle
        self.kernest_hits_label = tk.Label(self.root, text="Kernestin osumat: 0", font=("Arial", 16))
        self.kernest_hits_label.pack()

        self.ernesti_hits_label = tk.Label(self.root, text="Ernestin osumat: 0", font=("Arial", 16))
        self.ernesti_hits_label.pack()

        # Luodaan painikkeet Ernestin ja Kernestin tomaattiheitolle
        self.button_ernest = tk.Button(self.root, text="Heitä tomaatti Ernestiltä", command=self.throw_tomato_from_ernest)
        self.button_ernest.pack()

        self.button_kernest = tk.Button(self.root, text="Heitä tomaatti Kernestiltä", command=self.throw_tomato_from_kernest)
        self.button_kernest.pack()

        # Luodaan painikkeet Ernestin ja Kernestin liikuttamiselle
        self.move_ernest_button = tk.Button(self.root, text="Siirrä Ernesti", command=self.move_ernesti)
        self.move_ernest_button.pack()

        self.move_kernest_button = tk.Button(self.root, text="Siirrä Kernest", command=self.move_kernesti)
        self.move_kernest_button.pack()

        # Luodaan reset-painike
        self.reset_button = tk.Button(self.root, text="Nollaa tulokset", command=self.reset_scores)
        self.reset_button.pack()

    def animate_tomato(self, tomato, start_x, start_y, end_x, step=0, thrower=""):
        # Lasketaan uudet koordinaatit (vain x-akselin suuntaisesti, y-koordinaatti pysyy samana)
        new_x = start_x + step * (end_x - start_x) / 100
        
        # Päivitetään tomaatin sijainti
        self.canvas.coords(tomato, new_x, start_y)

        # Jatketaan animaatiota, jos step on alle 100
        if step < 100:
            self.root.after(10, self.animate_tomato, tomato, start_x, start_y, end_x, step + 1, thrower)
        else:
            # Tarkistetaan osuuko tomaatti maalitauluun osuma-alueen sisällä
            if self.target_hitbox_min_y <= start_y <= self.target_hitbox_max_y:
                # Poistetaan tomaatti ja lisätään splat-kuva
                self.canvas.delete(tomato)
                self.canvas.create_image(self.target_x, self.target_y, image=self.splat_img, anchor=tk.CENTER)

                # Toista osumaääni
                self.hit_sound.play()

                # Tallenna osuma
                self.hit_data[thrower] += 1
                print(f"{thrower} osui! Osumia yhteensä: {self.hit_data[thrower]}")

                # Päivitä osumalaskuri näytöllä
                self.update_hit_labels()
            else:
                # Jos tomaatti menee ohi, poistetaan vain tomaatti
                self.canvas.delete(tomato)
                print(f"{thrower} ei osunut.")

    def throw_tomato(self, start_x, start_y, thrower):
        # Tomaatin lentorata x-akselin suuntaisesti
        tomato = self.canvas.create_image(start_x, start_y, image=self.tomato_img)

        # Toista tomaatin heittoääni
        self.throw_sound.play()

        # Aloitetaan animaatio x-akselin suuntaisesti
        self.animate_tomato(tomato, start_x, start_y, self.target_x, thrower=thrower)

    def throw_tomato_from_ernest(self):
        # Käynnistä tomaattiheitto Ernestin kohdalta
        self.throw_tomato(self.ernesti_x + 50, self.ernesti_y + 50, "Ernesti")

    def throw_tomato_from_kernest(self):
        # Käynnistä tomaattiheitto Kernestin kohdalta
        self.throw_tomato(self.kernest_x + 50, self.kernest_y + 50, "Kernest")

    def move_ernesti(self):
        # Siirrä Ernesti satunnaiseen y-koordinaattiin
        new_y = random.randint(50, 550)
        self.canvas.coords(self.ernesti, self.ernesti_x, new_y)
        self.ernesti_y = new_y

    def move_kernesti(self):
        # Siirrä Kernest satunnaiseen y-koordinaattiin
        new_y = random.randint(50, 550)
        self.canvas.coords(self.kernest, self.kernest_x, new_y)
        self.kernest_y = new_y

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

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
