# SPDX-FileCopyrightText: 2023 Oxon AG
# SPDX-License-Identifier: BSD-3-Clause

"""
Build script for Oxocard firmware webpage.

This script generates the firmware webpage by processing firmware binaries,
creating manifest files, and copying necessary assets to the webpage directory.

Author: Jacques Supcik <jacques.supcik@hefr.ch>
"""

import sys
from dataclasses import field
from pathlib import Path
from shutil import copyfile

import typer
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from pydantic import BaseModel

app = typer.Typer()


class Card(BaseModel):
    name: str
    directory: str
    manifest: str
    blob: str = "*.bin"
    variables: dict = field(default_factory=dict)


artwork = Card(
    name="Oxocard Mini Artwork",
    manifest="artwork",
    directory="artwork",
    blob="oxocard_mini_artwork_v*.bin",
)
galaxy = Card(
    name="Oxocard Mini Galaxy",
    manifest="galaxy",
    directory="galaxy",
    blob="oxocard_mini_galaxy_v*.bin",
)
science = Card(
    name="Oxocard Mini Science",
    manifest="science",
    directory="science",
    blob="oxocard_mini_science_v*.bin",
)
science_plus = Card(
    name="Oxocard Mini Science + (PLUS)",
    manifest="scienceplus",
    directory="scienceplus",
    blob="oxocard_mini_science_plus_v*.bin",
)
connect = Card(
    name="Oxocard Mini Connect",
    manifest="connect",
    directory="connect",
    blob="oxocard_mini_connect_v*.bin",
)
connect_makey = Card(
    name="Oxocard Mini Connect (Makey Edition)",
    manifest="connect-makey",
    directory="connect",
    blob="oxocard_mini_connect_make_v*.bin",
)

firmware_path = Path("oxocard_binaries")

cards = [artwork, galaxy, science, science_plus, connect, connect_makey]


@app.command()
def build(debug: bool = False, quiet: bool = False):
    logger.remove()
    if debug:
        logger.add(sys.stdout, level="DEBUG")
    elif quiet:
        logger.add(sys.stdout, level="WARNING")
    else:
        logger.add(sys.stdout, level="INFO")

    logger.info("Building webpage...")

    env = Environment(
        loader=FileSystemLoader("templates"),
    )

    products = []
    (Path("webpage") / "firmware" / "common").mkdir(parents=True, exist_ok=True)

    copyfile(
        Path("oxocard_binaries") / "common" / "bootloader.bin",
        Path("webpage") / "firmware" / "common" / "bootloader.bin",
    )

    copyfile(
        Path("oxocard_binaries") / "common" / "partition-table.bin",
        Path("webpage") / "firmware" / "common" / "partition-table.bin",
    )

    for card in cards:
        firmware = sorted(
            list((firmware_path / card.directory).glob(card.blob)), reverse=True
        )[0]

        logger.info(f"Using firmware {firmware} for card {card.name}")
        version = firmware.stem.split("_")[-1]

        copyfile(
            firmware,
            Path("webpage") / "firmware" / firmware.name,
        )

        template = env.get_template("manifest.json")
        with open(Path("webpage") / f"manifest_{card.manifest}.json", "w") as f:
            f.write(
                template.render(
                    name=card.name,
                    version=version,
                    file_name=firmware.name,
                    **card.variables,
                )
            )

        products.append({"name": card.name, "stem": card.manifest, "version": version})

        template = env.get_template("index.html")
        with open(Path("webpage") / "index.html", "w") as f:
            f.write(template.render(products=products))

    logger.success("Build finished.")


if __name__ == "__main__":
    app()
