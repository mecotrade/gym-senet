import numpy as np
import pyglet
from pyglet import gl
import os
from gym_senet.envs.senet import Senet


class AnsiRenderer:

    HOUSE_NAMES = {Senet.HOUSE_OF_REBIRTH: 'RB',
                   Senet.HOUSE_OF_HAPPINESS: 'HA',
                   Senet.HOUSE_OF_WATER: 'WA',
                   Senet.HOUSE_OF_THREE_TRUTHS: '3T',
                   Senet.HOUSE_OF_RE_ATOUM: 'RA'}

    def __init__(self, cone='0', spool='X'):
        self.cone = cone
        self.spool = spool
        self.header = '|'.join(['{:-2d}'.format(h) for h in range(Senet.BOARD_SIZE)])
        self.separator = '+'.join([AnsiRenderer.HOUSE_NAMES.get(h, '--') for h in range(Senet.BOARD_SIZE)])

    def render(self, board):
        cones = np.where(board[0] == 1, self.cone, '')
        spools = np.where(board[1] == 1, self.spool, '')
        pieces = '|'.join([(cones[h] + spools[h]).rjust(2) for h in range(board.shape[1])])

        return '\n'.join([self.header, self.separator, pieces])

    def close(self):
        pass


class BoardRenderer:

    BOARD_W = 890
    BOARD_H = 278
    DANCER_SIZE = 59
    COORDINATES = np.array([[ 21, 196], [109, 196], [196, 196], [284, 196], [371, 196], [459, 196], [543, 196], [634, 196], [721, 196], [809, 196],
                            [809, 109], [721, 109], [634, 109], [543, 109], [459, 109], [371, 109], [284, 109], [196, 109], [109, 109], [ 21, 109],
                            [ 21,  22], [109,  22], [196,  22], [284,  22], [371,  22], [459,  22], [543,  22], [634,  22], [721,  22], [809,  22]], dtype=int)

    def __init__(self, width=None, height=None):

        self.width = width or (BoardRenderer.BOARD_W if height is None else int(height * BoardRenderer.BOARD_W / BoardRenderer.BOARD_H))
        self.height = height or (BoardRenderer.BOARD_H if width is None else int(width * BoardRenderer.BOARD_H / BoardRenderer.BOARD_W))

        self.scale_w = self.width / BoardRenderer.BOARD_W
        self.scale_h = self.height / BoardRenderer.BOARD_H

        self.window = pyglet.window.Window(width=self.width, height=self.height, display=None)
        
        pyglet.resource.path = [os.path.join(os.path.dirname(__file__), 'resources')]
        pyglet.resource.reindex()
        
        board = pyglet.resource.image('board5.png')
        board.width = self.width
        board.height = self.height
        self.board = board

        cone = pyglet.resource.image('cone.png')
        cone.width = BoardRenderer.DANCER_SIZE * self.scale_w
        cone.height = BoardRenderer.DANCER_SIZE * self.scale_h
        self.cone = cone

        spool = pyglet.resource.image('spool.png')
        spool.width = BoardRenderer.DANCER_SIZE * self.scale_w
        spool.height = BoardRenderer.DANCER_SIZE * self.scale_h
        self.spool = spool

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def close(self):
        self.window.close()

    def render(self, board):

        gl.glClearColor(1, 1, 1, 1)

        self.window.switch_to()
        self.window.dispatch_events()
        self.window.clear()

        batch = pyglet.graphics.Batch()
        sprites = [pyglet.sprite.Sprite(img=self.board, batch=batch)]

        for x, y in BoardRenderer.COORDINATES[board[Senet.CONS_PLAYER] == 1]:
            sprites.append(pyglet.sprite.Sprite(img=self.cone, x=x * self.scale_w, y=y * self.scale_h, batch=batch))
        for x, y in BoardRenderer.COORDINATES[board[Senet.SPOOLS_PLAYER] == 1]:
            sprites.append(pyglet.sprite.Sprite(img=self.spool, x=x * self.scale_w, y=y * self.scale_h, batch=batch))

        gl.glViewport(0, 0, self.window.width, self.window.height)
        batch.draw()

        self.window.flip()


        