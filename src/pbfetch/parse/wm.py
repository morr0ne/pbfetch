from subprocess import run


def parse_wm():
    managers = [
        "kwin",
        "river",
        "sway",
        "labwc",
        "anvil",
        "cosmic",
        "mirace",
        "mutter",
        "theseus",
        "wayfire",
        "weston",
        "cage",
        "gamescope",
        "qtile",
        "niri",
        "swayfx",
        "metacity",
        "gdm",
        "Hyprland",
    ]

    try:
        for manager in managers:
            output = run(["pgrep", "-l", manager], capture_output=True).stdout
            output = str(output)
            # print(output)

            if output and manager in output:
                return manager

        return "not found/supported"

    except Exception as e:
        print(e)
        return None
