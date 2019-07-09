# fip-indicator
<p>Ubuntu / Unity indicator applet for the "Best radio in the world": fipradio.</p>
<p>Displays currently playing track on main fip station or selected fip webradio</p>

![screenshot](https://raw.githubusercontent.com/feeloow/fip-indicator/master/screenshot.png "Indicator running in Unity")

## Installation

```bash
git clone https://github.com/feeloow/fip-indicator
pip3 install -r requirements.txt
python3 fip_indicator.py
```
## Configuration

* Set your spotify user name in [settings.yaml](https://github.com/feeloow/fip-indicator/blob/master/settings.yaml)
* Connect spotify through menu


## Known bugs
- [ ] App may loose track
- [ ] Quit menu not working 

## Roadmap / Wish List
- [ ] Support [new endpoints](https://www.fip.fr/latest/api/graphql?operationName=Now&variables=%7B%22bannerPreset%22%3A%22600x600-noTransform%22%2C%22stationId%22%3A64%2C%22previousTrackLimit%22%3A3%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%228a931c7d177ff69709a79f4c213bd2403f0c11836c560bc22da55628d8100df8%22%7D%7D)
- [ ] Setup script
- [ ] Show edition year 
- [ ] Link to album infos
- [ ] Display Disc Cover
- [x] Search on Spotify
- [x] Add on Spotify
- [ ] Play Station locally
- [ ] Launch Station on Alexa device
- [ ] Track on last.fm
- [ ] Download as mp3
