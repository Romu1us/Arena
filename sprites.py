import pygame

from settings import *
from utils import render_text
from utils import Debug


class Generic(pygame.sprite.Sprite):
    """
    用于 CameraGroup 的通用的 Sprite 类
    无碰撞箱
    """

    def __init__(self, pos, surf, group, z=LAYERS["default"]):
        super().__init__(group)
        self.image = surf
        self.z = z
        self.rect = self.image.get_rect(topleft=pos)


class GameObject(Generic):
    """
    矩形碰撞箱
    """

    def __init__(self, pos, surf, group, z=LAYERS["default"]):
        super().__init__(pos, surf, group, z)
        self.hitbox = self.rect.copy()


class Button(pygame.sprite.Sprite):
    """
    不可直接实例化, 必须通过其子类创建按钮
    """

    def __init__(self, pos, group, z=LAYERS["ui"]):
        super().__init__(group)
        self.pos = pos
        self.z = z
        self.rect = self.image.get_rect(topleft=pos)

        # * Bool * #
        self.active = False
        self.hover = False
        self.pressed = False
        self.clicked = False

    def update(self, dt):
        super().update()

        if self.active:
            self.respond_mouse()

    def activate(self):
        self.active = True
        Debug(True) << "Activated TextButton" << "\n"

    def deactivate(self):
        self.active = False
        Debug(True) << "Deactivated TextButton" << "\n"

    def click(self):
        """
        左键单机时调用
        """
        self.clicked = True
        self.deactivate()

    def _clicked(self):
        self.clicked = False

    def hovered_effect(self):
        """
        鼠标悬停效果
        """

    def cancel_hover(self):
        """
        鼠标停止悬停时的效果
        """

    def pressed_effect(self):
        """
        左键按下效果
        """

    def respond_mouse(self):
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hover:
            self.hovered_effect()
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                self.pressed_effect()
        else:
            self.cancel_hover()

        if self.pressed:
            if not pygame.mouse.get_pressed()[0]:
                self.click()
                self.pressed = False


class TextButton(Button):
    def __init__(self, text, size, color, pos, group, z=LAYERS["ui"]):
        self.image = pygame.surface.Surface((5, 5))
        super().__init__(pos, group, z)
        self.text = text
        self.size = size
        self.color = color

        self.former_size = self.size
        self.target_size = self.size + 5
        self.former_color = color
        self.target_color = (255, 255, 255)

    def update(self, dt):
        super().update(dt)
        self.image = render_text(self.text, FONT_ZH, self.size, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)

    def respond_mouse(self):
        super().respond_mouse()

    def hovered_effect(self):
        super().hovered_effect()
        self.size = self.target_size
        self.color = self.target_color

    def cancel_hover(self):
        super().cancel_hover()
        self.size = self.former_size
        self.color = self.former_color


class Fog(Generic):
    def __init__(self, pos, surf, group, z=LAYERS["fog"]):
        super().__init__(pos, surf, group, z)
        self.image.set_alpha(250)
        self.start_x = pos[0]
        self.move_speed = 1

    def move(self):
        self.rect.x += self.move_speed
        if self.rect.x >= SCR_SIZE[0]:
            self.rect.x = -SCR_SIZE[0]
