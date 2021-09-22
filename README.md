## About League of Scrapers
League of Scrapers is a REST API that scrapes the web in order to find useful information about League of Legends matches. Information are gathered by scraping op.gg using Selenium.

### API Endpoints
 * /counters/<string:champion>: returns the 3 best counters for the given champion
 * /winrates/<string:champion>: returns all the matchup stats (winrate, number of recorded matches) recorded for the given champion
 * /roles/<string:role>: returns all champions and their winrates for a specific role (bot, support, mid, jungle, top)
 * /build/<string:champion>: returns the graphic icons (64x64) of the items to build for a given champion divided in starter items, main items and boots
