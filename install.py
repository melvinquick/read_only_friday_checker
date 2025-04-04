import os
import sys
import subprocess
from textwrap import dedent


def print_green(skk):
    print("\033[92m {}\033[00m".format(skk))


def get_venv_path():
    home_dir = os.path.expanduser("~")
    venv_dir = os.path.join(home_dir, ".venvs")
    if not os.path.exists(venv_dir):
        os.makedirs(venv_dir)
    return os.path.join(venv_dir, "read_only_friday_checker_venv")


def create_venv(venv_path):
    print("Creating the virtual environment...", end="")
    sys.stdout.flush()
    subprocess.run(
        ["python3", "-m", "venv", venv_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("󰄬")

    print("Ensuring pip is up to date...", end="")
    sys.stdout.flush()
    pip_path = os.path.join(venv_path, "bin", "pip")
    subprocess.run(
        [pip_path, "install", "--upgrade", "pip"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("󰄬")


def install_app(venv_path):
    print("Installing Read Only Friday Checker into the virtual environment...", end="")
    sys.stdout.flush()
    pip_path = os.path.join(venv_path, "bin", "pip")
    subprocess.run(
        [pip_path, "install", "read_only_friday_checker"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("󰄬")


def get_icon(venv_path):
    site_packages = os.path.join(venv_path, "lib")
    for folder in os.listdir(site_packages):
        if folder.startswith("python"):
            site_packages = os.path.join(site_packages, folder, "site-packages")
            break

    icon_relative_path = (
        "read_only_friday_checker/resources/images/read_only_friday_checker-128.png"
    )
    full_icon_path = os.path.join(site_packages, icon_relative_path)
    return full_icon_path


def get_python_path(venv_path):
    return os.path.join(venv_path, "bin", "python3")


def get_app_path(venv_path):
    return os.path.join(venv_path, "bin", "read-only-friday-checker")


def create_desktop_file(icon, version, python, app):
    print("Creating the .desktop entry...", end="")
    sys.stdout.flush()
    desktop_content = dedent(f"""
    [Desktop Entry]
    Version={version}
    Type=Application
    Name=Read Only Friday Checker
    Comment=This checks to see if today is Read Only Friday.
    Exec={python} {app}
    Icon={icon}
    Terminal=false
    Categories=Utility;
    """)
    desktop_content = desktop_content.lstrip()
    with open(
        os.path.expanduser(
            "~/.local/share/applications/read_only_friday_checker.desktop"
        ),
        "w",
    ) as f:
        f.write(desktop_content)
    print_green("󰄬")


def install():
    venv_path = get_venv_path()
    create_venv(venv_path)
    install_app(venv_path)
    version = "1.0.2"
    icon = get_icon(venv_path)
    python = get_python_path(venv_path)
    app = get_app_path(venv_path)
    create_desktop_file(icon, version, python, app)


def main():
    install()


if __name__ == "__main__":
    main()
