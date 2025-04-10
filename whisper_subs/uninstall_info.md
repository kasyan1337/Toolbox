# Uninstalling Whisper Models

To completely remove the downloaded Whisper models from your system, follow these steps:

## Step 1: Locate the Cache Directory
The Whisper models are typically stored in the cache directory. The default location is:

- `~/.cache/whisper` (Linux/MacOS)
- `/Users/<your-username>/.cache/whisper` (MacOS specific example)

## Step 2: Identify the Model Files
The following model files may be present in the cache directory:

| Model   | Approx. Size |
|---------|--------------|
| `tiny.pt`   | 75 MB       |
| `base.pt`   | 142 MB      |
| `small.pt`  | 462 MB      |
| `medium.pt` | 1.5 GB      |
| `large.pt`  | 2.9 GB      |

## Step 3: Remove the Cache Directory
To delete the models, remove the entire cache directory. Use the following command in your terminal:

```bash
rm -rf ~/.cache/whisper
```