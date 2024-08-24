from os import environ, path
from subprocess import check_output
from platform import uname
from pathlib import Path


def get_config_dir():
    return environ.get("XDG_CONFIG_HOME", Path.home().joinpath(".config", "pbfetch"))

def configpath():
    return str(
        path.join(
            get_config_dir(),
            "config.txt"
        )
    )

# fill a tuple with uname info to use for other stats
_uname = tuple(uname())
environ =  dict(environ)

def system():
    return _uname[0]

def stat_host():
    return _uname[1]

def stat_architecture():
    return _uname[4]

def stat_hostname():
    # return f"{login.parse_login()}@{hostname.parse_hostname()}"
    return f"{environ["USER"]}@{stat_host()}"

def stat_datetime():
    return " ".join(
        check_output(["date"]).decode("utf-8").split()
    )

########################################

# keywords
uptime = "$upt"
comp = "$cmp"
user = "$usr"
host = "$hst"
sys = "$sys"
arch = "$ach"
kernel = "$ker"
ram = "$mem"
packages = "$pac"
cpu = "$cpu"
disc = "$dsk"
shell = "$shl"
window_man = "$wmn"
desktop_env = "$den"
filesystem = "$fsm"
locale = "$lcl"
battery = "$bat"
gpu = "$gpu"
motherboard = "$mbd"
bios = "$bio"
resolution = "$res"
date_time = "$dat"
theme ="$thm"
font = "$fnt"
term_font = "$tft"
config_path = "$configpath"
syst = "$system"

def stats(fetch_data):
    # init stats using keywords for configuration in .conf
    # TODO: add easter egg stats for fun dynamic things
    stats_dict = {syst: system(), host: stat_hostname()}

    # only import and add stats if keyword is present
    if uptime in fetch_data:
        print("uptime")
        from pbfetch.parse_funcs.parse_uptime import parse_uptime
        stats_dict[uptime] = parse_uptime()
    
    if sys in fetch_data:
        print("sys")
        from pbfetch.parse_funcs.parse_os import parse_os
        stats_dict[sys] = parse_os()
    
    if cpu in fetch_data:
        print("cpu")
        from pbfetch.parse_funcs.parse_cpu import parse_cpu
        stats_dict[cpu] = parse_cpu()
    
    if ram in fetch_data:
        print("ram")
        from pbfetch.parse_funcs.parse_mem import parse_mem
        stats_dict[ram] = parse_mem()
    
    if kernel in fetch_data:
        print("kernel")
        from pbfetch.parse_funcs.parse_kernel import parse_kernel_release
        stats_dict[kernel] = parse_kernel_release()
    
    if window_man in fetch_data:
        print("window_man")
        from pbfetch.parse_funcs.parse_wm import parse_wm
        stats_dict[window_man] = parse_wm()
    
    if desktop_env in fetch_data:
        print("desktop_env")
        from pbfetch.parse_funcs.parse_de import parse_de
        stats_dict[desktop_env] = parse_de()
    
    if filesystem in fetch_data:
        print("filesystem")
        from pbfetch.parse_funcs.parse_fs import parse_fs
        stats_dict[filesystem] = parse_fs()
    
    if gpu in fetch_data:
        print("gpu")
        from pbfetch.parse_funcs.parse_gpu_name import parse_gpu
        stats_dict[gpu] = parse_gpu()
    
    if battery in fetch_data:
        print("battery")
        from pbfetch.parse_funcs.parse_batt import parse_batt
        stats_dict[battery] = parse_batt()
    
    if motherboard in fetch_data:
        print("motherboard")
        from pbfetch.parse_funcs.parse_mb import parse_mb
        stats_dict[motherboard] = parse_mb()
    
    if comp in fetch_data:
        print("comp")
        from pbfetch.parse_funcs.parse_comp_name import parse_comp_name
        stats_dict[comp] = parse_comp_name()
    
    if bios in fetch_data:
        print("bios")
        from pbfetch.parse_funcs.parse_bios_type import parse_bios_type
        stats_dict[bios] = parse_bios_type()
    
    if resolution in fetch_data:
        print("resolution")
        from pbfetch.parse_funcs.parse_res import parse_res
        stats_dict[resolution] = parse_res()
    
    if packages in fetch_data:
        print("packages")
        from pbfetch.parse_funcs.parse_packages import parse_packages
        stats_dict[packages] = parse_packages()
    
    if disc in fetch_data:
        print("disc")
        from pbfetch.parse_funcs.parse_disc import parse_disc
        stats_dict[disc] = parse_disc()
    
    if shell in fetch_data:
        print("shell")
        from pbfetch.parse_funcs.parse_shell import parse_shell
        stats_dict[shell] = parse_shell()
    
    if theme in fetch_data:
        print("theme")
        from pbfetch.parse_funcs.parse_theme import parse_theme
        stats_dict[theme] = parse_theme()
    
    if font in fetch_data:
        print("font")
        from pbfetch.parse_funcs.parse_font import parse_font
        stats_dict[font] = parse_font()
    
    if term_font in fetch_data:
        print("term_font")
        from pbfetch.parse_funcs.parse_term_font import parse_term_font
        stats_dict[term_font] = parse_term_font()

    # stats_dict = {
    #     comp: parse_comp_name() if comp in fetch_data else None,
    #     user: environ["USER"] if user in fetch_data else None,
    #     host: stat_hostname() if host in fetch_data else None,
    #     sys: parse_os() if sys in fetch_data else None,
    #     arch: stat_architecture() if arch in fetch_data else None,
    #     kernel: parse_kernel_release() if kernel in fetch_data else None,
    #     ram: parse_mem() if ram in fetch_data else None,
    #     uptime: parse_uptime() if uptime in fetch_data else None,
    #     packages: parse_packages() if packages in fetch_data else None,
    #     cpu: parse_cpu() if cpu in fetch_data else None,
    #     disc: parse_disc() if disc in fetch_data else None,
    #     shell: parse_shell() if shell in fetch_data else None,
    #     window_man: parse_wm() if window_man in fetch_data else None,
    #     desktop_env: parse_de() if desktop_env in fetch_data else None,
    #     filesystem: parse_fs() if filesystem in fetch_data else None,
    #     locale: environ["LANG"] if locale in fetch_data else None,
    #     battery: parse_batt() if battery in fetch_data else None,
    #     gpu: parse_gpu() if gpu in fetch_data else None,
    #     motherboard: parse_mb() if motherboard in fetch_data else None,
    #     bios: parse_bios_type() if bios in fetch_data else None,
    #     resolution: parse_res() if resolution in fetch_data else None,
    #     date_time: stat_datetime() if date_time in fetch_data else None,
    #     theme: parse_theme() if theme in fetch_data else None,
    #     font: parse_font() if font in fetch_data else None,
    #     term_font: parse_term_font() if term_font in fetch_data else None,
    #     config_path: configpath() if config_path in fetch_data else None,
    #     syst: system(),
    # }

    return stats_dict
