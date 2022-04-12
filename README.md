# Mopidy-Mopidy
Backend plugin for Mopidy Satellites.

Plugin can be used to run satellite mopidy server, which gets music content from master mopidy server.

Master server must have [Mopidy-Master](https://github.com/stffart/mopidy-master) plugin installed

Features:
- Playlists lookup on master
- Library browsing on master
- Do search from master library


### Installation

Install by running:

```
pip install mopidy-mopidy
```

### Configuration

```
[mopidy_mopidy]
enabled = true
host = your_master_host

```

