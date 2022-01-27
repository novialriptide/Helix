# version 0.5
### New Features / Changes
1. Renamed `"\\"` to `"/"` in file paths.
2. Added camera shake.
3. Resolution size change.
4. The player can now aim and rotate.
5. Particles disappear more naturally.
6. 

# version 0.4
### New Features / Changes
1. Dialogue scene has been created.
2. Increased Berserk's hitbox size.
3. Waves Manager spawning has been rewritten.
4. All entities now load from `.py` files instead of `JSON` files to prevent partial entity loads.
5. Some enemies will no longer spawn bullets when they're moving.
6. Added "explosions" to every enemy dying. This will later be changed to work with specific enemies.
7. Added rain to Ocean.
8. Added shadows to entities.
9. Window caption displays entity and bullet count.
10. Ocean background has been darkened.
11. Berserk reskin.
12. `"pygame powered"` logo has been cleaned up.
13. Helix's speed has been changed from `2.0` to `2.5`.
14. The `Splash` scene can be skipped by pressing any button on the keyboard or controller.
15. `Try Again` button has been added.
16. Primitive title screen has been created.
17. Placeholder game logo created.
18. Improved bullet lighting.
19. Added overlays to make the game feel less bland.
20. Added primitive points system.
21. Version has been hard-coded to the game.

### Bug Fixes
1. Player no longer moves faster than it should if moving diagonally.
2. Entities now despawn and move to the bottom of the screen to despawn.
3. Window now resizes without crashing.
4. Fixed fullscreen option.
5. Berserk's healthbar is now centered properly.
6. Fixed internal issue where the game would sometimes crash if you were hit with 2 bullets at once.
7. Fixed bug where scene clock is not paused when the game is paused.

### Optimiziations
1. Background scrolling
2. Entity hitboxes are now `50%` faster.

# version 0.3
1. SakuyaEngine patches.
2. First Level Games deprecation.
3. Caption displays fps.
4. Renamed `load_scene` arg to `scene`.
5. Optimizations to bullets have been made.
6. FPS has been capped to `60`.
7. `CHANGELOG.md` has been created.
8. Particle lifetime has been reduced.
9. Enemies now emits particles depending on its health.
10. Entity optimizations.
11. Some enemies can now aim.
12. Resolution has been changed from `256x224` pixels to `256x336` pixels.
13. Bullets now face the right direction.
14. Increased player default speed from `1.5` to `2`.
15. Out of bounds collision added.
16. BulletSpawners are now accurate with targets
17. More spawn points added.
18. Proper "AI" has been implemented for the basic enemies.
19. Ado's bullet patterns have been changed.
20. Berserk (Enemy) has been created.
21. Added Pause Menu
22. Scrolling ocean background added.

# version 0.2
1. SakuyaEngine patches.
2. Lights added to bullets.
3. FPS has been capped to 30.
4. Players and enemies can now die.
5. Healthbar added to enemies.
6. Added ambient particles.
7. Renamed `"\"` to `"\\"` in file paths.
8. Entities can partially load from `JSON` files.
9. Added fire rates.
10. Reimplemented shooting mechanics for the Player.
11. Created `BulletTest` scene.
12. Added player shoot sound effect.
13. Created `Splash` scene.
14. Fixed a bug where the `Nintendo Switch Controller` would fire involuntarily.
15. Fixed a bug where entities would spawn before the player loads in the map.
16. Fixed a bug where only `8` sounds would play in 1 frame.
