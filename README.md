Reservation alert
==================

Send yourself an email when a reservation is available on the Explore Tock site.

## Installation
Clone the repository. This code was written for python 3 (3.8.12), you should also have [pip](https://pip.pypa.io/en/stable/) installed.

- To install required libraries:

`pip install --user -r requirements.txt`

note that one the libraries used is the `lxml` library, which requires a couple of extra packages on Ubuntu:

`[sudo] apt install libxml2-dev libxslt-dev`

## Configuration
Configuration is held in json format, `config.json` is used by default and has some configuration for reference, but a different file can be passed using the command line flags. you must set the emails you'd like to use. Required configuration:

- `email` (dictionary) - this is the configuration for the email server and credentials to use for sending out the email.
    - `to` - the email address to be used for authentication

- `base_url` (string) - the base url of the Explore Tock page that has the restaurant you'd like to book at.



## Running the script

```
$ ./reservation-alert.py --help
usage: reservation-alert.py [-h] [-c CONFIG] [-t POLL_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file path
  -t POLL_INTERVAL, --poll-interval POLL_INTERVAL
                        Time in seconds between checks
```

when running without any arguments, the script will use `config.json` for configuration and the default polling interval of 30 seconds.

