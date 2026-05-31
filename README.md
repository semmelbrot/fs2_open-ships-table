# FS2 Open Ship Config Repository

This repository contains FreeSpace Open ship configuration files. For FS2 Campaign and for the FreeSpace1 Port. I wanted to play the campaigns with glide active and in addition have the possibilty to use x, y and z thrusters, which can be assigned in the control options.

This is just a small project I did to experiance the campaign with semi-newtonian-physics for fun. This is not a balanced out mod and it may be too easy at times to avoid missiles or other shots. Its just very fun to play the game like this. This was just meant for me, but I thought I share it. So if anyone is interested, do whatever you want with it.

It is not my idea. The [Joshua's RealFlight Mod for FS2](https://freespacemods.net/download_519.html) does this. But the files do not seem to work properly with the current fs_open version. So I thought I try to achieve this myself.

## What I have done

I used [Sushi's Velocity Mod](https://freespacemods.net/download_168.html) as a basis. Because it has a complete ships.tbl for FS2. Then I reverted all the values back to it's original values, based on the multipliers given in the header of the velocity mod ships.tbl. I did this with the [revert.py script](./_archive/revert.py) This resulted in the [original_ships.tbl](./fs2/original_ships.tbl). This should basically be a ships.tbl with the default values of the original fs2 the game, but I cannot confirm that.

Then I used the [update_player_velocity.py script](./_archive/update_player_velocity.py) to change the x y and rear velocity values from 0 to half of the ships z(forward) velocity, which enables you to use the hotkeys assigned for up down and sideways thrust in addition to accalerate backwards.

After this I change `$Slide accel` and `$Slide decel` from 0.0 to 0.1 and added the line `$Glide: Yes`. This enables you to map the Glide button in the control config. When you use that button and hold it, your ship will move in the current direction with the current velocity while you can look around and shoot. You basically can shoot backwards while moving in the opposite direction.

I also added x and y values for the afterburner so that you can move up, down and sideways while using the afterburner.

I did these changes for all player ships.

## What is included

- `fs2/original_ships.tbl` — the 'original' unmodified ships.tbl which was generated from the velocity mod.
- `fs2/ships.tbl` — the ships.tbl for the fs2 campaing with semi-newtonian-physics enabled.
- `fs1/inertia-shp.tbm` — the ships table for the fs1 campaign of the FreeSpace port.
- `_archive/` — archived conversion scripts related to Velocity mod ship data.

## Usage

1. Place the ships.tbl in the installed FS2 mod folder `FS2\MVPS-5.0.2\data\tables\`.
    - Create the `tables` folder if it does not exist.
2. Start FreeSpace Open and assign the hotkeys for up, down, and sideways movement aswell as Glide.
3. If you want to use the mod with the FreeSpace port do the same thing with the inertia-ship.tbm in `FS2\fsport-mediavps-4.7.2\data\tables\`.

Change the version number respectively.

## FressSpace port

For the FreeSpace port the filename is inertia-ship.tbm, but it is otherwise the same as with the ships.tbl for fs2. Unfortunately I don't have the 'original' uneditet file anymore. You can edit it yourself. Maybe I will take the time to revert it and add it later.

## Disclaimer

I generated the python scripts with AI and I also did some editing of the files with AI so that i do not need edit the file by hand, which would have taken so long that I would not have done it at all. Again it's just a fun project play around with.

## License

[GPL](https://choosealicense.com/licenses/gpl-3.0/)