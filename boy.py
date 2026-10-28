from pathlib import Path
from time import monotonic

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_a
from transitions import Machine

CANVAS_WIDTH = 800
NORMAL_SIZE = 100
RUN_SPEED = 200
ANIMATION_FPS = 10



class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0.0
        self.face_dir = 1
        self.pressed_keys = set()
        self.direction = 0
        self.last_update = monotonic()
        self.image = load_image(str(Path(__file__).with_name('animation_sheet.png')))
        self.run_image = load_image(str(Path(__file__).with_name('run_animation.png')))

        self.machine = Machine(
            model=self,
            states=[{'name': 'IDLE', 'on_enter': 'enter_idle'},
                    {'name': 'RUN', 'on_enter': 'enter_run'}],
            transitions=[['run', 'IDLE', 'RUN'], ['stop', 'RUN', 'IDLE']],
            initial='IDLE',
            auto_transitions=False,
        )

    def enter_idle(self):
        self.frame = 0.0

    def enter_run(self):
        self.frame = 0.0

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
            if self.state == 'IDLE':
                self.run()
        elif self.state == 'RUN':
            self.stop()

    def update(self):
        now = monotonic()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        self.frame = (self.frame + ANIMATION_FPS * dt) % 8
        if self.state == 'RUN':
            half = NORMAL_SIZE / 2
            self.x = max(half, min(CANVAS_WIDTH - half,
                                  self.x + self.direction * RUN_SPEED * dt))

    def draw(self):
        frame = int(self.frame)
        if self.state in ('RUN',):
            size = NORMAL_SIZE
            # Anchor the feet to the same ground line when changing size.
            y = self.y + (size - NORMAL_SIZE) / 2
            self.run_image.clip_composite_draw(
                frame * 100, 0, 100, 100, 0,
                '' if self.face_dir == 1 else 'h',
                self.x, y, size, size,
            )
        else:
            row = 300 if self.face_dir == 1 else 200
            self.image.clip_draw(frame * 100, row, 100, 100, self.x, self.y)
