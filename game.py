import pyxel


SCREEN_WIDTH=160
SCREEN_HEIGHT=120
STONE_INTERVAL=10
GAME_OVER_DISPLAY_TIME=90
START_SCENE= "start"
PLAY_SCENE= "play"

class Stone:
    def __init__(self, x, y):
        self.x= x
        self.y= y
        
    def update(self):
        self.y += 3
        
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)
    
class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="ピクセル練習用ゲーム")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        pyxel.playm(0, loop=True)
        self.current_scene = START_SCENE
        pyxel.run(self.update, self.draw)
        
    def reset_play_scene(self):
        self.player_x = SCREEN_WIDTH//2
        self.player_y = SCREEN_HEIGHT * 4//5
        self.stones = []
        self.is_collision = False
        self.game_clear = False
        self.game_over_display_timer = GAME_OVER_DISPLAY_TIME
        
        
    def update_start_scene(self):
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE


    def update_play_scene(self):
        #GAMEOVERの時
        if self.is_collision:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
                self.current_scene = START_SCENE
            return 
        
        # 自分の移動
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) and self.player_x > -4:
            self.player_x -= 1
        elif pyxel.btn(pyxel.GAMEPAD_BUTTON_DPAD_RIGHT) and self.player_x < SCREEN_WIDTH - 13:
            self.player_x += 1
            
        # 石の追加をする
        if pyxel.frame_count % STONE_INTERVAL == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH-8),0)) 
        
        # 石の落下移動S
        for stone in self.stones:
            stone.update()
            
            if len(self.stones)>189:
                self.game_clear = True
                self.is_collision = False
        
            # 衝突したとき
            elif len(self.stones)<190 and (self.player_x-3 <= stone.x <= self.player_x+13 and
                self.player_y-6 <= stone.y <= self.player_y+14):
                self.is_collision = True
                
            
            
    
    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_CYAN)
        # 石
        for stone in self.stones:
            stone.draw()
        
        # 自分
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)
        
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT//2, "GAME OVER", 
                       pyxel.COLOR_YELLOW)
        if self.game_clear:
            pyxel.text(SCREEN_WIDTH//2 -20, SCREEN_HEIGHT//2, "GAME COMPLETE!!", 
                       pyxel.COLOR_YELLOW)
        
        
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
            
        if self.current_scene == START_SCENE:
            self.update_start_scene()
            
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()    
            
    def draw_start_scene(self):
        pyxel.blt(0, 0, 0, 32, 0, 160, 120)
        pyxel.text(SCREEN_WIDTH//2-8, SCREEN_HEIGHT//2, "Click to Start!!",
                   pyxel.COLOR_PINK)

    def draw(self):
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()

App()