# beautiful_qr_generator
CLI for creating beautiful QR codes


## Setup
This project uses pipenv.

`pipenv shell`
`pipenv install`

## Usage

`python qr_maker.py --help`

> Usage: qr_maker.py [OPTIONS]

>   The main application program.

> Options:
>   -c, --color TEXT
>   -d, --design [special|round|square]
>   -e, --eyes [square]
>   -ec, --eye_color TEXT
>   -ft, --file_type [pdf|png|svg]
>   -fn, --file_name TEXT
>   -v, --value TEXT
>   --logo / --no_logo
>   --grid / --no_grid
>   --help                          Show this message and exit.

`python qr_maker.py -c blue -d round`