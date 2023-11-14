from pathlib import Path
from shutil import copyfile
from subprocess import run

from jinja2 import Environment, FileSystemLoader

firmware_path = Path("oxocard_binaries")
cards = ["artwork", "galaxy", "science", "connect"]


def main():
    env = Environment(
        loader=FileSystemLoader("templates"),
    )

    products = []
    (Path("webpage") / "firmware" / "merged").mkdir(parents=True, exist_ok=True)
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
        firmware = sorted(list((firmware_path / card).glob("*.bin")), reverse=True)[0]
        version = firmware.stem.split("_")[-1]
        name = " ".join([i.title() for i in firmware.stem.split("_")[:-1]])
        # fmt: off
        cmd = [
            "esptool.py",
            "--chip", "esp32", "merge_bin",
            "-o", str(Path("webpage") / "firmware" / "merged" / firmware.name),
            "--flash_mode", "dio",
            "--flash_freq", "80m",
            "--flash_size", "8MB",
            "0x1000", "oxocard_binaries/common/bootloader.bin",
            "0x8000", "oxocard_binaries/common/partition-table.bin",
            "0x10000", str(firmware),
        ]
        # fmt: on
        run(cmd)

        copyfile(
            firmware,
            Path("webpage") / "firmware" / firmware.name,
        )

        template = env.get_template("manifest.json")
        with open(
            Path("webpage") / f"manifest_{firmware.with_suffix('.json').name}", "w"
        ) as f:
            f.write(
                template.render(name=name, version=version, file_name=firmware.name)
            )
        products.append({"name": name, "stem": firmware.stem, "version": version})

        template = env.get_template("index.html")
        with open(Path("webpage") / "index.html", "w") as f:
            f.write(template.render(products=products))


if __name__ == "__main__":
    main()
    main()
