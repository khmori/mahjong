# 136 tiles (34kinds*4)
# pin 1-9
# so 1-9
# man 1-9
# ton, nan, sha, pei (east, south, west, north)
# haku, hatsu, chun

#3 of same, or three in ascending
from settings import *


pool = []

def initialize():
    return tiles

def sort(hai):
    sorted_tiles = [x[::-1] for x in (sorted([pai[::-1] for pai in hai]))]
    return sorted_tiles

def deal(tiles):
    random.shuffle(tiles) # randomize the order of the tiles
    remaining_tiles = tiles
    haipai = sort(tiles[:13])
    for tile in haipai:
        remaining_tiles.remove(tile)
    return haipai, remaining_tiles

def deal_all(tiles):
    remaining_tiles = tiles
    p0, remaining_tiles = deal(remaining_tiles)
    p1, remaining_tiles = deal(remaining_tiles)
    p2, remaining_tiles = deal(remaining_tiles)
    p3, remaining_tiles = deal(remaining_tiles)

    return p0, p1, p2, p3, remaining_tiles
    

def compose(tile, size):
    img = pygame.image.load('faces/' + faces[tile] + '.png').convert_alpha()
    w = img.get_width()
    h = img.get_height()
    img = pygame.transform.scale(img, (w*size, h*size))
    return img


def display(hand, id, target):
    x,y = quadrant[id]
    d = 0
    if target != None:
        target = len(hand)

    if id == 0:
        for tile in hand:
            d += 1 
            img = compose(tile, img_multiplier)
            if d == target:
                screen.blit(img, ((x + (d*60)+30) ,y))
            else: 
                screen.blit(img, ((x + d*60) ,y))
    elif id == 1:
        img = pygame.transform.rotate(back, 90)
        for tile in hand:
            d += 1 
            if d == target:
                screen.blit(img, (x , (y + (d*60)+30)))
            else: 
                screen.blit(img, (x ,y + d*60))
    elif id == 2:
        img = back
        for tile in hand:
            d += 1
            if d == target:
                screen.blit(img, ((x - (d*60)-30) ,y))
            else: 
                screen.blit(img, ((x - d*60) ,y))
    elif id ==3:
        img = pygame.transform.rotate(back, 90)
        for tile in hand:
            d += 1 
            if d == target:
                screen.blit(img, (x , (y - (d*60)-30)))
            else: 
                screen.blit(img, (x , y - d*60))



def display_discarded_tiles(discarded_tiles):
    d = 0
    dx = sute_x
    dy = sute_y
    for tile in discarded_tiles:
        if d!=0 and d % 21 == 0:
            d = 0
            dy += 80
        d += 1
        img = compose(tile, 0.07)
        screen.blit(img, ((dx + d*50), dy))
        w = img.get_width()
        h = img.get_height()
        
def display_menu(score, tilecount):
    pygame.draw.rect(screen, (14, 20, 28), pygame.Rect(510, 345, 260, 250), 0, 5)
            
def tile_pos(x, y, hand):
    if 836 <= y <= 908: 
        #check tiles in hand
        tiles_in_hand = len(hand)
        print(tiles_in_hand)
        if 160 <= x <= (160 + ((tiles_in_hand-2) * 60) + 54):
            region = math.floor((x-160)/60)
            if x <= 160 + (region*60)+ 54: #if x in the space where tile is in that region (check if x less than the farthest, to right side, x coord of tile)
                return region+1
        #check if clicked drawn tile
        #if 970 <= x <= 1024: // if greater than (start of last hand tile + 90)(which would be 880+90) and less than that plus 54
        print("REGION")
        floor = (160 + ((tiles_in_hand-2) * 60) + 90)
        ceiling = ((160 + ((tiles_in_hand-2) * 60) + 90)+54)
        print(floor, x, ceiling)
        print( floor <= x <= ceiling )
        print(x )
        if (160 + ((tiles_in_hand-2) * 60) + 90) <= x <= (160 + ((tiles_in_hand-2) * 60) + 90)+54:
            print("DNASJDBNASJKDLA")
            return tiles_in_hand

    
def giri(tile, hand):
    new_hand = hand
    if tile not in hand:
        print('tile not in hand')
    else:
        new_hand.remove(tile)
        #place it in the middle ?
    return sort(new_hand)

def draw(hand):
    #give new hand but dont sort
    remaining_tiles = tiles
    new_tile = random.choice(remaining_tiles)
    hand.append(new_tile)
    remaining_tiles.remove(new_tile)

    return hand, remaining_tiles, new_tile


def yakuRAW(hand): 
    h = hand

    pattern_dict = {}
    pattern = []
    index = 1
    sum = 0

    print(hand)

    for tile in h:
        if tile not in pattern_dict:
            pattern_dict[tile] = index
            index += 1
        pattern.append(pattern_dict[tile])
        sum += pattern_dict[tile]

    
    print('pattern ' + str(pattern))
    print('sum '+ str(sum)) 

    if sum%3 == 0:
        possible_pairs = {3,6,9}
    elif sum%3 == 1:
        possible_pairs = {2,5,8}
    elif sum%3 == 2:
        possible_pairs = {1,4,7}


    print('possible pairs ' + str(possible_pairs))
    
    for pair in possible_pairs:
        if pattern.count(pair) == 2:
            pattern.remove(pair)
            pattern.remove(pair)
            print('pair spotted/removed ' + str(pattern))
            for x in range(len(pattern)+1):
                if pattern.count(x) >= 3:
                    pattern.remove(x)
                    pattern.remove(x)
                    pattern.remove(x)
                    print('set spotted/removed ' + str(pattern))
                elif (x-1) in pattern and (x+1) in pattern:
                    pattern.remove(x-1)
                    pattern.remove(x)
                    pattern.remove(x+1)
                    print('street spotted/removed ' + str(pattern))
    

    if len(pattern) == 0:
        return True
    else:
        return False
    

#returns what tile you need to fulfill a pon/chii
def pon_chii(hand):
    pon = set([x for x in hand if hand.count(x) > 1])
    chii = []

    consecutive = '123456789'


    h = [x for x in hand if x[1] != 'x' and x[1] != 'z']
    h = [pai[::-1] for pai in h]
    
    for n in range(0, len(h)-1):
        #check if same suit first
        if h[n][0] == h[n+1][0]:
            #check if the values are consecutive (h[n][1] + h[n+1][1] would be a string, ex. 3+4 = 34)
            if h[n][1] + h[n+1][1] in consecutive:
                #print(h[n], h[n+1])

                #always start with the lower one
                #the lower one CANNOT be 9 
                #if it is 8, the only possible is 7
                #if it is 1, the only possible is 3

                #return the numbers around them in consecutive 

                if h[n][1] == '8':
                    chii.append(h[n][0] + '7')
                elif h[n][1] == '1':
                    chii.append(h[n][0] + '3')
                else:
                   chii.append(h[n][0] + consecutive[int(h[n][1])-2])
                   chii.append(h[n][0] + consecutive[int(h[n][1])+1])

    return pon, [tile[::-1] for tile in chii]



def convert_notation(hand):
    m = ''.join(sorted(tile[0] for tile in ([tile for tile in hand if tile.endswith('m')])))
    p = ''.join(sorted(tile[0] for tile in ([tile for tile in hand if tile.endswith('p')])))
    s = ''.join(sorted(tile[0] for tile in ([tile for tile in hand if tile.endswith('s')])))
    z = ''.join(sorted((tenhou[tile])[0] for tile in ([tile for tile in hand if tile.endswith('x') or tile.endswith('z')])))

    return m, p, s, z

    #winning_suit = 

def is_winning(hand):
    m, p, s, z = convert_notation(hand)
    pattern = TilesConverter.string_to_34_array(man=m, pin=p, sou=s, honors=z)
    is_winning_hand = agari.is_agari(pattern)
    return is_winning_hand

def calculate_yaku(hand, win_tile):
    m, p, s, z = convert_notation(hand)

    win_tile_suit = suits[win_tile[1]]
    win_tile_value = win_tile[0]

    print(win_tile_suit, win_tile_value)
    
    pattern = TilesConverter.string_to_136_array(man=m, pin=p, sou=s, honors=z)
    win_tile = TilesConverter.string_to_136_array(**{win_tile_suit: win_tile_value})[0]
    result = calculator.estimate_hand_value(pattern, win_tile, config=HandConfig(is_tsumo=True))

    return result.cost['main'], result.yaku

def tiles_from_tenpai(hand):
    m, p, s, z = convert_notation(hand)
    pattern = TilesConverter.string_to_34_array(man=m, pin=p, sou=s, honors=z)
    result = shanten.calculate_shanten(pattern)
    return result
