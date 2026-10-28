"""Deterministic state/input checks; no display or real-time waiting required."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import boy


class BoyTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.clock = patch.object(boy, 'monotonic', side_effect=lambda: self.now)
        self.images = patch.object(boy, 'load_image', side_effect=lambda _: Mock())
        self.clock.start()
        self.images.start()
        self.addCleanup(self.clock.stop)
        self.addCleanup(self.images.stop)
        self.boy = boy.Boy()

    def key(self, key, down=True):
        self.boy.handle_event(SimpleNamespace(
            type=boy.SDL_KEYDOWN if down else boy.SDL_KEYUP, key=key))

    def advance(self, seconds):
        self.now += seconds
        self.boy.update()

    def test_idle_animation_without_movement(self):
        self.advance(0.1)
        self.assertEqual(self.boy.state, 'IDLE')
        self.assertEqual(self.boy.x, 400)
        self.assertAlmostEqual(self.boy.frame, 1)

    def test_run_and_release(self):
        self.key(boy.SDLK_RIGHT)
        self.advance(0.25)
        self.assertEqual(self.boy.x, 450)
        self.key(boy.SDLK_RIGHT, False)
        self.assertEqual(self.boy.state, 'IDLE')

    def test_opposite_keys_release(self):
        self.key(boy.SDLK_LEFT)
        self.key(boy.SDLK_RIGHT)
        self.assertEqual(self.boy.state, 'IDLE')
        self.key(boy.SDLK_RIGHT, False)
        self.assertEqual((self.boy.state, self.boy.direction), ('RUN', -1))

    def test_auto_entry_and_speed_without_held_key(self):
        self.key(boy.SDLK_a)
        self.key(boy.SDLK_a, False)
        self.advance(0.25)
        self.assertEqual(self.boy.state, 'AutoRun')
        self.assertEqual(self.boy.x, 500)
        self.assertIsInstance(self.boy.auto_run, boy.AutoRun)

    def test_auto_uses_facing_direction(self):
        self.boy.face_dir = -1
        self.key(boy.SDLK_a)
        self.advance(0.25)
        self.assertEqual(self.boy.x, 300)

    def test_size_and_ground_anchor_restore(self):
        self.key(boy.SDLK_a)
        self.boy.draw()
        self.assertEqual(self.boy.run_image.clip_composite_draw.call_args.args[-3:],
                         (115.0, 150.0, 150.0))
        self.key(boy.SDLK_RIGHT)
        self.boy.draw()
        self.assertEqual(self.boy.run_image.clip_composite_draw.call_args.args[-3:],
                         (90.0, 100, 100))

    def test_both_walls_and_entry_clamp(self):
        for x, direction, expected in [(720, 1, -1), (80, -1, 1)]:
            with self.subTest(direction=direction):
                self.setUpBoy(x, direction)
                self.advance(0.1)
                self.assertEqual(self.boy.face_dir, expected)
                self.assertGreaterEqual(self.boy.x, 75)
                self.assertLessEqual(self.boy.x, 725)
        self.setUpBoy(50, -1)
        self.assertEqual(self.boy.x, 75)

    def setUpBoy(self, x, direction):
        self.boy = boy.Boy()
        self.boy.x, self.boy.face_dir = x, direction
        self.key(boy.SDLK_a)

    def test_timeout_not_extended_by_wall_or_a(self):
        self.key(boy.SDLK_a)
        started = self.boy.auto_run.started_at
        for _ in range(9):
            self.advance(0.5)
        self.key(boy.SDLK_a)
        self.assertEqual(self.boy.auto_run.started_at, started)
        self.assertEqual(self.boy.state, 'AutoRun')
        x = self.boy.x
        self.advance(0.5)
        self.assertEqual(self.boy.state, 'IDLE')
        self.assertEqual(self.boy.x, x)

    def test_cancel_both_directions_and_normal_speed(self):
        for key, direction in [(boy.SDLK_LEFT, -1), (boy.SDLK_RIGHT, 1)]:
            with self.subTest(direction=direction):
                self.boy = boy.Boy()
                self.key(boy.SDLK_a)
                self.key(key)
                self.assertEqual((self.boy.state, self.boy.face_dir), ('RUN', direction))
                self.advance(0.25)
                self.assertEqual(self.boy.x, 400 + direction * 50)
                self.key(key, False)
                self.assertEqual(self.boy.state, 'IDLE')

    def test_a_during_run_is_ignored(self):
        self.key(boy.SDLK_RIGHT)
        self.key(boy.SDLK_a)
        self.assertEqual(self.boy.state, 'RUN')

    def test_long_frame_stays_in_bounds(self):
        self.key(boy.SDLK_a)
        self.advance(4.9)
        self.assertGreaterEqual(self.boy.x, 75)
        self.assertLessEqual(self.boy.x, 725)


if __name__ == '__main__':
    unittest.main()
