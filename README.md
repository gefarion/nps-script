# nps-script
A simple Python script to download items from https://nopaystation.com/

Notes:
- Only support downloading games (for now).
- Require python 2.7
- Require `pkg2zip` installed

Examples:

- List all PSP games:
`python nps-script.py --platform psp --list`

- List european PSX games:
`python nps-script.py --platform psx --list --region eu`

- List american PSV 'final fantasy' games:
`python nps-script.py --platform psv --list --filter 'final fantasy' --region us`

- Download Final fantasy III for PSP:
`python nps-script.py -p psp --download EU-NPEH00134`
