# Memory V2
# The second version contains the complete tile grid and the black panel on the right, there is score in the black panel. All 8 pairs of two tiles are covered by question mark when the game starts . Each time the game is played, the tiles spawn in random locations in the grid. Player can click tiles to reveal images. Game ends upon clicking close screen or all 16 tiles being exposed. Game occurs on a 4x4 grid.
import pygame,random

# User-defined functions
def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory v1')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   
   # start the main game loop by calling the play method on the game
#object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 
# User-defined classes
class Game:
   # An object in this class represents a complete game.
   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object
      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      Tile.set_surface(self.surface) 
      # tell grid to be size 4 meaning 4x4 or 16 squares total
      grid_size = 4
      self.create_grid(grid_size)
      self.score=0
   def draw_score(self):
         # this method draws the player's score in the top-right corner of the
         # game window.
         #  - self : the game the score is being drawn for
      font_color = pygame.Color("white")
      font_bg    = pygame.Color("black")
      font       = pygame.font.SysFont("arial", 32)
      text_img   = font.render(str(self.score), True, font_color, font_bg)     
      text_pos   = (460,0)
      self.surface.blit(text_img, text_pos)   
   def create_grid(self, grid_size):
      # Creates a grid of tiles that is grid_size x grid_size in size.

      self.grid = [ ]
      
      # Create list of image names to be used on the squares (we just append image(1-9) and the file type bmp
      # Then we create image surfaces of each image name and add image surfaces to itself which provides us with two of each image
      img_names = ['image' + str(i) + '.bmp' for i in range(1,9)]
      image_surfaces = [pygame.image.load(name) for name in img_names]
      image_surfaces = image_surfaces + image_surfaces
      random.shuffle(image_surfaces)      
      # this for loop creates each row in our grid     
      for row_num in range(grid_size):
         new_row = self.create_row(row_num, grid_size,image_surfaces)
         self.grid.append(new_row)
   def create_row(self, row_num, size,images):
      # Create one row in a grid. Each row contains size Tiles
      # required for calculating the tile's x,y coordinates on screen
      #  -  row_num: the nth row of the grid being created
      #  -   size  : the number of tiles in the row 
      # returns the newly created row'
      tile_height = self.surface.get_height() // size
      # 3/4 to leave space for black column on side
      tile_width = 3/4*self.surface.get_width() // size
      new_row = [ ]
      for col_num in range(size):
         # number of row x tile height produces y position 
         # number of col x tile_width produces x position
         # + 10 so it fits
        
         pos = (row_num*tile_height+10,col_num*tile_width+10)
         # assigns one of the images to each tile by pairing it with a unique coordinate
         #content = images[row_num*size+col_num]
         one_tile = Tile(pos, tile_width, tile_height)
         #cover=pygame.image.load('image0.bmp')
         
         content=images[row_num*size+col_num]
         
         
         one_tile.set_content(content)
         new_row.append(one_tile)
      return new_row
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.
      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()
         self.end_game()
         
         if self.continue_game:
            #self.update()
            
            self.update()
            self.decide_continue()
            #self.update()
            #self.end_game()
        
         self.game_Clock.tick(self.FPS) # run at most with FPS listed

   def handle_events(self):
      # Handle each user event by changing the game state

      # - self is the Game whose events will be handled
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)
   def handle_mouse_click(self, event):
      
         # responds to one mouse click on screen; that means flipping the
         # tile
         #print("Screen was clicked at " + str(event.pos))
      flip_over=False
         
      for row in self.grid:
         for tile in row:
            tiles_selected=[]
            
            
            if tile.select(event.pos)==True:
               tiles_selected.append(tile)
               if len(tiles_selected)==2:
                  if tiles_selected[0].content!=tiles.selected[1].content:
                     
                     tile.put_cover_on()
                     tiles_selected=[]
                  if tiles_selected[0].content==tiles_selected[1].content:
                     tiles_selected=[]
                     
                  
                  
               
               
            
               
               
               
      # responds to one mouse click on screen; that means flipping the
      # tile
      #print("Screen was clicked at " + str(event.pos))
      pass
   def draw(self):
      
      # Draw all game objects.
      # - self is the Game to draw
      self.surface.fill(self.bg_color) # clear the display surface
      # draws the grid
      for row in self.grid:
         for tile in row:
            tile.draw()
      self.draw_score()
      pygame.display.update() # updates the display
   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      self.score= pygame.time.get_ticks()//1000
      
      #return self.score
      pass
   def decide_continue(self):
      filled_tiles = [ ]
      
      for row in self.grid:
         for tile in row:
            if tile.tile_content()==True:
               filled_tiles.append(tile)
      #print(len(filled_tiles))         
      if len(filled_tiles) == 16:
         
         return False
      else:
         return True      
   def end_game(self):
      #print(self.decide_continue())
      if self.decide_continue()==False:
         self.continue_game=False
      return self.continue_game
         
      # Check and remember if the game should continue
      # - self is the Game to check    
      
class Tile:
   # A tile represents one location on a grid. Tiles hold content
   # (in this case, an X or an O).
   # class attributes that are common to all tiles
   # setting surface to none isnt exactly necessary, however we set class wide attributes here before putting it in a method
   surface = None
   content=pygame.image.load('image0.bmp')
   fg_color = pygame.Color("white")
   bg_color = pygame.Color("black")
   cover=pygame.image.load('image0.bmp')
   # set border width for each tile in grid
   
   border_width = 5
   @classmethod
   def set_surface(cls, surface):
      # sets the class attribute, surface
      cls.surface = surface   
   def __init__(self, screen_position, width, height):
      # initialize one instance of our Tile class. Tiles represent
      # one 'position' in our tic-tac-toe board.
      #  - self: the tile being initialized
      #  - screen_position: the [x, y] coordinates to draw the tile at
      #  - width: the width of the tile
      #  - height: the height of the tile
      self.screen_position = screen_position
      #self.cover=cover
      
      # create a rectangle defining our boundaries
      x, y = screen_position
      self.rect = pygame.Rect(x, y, width, height)
      self.selected=False
      #self.image=image
      #self.cover=cover
   def draw_content(self):
      # create an rect object of image so we can blit images to surface of grid tiles
      image_rect=self.content.get_rect(center=self.rect.center)
      Tile.surface.blit(self.content,image_rect)
   def draw_cover(self):
      cover_rect=self.cover.get_rect(center=self.rect.center)
      Tile.surface.blit(self.cover,cover_rect)
      

      
      
      
   def draw(self):
      # draw the contents of a tile to its surface.
      #  - self: the tile being drawn
      
      self.draw_cover()
      if self.selected==True:
         self.draw_content()
      pygame.draw.rect(Tile.surface, Tile.bg_color, self.rect,
Tile.border_width) 
   def set_content(self, new_content):
      # change our tile content. 
      
      #if self.selected==True:
    
      self.content = new_content
   def select(self,pos):
      
      if self.rect.collidepoint(pos):
         
         self.selected = True
   def put_cover_on(self):
      self.selected=False
   def tile_content(self):
      if self.selected==True:
         return True
         
              
         

         
main()