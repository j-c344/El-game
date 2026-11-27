import tkinter as tk
import random
import json
import os
import time

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

class SlotSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Sélection de partie")
        self.root.geometry("300x350")
        self.root.configure(bg="#121212")
        self.selected_slot = None

        title_label = tk.Label(root, text="CHOISISSEZ UNE PARTIE", font=("Helvetica", 14, "bold"), fg="white", bg="#121212")
        title_label.pack(pady=20)

        for slot_num in range(1, 4):
            save_filename = f"save_slot_{slot_num}.json"
            info_text = f"Partie {slot_num}"
            if os.path.exists(save_filename):
                try:
                    with open(save_filename, "r") as f:
                        data = json.load(f)
                        rolls = data.get("total_rolls", 0)
                        coins = data.get("coins", 0)
                        info_text = f"Partie {slot_num}\n(Rolls: {rolls} | Coins: {coins})"
                except Exception:
                    pass

            btn = tk.Button(
                root, text=info_text, font=("Helvetica", 10, "bold"),
                bg="#1e1e1e", fg="white", activebackground="#2896f0", activeforeground="white",
                bd=1, relief="solid", cursor="hand2",
                command=lambda s=slot_num: self.launch_game(s)
            )
            btn.pack(fill="x", padx=30, pady=10, ipady=8)

    def launch_game(self, slot_num):
        self.root.destroy()
        main_root = tk.Tk()
        app = RNGGame(main_root, slot_num)
        main_root.mainloop()

class RNGGame:
    def __init__(self, root, slot_num=1):
        self.root = root
        self.current_slot = slot_num
        self.root.title(f"Game - Partie {self.current_slot}")
        self.root.geometry("400x720")
        self.root.configure(bg="#121212")

        self.base_luck = 1.0
        self.current_luck = 1.0
        self.coins = 0
        self.total_rolls = 0
        self.play_time_seconds = 0
        self.is_rolling = False
        self.auto_roll_active = False
        self.roll_speed_multiplier = 1.0
        self.cutscenes_enabled = True
        self.flash_enabled = True

        self.temp_luck_boost = 0.0
        self.temp_speed_boost = 0.0
        self.temp_boost_end_time = 0

        self.roll_history = []
        self.scroll_velocity = 0
        self.scroll_timer = None
        self.current_canvas = None

        self.quests = []
        self.generate_new_quests()
        self.start_quest_timer()
        self.start_play_time_tracker()

        self.auras = {
            "Olive": {"chance": 3, "unlocked": False},
            "Expirimental": {"chance": 5, "unlocked": False},
            "Mint": {"chance": 8, "unlocked": False},
            "Laser": {"chance": 10, "unlocked": False},
            "No": {"chance": 15, "unlocked": False},
            "Streak": {"chance": 21, "unlocked": False},
            "Nani": {"chance": 22, "unlocked": False},
            "Upgraded Olive": {"chance": 33, "unlocked": False},
            "Ko": {"chance": 44, "unlocked": False},
            "Hunt Down": {"chance": 55, "unlocked": False},
            "Crash": {"chance": 59, "unlocked": False},
            "Troll": {"chance": 69, "unlocked": False},
            "Fortune": {"chance": 78, "unlocked": False},
            "Mega upgrader olive": {"chance": 83, "unlocked": False},
            "Autobotique": {"chance": 100, "unlocked": False},
            "Everything": {"chance": 115, "unlocked": False},
            "Robotic": {"chance": 150, "unlocked": False},
            "Mind Attack": {"chance": 222, "unlocked": False},
            "Killstreak": {"chance": 350, "unlocked": False},
            "Tungsten men": {"chance": 450, "unlocked": False},
            "Negatif": {"chance": 480, "unlocked": False},
            "Mandala": {"chance": 500, "unlocked": False},
            "Titan": {"chance": 600, "unlocked": False},
            "Banshee": {"chance": 666, "unlocked": False},
            "Demon": {"chance": 666, "unlocked": False},
            "Elemental force": {"chance": 750, "unlocked": False},
            "Godly": {"chance": 777, "unlocked": False},
            "Aurora": {"chance": 835, "unlocked": False},
            "Mystery": {"chance": 1000, "unlocked": False},
            "Brutality": {"chance": 1500, "unlocked": False},
            "Black": {"chance": 1750, "unlocked": False},
            "D E A T H": {"chance": 1666, "unlocked": False},
            "Double Ity": {"chance": 2500, "unlocked": False},
            "Nuclear assaut": {"chance": 2666, "unlocked": False},
            "Fatality": {"chance": 3000, "unlocked": False},
            "Darkness": {"chance": 4444, "unlocked": False},
            "RUPTURE": {"chance": 5000, "unlocked": False},
            "BUSTED": {"chance": 6666, "unlocked": False},
            "Night": {"chance": 8888, "unlocked": False},
            "BIG BANG": {"chance": 10000, "unlocked": False},
            "Azote": {"chance": 20000, "unlocked": False},
            "Gemini": {"chance": 30000, "unlocked": False},
            "Blood": {"chance": 25000, "unlocked": False},
            "End destroyer": {"chance": 50000, "unlocked": False},
            "Soul": {"chance": 100000, "unlocked": False},
            "Hacker": {"chance": 101100, "unlocked": False},
            "Blood moon": {"chance": 300000, "unlocked": False},
            "Tear of death": {"chance": 1666666, "unlocked": False},
            "Daylight": {"chance": 3000000, "unlocked": False},
            "Zodiac": {"chance": 7500000, "unlocked": False},
            "Glitch": {"chance": 1000000, "unlocked": False},
            "Olive god": {"chance": 10000000, "unlocked": False},
            "Corrupted": {"chance": 666666, "unlocked": False},
            "Horizon": {"chance": 674, "unlocked": False},
            "Nebula": {"chance": 1235, "unlocked": False},
            "Abyss": {"chance": 350, "unlocked": False},
            "Eclipse": {"chance": 2000, "unlocked": False},
            "Cataclysm": {"chance": 275666, "unlocked": False},
            "Thunderbolt": {"chance": 50, "unlocked": False},
            "Tsunami": {"chance": 300, "unlocked": False},
            "Hurricane": {"chance": 240, "unlocked": False},
            "Plasma": {"chance": 99999, "unlocked": False},
            "Dirt": {"chance": 17, "unlocked": False},
            "Cut": {"chance": 45, "unlocked": False},
            "Ultrapunch": {"chance": 25, "unlocked": False},
            "Drunk": {"chance": 33, "unlocked": False},
            "Poor": {"chance": 99, "unlocked": False},
            "Flying": {"chance": 140, "unlocked": False},
            "Leviating": {"chance": 280, "unlocked": False},
            "Speedo": {"chance": 300, "unlocked": False},
            "Rage extreme": {"chance": 400, "unlocked": False},
            "Ultra olive": {"chance": 499, "unlocked": False},
            "Prime olive": {"chance": 900, "unlocked": False},
            "Rich": {"chance": 999, "unlocked": False},
            "Asteroid": {"chance": 759, "unlocked": False},
            "Entity": {"chance": 9999, "unlocked": False}
        }

        self.shop_items = [
            {"id": 1, "type": "luck", "boost": 0.5, "price": 10, "owned": False, "equipped": False},
            {"id": 2, "type": "luck", "boost": 1.0, "price": 25, "owned": False, "equipped": False},
            {"id": 3, "type": "luck", "boost": 2.0, "price": 60, "owned": False, "equipped": False},
            {"id": 4, "type": "luck", "boost": 5.0, "price": 150, "owned": False, "equipped": False},
            {"id": 5, "type": "luck", "boost": 10.0, "price": 400, "owned": False, "equipped": False},
            {"id": 6, "type": "luck", "boost": 20.0, "price": 1000, "owned": False, "equipped": False},
            {"id": 7, "type": "luck", "boost": 50.0, "price": 2500, "owned": False, "equipped": False},
            {"id": 8, "type": "luck", "boost": 100.0, "price": 5000, "owned": False, "equipped": False},
            {"id": 9, "type": "luck", "boost": 250.0, "price": 12000, "owned": False, "equipped": False},
            {"id": 10, "type": "luck", "boost": 500.0, "price": 25000, "owned": False, "equipped": False},
            {"id": 16, "type": "luck", "boost": 1000.0, "price": 60000, "owned": False, "equipped": False},
            {"id": 17, "type": "luck", "boost": 2500.0, "price": 150000, "owned": False, "equipped": False},
            {"id": 18, "type": "luck", "boost": 5000.0, "price": 400000, "owned": False, "equipped": False},
            {"id": 19, "type": "luck", "boost": 10000.0, "price": 1000000, "owned": False, "equipped": False},
            {"id": 11, "type": "speed", "speed_mult": 1.5, "price": 500, "owned": False, "equipped": False, "name": "Vitesse I (x1.5)"},
            {"id": 12, "type": "speed", "speed_mult": 2.0, "price": 2000, "owned": False, "equipped": False, "name": "Vitesse II (x2.0)"},
            {"id": 13, "type": "speed", "speed_mult": 3.5, "price": 6000, "owned": False, "equipped": False, "name": "Vitesse III (x3.5)"},
            {"id": 14, "type": "speed", "speed_mult": 6.0, "price": 12000, "owned": False, "equipped": False, "name": "Vitesse IV (x6.0)"},
            {"id": 15, "type": "speed", "speed_mult": 10.0, "price": 25000, "owned": False, "equipped": False, "name": "Vitesse Divine (x10.0)"},
            {"id": 20, "type": "speed", "speed_mult": 15.0, "price": 75000, "owned": False, "equipped": False, "name": "Vitesse Suprême (x15.0)"},
            {"id": 21, "type": "speed", "speed_mult": 25.0, "price": 200000, "owned": False, "equipped": False, "name": "Vitesse Éclair (x25.0)"},
            {"id": 22, "type": "speed", "speed_mult": 50.0, "price": 600000, "owned": False, "equipped": False, "name": "Vitesse Infinie (x50.0)"}
        ]

        self.pets = [
            {"id": 101, "name": "Petit Robot", "bonus_type": "coins", "bonus_val": 5, "price": 300, "owned": False, "equipped": False, "desc": "+5 Coins par roll"},
            {"id": 102, "name": "Chaton Mystique", "bonus_type": "luck", "bonus_val": 0.5, "price": 1000, "owned": False, "equipped": False, "desc": "+0.5 Luck passive"},
            {"id": 103, "name": "Dragonnet", "bonus_type": "speed", "bonus_val": 0.5, "price": 3000, "owned": False, "equipped": False, "desc": "+0.5 Multiplicateur de vitesse"},
            {"id": 104, "name": "Lutin Fortune", "bonus_type": "coins", "bonus_val": 25, "price": 7500, "owned": False, "equipped": False, "desc": "+25 Coins par roll"},
            {"id": 105, "name": "Renard Astral", "bonus_type": "luck", "bonus_val": 2.0, "price": 15000, "owned": False, "equipped": False, "desc": "+2.0 Luck passive"},
            {"id": 106, "name": "Phénix Céleste", "bonus_type": "speed", "bonus_val": 1.5, "price": 25000, "owned": False, "equipped": False, "desc": "+1.5 Multiplicateur de vitesse"},
            {"id": 107, "name": "Golem Doré", "bonus_type": "coins", "bonus_val": 100, "price": 50000, "owned": False, "equipped": False, "desc": "+100 Coins par roll"},
            {"id": 108, "name": "Esprit Divin", "bonus_type": "luck", "bonus_val": 10.0, "price": 100000, "owned": False, "equipped": False, "desc": "+10.0 Luck passive"},
            {"id": 109, "name": "Chrono-Cyber", "bonus_type": "speed", "bonus_val": 3.0, "price": 180000, "owned": False, "equipped": False, "desc": "+3.0 Multiplicateur de vitesse"},
            {"id": 110, "name": "Dragon Noir Cosmique", "bonus_type": "luck", "bonus_val": 50.0, "price": 500000, "owned": False, "equipped": False, "desc": "+50.0 Luck passive"}
        ]

        self.load_game()

        self.top_frame = tk.Frame(root, bg="#121212")
        self.top_frame.pack(fill="x", padx=5, pady=5)
        self.stats_container = tk.Frame(self.top_frame, bg="#121212")
        self.stats_container.pack(anchor="center", pady=2)

        self.luck_box = tk.Frame(self.stats_container, bg="#2ecc71", bd=1, relief="solid")
        self.luck_box.pack(side="left", padx=2)
        self.luck_label = tk.Label(self.luck_box, text=f"Luck: x{self.current_luck:.1f}", font=("Helvetica", 8, "bold"), fg="#121212", bg="#2ecc71", padx=4, pady=2)
        self.luck_label.pack()

        self.speed_box = tk.Frame(self.stats_container, bg="#3498db", bd=1, relief="solid")
        self.speed_box.pack(side="left", padx=2)
        self.speed_label = tk.Label(self.speed_box, text=f"Speed: x{self.roll_speed_multiplier:.1f}", font=("Helvetica", 8, "bold"), fg="#ffffff", bg="#3498db", padx=4, pady=2)
        self.speed_label.pack()

        self.coins_box = tk.Frame(self.stats_container, bg="#f1c40f", bd=1, relief="solid")
        self.coins_box.pack(side="left", padx=2)
        self.coins_label = tk.Label(self.coins_box, text=f"Coins: {self.coins}", font=("Helvetica", 8, "bold"), fg="#121212", bg="#f1c40f", padx=4, pady=2)
        self.coins_label.pack()

        self.extra_stats_container = tk.Frame(self.top_frame, bg="#121212")
        self.extra_stats_container.pack(anchor="center", pady=2)
        self.rolls_label = tk.Label(self.extra_stats_container, text=f"Rolls: {self.total_rolls}", font=("Helvetica", 8, "bold"), fg="#aaaaaa", bg="#121212", padx=4)
        self.rolls_label.pack(side="left", padx=5)
        self.time_label = tk.Label(self.extra_stats_container, text="Temps: 00:00", font=("Helvetica", 8, "bold"), fg="#aaaaaa", bg="#121212", padx=4)
        self.time_label.pack(side="left", padx=5)

        self.center_frame = tk.Frame(root, bg="#121212")
        self.center_frame.pack(expand=True, fill="both")
        self.roulette_frame = tk.Frame(self.center_frame, bg="#1e1e1e", bd=2, relief="solid", highlightbackground="#2896f0", highlightthickness=2)
        self.roulette_frame.place(relx=0.5, rely=0.42, anchor="center", relwidth=0.96, height=300)
        self.canvas = tk.Canvas(self.roulette_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.update_canvas_center)
        self.center_x = 190
        self.center_y = 150

        self.bottom_frame = tk.Frame(root, bg="#121212")
        self.bottom_frame.pack(side="bottom", pady=10)
        self.roll_button = tk.Button(self.bottom_frame, text="ROLL", font=("Helvetica", 16, "bold"), bg="#2896f0", fg="white", width=16, height=2, bd=0, relief="flat", cursor="hand2", command=self.start_roll, activebackground="#1f6eb3", activeforeground="white")
        self.roll_button.pack(pady=4)
        self.auto_button = tk.Button(self.bottom_frame, text="AUTO ROLL : OFF", font=("Helvetica", 10, "bold"), bg="#262626", fg="#aaaaaa", width=22, pady=3, bd=0, relief="flat", cursor="hand2", command=self.toggle_auto_roll)
        self.auto_button.pack(pady=3)
        self.menu_frame = tk.Frame(self.bottom_frame, bg="#121212")
        self.menu_frame.pack(pady=6)

        buttons = [
            ("Shop", "#1e2922", "#2ecc71", self.open_shop),
            ("Index", "#292218", "#f1c40f", self.open_index),
            ("Quêtes", "#221e29", "#9b59b6", self.open_quests),
            ("Historique", "#1a252f", "#3498db", self.open_history),
            ("Pets", "#291a1a", "#e74c3c", self.open_pets),
            ("Options", "#222222", "#7f8c8d", self.open_settings)
        ]
        for label, bg, fg, command in buttons:
            frame = tk.Frame(self.menu_frame, bg=bg, highlightbackground=fg, highlightthickness=2, cursor="hand2")
            frame.pack(side="left", padx=3)
            lbl = tk.Label(frame, text=label, font=("Helvetica", 8, "bold"), fg=fg, bg=bg, padx=4, pady=4)
            lbl.pack(side="left")
            frame.bind("<Button-1>", lambda e, c=command: c())
            lbl.bind("<Button-1>", lambda e, c=command: c())

        self.overlay_frame = None

    def generate_new_quests(self):
        quest_templates = [
            {"type": "rolls", "target": random.randint(15, 30), "reward_type": "coins", "reward_val": 50, "desc": "Effectuer {target} rolls"},
            {"type": "coins", "target": random.randint(100, 300), "reward_type": "coins", "reward_val": 80, "desc": "Gagner {target} coins au total"},
            {"type": "rolls", "target": random.randint(10, 20), "reward_type": "luck", "reward_val": 5.0, "duration": 60, "desc": "Effectuer {target} rolls -> +5 Luck (60s)"},
            {"type": "rolls", "target": random.randint(25, 45), "reward_type": "speed", "reward_val": 2.0, "duration": 60, "desc": "Effectuer {target} rolls -> +2 Speed (60s)"},
        ]
        self.quests = []
        for q in random.sample(quest_templates, min(4, len(quest_templates))):
            self.quests.append({"desc": q["desc"].format(target=q["target"]), "type": q["type"], "target": q["target"], "progress": 0, "reward_type": q["reward_type"], "reward_val": q["reward_val"], "duration": q.get("duration", 60), "completed": False, "claimed": False})

    def start_quest_timer(self):
        def countdown():
            if self.temp_boost_end_time > 0 and time.time() >= self.temp_boost_end_time:
                self.temp_luck_boost = 0.0
                self.temp_speed_boost = 0.0
                self.temp_boost_end_time = 0
                self.recalculate_stats()
            self.root.after(1000, countdown)
        self.root.after(1000, countdown)

    def start_play_time_tracker(self):
        def track_time():
            self.play_time_seconds += 1
            mins, secs = divmod(self.play_time_seconds, 60)
            if hasattr(self, "time_label"):
                self.time_label.config(text=f"Temps: {mins:02d}:{secs:02d}")
            self.root.after(1000, track_time)
        self.root.after(1000, track_time)

    def update_quest_progress(self, q_type, amount=1):
        for q in self.quests:
            if not q["completed"] and q["type"] == q_type:
                q["progress"] += amount
                if q["progress"] >= q["target"]:
                    q["progress"] = q["target"]
                    q["completed"] = True
                    self.save_game()

    def claim_quest(self, q):
        if q["completed"] and not q["claimed"]:
            q["claimed"] = True
            if q["reward_type"] == "coins":
                self.coins += int(q["reward_val"])
                self.coins_label.config(text=f"Coins: {self.coins}")
            elif q["reward_type"] == "luck":
                self.temp_luck_boost = float(q["reward_val"])
                self.temp_boost_end_time = time.time() + q["duration"]
                self.recalculate_stats()
            elif q["reward_type"] == "speed":
                self.temp_speed_boost = float(q["reward_val"])
                self.temp_boost_end_time = time.time() + q["duration"]
                self.recalculate_stats()
            self.save_game()
            self.open_quests()

    def toggle_auto_roll(self):
        self.auto_roll_active = not self.auto_roll_active
        if self.auto_roll_active:
            self.auto_button.config(text="AUTO ROLL : ON", bg="#e67e22", fg="#ffffff")
            if not self.is_rolling:
                self.start_roll()
        else:
            self.auto_button.config(text="AUTO ROLL : OFF", bg="#262626", fg="#aaaaaa")

    def create_fullscreen_overlay(self, title):
        self.overlay_frame = tk.Frame(self.root, bg="#141414")
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Label(self.overlay_frame, text=title, font=("Helvetica", 16, "bold"), fg="white", bg="#141414").pack(pady=(12, 5))
        tk.Button(self.overlay_frame, text="X", font=("Helvetica", 18, "bold"), bg="#e74c3c", fg="white", bd=0, relief="flat", cursor="hand2", command=self.close_overlay, activebackground="#c0392b", activeforeground="white").place(relx=0.78, rely=0.01, width=60, height=40)

    def close_overlay(self):
        if self.overlay_frame:
            self.unbind_scroll_events()
            self.overlay_frame.destroy()
            self.overlay_frame = None

    def save_game(self):
        data = {
            "coins": self.coins, "total_rolls": self.total_rolls, "play_time_seconds": self.play_time_seconds,
            "cutscenes_enabled": self.cutscenes_enabled, "flash_enabled": self.flash_enabled,
            "unlocked_auras": [name for name, val in self.auras.items() if val["unlocked"]],
            "shop": [{"id": item["id"], "owned": item["owned"], "equipped": item["equipped"]} for item in self.shop_items],
            "pets": [{"id": pet["id"], "owned": pet["owned"], "equipped": pet["equipped"]} for pet in self.pets]
        }
        try:
            with open(f"save_slot_{self.current_slot}.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Erreur de sauvegarde: {e}")

    def load_game(self):
        filename = f"save_slot_{self.current_slot}.json"
        if not os.path.exists(filename):
            return
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.coins = data.get("coins", 0)
            self.total_rolls = data.get("total_rolls", 0)
            self.play_time_seconds = data.get("play_time_seconds", 0)
            self.cutscenes_enabled = data.get("cutscenes_enabled", True)
            self.flash_enabled = data.get("flash_enabled", True)
            unlocked = data.get("unlocked_auras", [])
            for name in unlocked:
                if name in self.auras:
                    self.auras[name]["unlocked"] = True
            saved_shop = {item["id"]: item for item in data.get("shop", [])}
            for item in self.shop_items:
                if item["id"] in saved_shop:
                    item["owned"] = saved_shop[item["id"]]["owned"]
                    item["equipped"] = saved_shop[item["id"]]["equipped"]
            saved_pets = {pet["id"]: pet for pet in data.get("pets", [])}
            for pet in self.pets:
                if pet["id"] in saved_pets:
                    pet["owned"] = saved_pets[pet["id"]]["owned"]
                    pet["equipped"] = saved_pets[pet["id"]]["equipped"]
            self.recalculate_stats()
        except Exception as e:
            print(f"Erreur de chargement: {e}")

    def recalculate_stats(self):
        equipped_luck = next((i for i in self.shop_items if i["type"] == "luck" and i["equipped"]), None)
        added_luck = equipped_luck["boost"] if equipped_luck else 0.0
        pet_luck = sum(p["bonus_val"] for p in self.pets if p["owned"] and p["equipped"] and p["bonus_type"] == "luck")
        self.current_luck = self.base_luck + added_luck + pet_luck + self.temp_luck_boost
        if hasattr(self, "luck_label"):
            self.luck_label.config(text=f"Luck: x{self.current_luck:.1f}")
        equipped_speed = next((i for i in self.shop_items if i["type"] == "speed" and i["equipped"]), None)
        base_speed = equipped_speed["speed_mult"] if equipped_speed else 1.0
        pet_speed = sum(p["bonus_val"] for p in self.pets if p["owned"] and p["equipped"] and p["bonus_type"] == "speed")
        self.roll_speed_multiplier = base_speed + pet_speed + self.temp_speed_boost
        if hasattr(self, "speed_label"):
            self.speed_label.config(text=f"Speed: x{self.roll_speed_multiplier:.1f}")

    def update_canvas_center(self, event):
        self.center_x, self.center_y = event.width / 2, event.height / 2
        if not self.is_rolling:
            self.canvas.delete("all")
            self.canvas.create_text(self.center_x, self.center_y, text="Appuie sur ROLL", font=("Helvetica", 16, "bold"), fill="#ffffff", anchor="center")

    def play_tick_sound(self, frequency=600):
        if HAS_WINSOUND:
            try:
                winsound.Beep(frequency, 25)
            except Exception:
                pass

    def play_win_sound(self, rarity):
        if HAS_WINSOUND:
            try:
                if rarity >= 1000:
                    for f in [350, 450, 600, 800, 1000, 1300, 1600]:
                        winsound.Beep(f, 50)
                elif rarity >= 100:
                    for f in [440, 554, 659]:
                        winsound.Beep(f, 60)
                else:
                    winsound.Beep(440, 80)
            except Exception:
                pass

    def set_dark_mode(self, dark=True):
        bg = "#050505" if dark else "#121212"
        roulette_bg = "#0a0a0a" if dark else "#1e1e1e"
        border = "#0e4b85" if dark else "#2896f0"
        for widget in (self.root, self.top_frame, self.stats_container, self.extra_stats_container, self.center_frame, self.bottom_frame, self.menu_frame):
            widget.configure(bg=bg)
        self.roulette_frame.configure(bg=roulette_bg, highlightbackground=border)
        self.canvas.configure(bg=roulette_bg)

    def get_rarity_colors(self, chance):
        if chance < 100: return ("#ffffff", "#777777")
        if chance < 500: return ("#2ecc71", "#145a32")
        if chance < 1000: return ("#f1c40f", "#7d6608")
        if chance < 10000: return ("#e74c3c", "#641e16")
        if chance < 100000: return ("#9b59b6", "#4a235a")
        if chance < 1000000: return ("#d35400", "#5a2400")
        return ("#ffdf00", "#554400")

    def set_buttons_state(self, state):
        self.roll_button.config(state=state)

    def calculate_roll(self):
        for name, data in sorted(self.auras.items(), key=lambda x: x[1]["chance"], reverse=True):
            if random.random() <= (1 / data["chance"]) * self.current_luck:
                return name
        return "Olive"

    def start_roll(self):
        if self.is_rolling: return
        self.is_rolling = True
        self.set_buttons_state(tk.DISABLED)
        self.close_overlay()
        self.set_dark_mode(True)
        self.roll_button.config(text="Rolling...")
        self.animation_step = 0
        self.total_steps = 16
        self.animate_roll()

    def animate_roll(self):
        self.canvas.delete("all")
        random_name = random.choice(list(self.auras.keys()))
        chance = self.auras[random_name]["chance"]
        bright_color, _ = self.get_rarity_colors(chance)
        text = f"{random_name} - 1/{chance}"
        font_size = 14 if len(text) > 22 else 16
        start_y, target_y = 250, 20
        text_id = self.canvas.create_text(self.center_x, start_y, text=text, font=("Helvetica", font_size, "bold"), fill=bright_color, anchor="center")
        steps = 6
        delay = int((80 + self.animation_step * 7) / self.roll_speed_multiplier)

        def move_text(step):
            if not self.canvas.winfo_exists(): return
            y = start_y - (start_y - target_y) * (step / steps)
            self.canvas.coords(text_id, self.center_x, y)
            if step > 4: self.canvas.itemconfig(text_id, fill="#444444")
            if step < steps:
                self.root.after(max(10, int(delay / steps)), lambda: move_text(step + 1))
        move_text(1)
        self.play_tick_sound(350 + self.animation_step * 25)
        self.animation_step += 1
        if self.animation_step < self.total_steps:
            self.root.after(max(15, delay), self.animate_roll)
        else:
            self.root.after(max(20, delay + 30), self.finish_roll)

    def play_cutscene(self, aura_name, chance, callback):
        cut_frame = tk.Frame(self.root, bg="black")
        cut_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        cut_canvas = tk.Canvas(cut_frame, bg="black", highlightthickness=0)
        cut_canvas.pack(fill="both", expand=True)
        cx = self.root.winfo_width() / 2 or 200
        cy = self.root.winfo_height() / 2 or 300

        def end_cutscene():
            if cut_frame.winfo_exists():
                cut_frame.destroy()
            callback()

        def frame_step(i):
            if not cut_frame.winfo_exists(): return
            if i > 45: return end_cutscene()
            cut_canvas.delete("all")
            cut_canvas.configure(bg="#080808")
            color, title = self.get_cutscene_style(aura_name, i)
            cut_canvas.create_text(cx, cy, text=title, font=("Helvetica", 30, "bold"), fill=color, anchor="center")
            self.root.after(60, lambda: frame_step(i + 1))

        frame_step(0)

    def get_cutscene_style(self, name, i):
        styles = {
            "Mystery": ("#c39bd3", "?"), "Brutality": ("#ff3333", "BRUTALITY"),
            "Black": ("#ffffff", "BLACK"), "D E A T H": ("#ff4d4d", "D E A T H"),
            "Double Ity": ("#3498db", "DOUBLE ITY"), "Nuclear assaut": ("#f1c40f", "NUCLEAR"),
            "Fatality": ("#ffffff", "FATALITY"), "Darkness": ("#dddddd", "DARKNESS"),
            "RUPTURE": ("#00ffff", "RUPTURE"), "BUSTED": ("#f1c40f", "BUSTED"),
            "Night": ("#74b9ff", "NIGHT"), "BIG BANG": ("#ffffff", "BIG BANG"),
            "Azote": ("#81ecec", "AZOTE"), "Gemini": ("#ffffff", "GEMINI"),
            "Blood": ("#ff4d4d", "BLOOD"), "End destroyer": ("#e056fd", "END DESTROYER"),
            "Soul": ("#81ecec", "SOUL"), "Hacker": ("#27ae60", "HACKER"),
            "Blood moon": ("#ffffff", "BLOOD MOON"), "Tear of death": ("#c0392b", "TEAR OF DEATH"),
            "Daylight": ("#f1c40f", "DAYLIGHT"), "Zodiac": ("#ffffff", "ZODIAC"),
            "Glitch": ("#ff00ff", "G-L-I-T-C-H"), "Olive god": ("#f1c40f", "OLIVE GOD"),
            "Nebula": ("#ee82ee", "NEBULA"), "Eclipse": ("#ffa500", "ECLIPSE"),
            "Plasma": ("#00ffcc", "PLASMA"), "Entity": ("#ff3333", "ENTITY"),
            "Cataclysm": ("#ff4500", "CATACLYSM"), "Corrupted": ("#00ff00", "CORRUPTED")
        }
        return styles.get(name, ("#ffffff", name.upper()))

    def finish_roll(self):
        won = self.calculate_roll()
        self.auras[won]["unlocked"] = True
        self.total_rolls += 1
        self.rolls_label.config(text=f"Rolls: {self.total_rolls}")
        chance = self.auras[won]["chance"]
        earned = max(0, chance // 10)
        earned += sum(p["bonus_val"] for p in self.pets if p["owned"] and p["equipped"] and p["bonus_type"] == "coins")
        self.coins += earned
        self.coins_label.config(text=f"Coins: {self.coins}")
        self.roll_history.insert(0, {"name": won, "chance": chance, "roll_num": self.total_rolls})
        self.roll_history = self.roll_history[:30]
        self.update_quest_progress("rolls", 1)
        self.update_quest_progress("coins", earned)
        self.save_game()

        def display():
            color, _ = self.get_rarity_colors(chance)
            self.canvas.delete("all")
            text = f"{won} - 1/{chance}"
            self.canvas.create_text(self.center_x, self.center_y, text=text, font=("Helvetica", 15 if len(text) > 22 else 18, "bold"), fill=color, anchor="center")
            self.play_win_sound(chance)
            delay = int(1200 / self.roll_speed_multiplier)
            self.root.after(delay, lambda: self.set_dark_mode(False))
            self.root.after(delay + 200, self.reset_roll_button)

        if chance >= 1000 and self.cutscenes_enabled:
            self.play_cutscene(won, chance, display)
        else:
            display()

    def reset_roll_button(self):
        self.roll_button.config(text="ROLL")
        self.set_buttons_state(tk.NORMAL)
        self.is_rolling = False
        if self.auto_roll_active:
            self.root.after(150, self.start_roll)

    def unbind_scroll_events(self):
        if self.scroll_timer:
            self.root.after_cancel(self.scroll_timer)
            self.scroll_timer = None
        for sequence in ("<MouseWheel>", "<Button-4>", "<Button-5>", "<ButtonPress-1>", "<B1-Motion>", "<ButtonRelease-1>"):
            self.root.unbind_all(sequence)

    def create_scrollable_container(self):
        container = tk.Frame(self.overlay_frame, bg="#141414")
        container.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        scrollbar = tk.Scrollbar(container, orient="vertical", bg="#2c3e50", troughcolor="#0a0a0a", activebackground="#00ffff", bd=1, width=28, relief="raised")
        scrollbar.pack(side="left", fill="y", padx=(0, 4))
        canvas = tk.Canvas(container, bg="#141414", highlightthickness=0, yscrollcommand=scrollbar.set)
        scrollbar.config(command=canvas.yview)
        frame = tk.Frame(canvas, bg="#141414")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        window = canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window, width=e.width))
        self.current_canvas = canvas
        self.touch_last_y = 0

        def smooth_scroll():
            if abs(self.scroll_velocity) > 0.1 and self.current_canvas:
                try:
                    self.current_canvas.yview_scroll(int(-self.scroll_velocity), "units")
                    self.scroll_velocity *= 0.88
                    self.scroll_timer = self.root.after(12, smooth_scroll)
                except Exception:
                    self.scroll_velocity = 0
            else:
                self.scroll_velocity = 0

        def press(event):
            if self.scroll_timer:
                self.root.after_cancel(self.scroll_timer)
            self.touch_last_y = event.y_root
            self.scroll_velocity = 0

        def drag(event):
            dy = event.y_root - self.touch_last_y
            self.touch_last_y = event.y_root
            self.scroll_velocity = dy / 4
            try: canvas.yview_scroll(int(-dy / 8), "units")
            except Exception: pass

        def release(event):
            smooth_scroll()

        def wheel(event):
            try:
                if getattr(event, "delta", 0):
                    canvas.yview_scroll(int(-event.delta / 60), "units")
                elif getattr(event, "num", None) == 4:
                    canvas.yview_scroll(-2, "units")
                elif getattr(event, "num", None) == 5:
                    canvas.yview_scroll(2, "units")
            except Exception: pass

        self.unbind_scroll_events()
        self.root.bind_all("<MouseWheel>", wheel)
        self.root.bind_all("<Button-4>", wheel)
        self.root.bind_all("<Button-5>", wheel)
        self.root.bind_all("<ButtonPress-1>", press)
        self.root.bind_all("<B1-Motion>", drag)
        self.root.bind_all("<ButtonRelease-1>", release)
        canvas.pack(side="right", fill="both", expand=True)
        return frame

    def open_shop(self):
        if self.is_rolling: return
        self.close_overlay()
        self.create_fullscreen_overlay("BOUTIQUE (POTIONS)")
        tk.Label(self.overlay_frame, text=f"Solde : {self.coins} Coins", font=("Helvetica", 12, "bold"), fg="#f1c40f", bg="#141414").pack(pady=2)
        frame = self.create_scrollable_container()
        tk.Label(frame, text="--- POTIONS DE LUCK ---", font=("Helvetica", 11, "bold"), fg="#2ecc71", bg="#141414").pack(pady=(5, 5))
        for item in [i for i in self.shop_items if i["type"] == "luck"]:
            self.create_shop_card(frame, item)
        tk.Label(frame, text="--- POTIONS DE VITESSE ---", font=("Helvetica", 11, "bold"), fg="#3498db", bg="#141414").pack(pady=(15, 5))
        for item in [i for i in self.shop_items if i["type"] == "speed"]:
            self.create_shop_card(frame, item)
        tk.Frame(frame, bg="#141414", height=80).pack(fill="x")

    def create_shop_card(self, parent, item):
        card = tk.Frame(parent, bg="#1f1f1f", highlightbackground="#2c2c2c", highlightthickness=1)
        card.pack(fill="x", pady=4, ipady=6, padx=5)
        title = f"+{item['boost']} Luck" if item["type"] == "luck" else item["name"]
        tk.Label(card, text=title, font=("Helvetica", 11, "bold"), fg="#ffffff", bg="#1f1f1f").pack(pady=2)
        if not item["owned"]:
            btn = tk.Button(card, text=f"Acheter ({item['price']} C)", font=("Helvetica", 9, "bold"), bg="#27ae60" if self.coins >= item["price"] else "#333333", fg="white" if self.coins >= item["price"] else "#777777", bd=0, command=lambda i=item: self.buy_shop_item(i))
        else:
            btn = tk.Button(card, text="EQUIPE" if item["equipped"] else "EQUIPER", font=("Helvetica", 9, "bold"), bg="#e74c3c" if item["equipped"] else "#2980b9", fg="white", bd=0, command=lambda i=item: self.toggle_equip_item(i))
        btn.pack(fill="x", padx=12, pady=4)

    def buy_shop_item(self, item):
        if not item["owned"] and self.coins >= item["price"]:
            self.coins -= item["price"]
            item["owned"] = True
            for other in self.shop_items:
                if other["type"] == item["type"]: other["equipped"] = False
            item["equipped"] = True
            self.coins_label.config(text=f"Coins: {self.coins}")
            self.recalculate_stats()
            self.save_game()
            self.open_shop()

    def toggle_equip_item(self, item):
        if item["owned"]:
            state = not item["equipped"]
            for other in self.shop_items:
                if other["type"] == item["type"]: other["equipped"] = False
            item["equipped"] = state
            self.recalculate_stats()
            self.save_game()
            self.open_shop()

    def open_pets(self):
        if self.is_rolling: return
        self.close_overlay()
        self.create_fullscreen_overlay("BOUTIQUE DE PETS")
        tk.Label(self.overlay_frame, text=f"Solde : {self.coins} Coins", font=("Helvetica", 12, "bold"), fg="#f1c40f", bg="#141414").pack(pady=2)
        frame = self.create_scrollable_container()
        tk.Label(frame, text="--- FAMILIERS PASSIFS ---", font=("Helvetica", 11, "bold"), fg="#e74c3c", bg="#141414").pack(pady=(5, 5))
        for pet in self.pets:
            card = tk.Frame(frame, bg="#1f1f1f", highlightbackground="#2c2c2c", highlightthickness=1)
            card.pack(fill="x", pady=4, ipady=6, padx=5)
            tk.Label(card, text=f"{pet['name']} ({pet['desc']})", font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#1f1f1f").pack(pady=2)
            if not pet["owned"]:
                btn = tk.Button(card, text=f"Acheter ({pet['price']} C)", font=("Helvetica", 9, "bold"), bg="#27ae60" if self.coins >= pet["price"] else "#333333", fg="white" if self.coins >= pet["price"] else "#777777", bd=0, command=lambda p=pet: self.buy_pet(p))
            else:
                btn = tk.Button(card, text="EQUIPE" if pet["equipped"] else "EQUIPER", font=("Helvetica", 9, "bold"), bg="#e74c3c" if pet["equipped"] else "#2980b9", fg="white", bd=0, command=lambda p=pet: self.toggle_equip_pet(p))
            btn.pack(fill="x", padx=12, pady=4)
        tk.Frame(frame, bg="#141414", height=80).pack(fill="x")

    def buy_pet(self, pet):
        if not pet["owned"] and self.coins >= pet["price"]:
            self.coins -= pet["price"]
            pet["owned"] = True
            pet["equipped"] = True
            self.coins_label.config(text=f"Coins: {self.coins}")
            self.recalculate_stats()
            self.save_game()
            self.open_pets()

    def toggle_equip_pet(self, pet):
        if pet["owned"]:
            pet["equipped"] = not pet["equipped"]
            self.recalculate_stats()
            self.save_game()
            self.open_pets()

    def open_history(self):
        if self.is_rolling: return
        self.close_overlay()
        self.create_fullscreen_overlay("HISTORIQUE DES ROLLS")
        frame = self.create_scrollable_container()
        tk.Label(frame, text="--- DERNIÈRES ATTAQUES OBTENUES ---", font=("Helvetica", 11, "bold"), fg="#3498db", bg="#141414").pack(pady=(5, 10))
        if not self.roll_history:
            tk.Label(frame, text="Aucun roll effectué pour le moment !", font=("Helvetica", 10), fg="#777777", bg="#141414").pack(pady=10)
        else:
            for entry in self.roll_history:
                color, _ = self.get_rarity_colors(entry["chance"])
                card = tk.Frame(frame, bg="#1f1f1f", highlightbackground="#2c2c2c", highlightthickness=1)
                card.pack(fill="x", pady=2, ipady=4, padx=5)
                tk.Label(card, text=f"Roll #{entry['roll_num']} : {entry['name']} (1/{entry['chance']})", font=("Helvetica", 10, "bold"), fg=color, bg="#1f1f1f").pack(pady=2)
        tk.Frame(frame, bg="#141414", height=80).pack(fill="x")

    def open_index(self):
        if self.is_rolling: return
        self.close_overlay()
        self.create_fullscreen_overlay("INDEX DES AURAS")
        frame = self.create_scrollable_container()
        sorted_auras = sorted(self.auras.items(), key=lambda x: x[1]["chance"])
        categories = [
            ("BLANC (Commun)", lambda c: c < 100),
            ("VERT (Rare)", lambda c: 100 <= c < 500),
            ("JAUNE (Épique)", lambda c: 500 <= c < 1000),
            ("ROUGE (Mythique)", lambda c: 1000 <= c < 10000),
            ("MAUVE (Légendaire)", lambda c: 10000 <= c < 100000),
            ("BRONZE/CUIVRE (Cosmique)", lambda c: 100000 <= c < 1000000),
            ("OR DIVIN (Ultime)", lambda c: c >= 1000000)
        ]
        for category, condition in categories:
            items = [(n, d) for n, d in sorted_auras if condition(d["chance"])]
            if not items: continue
            tk.Label(frame, text=f"--- {category} ---", font=("Helvetica", 11, "bold"), fg="#aaaaaa", bg="#141414").pack(pady=(10, 5))
            for name, data in items:
                chance = data["chance"]
                bright, dark = self.get_rarity_colors(chance)
                card = tk.Frame(frame, bg="#1f1f1f", highlightbackground="#2c2c2c", highlightthickness=1)
                card.pack(fill="x", pady=2, ipady=4, padx=5)
                shown = name if data["unlocked"] else "???"
                color = bright if data["unlocked"] else dark
                tk.Label(card, text=shown, font=("Helvetica", 11, "bold"), fg=color, bg="#1f1f1f").pack()
                tk.Label(card, text=f"Rareté : 1/{chance}", font=("Helvetica", 8), fg=color, bg="#1f1f1f").pack()
        tk.Frame(frame, bg="#141414", height=80).pack(fill="x")

    def open_quests(self):
        if self.is_rolling: return
        self.close_overlay()
        self.create_fullscreen_overlay("QUÊTES TEMPORAIRES")
        frame = self.create_scrollable_container()
        for q in self.quests:
            card = tk.Frame(frame, bg="#1f1f1f", highlightbackground="#2c2c2c", highlightthickness=1)
            card.pack(fill="x", pady=6, ipady=6, padx=5)
            status_color = "#2ecc71" if q["completed"] else "#ffffff"
            status = "Terminée !" if q["completed"] else f"Progression : {q['progress']} / {q['target']}"
            tk.Label(card, text=q["desc"], font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#1f1f1f").pack(pady=2)
            if q["reward_type"] == "coins": reward = f"Récompense : {q['reward_val']} Coins"
            elif q["reward_type"] == "luck": reward = f"Récompense : +{q['reward_val']} Luck ({q['duration']}s)"
            else: reward = f"Récompense : +{q['reward_val']} Speed ({q['duration']}s)"
            tk.Label(card, text=f"{status} | {reward}", font=("Helvetica", 8), fg=status_color, bg="#1f1f1f").pack(pady=2)
            if q["completed"] and not q["claimed"]:
                tk.Button(card, text="CLAIM", font=("Helvetica", 9, "bold"), bg="#27ae60", fg="white", bd=0, command=lambda quest=q: self.claim_quest(quest)).pack(fill="x", padx=12, pady=4)
            elif q["claimed"]:
                tk.Label(card, text="RÉCOMPENSÉ", font=("Helvetica", 8, "bold"), fg="#777777", bg="#1f1f1f").pack(pady=2)
        tk.Frame(frame, bg="#141414", height=80).pack(fill="x")

    def open_settings(self):
        if self.is_rolling: return
        self.close_overlay()
        self.create_fullscreen_overlay("OPTIONS DU JEU")
        frame = self.create_scrollable_container()
        tk.Label(frame, text=f"--- PARAMÈTRES (Partie actuelle : {self.current_slot}) ---", font=("Helvetica", 11, "bold"), fg="#7f8c8d", bg="#141414").pack(pady=(5, 10))
        slot_card = tk.Frame(frame, bg="#1f1f1f", highlightbackground="#2c2c2c", highlightthickness=1)
        slot_card.pack(fill="x", pady=4, ipady=6, padx=5)
        tk.Label(slot_card, text="Changer de partie (Slot)", font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#1f1f1f").pack(pady=2)
        tk.Button(slot_card, text="RETOURNER AU MENU DES SLOTS", font=("Helvetica", 9, "bold"), bg="#2980b9", fg="white", bd=0, command=self.return_to_slot_selector).pack(fill="x", padx=12, pady=4)

        card1 = tk.Frame(frame, bg="#1f1f1f", highlightbackground="#2c2c2c", highlightthickness=1)
        card1.pack(fill="x", pady=4, ipady=6, padx=5)
        tk.Label(card1, text="Cutscenes rares (1/1000+)", font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#1f1f1f").pack(pady=2)
        self.cutscene_toggle_btn = tk.Button(card1, text="ACTIVÉES" if self.cutscenes_enabled else "DÉSACTIVÉES", font=("Helvetica", 9, "bold"), bg="#27ae60" if self.cutscenes_enabled else "#c0392b", fg="white", bd=0, command=self.toggle_cutscenes_option)
        self.cutscene_toggle_btn.pack(fill="x", padx=12, pady=4)

        card2 = tk.Frame(frame, bg="#1f1f1f", highlightbackground="#2c2c2c", highlightthickness=1)
        card2.pack(fill="x", pady=4, ipady=6, padx=5)
        tk.Label(card2, text="Flashs / Clignotements (Anti-stroboscopique)", font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#1f1f1f").pack(pady=2)
        self.flash_toggle_btn = tk.Button(card2, text="ACTIVÉS" if self.flash_enabled else "DÉSACTIVÉS", font=("Helvetica", 9, "bold"), bg="#27ae60" if self.flash_enabled else "#c0392b", fg="white", bd=0, command=self.toggle_flash_option)
        self.flash_toggle_btn.pack(fill="x", padx=12, pady=4)
        tk.Frame(frame, bg="#141414", height=80).pack(fill="x")

    def return_to_slot_selector(self):
        self.save_game()
        self.root.destroy()
        new_root = tk.Tk()
        SlotSelector(new_root)
        new_root.mainloop()

    def toggle_cutscenes_option(self):
        self.cutscenes_enabled = not self.cutscenes_enabled
        self.cutscene_toggle_btn.config(text="ACTIVÉES" if self.cutscenes_enabled else "DÉSACTIVÉES", bg="#27ae60" if self.cutscenes_enabled else "#c0392b")
        self.save_game()

    def toggle_flash_option(self):
        self.flash_enabled = not self.flash_enabled
        self.flash_toggle_btn.config(text="ACTIVÉS" if self.flash_enabled else "DÉSACTIVÉS", bg="#27ae60" if self.flash_enabled else "#c0392b")
        self.save_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = SlotSelector(root)
    root.mainloop()
