# nps-script
A simple Python script to download items from https://nopaystation.com/

Notes:
- Only support downloading games (for now).
- Require python 2.7
- Require `pkg2zip` installed (you can define a custom path using '-P')

Examples:

- List all PSP games:
`python nps-script.py -p psp -l`

- List european PSX games:
`python nps-script.py -p psx -l -r eu`

- List american PSV 'final fantasy' games:
`python nps-script.py -p psv -l -f 'final fantasy' -r us`

- Download Final fantasy III for PSP:
`python nps-script.py -p psp -d EU-NPEH00134`

- Use a custom path for `pkg2zip`:
`python nps-script.py -p psp -d EU-NPEH00134 -P /opt/bin/pkg2zip`

- Refresh the NPS database:
`python nps-script.py -p psp -l -R`
