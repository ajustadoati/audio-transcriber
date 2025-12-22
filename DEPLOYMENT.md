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

Audio files are stored in a Docker volume named `audio-transcriber-data` which persists across deployments.

To view stored audios on your VPS:

```bash
docker exec -it audio-transcriber ls -la /app/shared_audios
```

To backup the volume:

```bash
docker run --rm -v audio-transcriber-data:/data -v $(pwd):/backup alpine tar czf /backup/audio-backup.tar.gz /data
```

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
   docker exec -it audio-transcriber ls -la /app/shared_audios
   ```
