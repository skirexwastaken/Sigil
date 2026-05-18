(lambda os, random:(
    ( # --- World map and its layers ---
        worldMap := [
            ["🌳","🌳","🌳","🌳","🌳","🌳","🌳","🌳","🌳","🌳","🌳"],
            ["🌳","⬛","⬛","⬛","🌳","⬛","⬛","⬛","⬛","⬛","🌳"],
            ["🌳","⬛","🌳","⬛","🌳","⬛","🌳","🌳","⬛","⬛","🌳"],
            ["🌳","⬛","🌳","⬛","⬛","⬛","⬛","🌳","⬛","🌳","🌳"],
            ["🌳","🌳","🌳","🌳","🌳","🌳","⬛","🌳","⬛","⬛","🌳"],
            ["🌳","⛲","🌵","🦉","⬛","🌳","⬛","🌳","🌳","⬛","🌳"],
            ["🌳","🌳","🌳","⬛","⬛","🌳","⬛","⬛","🌳","⬛","🌳"],
            ["🌳","📦","🌳","⬛","🌳","🌳","🌳","⬛","🌳","⬛","🌳"],
            ["🌳","⬛","🌳","⬛","⬛","🪨","⬛","⬛","⬛","⬛","🌳"],
            ["🌳","⬛","⛄","⬛","🌳","🌳","⬛","🌳","⬛","⬛","🌳"],
            ["🌳","🌳","🌳","🌳","🌳","🌳","🌳","🌳","🌳","🌳","🌳"],
            ],
        boxLayer := [
            ["","","","","","","","","","",""],
            ["","","","","","","","","","",""],
            ["","","","","","","","","","",""],
            ["","","","","","","","","","",""],
            ["","","","","","","","","","",""],
            ["","","","","","","","","","",""],
            ["","","","","","","","","","",""],
            ["","Ancient Book","","","","","","","","",""],
            ["","","","","","","","","","",""],
            ["","","","","","","","","","",""],
            ["","","","","","","","","","",""],
        ],
    ),

    (# --- User data -> 0 alpha, 1 beta, 2 inventory, 3 health, 4 maxHealth, 5 console ---
        user := [5,4,[], 5, 5, " ... "],
        userPointers := {
            "alpha":0,
            "beta":1,
            "inventory":2,
            "health":3,
            "maxHealth":4,
            "console":5
        }
    ),
    
    ( # --- Fighting mechanic ---
        fightMechanic := lambda user, userPointers, worldMap, boxLayer, enemyHealth, enemyIcon, roundResult :(
            os.system('cls' if os.name == 'nt' else 'clear'),

            ( # --- Combat render ---
                print(f". . . . . . .\n. {"🧙"} . . {enemyIcon} .\n. . . . . . ."),
                print(f"Player: {user[3]}/{user[4]} ❤️  Enemy: {enemyHealth} ❤️ ")
            ),

            userControl := input("[Rock/Paper/Scissors]: "),

            # --- If user input is invalid -> new input is taken ---    
            fightMechanic(user,userPointers, worldMap, boxLayer, enemyHealth, enemyIcon, roundResult) if userControl not in ["Rock","Paper","Scissors"] else None,

            ( # --- Part that runs one fight round ---
                
                # --- Random enemy choice ---
                enemyControl := random.choice(["Rock","Paper","Scissors"]),

                # --- Result of the fight round ---
                roundResult := "Player" if {"Rock":"Scissors","Scissors":"Paper","Paper":"Rock"}[userControl] == enemyControl else "Enemy",

                # --- Part that determines who won the last fight and if any states were hit ---
                user.__setitem__(3, user[3] - 1 if roundResult == "Enemy" else user[3]),
                enemyHealth := enemyHealth - 1 if roundResult == "Player" else enemyHealth,

                ( # --- Game over mechanic ---
                    os.system('cls' if os.name == 'nt' else 'clear'),
                    print("Game Over"),input("Press Enter to exit ..."),
                    os.system('cls' if os.name == 'nt' else 'clear'),exit(),
                ) if user[3] == 0 else None,
                
                ( # --- Message that is displayed at the end of a fight
                    worldMap[9].__setitem__(2, "⬛"), # <- Removing enemy from map
                    print(f"You won the fight!"),
                    input("Press Enter to continue ..."),
                    os.system('cls' if os.name == 'nt' else 'clear'),
                ) if enemyHealth == 0 else fightMechanic(user,userPointers, worldMap, boxLayer, enemyHealth, enemyIcon, roundResult)         
            ),
        ),
    ),

    ( # --- Welcome message ---
        os.system('cls' if os.name == 'nt' else 'clear'),
        print("Welcome to the Sigil! You are a wizard lost in a forest and your goal is to get to the city by completing quests and solving puzzles along the way."),
        print("Use WASD to move around. When you encounter a friendly NPC you can talk with them using Talk."),
        print("The rest is for you to discorver adventurer! Good luck!"),
        input("Press Enter to start ..."),
    ),

    # --- Main Loop ---
    (main := lambda user,userPointers, worldMap, boxLayer:(
        ( # --- Render Script ---
            os.system('cls' if os.name == 'nt' else 'clear'),
            print(
            "\n".join(
                " ".join(
                    "🧙" if [i, j] == [user[0],user[1]] else worldMap[i][j]
                    for j in range(len(worldMap[i]))
                ) for i in range(len(worldMap)))),
            print(f"Health: {user[3]}/{user[4]} ❤️  Inventory: {user[2]}"),
            print(f"Console: {user[5]}")
        ),

        # --- Main user input ---
        characterControl := input("> "),

        ( # --- Player Movement ---
            user.__setitem__(0, user[0] - 1)  if characterControl == "w" and worldMap[user[0] - 1][user[1]] not in ["🌳", "⛄", "🪨"] else # <- Changing Alpha
            user.__setitem__(0, user[0] + 1) if characterControl == "s" and worldMap[user[0] + 1][user[1]] not in  ["🌳", "⛄", "🪨"] else # <- Changing Alpha
            user.__setitem__(1, user[1] + 1) if characterControl == "d" and worldMap[user[0]][user[1] + 1] not in  ["🌳", "⛄", "🪨"] else # <- Changing Beta
            user.__setitem__(1, user[1] - 1) if characterControl == "a" and worldMap[user[0]][user[1] - 1] not in  ["🌳", "⛄", "🪨"] else None, # <- Changing Beta
        ),

        ( # --- Console message ---
            console := 
                # --- Owl Ancient Book Quest -> End ---
                "Thanks for the book adventurer! The path to the healing fountain is now clear. You can drink from it to restore your health using Drink when you are next to it." 
                if worldMap[user[0]][user[1]] == "🦉" and "Ancient Book" in user[2] and characterControl == "Talk" else 
                
                # --- Owl Ancient Book Quest -> Start ---
                "Hello adventurer! I'm the magical owl! Some Snowman stole my Ancient Book. "+ 
                "If you bring it back to me, I will clear the path to the healing fountain in return. You can fight the Snowman using Fight when you are next to him."
                if worldMap[user[0]][user[1]] == "🦉" and "Ancient Book" not in user[2] and characterControl == "Talk" and worldMap[9][2] == "⛄" else


                "Good job defeating the Snowman! He hides the Ancient Book in his box. You can open it by Open while standing on top of it." 
                if worldMap[user[0]][user[1]] == "🦉" and "Ancient Book" not in user[2] and characterControl == "Talk" and worldMap[7][1] == "📦" else
                
                # --- Owl Pickaxe Quest ---
                "To continue further, you will need to mine that rock. Here are some resources you will need to craft a pickaxe. You can do so by Craft Pickaxe."
                if worldMap[user[0]][user[1]] == "🦉" and user[3] == user[4] and worldMap[9][2] == "⬛" and characterControl == "Talk" and "Pickaxe" not in user[userPointers["inventory"]] else


                # --- Default console message ---
                " ... ",
            user.__setitem__(5, console) # <- Setting console message to user list
        ),
        
        ( # --- Quest support logic ---
            ( # --- Owl Ancient Book Quest -> Removing book and unlocking the healing fountain area ---
                worldMap[5].__setitem__(2, "⬛"), # <- Removing cactus from map
                user[2].remove("Ancient Book") # <- Removing book from inventory
            ) if worldMap[user[0]][user[1]] == "🦉" and "Ancient Book" in user[2] and characterControl == "Talk" else 

            ( # --- Owl Pickaxe Quest ---
                user[2].append("Rock"),
                user[2].append("Stick")
            ) if worldMap[user[0]][user[1]] == "🦉" and user[3] == user[4] and worldMap[9][2] == "⬛" and characterControl == "Talk" and "Pickaxe" not in user[userPointers["inventory"]] and "Rock" not in user[userPointers["inventory"]] and worldMap[7][1] != "📦"  and worldMap[5][2] != "🌵" else None
        ),

        ( # --- Opening box feature ---
            worldMap[user[0]].__setitem__(user[1], "⬛"), # <- Removing box from map
            user[2].append(boxLayer[user[0]][user[1]]) # <- Adding box content to inventory
        ) if characterControl == "Open" and worldMap[user[0]][user[1]] == "📦" else None,
        
        ( # --- Healing ---
            user.__setitem__(3, user[4]), # <- Healing player to max health
            user.__setitem__(5, "You have full health again!"), 
        ) if [user[0], user[1]] == [5,1] and characterControl == "Drink" else user[3],

        ( # --- Crafting Mechanic ---
            (
                user[2].remove("Rock"),
                user[2].remove("Stick"),
                user[2].append("Pickaxe"),
                user.__setitem__(5,"You crafted a pickaxe.")

            ) if characterControl == "Craft Pickaxe" and "Rock" in user[2] and "Stick" in user[2] else None
        ),

        # --- Fighting Command ---
        fightMechanic(user,userPointers, worldMap, boxLayer, 1, "⛄", None) if [user[0], user[1]] == [9,3] and characterControl == "Fight" else None, 
        
        ( # --- Exit Mechanic ---
            os.system('cls' if os.name == 'nt' else 'clear'),
            exit()
        ) if characterControl == "Exit" else None,
            
        main(user,userPointers, worldMap, boxLayer),
    ))(user,userPointers,worldMap,boxLayer)
))(__import__("os"),__import__("random")) # TDL: Add mining quest and the feature itself, enemy layer, merge all layers into one list like user