
# pyRCX (heavy refactor in progress)

  

![Tests](https://github.com/cwebbtw/pyRCX/actions/workflows/github-actions-python-tests.yml/badge.svg)

A pure python IRCX (https://www.ietf.org/archive/id/draft-pfenning-irc-extensions-04.txt) server originally written with Python 2.3 and ported to 3.11.4 many years later.

### Backwards compatibility

Clients that do not send IRCX will be treated as IRCII compatibility.

### User modes supported

Standard user modes for IRCX should be supported however additional modes are also supported.

`abAfghiInoOpPrwzX`

#### Self Modes

- `h - "Host" - Used to host/owner yourself in a room (MODE YourName +h Password)`
- `i - "Invisible" - Your info cannot be seen unless a user is in the same room as you are.`
- `x - "IsIRCX" - Your connection is using IRCX mode. /IRCX to see Owner +q and /prop`

_(Further modes to be documented)_

##### Example

`mode <my nickname> +i - Sets your user to invisible`
`/mode <my nickname> +h` <key> - If the <key> matches a channel's it will give you operator access.`

### Channel modes supported

Standard channel modes for IRCX should be supported however additional modes are also supported.

You can set up to 20 modes, eg: /mode #channel +ooooooooooo-vvvvvvvv name1 name2 name3...

- `a - "Authenticated Only" - Only authenticated clients may join.`
- `A - "Admin Only" - Only Admins (non-sysop and guides) may enter the channel`
- `b - "Ban" - Can be used to get a list of ban (ACCESS DENY) entries.`
- `c - "No colors" - Colors are disallowed and message blocked.`
- `C - "Strip Colors" - Colors, bold, etc are removed from messages`
- `d - "Cloneable" - When the room fills up, a new room will be created with the same name, plus a number between 1 and 99. Cannot be set by normal users. #x becomes #x1 #x2 etc.`
- `e - "Clone" - This room is a clone of a room that is set to mode +d. Cannot be set by normal users. #x1 gets mode +e to tell clients it's not the original channel.`
- `f - "Filter" - IRCX's built-in profanity filter is being used. Can only be set during room creation.`
- `G - "Gag on ban" - Banned users can't talk`
- `h - "Hidden" - Room is not shown on any sort of room listings. Same as +s, can't be used with +p or +s.`
- `i - "Invite" - Room is set as invite only.`
- `k - "Key" - Room has an entry password set. Same as PROP MEMBERKEY. /join #channel key`
- `l - "Limit" - Room has a user limit set. Anything above 100 users must be set during room creation and may not actually be enforced.`
- `m - "Moderated" - Users in the room can be "specced", or set mode -v, and they cannot speak.`
- `M - "Owner only mode changes" - Only owners can /mode"`
- `n - "No External Messages" - Only people that are actually in the room, can speak in the room. If this mode is not set, you can talk in the room without actually being there.`
- `N - "Service Channel" - Services channel, only operators and services may utilize.`
- `p - "Private" - Room is not shown on the room listings, and you can only find out the amount of people in the room and the name. Cannot be used with +h or +s. Only shows #name in /list and /listx`
- `P - "Owner ACL Only" - Only chan owners can set /access"`
- `Q - "Owner Kick" - Only owners can /kick.`
- `r - "Registered" - Official registered room, doesn't delete if empty.`
- `R - "Registered Only" - Only registered users may join.`
- `s - "Secret" - Room is not shown on any sort of room listings. Same as +h, cannot be used with +h or +p.`
- `S - "No Mode Changes" - Modes are locked upon channel creation.`
- `t - "Only Hosts Set Topic" - Only a host, owner, or MSN official can change the room topic. If -t, any user can change the topic.`
- `T - "Owner /Topic Only" - Only owners can change the channel topic.`
- `u - "Knock" - When someone can't get into the room for whatever reason, all hosts recieve a message stating so.`
- `w - "No Whispers" - Normal users cannot whisper non-hosts.`
- `W - "No Guest Whispers" - (Non-registered) Guests cannot whisper non-hosts. Note that this is an UPPERCASE W.`
- `x - "Auditorium Mode" - Normal users cannot see each other in the room and can only see hosts, while hosts can see everyone. Cannot be set by normal users.`
- `Z - "NO IRCX" - Only clients that utilize regular IRC can join`

#### Channel User Modes (/mode channel +q nickname)

- `v - "Voice" - User can speak in a moderated (+m) room.`
- `o - "Host" - User is a host in the channel.`
- `q - "Owner" - User is an owner in the channel.`

### Properties supported

Prop supports channel properties of:
-  `CLIENT`
-  `HOSTKEY`
-  `LAG`
-  `LANGUAGE`
-  `MEMBERKEY`
-  `ONJOIN`
-  `ONPART`
-  `OWNERKEY`
-  `RESET`
-  `SUBJECT`
-  `TOPIC`

#### Example

- `/prop #channel HOSTKEY <key>`
- `/mode me +h somekey and the server will mode +o the user`
- `/prop #channel OWNERKEY <key>`  

### Access supported

Access supports add, deny, list and clear at channel, user and server levels:

-  `VOICE`
-  `GRANT`
-  `HOST`
-  `OWNER`

Additional REGISTER access is provided with a founder mode which diverts from the IRCX rfc but provides
a mechanism for a registered channel to be assigned to a registered nickname.

### NickServ

This server supports nickserv and has the following behaviour

-  `REGISTER`
-  `IDENTIFY`
-  `GHOST`
-  `INFO`
-  `DROP`
-  `GROUP/UNGROUP`
-  `SET`
-  `DEFCON`
-  `IPLOCK`

Note that ChanServ is not supported and should not be required given ACCESS and PROP.

#### WHISPER

`/whisper channel nickname :message`

Whispers are channel specific and offer a different set of options.
It's still a private message, but dictated by the channel hosts/operators.
Some IRCds have no private message umodes unless you're in common channels, same idea, different concept.

## Usage

Run the main file to start the server

`python start.py` (python3 start.py) on systems with multiple python versions

### Tests

`python -m unittest`

### Dependencies

`None yet.`

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

