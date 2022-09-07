### An efficient pure Python/Pygame grass module. Feel free to use however you'd like.

![](https://i.imgur.com/nfHCMfb.gif)

Please see grass_demo.py for an example of how to use GrassManager.

Important functions and objects:

### `grass.GrassManager(grass_path, tile_size=15, shade_amount=100, stiffness=360, max_unique=10, place_range=[1, 1], padding=13)`

Initialize a grass manager object.

### `grass.GrassManager.enable_ground_shadows(shadow_strength=40, shadow_radius=2, shadow_color=(0, 0, 1), shadow_shift=(0, 0))`

Enables shadows for individual blades (or disables if shadow_strength is set to 0). shadow_radius determines the radius of the
shadow circle, shadow_color determines the base color of the shadow, and shadow_shift is the offset of the shadow relative to
the base of the blade.

### `grass.GrassManager.place_tile(location, density, grass_options)`

Adds new grass. location specifies which "tile" the grass should be placed at, so the pixel-position of the tile will depend
on the GrassManager's tile size. density specifies the number of blades the tile should have and grass_options is a list of blade
image IDs that can be used to form the grass tile. The blade image IDs are the alphabetical index of the image in the asset folder
provided for the blades. Please note that you can specify the same ID multiple times in the grass options to make it more likely
to appear.

### `grass.GrassManager.apply_force(location, radius, dropoff)`

Applies a physical force to the grass at the given location. The radius is the range at which the grass should be fully bent over at.
The dropoff is the distance past the end of the "radius" that it should take for the force to be eased into nothing.

### `grass.GrassManager.update_render(surf, dt, offset=(0, 0), rot_function=None)`

Renders the grass onto a surface and applies updates. surf is the surface rendered onto, dt is the amount of seconds passed since the
last update, offset is the camera's offset, and the rot_function is for custom rotational modifiers. The rot_function passed as an
argument should take an X and Y value while returning a rotation value. Take a look at grass_demo.py to how you can create a wind
effect with this.

Notes about configuration of the GrassManager:

`<grass_path>`

The only required argument. It points to a folder with all of the blade images. The names of the images don't matter. When creating
tiles, you provide a list of IDs, which are the indexes of the blade images that can be used. The indexes are based on alphabetical
order, so if be careful with numbers like img_2.png and img_10.png because img_10.png will come first. It's recommended that you do
img_02.png and img_10.png if you need double digits.

`<tile_size>`

This is used to define the "tile size" for the grass. If your game is tile based, your actual tile size should be some multiple of the
number given here. This affects a couple things. First, it defines the smallest section of grass that can be individually affected by
efficient rotation modifications (such as wind). Second, it affects performance. If the size is too large, an unnecessary amount of
calculations will be made for applied forces. If the size is too small, there will be too many images render, which will also reduce
performance. It's good to play around with this number for proper optimization.

`<shade_amount>`

The shade amount determines the maximum amount of transparency that can be applied to a blade as it tilts away from its base angle.
This should be a value from 0 to 255.

`<stiffness>`

This determines how fast the blades of grass bounce back into place after being rotated by an applied force.

`<max_unique>`

This determines the maximum amount of variants that can be used for a specific tile configuration (a configuration is the combination
of the amount of blades of grass and the possible set of blade images that can be used for a tile). If the number is too high, the
application will use a large amount of RAM to store all of the cached tile images. If the number is too low, you'll start to see
consistent patterns appear in the layout of your grass tiles.

`<place_range>`

This determines the vertical range that the base of the blades can be placed at. The range should be any range in the range of 0 to 1.
Use [1, 1] when you want the base of the blades to be placed at the bottom of the tile (useful for platformers) or [0, 1] if you want
the blades to be placed anywhere in the tile (useful for top-down games).

`<padding>`

This is the amount of spacial padding the tile images have to fit the blades spilling outside the bounds of the tile. This should
probably be set to the height of your tallest blade of grass.

`<precision>`

This is the amount of precision the angles can have. The lower precision, the choppier the motion will appear. However, using a high
precision will use a large amount of RAM. The integer given is the amount of distinct angles allowed in a 90 degree range.
