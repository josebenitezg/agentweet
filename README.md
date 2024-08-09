# AgenTweet

AgenTweet is an automated tool designed to research the latest scientific papers and share them on Twitter (X).

## Features

- Automatically searches for recent scientific papers
- Analyzes and summarizes paper content
- Posts tweets with paper information and insights
- Customizable search parameters and posting frequency

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/AgenTweet.git
cd AgenTweet
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

- Copy .env.example to .env
- Fill in the required API keys and other configuration details

4. Run the app:

```bash
python main.py
```

### Docker Setup

1. Build the Docker image:

```bash
docker build -t agentweet .
```

2. Run the Docker image:
    
```bash
docker run -d --env-file .env agentweet
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support
If you encounter any problems or have any questions, please open an issue in the GitHub repository.

---
Take inspiration (and some code) from https://github.com/FrancescoSaverioZuppichini/LinkedInGPT