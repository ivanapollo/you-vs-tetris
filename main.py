import game

game_instance = game.Game()

while True:

    if not game_instance.do_cycle():
        break
        # но вообще надо спросить, будем снова играть или нет

    game_instance.draw()
