# 🔴 Discord Bot - Your All-in-One Server Solution

<div align="center">
  
[![Discord](https://img.shields.io/badge/Discord-Bot-red?style=for-the-badge&logo=discord)](https://discord.com)
[![Python](https://img.shields.io/badge/Python-3.8+-red?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)

**Transform your Discord server with powerful moderation, entertainment, and utility features!**

[Features](#-features) • [Installation](#-installation) • [Commands](#-commands) • [Support](#-support)

</div>

---

## 🚀 Why Choose Our Bot?

This comprehensive Discord bot is designed to be your **ultimate server companion**. Whether you're running a small community or a large server, our bot provides all the tools you need to manage, entertain, and engage your members.

### ✨ What Makes Us Different?

- 🛡️ **Professional Moderation** - Keep your server safe and organized
- 🎵 **Music Integration** - Entertainment for your voice channels
- 🎮 **Interactive Games** - Keep your community engaged
- 🎫 **Ticket System** - Professional support management
- 📊 **Level Tracking** - Reward active members
- ⚡ **Lightning Fast** - Optimized performance
- 🔧 **Highly Customizable** - Tailor it to your needs

---

## 🎯 Features

### 🛡️ Moderation Tools
Keep your server safe and organized with powerful moderation commands:
- **Kick/Ban/Unban** - Manage problematic members
- **Mute/Unmute** - Timeout system for temporary restrictions
- **Warn** - Issue warnings to members
- **Clear** - Bulk delete messages
- **Slowmode** - Control chat speed

### 🎵 Music Player
Bring life to your voice channels:
- **Play/Pause/Resume** - Control playback
- **Skip** - Move to the next song
- **Queue** - View upcoming tracks
- **Volume Control** - Adjust playback volume
- **Now Playing** - See current track info

### 🎮 Fun Games
Engage your community with interactive games:
- **8-Ball** - Ask the magic 8-ball
- **Trivia** - Test your knowledge
- **Rock Paper Scissors** - Classic game
- **Number Guessing** - Challenge yourself
- **Dice Rolling** - Random number generation
- **Coin Flip** - Make decisions easy

### 🎫 Ticket System
Professional support management:
- **Create Tickets** - Open support requests
- **Close Tickets** - Archive resolved issues
- **Claim Tickets** - Staff can claim tickets
- **User Management** - Add/remove users from tickets

### 🎭 Fun Commands
Keep your server entertaining:
- **Jokes** - Random humor
- **Facts** - Interesting trivia
- **Memes** - Shareable content
- **Ship** - Compatibility calculator
- **Rate** - Rate anything out of 10
- **ASCII Art** - Text-based art

### 📊 Level System
Reward active members:
- **XP Tracking** - Earn experience for activity
- **Levels** - Automatic level progression
- **Leaderboard** - See top members
- **Rank Cards** - View your stats
- **Admin Controls** - Manage user XP

### 🔧 Utility Commands
Essential tools for every server:
- **User Info** - Detailed member information
- **Server Info** - Server statistics
- **Avatar** - View user avatars
- **Role Info** - Role details
- **Polls** - Create community polls
- **Reminders** - Never forget important tasks

### ⚙️ Admin Features
Powerful configuration options:
- **Custom Prefix** - Set your own command prefix
- **Welcome Messages** - Greet new members
- **Auto-roles** - Automatic role assignment
- **Role Management** - Create, delete, assign roles
- **Nickname Management** - Control member nicknames

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/discord-bot.git
   cd discord-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and settings
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

### Configuration

Edit `.env` file with your settings:

```env
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
DATABASE_PATH=bot.db
```

---

## 📚 Commands

### Moderation
| Command | Description | Permission |
|---------|-------------|------------|
| `!kick <user> [reason]` | Kick a member | Kick Members |
| `!ban <user> [reason]` | Ban a member | Ban Members |
| `!unban <user_id>` | Unban a user | Ban Members |
| `!mute <user> [duration] [reason]` | Timeout a member | Moderate Members |
| `!unmute <user>` | Remove timeout | Moderate Members |
| `!warn <user> [reason]` | Warn a member | Kick Members |
| `!clear [amount]` | Delete messages | Manage Messages |
| `!slowmode [seconds]` | Set slowmode | Manage Channels |

### Music
| Command | Description |
|---------|-------------|
| `!join` | Join voice channel |
| `!leave` | Leave voice channel |
| `!play <query>` | Play a song |
| `!pause` | Pause playback |
| `!resume` | Resume playback |
| `!stop` | Stop playback |
| `!skip` | Skip current song |
| `!queue` | View queue |
| `!volume [0-100]` | Set volume |
| `!nowplaying` | Current song info |

### Games
| Command | Description |
|---------|-------------|
| `!8ball <question>` | Ask magic 8-ball |
| `!dice [sides]` | Roll a dice |
| `!coinflip` | Flip a coin |
| `!trivia` | Trivia question |
| `!rps <choice>` | Rock Paper Scissors |
| `!guess [max]` | Number guessing game |

### Levels
| Command | Description |
|---------|-------------|
| `!rank [user]` | View rank card |
| `!leaderboard [page]` | Server leaderboard |
| `!givexp <user> <amount>` | Give XP (Admin) |

### Utility
| Command | Description |
|---------|-------------|
| `!userinfo [user]` | User information |
| `!serverinfo` | Server information |
| `!avatar [user]` | User's avatar |
| `!poll <question> <options>` | Create a poll |
| `!reminder <seconds> <message>` | Set a reminder |
| `!botinfo` | Bot statistics |
| `!invite` | Get invite link |

### Admin
| Command | Description | Permission |
|---------|-------------|------------|
| `!setprefix <prefix>` | Set custom prefix | Administrator |
| `!setwelcome <channel> <message>` | Set welcome message | Administrator |
| `!setautorole <role>` | Set auto-role | Administrator |
| `!settings` | View server settings | Administrator |
| `!addrole <user> <role>` | Add role to user | Manage Roles |
| `!removerole <user> <role>` | Remove role from user | Manage Roles |

---

## 🎨 Customization

### Custom Prefix
```
!setprefix ?
```
Changes the bot's command prefix to `?`

### Welcome Messages
```
!setwelcome #welcome Welcome {user} to {server}!
```
Sets up automatic welcome messages in the specified channel.

### Auto-roles
```
!setautorole @Member
```
Automatically assigns the @Member role to new users.

---

## 🛠️ Development

### Project Structure
```
discord-bot/
├── bot.py              # Main bot file
├── cogs/               # Command modules
│   ├── moderation.py   # Moderation commands
│   ├── music.py        # Music commands
│   ├── games.py        # Game commands
│   ├── tickets.py      # Ticket system
│   ├── fun.py          # Fun commands
│   ├── levels.py       # Level tracking
│   ├── utility.py      # Utility commands
│   ├── general.py      # General commands
│   └── admin.py        # Admin commands
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md          # Documentation
```

### Adding New Commands

Commands are organized into cogs. To add a new command:

1. Navigate to the appropriate cog file in `/cogs`
2. Add your command using the `@commands.command()` decorator
3. The bot will automatically load it on restart

Example:
```python
@commands.command(name='mycommand')
async def my_command(self, ctx):
    """Command description"""
    await ctx.send("Hello!")
```

---

## 🔒 Security & Privacy

- ✅ Secure token handling with environment variables
- ✅ Permission-based command access
- ✅ SQLite database for local data storage
- ✅ No data sharing with third parties

---

## 📞 Support

Need help? We're here for you!

- 📖 Check our [documentation](#-commands)
- 💬 Join our [Discord server](#)
- 🐛 Report [issues](https://github.com/yourusername/discord-bot/issues)
- 💡 Suggest [features](https://github.com/yourusername/discord-bot/issues/new)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Inspired by the Discord community
- Thanks to all contributors!

---

<div align="center">

### ⭐ Star us on GitHub!

**Made with ❤️ for the Discord community**

[⬆ Back to Top](#-discord-bot---your-all-in-one-server-solution)

</div>
