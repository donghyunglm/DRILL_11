from pathlib import Path
from math import pi
from time import monotonic

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT
from transitions import Machine

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.pressed_keys = set()
        self.direction = 0
        self.last_update = monotonic()
        self.image = load_image(str(Path(__file__).with_name('animation_sheet.png')))
        self.run_image = load_image(str(Path(__file__).with_name('run_animation.png')))
        self.idle_started_at = monotonic()
        self.machine = Machine(
            model=self,
            states=[{'name': 'IDLE', 'on_enter': 'enter_idle'},
                    'RUN', {'name': 'SLEEP', 'on_enter': 'enter_sleep'}],
            transitions=[['sleep', 'IDLE', 'SLEEP'],
                         ['run', ['IDLE', 'SLEEP'], 'RUN'],
                         ['stop', 'RUN', 'IDLE']],
            initial='IDLE',
            auto_transitions=False,
        )

    def enter_idle(self):
        self.idle_started_at = monotonic()
        self.frame = 0

    def enter_sleep(self):
        self.frame = 0

    def handle_event(self, event):
        if event.type not in (SDL_KEYDOWN, SDL_KEYUP):
            return
        if event.key not in (SDLK_LEFT, SDLK_RIGHT):
            return
        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
        else:
            self.pressed_keys.discard(event.key)
        self.direction = (int(SDLK_RIGHT in self.pressed_keys)
                          - int(SDLK_LEFT in self.pressed_keys))
        if self.direction:
            self.face_dir = self.direction
            if self.state != 'RUN':
                self.frame = 0
                self.run()
        elif self.state == 'RUN':
            self.stop()

    def update(self):
        now = monotonic()
        dt = now - self.last_update
        self.last_update = now
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            if monotonic() - self.idle_started_at >= 5.0:
                self.sleep()
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x = max(25, min(775, self.x + self.direction * 200 * dt))

    def draw(self):
        if self.state == 'SLEEP':
            # Keep the face upward so the boy sleeps on his back.
            row = 300 if self.face_dir == 1 else 200
            angle = pi / 2 if self.face_dir == 1 else -pi / 2
            self.image.clip_composite_draw(
                0, row, 100, 100, angle, '', self.x, self.y - 25, 100, 100
            )
            return
        if self.state == 'RUN':
            self.run_image.clip_composite_draw(
                self.frame * 100, 0, 100, 100, 0,
                '' if self.face_dir == 1 else 'h',
                self.x, self.y, 100, 100
            )
        elif self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
