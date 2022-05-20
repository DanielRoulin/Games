import sys
from update import check_update
import os
import subprocess

root_path = os.path.dirname(os.path.realpath(__file__))
games_path = os.path.join(root_path, "games")

if __name__ == "__main__":
    check_update()

    games = [path for path in os.listdir(games_path)]
    while True:
        print("What game do you want to play?")
        for i, name in enumerate(games):
            print(f"{i + 1}. {name}")

        text = input("Your choice: ")
        try:
            choice = int(text)
        except:
            print("Your choice should be a number")
            continue
        
        if choice < 1 or choice > len(games):
            print(f"Your choice should be between 1 and {len(games)}")
            continue
        break

    game = games[choice - 1]
    print("Starting game: " + game)

    subprocess.call("python3 " + os.path.join(games_path, game, game + ".py"), shell = True)