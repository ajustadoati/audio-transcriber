# Deployment Guide

## VPS Configuration

### 1. Configure secrets.toml on your VPS

SSH into your VPS and create/update the secrets file:

```bash
ssh user@your-vps
cd /home/ajustado/audio-transcriber
nano .streamlit/secrets.toml
```

Add the following content:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
base_url = "https://qr.ajustadoati.com"
```

**Important**: Make sure `base_url` matches your actual domain (without trailing slash).

### 2. Push changes to GitHub

```bash
git add .
git commit -m "Add shareable audio player functionality"
git push origin main
```

The GitHub Action will automatically:
- Stop the old container
- Build a new image with the `pages/` directory
- Create a persistent volume for `shared_audios/`
- Start the new container

### 3. Test the deployment

1. Go to your app: https://qr.ajustadoati.com
2. Record an audio and transcribe it
3. Copy the share link
4. Open the share link in a new tab
5. You should see the audio player with the transcription

## Persistent Storage

Audio files are stored in `/home/ajustado/audio-transcriber-data` on your VPS, which is mounted into the Docker container at `/app/shared_audios`.

### Access files directly on VPS:

```bash
# View stored audios
ls -la /home/ajustado/audio-transcriber-data

# Delete old files (older than 7 days)
find /home/ajustado/audio-transcriber-data -type f -mtime +7 -delete

# Delete all files
rm -rf /home/ajustado/audio-transcriber-data/*
```

### Backup the data:

```bash
cd /home/ajustado
tar czf audio-backup-$(date +%Y%m%d).tar.gz audio-transcriber-data/
```

### Setup automatic cleanup (optional):

Create a cron job to delete files older than 30 days:

```bash
crontab -e
```

Add this line:

```
0 2 * * * find /home/ajustado/audio-transcriber-data -type f -mtime +30 -delete
```

This will run daily at 2 AM and delete files older than 30 days.

## Troubleshooting

### If the player page doesn't load:

1. Check if the container is running:
   ```bash
   docker ps | grep audio-transcriber
   ```

2. Check container logs:
   ```bash
   docker logs audio-transcriber
   ```

3. Verify the secrets file exists:
   ```bash
   docker exec -it audio-transcriber cat /app/.streamlit/secrets.toml
   ```

4. Check if shared_audios directory exists and has files:
   ```bash
   # From host (outside Docker)
   ls -la /home/ajustado/audio-transcriber-data

   # From inside container
   docker exec -it audio-transcriber ls -la /app/shared_audios
   ```

5. Verify directory permissions:
   ```bash
   ls -ld /home/ajustado/audio-transcriber-data
   # Should be readable/writable
   ```
