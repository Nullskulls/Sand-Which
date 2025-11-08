import os, random, json, sys
import time as Time

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAVES_FILE = os.path.join(BASE_DIR, "Sand-Which Saves")

TYPING_PHRASES = [
    "Stack it fast before the lunch rush hits",
    "Quick hands make the best sandwiches",
    "Speed and precision wins the day",
    "The clock is ticking tick tick tick",
    "Faster faster the customer is waiting",
    "Layer lettuce like your life depends on it",
    "Spread mayo with surgical precision",
    "The perfect sandwich is an art form",
    "Every ingredient tells a story",
    "Balance flavor texture and satisfaction",
    "The customer is getting more impatient hurry up",
    "They look angry move it move it",
    "Five stars or bust make it count",
    "Tips depend on your speed kid",
    "They want extra protein right now",
    "Tomatoes are flying everywhere",
    "The lettuce is wilting hurry up",
    "Become one with the ingredients",
    "Greatness is one sandwich away",
    "Customers demand perfection or else.."
]


class Customer:
    """
    Class used to store customer info
    """
    def __init__(self, customer, order, spent):
        self.Customer = customer
        self.Order = order
        self.Spent = spent

class Game:
    """
    Class holding everything needed for the game
    """
    def __init__(self, ingredients, characters, data, path):
        self.Ingredients = ingredients
        self.Characters  = characters
        self.Data = data
        self.Path = path


    def save(self):
        """
        Function used to save the data
        """
        try:
            with open(os.path.join(SAVES_FILE, self.Path, "ingredients.json"), "w") as file:
                json.dump(self.Ingredients, file, indent=4)
            with open(os.path.join(SAVES_FILE, self.Path, "characters.json"), "w") as file:
                json.dump(self.Characters, file, indent=4)
            with open(os.path.join(SAVES_FILE, self.Path, "data.json"), "w") as file:
                json.dump(self.Data, file, indent=4)
        except Exception as e:
            print(f"Failed to save files, Error: {e}\nExiting game to prevent data corruption...")
            sys.exit("error occurred")

    def update_user_balance(self, amount):
        """
        Function used to update the user's balance
        """
        self.Data["Balance"] += amount

    def update_customer_info(self, customer, amount, tip):
        """
        Function used to update customer statistics
        """
        self.Data["Customers_Served"] +=1
        self.Characters[customer]["Total_Spent"] += amount + tip
        self.Characters[customer]["Total_Visits"] += 1
        self.Characters[customer]["Tips_Given"] += tip

    def get_customer(self):
        """
        Function used to randomly generate a customer and their order
        """
        customer = random.choice(list(self.Characters.keys()))
        choices = []
        spent = 0
        ingredients_copy = self.Ingredients
        for i in range(random.randint(3, 7)):
            choice = random.choice(list(self.Ingredients.keys()))
            while ingredients_copy[choice]["Amount"] == 0:
                choice = random.choice(list(self.Ingredients.keys()))
            ingredients_copy[choice]["Amount"] -= 1
            choices.append(choice)
            spent += self.Ingredients[choice]["Cost"]
        spent *= 1.3 * (1 + self.Data["Perfection_Rate"] / 10)
        spent = round(spent)
        return Customer(spent=spent, order=choices, customer=customer)

    def display_shop(self):
        """
        Function used to display the shop
        """
        os.system("cls" if os.name == "nt" else "clear")
        ingredients_list = list(self.Ingredients.keys())
        message = "      Item     |     Cost \n"
        for item in enumerate(self.Ingredients):
            message += f"[{item[0]+1}]  {item[1]}: {self.Ingredients[item[1]]["Cost"]}\n"
        print(message, end="")
        choice = 0
        try:
            choice = int(input("Pick a product to buy or press enter to continue...\n$ "))
        except ValueError:
            return
        if 0 < choice <= len(self.Ingredients):
            if self.Ingredients[ingredients_list[choice-1]]["Cost"] > self.Data["Balance"]:
                print("You cant afford this...")
                Time.sleep(1)
                return
            self.update_user_balance(self.Ingredients[ingredients_list[choice-1]]["Cost"] * -1)
            self.Ingredients[ingredients_list[choice-1]]["Amount"] += 1
            self.save()
            return
        self.display_shop()


    def display_stats(self):
        """
        Function used to display current save stats
        """
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Total money you've earned is {self.Data["Total_Earned"]}\nTotal shifts you've survived os {self.Data['Total_Shifts']}\nTotal tips you've received {self.Data['Tips_Received']}\nTotal customers you've serverd is {self.Data['Customers_Served']}\nYou've spent a total of {self.Data['Total_Spent']}\nYour perfection rating is {self.Data['Perfection_Rate']}/10")
        input("Press enter to continue...")

    def display_inventory(self):
        """
        Function used to display current inventory
        """
        os.system("cls" if os.name == "nt" else "clear")
        message = "\n\n"
        for ingredient in self.Ingredients:
            if self.Ingredients[ingredient]["Amount"] > 0:
                message += f"- {ingredient}: {self.Ingredients[ingredient]['Amount']}\n"
        print(message)
        input("Press enter to continue...")

    def display_hud(self, time, customer):
        """
        Function used to display the hud between customers and days
        """
        os.system("cls" if os.name == "nt" else "clear")
        if time < 12:
            time = f"{time}AM"
        else:
            if time > 17:
                time = 17
            time = f"{time-12}PM"
        print(f"Shift: {self.Data['Total_Shifts']} | Balance: {self.Data['Balance']} | Time: {time}")
        if not customer:
            entered = input("[E] Exit game - [S] Shop - [Q] Stats - [I] Inventory - Press enter to continue...\n$").upper()
            if entered == "E":
                sys.exit()
            elif entered == "I":
                self.display_inventory()
            elif entered == "Q":
                self.display_stats()
            elif entered == "S":
                self.display_shop()
            return
        sandwich_ingredients = ""
        for ingredient in enumerate(customer.Order):
            if ingredient[0] == len(customer.Order)-1:
                sandwich_ingredients += f"{ingredient[1]}"
            elif ingredient[0] == len(customer.Order)-2:
                sandwich_ingredients += f"{ingredient[1]} and "
            else:
                sandwich_ingredients += f"{ingredient[1]}, "

        print(f"*{customer.Customer} walks in...*\n{customer.Customer}: Good day!\nYou: ...\n{customer.Customer}: Okay..?\n{customer.Customer}: I'd like a sandwich with {sandwich_ingredients}")

    def type_test(self, customer):
        input("Press enter to start cooking...")
        total_score = 0
        total_time_taken = 0
        for ingredient in customer.Order:
            print(f"Add the {ingredient}..")
            phrase = self.get_quote()
            start_time = Time.time()
            user_input = input(f'Type it as fast as you can!\n-->"{phrase}"<--\n$')
            time_taken = Time.time() - start_time
            score = 0.01
            for letter in enumerate(phrase):
                if letter[0] >= len(user_input):
                    break
                elif letter[1] == user_input[letter[0]]:
                    score += 1
            score /= len(phrase)
            os.system("cls" if os.name == "nt" else "clear")
            if score >= 0.9:
                print("Perfectly done!")
                self.Data["Perfection_Rate"] += .1
            elif score > 0.7:
                print("Still edible...")
            else:
                print("You botched it..")
                self.Data["Perfection_Rate"] -= .2
            self.Data["Perfection_Rate"] = max(0, min(10, self.Data["Perfection_Rate"]))
            total_score += score
            total_time_taken += time_taken
        return total_score, total_time_taken


    def play_day(self):
        """
        Function used to play day
        """
        self.save()
        time = 7
        if self.Data["Balance"] <= 0:
            self.game_over()
        customer_number = random.randint(2, 3+self.Data["Rating"])
        self.display_hud(time, customer=None)
        for _ in range(customer_number):
            time += round(12/customer_number)
            customer = self.get_customer()
            self.display_hud(time=time, customer=customer)
            total_score, total_time_taken = self.type_test(customer)
            avg_accuracy = total_score / len(customer.Order)
            estimated_word_count = len(customer.Order) * 8
            wpm = (estimated_word_count / total_time_taken) * 60
            tip_multiplier = 0
            if avg_accuracy >= 0.9:
                self.Data["Satisfied_Customers"] += 1
                if wpm >= 60:
                    tip_multiplier = 0.25
                elif wpm >= 40:
                    tip_multiplier = 0.125
                else:
                    tip_multiplier = 0.05
            elif avg_accuracy <= 0.7:
                self.Data["Dissatisfied_Customers"] += 1
                tip_multiplier = 0.05 if wpm >= 50 else 0

            tip = round(tip_multiplier * customer.Spent)
            self.Data["Total_Earned"] += customer.Spent
            self.Data["Tips_Received"] += tip
            self.update_user_balance(tip+customer.Spent)
            self.update_customer_info(customer.Customer, customer.Spent, tip)
            self.Data["Rating"] = max(0, min(10, (self.Data["Satisfied_Customers"] // 10) - (self.Data["Dissatisfied_Customers"] // 5)))
            character_data = self.Characters[customer.Customer]
            if avg_accuracy >= 0.9:
                quote = random.choice(character_data["Happy_Phrases"])
                if tip > 0:
                    quote += f"\n{random.choice(character_data['Tipping_Phrases'])}"
            elif avg_accuracy >= 0.7:
                quote = random.choice(character_data["Neutral_Phrases"])
            else:
                quote = random.choice(character_data["Angry_Phrases"])
            os.system("cls")
            print(f"{customer.Customer}: {quote}\n \n")
            print(f"\n{avg_accuracy * 100:.0f}% accuracy, {wpm:.0f} WPM")
            print(f"Earned: ${customer.Spent} + ${tip} tip = ${customer.Spent + tip}")
            input("Press enter to continue...")



    def game_over(self):
        """
        Function used to display the game over screen
        """
        print(f"CONGRATS! You've gone bankrupt!\nSo here are your stats:\nTotal money you've earned is {self.Data["Total_Earned"]}\nTotal shifts you've survived os {self.Data['Total_Shifts']}\nTotal tips you've received {self.Data['Tips_Received']}\nTotal customers you've serverd is {self.Data['Customers_Served']}\nYou've spent a total of {self.Data['Total_Spent']}\nYour perfection rating is {self.Data['Perfection_Rate']}/10")

    @staticmethod
    def get_quote():
        """
        Function used to get a random quote for typing mini-game
        """
        return random.choice(TYPING_PHRASES)


def menu():
    """
    Function used to show the start menu
    """
    returned = 0
    try:
        returned = int(input("[1] New Game \n[2] Load Saves \n[3] Exit\n$"))
    except ValueError:
        print("Please enter a number.")
        return menu()

    match returned:
        case 1:
            save_file = input("Enter save file name: \n$")
            return initialize_game(save_file)

        case 2:
            saved_games = get_saves()

            if not saved_games:
                print("No saves found.")
                return menu()

            message = "Select a game file:\n"

            for saved_game in enumerate(saved_games):
                message += f"[{saved_game[0]+1}] {saved_game[1]}\n"
            try:
                selected_game = int(input(message + "\n$")) - 1
            except ValueError:
                print("Please enter a number.")
                return menu()
            if selected_game < 0 or selected_game >= len(saved_games):
                menu()
                return menu()
            return initialize_game(saved_games[selected_game])
        case 3:
            sys.exit()
        case _:
            print("Invalid input.")
            return menu()

    return "holder"

def load_ingredients(save_path):
    """
    Function used for loading a previous game's ingredients or initializing a new game's ingredients
    """
    if not os.path.exists(os.path.join(SAVES_FILE, save_path, "ingredients.json")):
        with open(os.path.join(SAVES_FILE, save_path, "ingredients.json"), "w") as file:
            ingredients = {
                "Bread": {"Cost": 10, "Amount": random.randint(1, 5), "Type": "Base"},
                "Whole Wheat Bread": {"Cost": 12, "Amount": random.randint(1, 5), "Type": "Base"},
                "Wrap": {"Cost": 10, "Amount": random.randint(1, 5), "Type": "Base"},
                "Patties": {"Cost": 50, "Amount": random.randint(1, 3), "Type": "Protein"},
                "Ham": {"Cost": 20, "Amount": random.randint(1, 7), "Type": "Protein"},
                "Egg": {"Cost": 5, "Amount": random.randint(1, 12), "Type": "Protein"},
                "Cheese": {"Cost": 5, "Amount": random.randint(1, 5), "Type": "Dairy"},
                "Lettuce": {"Cost": 1, "Amount": random.randint(1, 20), "Type": "Vegetable"},
                "Tomato": {"Cost": 2, "Amount": random.randint(1, 20), "Type": "Vegetable"},
                "Onion": {"Cost": 1, "Amount": random.randint(1, 20), "Type": "Vegetable"},
                "Pickles": {"Cost": 3, "Amount": random.randint(1, 10), "Type": "Vegetable"},
                "Cucumber": {"Cost": 2, "Amount": random.randint(1, 10), "Type": "Vegetable"},
                "Mayo": {"Cost": 10, "Amount": random.randint(5, 20), "Type": "Sauce"},
                "Ketchup": {"Cost": 10, "Amount": random.randint(5, 20), "Type": "Sauce"},
                "Mustard": {"Cost": 6, "Amount": random.randint(5, 20), "Type": "Sauce"},
                "Baguette": {"Cost": 15, "Amount": 0, "Type": "Base"},
                "Ciabatta": {"Cost": 18, "Amount": 0, "Type": "Base"},
                "Rye Bread": {"Cost": 14, "Amount": 0, "Type": "Base"},
                "Steak": {"Cost": 100, "Amount": 0, "Type": "Protein"},
                "Chicken Breast": {"Cost": 35, "Amount": 0, "Type": "Protein"},
                "Bacon": {"Cost": 25, "Amount": 0, "Type": "Protein"},
                "Turkey": {"Cost": 30, "Amount": 0, "Type": "Protein"},
                "Tuna": {"Cost": 25, "Amount": 0, "Type": "Protein"},
                "Sausage": {"Cost": 15, "Amount": 0, "Type": "Protein"},
                "Salami": {"Cost": 20, "Amount": 0, "Type": "Protein"},
                "Swiss Cheese": {"Cost": 8, "Amount": 0, "Type": "Dairy"},
                "Cheddar": {"Cost": 8, "Amount": 0, "Type": "Dairy"},
                "Mozzarella": {"Cost": 9, "Amount": 0, "Type": "Dairy"},
                "Blue Cheese": {"Cost": 12, "Amount": 0, "Type": "Dairy"},
                "Spinach": {"Cost": 2, "Amount": 0, "Type": "Vegetable"},
                "Bell Peppers": {"Cost": 3, "Amount": 0, "Type": "Vegetable"},
                "Jalapeños": {"Cost": 4, "Amount": 0, "Type": "Vegetable"},
                "Avocado": {"Cost": 15, "Amount": 0, "Type": "Vegetable"},
                "Mushrooms": {"Cost": 4, "Amount": 0, "Type": "Vegetable"},
                "Olives": {"Cost": 2, "Amount": 0, "Type": "Vegetable"},
                "Fried Onions": {"Cost": 4, "Amount": 0, "Type": "Vegetable"},
                "Caramelized Onions": {"Cost": 5, "Amount": 0, "Type": "Vegetable"},
                "Coleslaw": {"Cost": 6, "Amount": 0, "Type": "Vegetable"},
                "Sun-Dried Tomatoes": {"Cost": 7, "Amount": 0, "Type": "Vegetable"},
                "Pickled Onions": {"Cost": 3, "Amount": 0, "Type": "Vegetable"},
                "BBQ Sauce": {"Cost": 8, "Amount": 0, "Type": "Sauce"},
                "Ranch": {"Cost": 7, "Amount": 0, "Type": "Sauce"},
                "Garlic Sauce": {"Cost": 6, "Amount": 0, "Type": "Sauce"},
                "Hot Sauce": {"Cost": 7, "Amount": 0, "Type": "Sauce"},
                "Honey Mustard": {"Cost": 7, "Amount": 0, "Type": "Sauce"},
                "Pesto": {"Cost": 10, "Amount": 0, "Type": "Sauce"},
                "Hummus": {"Cost": 8, "Amount": 0, "Type": "Sauce"}
            }

            json.dump(ingredients, file, indent=4)
    with open(os.path.join(SAVES_FILE, save_path, "ingredients.json"), "r") as f:
        return json.load(f)

def load_characters(save_path):
    """
    Function used for loading a previous game's characters or initializing a new game's characters
    """
    if not os.path.exists(os.path.join(SAVES_FILE, save_path, "characters.json")):
        with open(os.path.join(SAVES_FILE, save_path, "characters.json"), "w") as file:
            characters = {
                "Greg": {
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(40, 100),
                    "Favorite_Ingredients": ["Bacon", "Cheddar", "Lettuce", "Tomato"],
                    "Disliked_Ingredients": ["Olives", "Blue Cheese", "Avocado"],
                    "Happy_Phrases": [
                        "Woah that looks fire..", "I can't wait to eat this!", "I'm drooling.",
                        "Now THAT'S a sandwich!", "This might just be your best one yet.",
                        "Perfection on bread.", "You outdid yourself today.", "Mmm… *chef’s kiss*",
                        "I could eat this every day.", "You’re getting better at this, huh?"
                    ],
                    "Angry_Phrases": [
                        "How did you even manage to screw it up this bad?", "What is this supposed to be?",
                        "Did you drop it before serving?", "This looks like something the dog wouldn’t touch.",
                        "I asked for food, not a crime scene.", "Bruh.", "I’m never coming back here again.",
                        "This is worse than cafeteria food.", "You call this cooking?",
                        "I wouldn’t serve this to my enemies."
                    ],
                    "Neutral_Phrases": [
                        "Hmm… it’s alright I guess.", "Not bad, not great either.", "Yeah, edible.",
                        "It’s fine, I’ve had worse.", "I wouldn’t complain if it was free.",
                        "Could use a little more effort next time.", "Average sandwich, average day.",
                        "I’ll give you a pass this time."
                    ],
                    "Tipping_Phrases": [
                        "Keep the change, you earned it.", "That sandwich was worth every cent.",
                        "Don’t spend it all in one place.", "Here, buy yourself some better ingredients.",
                        "A little extra for the effort.", "You deserve a tip for that one."
                    ]
                },

                "Karen": {
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(10, 40),
                    "Favorite_Ingredients": ["Avocado", "Lettuce", "Spinach", "Tomato"],
                    "Disliked_Ingredients": ["Bacon", "Sausage", "Onion"],
                    "Happy_Phrases": [
                        "Finally, someone who knows how to make food right.", "This is *acceptable.*",
                        "Okay fine, I actually like it.", "Wow… this doesn’t look awful for once."
                    ],
                    "Angry_Phrases": [
                        "I want to speak to your manager.", "Is this what you call customer service?",
                        "You ruined my day.", "Completely unacceptable!", "You’ll be hearing from me.",
                        "This place used to be good!", "Disgusting.", "Refund. Now."
                    ],
                    "Neutral_Phrases": ["It’s fine I guess.", "You’re lucky I’m hungry."],
                    "Tipping_Phrases": ["Don’t say I never gave you anything."]
                },

                "Chad": {
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(60, 120),
                    "Favorite_Ingredients": ["Steak", "Bacon", "Cheddar", "BBQ Sauce"],
                    "Disliked_Ingredients": ["Lettuce", "Spinach"],
                    "Happy_Phrases": [
                        "Bro this SLAPS!", "You’re a real one for this sandwich.",
                        "That’s a PR sandwich right there!", "Gains secured.",
                        "You put your heart into that one, huh?"
                    ],
                    "Angry_Phrases": [
                        "Bro… this ain’t it.", "I said steak, not sadness.", "Mid sandwich.",
                        "I’m losing gains eating this.", "Come on man, what is this?"
                    ],
                    "Neutral_Phrases": ["Yeah, it’s fuel I guess.", "It’ll do for now."],
                    "Tipping_Phrases": ["Here bro, protein tax.", "Respect for the effort."]
                },

                "Sophia": {
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(50, 100),
                    "Favorite_Ingredients": ["Mozzarella", "Tomato", "Pesto", "Ciabatta"],
                    "Disliked_Ingredients": ["Ketchup", "Blue Cheese"],
                    "Happy_Phrases": [
                        "That looks beautiful!", "It’s giving gourmet.", "Oh my god, perfection!",
                        "I’m totally posting this.", "You’re seriously underrated."
                    ],
                    "Angry_Phrases": [
                        "Ew, aesthetic ruined.", "Why does it look like that?",
                        "This tastes... wrong.", "Yeah, I’m not eating this."
                    ],
                    "Neutral_Phrases": ["Looks okay I guess.", "It’s fine but I expected more."],
                    "Tipping_Phrases": ["You deserve a little something extra!"]
                },

                "Old Man Jenkins": {
                    "Balance": random.randint(5, 30),
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(20, 60),
                    "Favorite_Ingredients": ["Ham", "Cheese", "Onion", "Mustard"],
                    "Disliked_Ingredients": ["Avocado", "Hot Sauce"],
                    "Happy_Phrases": [
                        "Reminds me of the good ol’ days.", "Now that’s a proper meal.",
                        "Tastes like my late wife’s cooking.", "I’ll be back tomorrow, son."
                    ],
                    "Angry_Phrases": [
                        "What is this millennial garbage?", "In my day, sandwiches had *flavor!*",
                        "Too fancy for me.", "I can’t chew half of this."
                    ],
                    "Neutral_Phrases": ["Eh, I’ve had better.", "Not bad, not bad."],
                    "Tipping_Phrases": ["Here’s a nickel, don’t spend it all at once."]
                },

                "Zoe": {
                    "Balance": random.randint(30, 100),
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(70, 120),
                    "Favorite_Ingredients": ["Avocado", "Lettuce", "Spinach", "Pesto"],
                    "Disliked_Ingredients": ["Bacon", "Onion"],
                    "Happy_Phrases": [
                        "Oh this is so fresh!", "This tastes healthy, I love it!",
                        "You really care about ingredients, huh?", "Perfect balance of everything."
                    ],
                    "Angry_Phrases": [
                        "This feels greasy.", "You used meat, didn’t you?", "Too much sauce!",
                        "My diet is ruined!"
                    ],
                    "Neutral_Phrases": ["It’s fine, just… not what I usually eat."],
                    "Tipping_Phrases": ["Here! Support local businesses!"]
                },

                "Marcus": {
                    "Balance": random.randint(100, 250),
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(60, 90),
                    "Favorite_Ingredients": ["Steak", "BBQ Sauce", "Cheddar", "Bacon"],
                    "Disliked_Ingredients": ["Lettuce", "Mayo"],
                    "Happy_Phrases": [
                        "That’s high-quality stuff!", "Finally, someone who knows flavor.",
                        "I could eat here every day.", "You’ve got talent, kid."
                    ],
                    "Angry_Phrases": [
                        "What did you do to the meat?", "Dry. Completely dry.",
                        "That’s not steak, that’s rubber.", "Disgraceful."
                    ],
                    "Neutral_Phrases": ["Acceptable, but barely."],
                    "Tipping_Phrases": ["Keep this up and you’ll go places."]
                },

                "Emily": {
                    "Balance": random.randint(20, 70),
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(50, 100),
                    "Favorite_Ingredients": ["Cheese", "Tomato", "Cucumber", "Mayo"],
                    "Disliked_Ingredients": ["Hot Sauce", "Onion"],
                    "Happy_Phrases": [
                        "Aww this is cute!", "Tastes just right!", "You made it with love didn’t you?",
                        "Perfect bite every time!"
                    ],
                    "Angry_Phrases": [
                        "It’s too spicy!", "I didn’t ask for that!", "Ugh, soggy bread again?",
                        "Why do you hate me?"
                    ],
                    "Neutral_Phrases": ["It’s okay, just okay."],
                    "Tipping_Phrases": ["You’re sweet, keep the change!"]
                },

                "Rico": {
                    "Balance": random.randint(10, 60),
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(30, 70),
                    "Favorite_Ingredients": ["Salami", "Onion", "Pickles", "Mustard"],
                    "Disliked_Ingredients": ["Pesto", "Hummus"],
                    "Happy_Phrases": [
                        "Ay yo this hits!", "You got skills!", "Best sandwich I’ve had all week!",
                        "Bro’s cooking with passion!"
                    ],
                    "Angry_Phrases": [
                        "Nah this ain’t right.", "You tryna poison me?", "What’s this texture?",
                        "Unbelievable, bro."
                    ],
                    "Neutral_Phrases": ["It’s cool, I guess."],
                    "Tipping_Phrases": ["Here, respect for the hustle."]
                },

                "Luna": {
                    "Balance": random.randint(50, 150),
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(80, 150),
                    "Favorite_Ingredients": ["Mozzarella", "Tomato", "Pesto", "Spinach"],
                    "Disliked_Ingredients": ["Ketchup", "Sausage"],
                    "Happy_Phrases": [
                        "Oh wow, this is actually amazing.", "It tastes like summer.",
                        "Everything’s balanced perfectly.", "I’m so coming back here."
                    ],
                    "Angry_Phrases": [
                        "This doesn’t taste fresh.", "You rushed this, didn’t you?",
                        "Too much of something… can’t tell what.", "I’m disappointed, honestly."
                    ],
                    "Neutral_Phrases": ["It’s… fine.", "I expected more from you."],
                    "Tipping_Phrases": ["I’ll tip because I believe in you."]
                },

                "Big Tony": {
                    "Balance": random.randint(70, 180),
                    "Total_Spent": 0,
                    "Total_Visits": 0,
                    "Tips_Given": 0,
                    "Patience": random.randint(50, 90),
                    "Favorite_Ingredients": ["Steak", "Onion", "Cheddar", "BBQ Sauce"],
                    "Disliked_Ingredients": ["Lettuce", "Avocado"],
                    "Happy_Phrases": [
                        "Now *that’s* what I’m talkin’ about!", "You got good hands, kid.",
                        "This sandwich reminds me of home.", "Fuhgeddaboudit, that’s amazing!"
                    ],
                    "Angry_Phrases": [
                        "What is this trash?", "You insult my taste buds like this?",
                        "Don’t ever serve me that again.", "Disgrace to the art of sandwiches."
                    ],
                    "Neutral_Phrases": ["It’s okay. I’ve had worse."],
                    "Tipping_Phrases": ["You did good, here’s a little bonus."]
                }
            }
            json.dump(characters, file, indent=4)

    with open(os.path.join(SAVES_FILE, save_path, "characters.json"), "r") as f:
        return json.load(f)

def load_state(save_path):
    """
    Function used to load a previous game's data or initialize a new one
    """
    if not os.path.exists(os.path.join(SAVES_FILE, save_path, "data.json")):
        with open(os.path.join(SAVES_FILE, save_path, "data.json"), "w") as file:
            data = {
                "Total_Earned": 0,
                "Total_Shifts": 0,
                "Tips_Received": 0,
                "Customers_Served": 0,
                "Total_Spent": 0,
                "Balance": 20,
                "Satisfied_Customers": 0,
                "Dissatisfied_Customers": 0,
                "Rating": 0, #from 0-10 every 10 satisfied customers you gain a "star" and every 5 u lose a "star" each star adds 10% more money
                "Perfection_Rate": 1 #from 1-9 the higher the number the more ur tipped
            }
            json.dump(data, file, indent=4)

    with open(os.path.join(SAVES_FILE, save_path, "data.json"), "r") as file:
        return json.load(file)


def initialize_game(save_path):
    """
    Function used to initialize a new game or load an old one
    """
    os.makedirs(os.path.join(SAVES_FILE, save_path), exist_ok=True)
    game_state = Game(
        ingredients=load_ingredients(save_path),
        characters=load_characters(save_path),
        data=load_state(save_path),
        path=save_path
    )
    return game_state

def get_saves():
    """
    Function used to find all previously saved games
    """
    os.makedirs(SAVES_FILE, exist_ok=True)
    saves = [f for f in os.listdir(SAVES_FILE) if os.path.isdir(os.path.join(SAVES_FILE, f)) and not f.startswith("__")]
    return saves