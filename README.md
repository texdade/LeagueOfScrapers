## About League of Scrapers
League of Scrapers is a REST API that scrapes the web in order to find useful information about League of Legends matches. Information are gathered by scraping op.gg using Selenium.

### API Endpoints
/counters/<string:champion>: returns the 3 best counters for the given champion
/winrates/<string:champion>: returns all the matchup stats (winrate, number of recorded matches) recorded for the given champion
