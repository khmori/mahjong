from game import *

game = Game()
game.add_player('user', hidden_tiles = False)
game.add_player('cpu0', cpu=True, hidden_tiles=True)
game.add_player('cpu1', cpu=True, hidden_tiles=True)
game.add_player('cpu2', cpu=True, hidden_tiles=True)
game.deal_all()

user = game.players[0]

running = True
selected_tile = None

current_player = game.players[3]
    
game.initialize()
#test hand (shanten 1)
#user.hand = ['1m', '1m', '1m', '3m', '3m', '3m', '4p', '4p', '5s', '6s', '7s', '2m', '2m']
time.sleep(1)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    if not tiles:
        break

    previous_player = current_player
    current_player = game.determine_current_player(previous_player)
    game.update_info(current_player)

    print("current player: " + str(current_player.name))
    print("current player hand: " + str(len(current_player.hand)))

    if current_player.cpu == False:
        if current_player.called == False:
            #if they called, dont draw
                game.draw_tile(current_player)
                print('user has drawn: ' + str(current_player.drawn_tile))
                #game.update()
                game.update_hand(current_player)

        if game.win_check(current_player) == True:
            game.win_screen(current_player)
            break


        while selected_tile == None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    posx, posy = pygame.mouse.get_pos()
                    print(posx, posy)
                    pos = tile_pos(posx, posy, current_player.hand)
                    if pos != None:
                        selected_tile = current_player.hand[pos-1]


        print("user has " + "discarded: " + str(selected_tile))
        game.discard_tile(current_player, selected_tile)

        current_player.drawn_tile = None

        current_player.hand = sort(current_player.hand)

        game.update_hand(current_player)
        game.update_pile(current_player)
        game.call_check(current_player, selected_tile)
        selected_tile = None
        user.called = False
    
    else:
        if current_player.called == False:
            game.draw_tile(current_player)
            print(current_player.name + " has drawn: " + current_player.hand[-1])
        
        game.update_hand(current_player)
        
        if game.win_check(current_player) == True:
            running = False

        selected_tile = random.choice(current_player.hand)
        time.sleep(cpu_delay)
        print(current_player.name +  " has discarded: " + str(selected_tile))
        

        game.discard_tile(current_player, selected_tile)

        #testing pon/chii for user

        #selected_tile = "5s"
        #game.discard_tile(current_player, selected_tile)

        """
        pon, chii = pon_chii(game.players[0].hand)
        if list(pon) != []:
            selected_tile = random.choice(list(pon))
        #if list(chii) != []:
        #    selected_tile = random.choice(list(chii))
        else:
            selected_tile = random.choice(current_player.hand)

        game.discard_tile(current_player, selected_tile)
        """

        current_player.drawn_tile = None

        current_player.discarded = True
        current_player.hand = sort(current_player.hand)
        game.update_hand(current_player)
        game.update_pile(current_player)
        game.call_check(current_player, selected_tile)
        selected_tile = None
        time.sleep(cpu_delay)
        
    print("")

    clock.tick(FPS)  