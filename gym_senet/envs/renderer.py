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
                   Senet.HOUSE_OF_ISIS_AND_NEPHTHYS: 'IN',
                   Senet.HOUSE_OF_RA_HORAKHTY: 'RA'}

    def __init__(self, cone='0', spool='1', mandatory='*'):
        self.cone = cone
        self.spool = spool
        self.mandatory = mandatory
        self.header = '|'.join(['{:-2d}'.format(h) for h in range(Senet.BOARD_SIZE)])
        self.separator = '+'.join([AnsiRenderer.HOUSE_NAMES.get(h, '--') for h in range(Senet.BOARD_SIZE)])

    def render(self, board):
        cones = np.where(board[0] != 0, self.cone, '')
        spools = np.where(board[1] != 0, self.spool, '')
        mandatory = np.where(np.logical_or(board[0] == -1, board[1] == -1), self.mandatory, '')
        pieces = '|'.join([(mandatory[h] + cones[h] + spools[h]).rjust(2) for h in range(board.shape[1])])

        return '\n'.join([self.header, self.separator, pieces])

    def close(self):
        pass


class RgbRenderer:

    BOARD_W = 890
    BOARD_H = 278
    DANCER_SIZE = 59
    COORDINATES = np.array([[ 21, 196], [109, 196], [196, 196], [284, 196], [371, 196], [459, 196], [543, 196], [634, 196], [721, 196], [809, 196],
                            [809, 109], [721, 109], [634, 109], [543, 109], [459, 109], [371, 109], [284, 109], [196, 109], [109, 109], [ 21, 109],
                            [ 21,  22], [109,  22], [196,  22], [284,  22], [371,  22], [459,  22], [543,  22], [634,  22], [721,  22], [809,  22]], dtype=int)

    def __init__(self, width=None, height=None):

        self.width = width or (RgbRenderer.BOARD_W if height is None else int(height * RgbRenderer.BOARD_W / RgbRenderer.BOARD_H))
        self.height = height or (RgbRenderer.BOARD_H if width is None else int(width * RgbRenderer.BOARD_H / RgbRenderer.BOARD_W))

        self.window = pyglet.window.Window(width=self.width, height=self.height, display=None, visible=False)

        self.scale_w = self.width / RgbRenderer.BOARD_W
        self.scale_h = self.height / RgbRenderer.BOARD_H

        pyglet.resource.path = [os.path.join(os.path.dirname(__file__), 'resources')]
        pyglet.resource.reindex()
        
        board = pyglet.resource.image('board6.png')
        board.width = self.width
        board.height = self.height
        self.board = board

        cone = pyglet.resource.image('cone.png')
        cone.width = RgbRenderer.DANCER_SIZE * self.scale_w
        cone.height = RgbRenderer.DANCER_SIZE * self.scale_h
        self.cone = cone

        spool = pyglet.resource.image('spool.png')
        spool.width = RgbRenderer.DANCER_SIZE * self.scale_w
        spool.height = RgbRenderer.DANCER_SIZE * self.scale_h
        self.spool = spool

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def render(self, board):

        gl.glClearColor(1, 1, 1, 1)

        batch = pyglet.graphics.Batch()
        sprites = [pyglet.sprite.Sprite(img=self.board, batch=batch)]

        for x, y in RgbRenderer.COORDINATES[board[Senet.CONS_PLAYER] != 0]:
            sprites.append(pyglet.sprite.Sprite(img=self.cone, x=x * self.scale_w, y=y * self.scale_h, batch=batch))
        for x, y in RgbRenderer.COORDINATES[board[Senet.SPOOLS_PLAYER] != 0]:
            sprites.append(pyglet.sprite.Sprite(img=self.spool, x=x * self.scale_w, y=y * self.scale_h, batch=batch))

        gl.glViewport(0, 0, self.width, self.height)
        batch.draw()

        image_data = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
        rgb = np.fromstring(image_data.get_data(), dtype=np.uint8, sep='').reshape([self.height, self.width, 4])

        return rgb[::-1, :, 0:3]

    def close(self):
        self.window.close()


class HumanRenderer(RgbRenderer):

    def __init__(self, width=None, height=None):

        super(HumanRenderer, self).__init__(width, height)

        self.window.set_visible(True)

    def render(self, board):

        self.window.switch_to()
        self.window.dispatch_events()
        self.window.clear()

        rgb = super(HumanRenderer, self).render(board)

        self.window.dispatch_event('on_draw')
        self.window.flip()

        return rgb
