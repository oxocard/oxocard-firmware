from dataclasses import dataclass, field
from pathlib import Path
from shutil import copyfile

from jinja2 import Environment, FileSystemLoader


@dataclass
class Card:
    name: str
    stem: str
    manifest: str
    variables: dict = field(default_factory=dict)


artwork = Card(name="Oxocard Mini Artwork", manifest="artwork", stem="artwork")
galaxy = Card(name="Oxocard Mini Galaxy", manifest="galaxy", stem="galaxy")
science = Card(name="Oxocard Mini Science", manifest="science", stem="science")
connect = Card(name="Oxocard Mini Connect", manifest="connect", stem="connect")
connect_makey = Card(
    name="Oxocard Mini Connect (Makey Edition)",
    manifest="connect-makey",
    stem="connect",
    variables={"is_makey": True},
)

firmware_path = Path("oxocard_binaries")

cards = [artwork, galaxy, science, connect, connect_makey]


def main():
    env = Environment(
        loader=FileSystemLoader("templates"),
    )

    products = []
    (Path("webpage") / "firmware" / "common").mkdir(parents=True, exist_ok=True)
    (Path("webpage") / "firmware" / "nvs").mkdir(parents=True, exist_ok=True)

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
            list((firmware_path / card.stem).glob("*.bin")), reverse=True
        )[0]
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

    copyfile(
        Path("nvs") / "makey.bin",
        Path("webpage") / "firmware" / "nvs" / "nvs-makey.bin",
    )


if __name__ == "__main__":
    main()
