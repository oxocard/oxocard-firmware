# oxocard-firmware
Repository for the Oxocard Firmware including Cartridge scripts and Oxocard binaries.

## How to re-flash my Oxocard?
1. Make sure python and pip are installed
2. Open a console and run: `pip install esptool` (Documentation: https://docs.espressif.com/projects/esptool/en/latest/esp32/)
3. Connect your Oxocard and find its port with `ls /dev/cu*` (macOS/linux) or `chgport`(Windows)
4. Replace (PORT) and run: `esptool.py -p (PORT) erase_flash`
5. Navigate into the ".../oxocard_binaries/" directory
6. In the following command: Make sure the paths to the binary files you want to flash are correct, replace (PORT) and run: `esptool.py -p (PORT) -b 921600 --before default_reset --after hard_reset --chip esp32  write_flash --flash_mode dio --flash_size detect --flash_freq 80m 0x1000 common/bootloader.bin 0x8000 common/partition-table.bin 0x10000 connect/oxocard_mini_connect_v142.bin`
7. On the very first startup, the HW test may have to be completed

Example of flashing an Oxocard Science using macOS:
```
esptool.py -p /dev/cu.wchusbserial1440 erase_flash
esptool.py -p /dev/cu.wchusbserial1440 -b 921600 --before default_reset --after hard_reset --chip esp32 write_flash --flash_mode dio --flash_size detect --flash_freq 80m 0x1000 common/bootloader.bin 0x8000 common/partition-table.bin 0x10000 science/oxocard_mini_science_v142.bin
```

Example of flashing an Oxocard Blockly using macOS:
```
esptool.py -p /dev/cu.wchusbserial1440 erase_flash
esptool.py -p /dev/cu.wchusbserial1440 -b 921600 --before default_reset --after hard_reset --chip esp32  write_flash --flash_mode dio --flash_size detect --flash_freq 80m 0x1000 blockly/bootloader.bin 0x8000 blockly/partition-table.bin 0x10000 blockly/oxocard_blockly_v219.bin
```

## How to program a Cartridge?
1. Plug in an Oxocard Connect and connect it to the NanoPy environment via USB or WiFi
2. Copy the "\<cartridge_name>.npy" and "\<cartridge_name>_autostart.npy" files of the cartridge you want to program, into the NanoPy editor
3. Save the scripts as your own and rename them to fit the file names
4. Load those scripts onto your Oxocard Connect using the "Load on card" function within "My Scripts"
5. Copy the "\<cartridge_name>_flasher.npy" file into the NanoPy editor and flash it on the Oxocard Connect using "Run code" 
6. Connect the cartridge with your Oxocard Connect (if you haven't yet) and click a button to write the data to the EERPOM on the cartridge
