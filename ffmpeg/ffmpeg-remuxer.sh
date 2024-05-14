#!/bin/bash

# Check if at least one file is provided
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 ...]"
    exit 1
fi

# Process each file passed as an argument
for f in "$@"; do
    # Check whether the file exists
    if [ ! -f "$f" ]; then
        echo "File not found: $f"
        continue
    fi
    
    # Find the first video and audio stream indices using ffprobe
    video_stream_index=$(ffprobe -v error -select_streams v:0 -show_entries stream=index -of default=nw=1:nk=1 "$f")
    audio_stream_index=$(ffprobe -v error -select_streams a:0 -show_entries stream=index -of default=nw=1:nk=1 "$f")

    # Construct the new filename
    remuxed_file="remuxed_$f"
    
    # Remux the file if necessary
    if [ "$video_stream_index" -ne "0" ]; then
        echo "Remuxing $f to ensure video stream is at index 0"
        ffmpeg -i "$f" \
        -map 0:v -map 0:a \
        -c copy \
        -metadata:s:v:0 language=eng \
        -metadata:s:a:0 language=eng \
        "$remuxed_file" && mv "$f" "$f.bak" && mv "$remuxed_file" "$f"
    else
        echo "Video stream is already at index 0 for $f"
    fi
done

echo "Remuxing completed."