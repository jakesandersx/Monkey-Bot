<div align="center">
<h1> Monkey Bot </h1>
</div>


### Monkey Bot is a multi-role discord bot in python that I have worked on/off with for a span of about two years. It includes a wide vartiety of commands including games, clash royale API scraping data, or user / server information. It also tracks message data via MySQL.

# Commands:

### Administrative
- Accounts -> %accounts will show all of the users with their discord account linked to their clash royale account in the server
- Ban -> %ban @User will ban a user from the server
- Clear -> %clear # will delete a specified number of messages from chat
- Data -> %data will send a set of administrative statistics privately to the user
- Kick -> %kick @User will kick a user from the server
- Mute -> %mute @User time will mute a user from chatting for a specified amount of time
- Ping -> %ping will send out a discord alert to users to attack in the clan war (partnered with %link)
- Timeout -> %timeout @User time will not let a user speak in voice chat for a specified amount of time
- Unban -> %unban USERID will unban a user from the server
- Unmute -> %unmute @User will unmute a user from the server

### Games
- Coinflip -> flips a coin
- Rps -> will play rock paper scissors
- 8ball -> %eightball {question} will ask the 8ball a question

### Fun
- Random -> will send something random to the chat
- Song -> will send a random song to the chat

### Using Clash Royale API
- Claninfo -> %claninfo #clantag provides clan information on any given clan
- Deck -> %deck {trophies} {name} retrives a players deck using their in game name and trophy count
- Stats -> stats {trophies} {name} will return some basic stats about any given player
- Leaderboard -> %leaderboard will return a leaderboard of clan war score of any given clan. defaulted to my personal clan
- Attacks -> %attacks will show who still needs to attack in the current clan war, and how many attacks they have left

### Misc
- Credits -> %credits will give credit anyone who helped with this project
- Help -> %help provides a list of all commands. can use %help [commandname] for further description
- Link -> %link [clash royale tag] will connect a player's discord account to their CR account via a .txt file
- Profile -> %profile @User will display a user's server profile
- Serverinfo -> %serverinfo will display information about the current discord server
- Uptime -> %uptime shows how long the bot has currently been online
