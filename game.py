from hand import *
from settings import *
from player import *
import time

class Game:
    def __init__(self):
        self.players = []
        self.discarded_tiles = {}
        self.tiles = tiles
        self.round = 0
        
    def add_player(self, name, cpu=False, hidden_tiles=True):
        player = Player(name, cpu, hidden_tiles)
        self.players.append(player)
        
    def deal_all(self):
        for player in self.players:
            hand = sort(tiles[:13])
            for tile in hand:
                self.tiles.remove(tile)
            player.hand = hand

    def draw_tile(self, player):
        new_tile = tiles[0]
        player.hand.append(new_tile)
        self.tiles.remove(new_tile)
        player.drawn_tile = new_tile

        self.update_info(player)
    
    def discard_tile(self, player, tile):
        if tile in player.hand:
            player.hand.remove(tile)

        index = self.players.index(player)
        if index in self.discarded_tiles:
            self.discarded_tiles[index].append(tile)
        else:
            self.discarded_tiles[index] = [tile]
            
        return tile


    def update_info(self, player):
        turn = big_font.render((player.name + "'s turn"), 1, (255,255,255))
        tile_count = big_font.render((str(len(self.tiles)) + " tiles remaining"), 1, (255,255,255)) 
        turn_x = get_center(turn, info_rect)[0]
        tile_count_x = get_center(tile_count, info_rect)[0]
        pygame.draw.rect(screen, (0,0,0), info_rect, border_radius=5)
        screen.blit(turn, (turn_x, 180))
        screen.blit(tile_count, (tile_count_x, 250))
        pygame.display.update(info_rect)

    def initialize(self):
        for player in self.players:
            self.update_hand(player)

        for i in range(0,4):
            p = self.players[i].name
            nameplate = small_font.render(p, 1, (255,255,255))
            x, y, w, h = pile_rects[i]
            y -= 25
            
            screen.blit(nameplate, (x,y))

        pygame.draw.rect(screen, (180, 180, 180), pon_rect, border_radius=5)
        pygame.draw.rect(screen, (180, 180, 180), chii_rect, border_radius=5)
        pygame.draw.rect(screen, (180, 180, 180), ron_rect, border_radius=5)

        pon_text = big_font.render("Pon", 1, (255,255,255))
        chii_text = big_font.render("Chii", 1, (255,255,255))
        ron_text = big_font.render("Ron", 1, (255,255,255))
        texts = [pon_text, chii_text, ron_text]
        
        for i in range(0,3):
            x, y = get_center(texts[i], call_rects[i])
            screen.blit(texts[i], (x, y))

        self.update_info(self.players[0])

        pygame.display.flip()


    def update_hand(self, player):
        player_index = self.players.index(player)
        rect = hand_rects[player_index]

        pygame.draw.rect(screen, bgcolor, rect)
        self.display_hand(player, player.drawn_tile)

        pygame.display.update(rect)


    def update_pile(self, player):
        player_index = self.players.index(player)
        rect = pile_rects[player_index]


        dy = 100 + 175 * player_index + 30
        j = 0
                

        pygame.draw.rect(screen, bgcolor, rect)

        for tile in self.discarded_tiles[player_index]:
            if j >= 16:
                dy += 70
                j = 0

            img = compose(tile, 0.07)
            screen.blit(img, (100+j*50, dy))
            j += 1
        pygame.display.update(rect)

    def display_hand(self, player, target):
        id = self.players.index(player)
        x,y = quadrant[id]
        d = 0
        if target != None:
            target = len(player.hand)

        for tile in player.hand:
            if player.hidden_tiles == False:
                img = compose(tile, img_multiplier)
            else:
                img = back

            d += 1

            if id == 0:
                if d == target:
                    screen.blit(img, ((x + (d*60)+30) ,y))
                else: 
                    screen.blit(img, ((x + d*60) ,y))
            elif id == 1:
                img = pygame.transform.rotate(img, 90)
                if d == target:
                    screen.blit(img, (x , (y + (d*60)+30)))
                else: 
                    screen.blit(img, (x ,y + d*60))
            elif id == 2:
                if d == target:
                    screen.blit(img, ((x - (d*60)-30) ,y))
                else: 
                    screen.blit(img, ((x - d*60) ,y))
            elif id == 3:
                img = pygame.transform.rotate(img, 90)
                if d == target:
                    screen.blit(img, (x , (y - (d*60)-30)))
                else: 
                    screen.blit(img, (x , y - d*60))
    
    def get_full_hand(self, player):
        full_hand = []
        
        for tile in player.hand:
            full_hand.append(tile)
        for meld in player.meld:
            for tile in meld:
                full_hand.append(tile)


        full_hand = sort(full_hand)

        return full_hand


    def calculate_shanten(self, player):
        full_hand = self.get_full_hand(player)


        m, p, s, z = convert_notation(full_hand)
        pattern = TilesConverter.string_to_34_array(man=m, pin=p, sou=s, honors=z)
        result = shanten.calculate_shanten(pattern)
        return result



    def call_check(self, discarder, discarded_tile):
        call_type = 0
        callers = {}
        for player in self.players:
            if discarder != player:
                pon, chii = pon_chii(player.hand) #get tiles that are required to fulfill a pon / chii
                
                if discarded_tile in pon:

                    if player in callers:
                        callers[player].append("pon")
                    else:    
                        callers[player] = ["pon"]
                if self.players.index(discarder) == self.players.index(player) + 1:
                    if discarded_tile in chii:
                        if player in callers:
                            callers[player].append("chii")
                        else:    
                            callers[player] = ["chii"]

        if len(callers) != 0:
            for caller in callers:
                print(caller.name + " can " + str(callers[caller]) + " " + discarder.name)

            if self.players[0] in callers:
                print(discarder, discarded_tile, self.players[0], callers[self.players[0]])
                self.call(discarder, discarded_tile, self.players[0], callers[self.players[0]])        
        



    def call(self, victim, target, caller, action):
        model = copy.deepcopy(caller)
        model.hand.append(target)
        

        """
        if self.calculate_shanten(caller) == 0:
            action.append("ron")
        """

        if self.win_check(model) == True:
            action.append("ron")
        for type in action:
            self.update_button(True, type)


        choice = 0

        while choice == 0:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for type in action:
                        if call_rects[types.index(type)].collidepoint(pygame.mouse.get_pos()):
                            print('clicked ' + str(type))
                            choice = type

                    if choice == 0:
                        self.update_button()
                        return
                        
                    
        print("choice" + str(choice))

        if choice == "ron":
            caller.hand.append(target)
            caller.ron_tile = target

        else:
            if choice == "pon":
                tiles_to_remove = [target, target]

            elif choice == "chii":
                target_value = int(target[0])
                target_suit = target[1]
                h = [x[0] for x in caller.hand if x[1] == target_suit and x != target]

                h = ''.join(h)

                print(h)

                if str(target_value-2) + str(target_value-1)  in h:
                    tiles_to_remove = [(str(target_value-2) + target_suit), (str(target_value-1) + target_suit)]

                if str(target_value-1)  + str(target_value+1)  in h:
                    tiles_to_remove = [(str(target_value-1) + target_suit), (str(target_value+1) + target_suit)]

                if str(target_value+1)  + str(target_value+2)  in h:
                    tiles_to_remove = [(str(target_value+1) + target_suit), (str(target_value+2) + target_suit)]


                print(tiles_to_remove)

            try:
                for tile in tiles_to_remove:
                    caller.hand.remove(tile)
            except:
                print("error removing tiles")
                return
            
            meld = [tiles_to_remove[0], tiles_to_remove[1], target]
            meld = sort(meld)

            caller.meld.append(meld)
            self.display_meld(caller)


        #remove tile from victim's discarded pile
        victim_index = self.players.index(victim)
        self.discarded_tiles[victim_index] = self.discarded_tiles[victim_index][:-1]

        caller.hand = sort(caller.hand)

        self.update_pile(victim)
        self.update_hand(victim)
        self.update_hand(caller)


        self.update_button()
        

        print("user has declared " + choice + " on " + target + " from " + victim.name)
        caller.called = True
        print("0user hand" + str(caller.hand))

        

    def update_button(self, status=False, type=None):
        if status:
            pygame.draw.rect(screen, action_colours[types.index(type)], call_rects[types.index(type)], border_radius=5)
            text = big_font.render(type.capitalize(), 1, (255,255,255))
            screen.blit(text, get_center(text, call_rects[types.index(type)]))
            pygame.display.update(call_rects[types.index(type)])
        else:
            for type in types:
                pygame.draw.rect(screen, (180, 180, 180), call_rects[types.index(type)], border_radius=5)
                text = big_font.render(type.capitalize(), 1, (255,255,255))
                screen.blit(text, get_center(text, call_rects[types.index(type)]))
                pygame.display.update(call_rects[types.index(type)])

    def determine_current_player(self, previous):
        for player in self.players:
            if player.called == True:
                return player

        prev_index = self.players.index(previous)
        if prev_index == 3:
            return self.players[0]
        else:
            return self.players[prev_index + 1]
        


    #not used
    def player_action(self, player):
        print(player.name)
        if player.called == False:
            self.draw_tile(player)
            print("will draw")


        if player.cpu == True:
            #random_discard = random.choice(player.hand)
            #self.discard_tile(random_discard)
            selected_tile = random.choice(player.hand)
        else:  
            selected_tile = self.user_discard_loop(player)

        self.discard_tile(player, selected_tile)

        player.discarded = True
        player.hand = sort(player.hand)

    #not used
    def user_discard_loop(self, player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                posx, posy = pygame.mouse.get_pos()
                print(posx, posy)
                pos = tile_pos(posx, posy)
                if pos != None:
                    selected_tile = player.hand[pos-1]

        return selected_tile
    

    def win_check(self, player):
        full_hand = self.get_full_hand(player)

        #print("FULL HAND" + str(full_hand))


        m, p, s, z = convert_notation(full_hand)
        pattern = TilesConverter.string_to_34_array(man=m, pin=p, sou=s, honors=z)
        is_winning_hand = agari.is_agari(pattern)
        print(is_winning_hand)
        return is_winning_hand


    def calculate_score(self, player):
        full_hand = self.get_full_hand(player)

        if player.ron_tile != None:
            win_tile = player.ron_tile
        else:
            win_tile = player.drawn_tile

        print("FULL HAND" + str(full_hand))
        print("WIN TILE" + str(win_tile))
        score = calculate_yaku(full_hand, win_tile)

        return score

    def win_screen(self, player):
        player_statement = big_font.render((player.name + " wins!"), 1, (255,255,255))

        score = self.calculate_score(player)
        points, yaku = score
        print(points)
        print(yaku)

        score_text = (str(points) + ", " + str(yaku))

        score_statement = small_font.render((score_text), 1, (255,255,255))

        pygame.draw.rect(screen, (25, 59, 138), win_rect, border_radius=5)

        x,y = get_center(player_statement, win_rect)
        screen.blit(player_statement, (x,y-20))

        x,y = get_center(score_statement, win_rect)
        screen.blit(score_statement, (x,y+15))


        pygame.display.update(win_rect)

        time.sleep(5)

    def display_meld(self, player):
        pygame.draw.rect(screen, (bgcolor), meld_rect, border_radius=5)
        y = 0
        for meld in player.meld:
            x = 0
            y += 1
            for tile in meld:
                img = compose(tile, 0.05)
                screen.blit(img, (1065 + x*35, 750 + y*40))
                x += 1
        pygame.display.flip()   