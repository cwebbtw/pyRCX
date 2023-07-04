# pyRCX 

![Tests](https://github.com/cwebbtw/pyRCX/actions/workflows/github-actions-python-tests.yml/badge.svg)

A pure python IRCX (https://www.ietf.org/archive/id/draft-pfenning-irc-extensions-04.txt) server originally written with Python 2.3 and ported to 3.11.4 many years later.

## Documentation

Documentation is currently limited and needs to be improved:

### Backwards compatibility

Clients that do not send IRCX will be treated as IRCII compatibility.

### User modes supported

Standard user modes for IRCX should be supported however additional modes are also supported.

`abAfghiInoOpPrwzX`

(documentation should include the behaviour for each mode)

### Channel modes supported

Standard channel modes for IRCX should be supported however additional modes are also supported.

`aAbcCdefGhikKlmMnNopPqQrRsStTuvwxXZ`

(documentation should include the behaviour for each mode)

### Properties supported

Prop supports channel properties of:

- `CLIENT`
- `HOSTKEY`
- `LAG`
- `LANGUAGE`
- `MEMBERKEY`
- `ONJOIN`
- `ONPART`
- `OWNERKEY`
- `RESET`
- `SUBJECT`
- `TOPIC`

### Access supported

Access supports add, deny, list and clear at channel, user and server levels:

- `VOICE`
- `GRANT`
- `HOST`
- `OWNER`

Additional REGISTER access is provided with a founder mode which diverts from the IRCX rfc but provides
a mechanism for a registered channel to be assigned to a registered nickname.

### NickServ

This server supports nickserv and has the following behaviour

- `REGISTER`
- `IDENTIFY`
- `GHOST`
- `INFO`
- `DROP`
- `GROUP/UNGROUP`
- `SET`
- `DEFCON`
- `IPLOCK`

Note that ChanServ is not supported and should not be required given ACCESS and PROP.

## Usage

Run the main file to start the server

`python start.py`

### Tests

`python -m unittest`

### Dependencies

None yet

## Contributors

Please feel free to make a pull request and please forgive the horrors that you find in the code as they were written by a much younger, but arguably smarter, me.

There is currently no contributors guide as the code needs a considerable amount of work to ensure quality and stability.

## License

Apache 2.0

## Credits

_With thanks to_

Darren Davies, Rob Lancaster, Kevin Deveau, Aaron Caffrey, Shane Britt

_In loving memory of_

Danny Moon and Ricky Laurn

Be kind to one another, love like it's your last day on this amazing planet.
