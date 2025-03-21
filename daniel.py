import tkinter as tk

# Fensterabmessungen
WIDTH, HEIGHT = 300, 100
dx, dy = 5, 5  # Geschwindigkeiten für x und y

def move_window():
    global dx, dy
    
    x = root.winfo_x()
    y = root.winfo_y()
    
    # Bildschirm-Auflösung
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Kollision links/rechts
    if x + dx < 0 or x + WIDTH + dx > screen_w:
        dx = -dx

    # Kollision oben/unten
    if y + dy < 0 or y + HEIGHT + dy > screen_h:
        dy = -dy

    # Neue Position
    x += dx
    y += dy
    
    # Fenster verschieben
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    # Nach 20 ms erneut aufrufen
    root.after(20, move_window)

# Hauptfenster einrichten
root = tk.Tk()
root.title("Fenster immer im Vordergrund")

# --> Wichtig: '-topmost' sorgt dafür, dass das Fenster oben bleibt
root.attributes("-topmost", True)

# Initiale Position + Größe
root.geometry(f"{WIDTH}x{HEIGHT}+100+100")

# Label mit Text
label = tk.Label(root, text="Daniel ", font=("Arial", 50))
label.pack(expand=True)

# Startet die Bewegung
root.after(20, move_window)

# Tkinter-Hauptschleife
root.mainloop()
