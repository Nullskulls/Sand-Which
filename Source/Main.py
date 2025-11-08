import Helpers

def main():
    game_state = Helpers.menu()
    while True:
        game_state.play_day()
        input("Day over... press enter to continue...")
        game_state.Data["Total_Shifts"] += 1
        game_state.save()
if __name__ == '__main__':
    main()