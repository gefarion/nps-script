# nps-script
A simple Python script to download items from https://nopaystation.com/

Notes:
- Require python 2.7
- Require `pkg2zip` installed

Examples:

- List all PSP games:
`python nps-script.py --platform psp`

- List european PSX games:
`python nps-script.py --platform psx --region eu`

- List american PSV 'final fantasy' games:
`python nps-script.py --platform psv --filter 'final fantasy' --region us`

- Download Final fantasy III for PSP:
`python nps-script.py -p psp --download EU-NPEH00134`
