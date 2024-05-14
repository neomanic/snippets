#!/bin/bash

# Initialize the concat input list file
concat_file="ffmpeg_concat_script.txt"
echo "" > $concat_file

# Loop over your .mov files, ordered by filename
for f in "$@"; do
    # Use ffprobe to get the video and audio stream index
    video_index=$(ffprobe -v error -select_streams v:0 -show_entries stream=index -of csv=p=0 "$f")
    audio_index=$(ffprobe -v error -select_streams a:0 -show_entries stream=index -of csv=p=0 "$f")
    
    # Check if both audio and video streams are present
    if [[ -z $video_index ]] || [[ -z $audio_index ]]; then
        echo "Warning: Skipping '$f' as it lacks either an audio or video stream."
        continue
    fi
    # Add the file and its stream mappings to the concat file
    echo "file '$f'" >> $concat_file
    echo "stream_map V:$video_index A:$audio_index" >> $concat_file

done

# Now you can run ffmpeg with the generated script
# ffmpeg -f concat -safe 0 -i $concat_file -c copy output.mov


exit 0

# -----------------------------------------------------------
# 2024-03-06T07:20:08    conversation: 01hr9a57dxvrfcw5whpega3sah

Model: **gpt-4-1106-preview**

## Prompt:

show me the ffprobe command to give the stream identifier of the video stream in the file only. be concise

## Response:

To obtain the stream identifier (index) of the video stream(s) in a file using ffprobe, you can use the following command:

```sh
ffprobe -loglevel error -select_streams v:0 -show_entries stream=index -of csv=p=0 input_file
```

Replace `input_file` with the path to your video file.

Explanation of the options:
- `-loglevel error`: This option will only show error messages in the output.
- `-select_streams v:0`: This option specifies that we are looking for the first video stream.
- `-show_entries stream=index`: This option tells ffprobe to show the index of the selected stream.
- `-of csv=p=0`: This sets the output format to CSV (Comma-Separated Values) without printing the section name.

If there are multiple video streams, and you want to get all their indexes, remove the stream specifier `:0` to get the indexes for all video streams:

```sh
ffprobe -loglevel error -select_streams v -show_entries stream=index -of csv=p=0 input_file
```

# 2024-03-06T07:23:31    conversation: 01hr9abdvqe67ffe224kwxpc0v

Model: **gpt-4-1106-preview**

## Prompt:

Given a number of sequential input files, ie 7780.mov, 7781.mov and so on, give the terminal commands to construct an ffmpeg input script file to be passed to ffmpeg -f concat to join them. Use ffprobe to get the index of the video and audio streams which could be either 0 or 1 in any of the files, and use that to construct the stream mapping. Be concise

## Response:

To generate an ffmpeg script file for concatenation using `ffmpeg -f concat`, you would typically create a text file with the format `file 'filename'` for each filename you want to concatenate. However, determining the correct video and audio stream indices for mapping with `ffprobe` complicates the process because you need to analyze the streams of each file.

Here's a concise bash script that illustrates how you might achieve this. This script requires that the files are named sequentially and assumes `.mov` files, but you can adjust the file pattern and extensions as needed.

```bash
#!/bin/bash

# Initialize the concat input list file
concat_file="ffmpeg_concat_script.txt"
echo "" > $concat_file

# Loop over your .mov files, ordered by filename
for f in ./*.mov; do
  
  # Use ffprobe to get the video stream index
  video_index=$(ffprobe -v error -select_streams v:0 -show_entries stream=index -of csv=p=0 "$f")
  
  # Use ffprobe to get the audio stream index
  audio_index=$(ffprobe -v error -select_streams a:0 -show_entries stream=index -of csv=p=0 "$f")
  
  # Add the file and its stream mappings to the concat file
  echo "file '$f'" >> $concat_file
  echo "stream_map V:$video_index A:$audio_index" >> $concat_file
  
done

# Now you can run ffmpeg with the generated script
ffmpeg -f concat -safe 0 -i $concat_file -c copy output.mov
```

Please make sure that the script file is executable by running `chmod +x script_name.sh` and then execute it with `./script_name.sh`.

Explanation of the script sections:

- Initializes a text file to hold the concat list.
- Loops through each `.mov` file in the current directory.
- Uses `ffprobe` to find the indices of the first video and audio streams.
- Writes the file and its stream mapping to the concat list.
- The `-safe 0` flag is added to the `ffmpeg` command to allow processing of files with potentially unsafe filenames.
- Assumes that the video and audio stream mappings are consistent across all files.

Make sure that all the input files are of the same format and codecs if you're copying the streams directly with `-c copy`. If they are not, you may have to re-encode them during concatenation by specifying the encoder instead of using `-c copy`.

# 2024-03-06T07:25:35    conversation: 01hr9abdvqe67ffe224kwxpc0v

Model: **gpt-4-1106-preview**

## Prompt:

Modify the script so the list of files is passed as args, so I can use shell wild cards to provide them.

## Response:

You can modify the script to accept a list of files as arguments by using `"$@"` to reference all the arguments passed to the script. Here's a revised version of the script that supports arguments:

```bash
#!/bin/bash

# Check if at least one file is provided
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 ...]"
    exit 1
fi

# Initialize the concat input list file
concat_file="ffmpeg_concat_script.txt"
echo "" > $concat_file

# Process each file provided as an argument
for f in "$@"; do
  
  # Use ffprobe to get the video stream index
  video_index=$(ffprobe -v error -select_streams v:0 -show_entries stream=index -of csv=p=0 "$f")
  
  # Use ffprobe to get the audio stream index
  audio_index=$(ffprobe -v error -select_streams a:0 -show_entries stream=index -of csv=p=0 "$f")

  # Check if both audio and video streams are present
  if [[ -z $video_index ]] || [[ -z $audio_index ]]; then
    echo "Warning: Skipping '$f' as it lacks either an audio or video stream."
    continue
  fi
  
  # Add the file and its stream mappings to the concat file
  echo "file '$f'" >> $concat_file
  echo "stream_map V:$video_index A:$audio_index" >> $concat_file
  
done

# Now you can run ffmpeg with the generated script
ffmpeg -f concat -safe 0 -i $concat_file -c copy output.mov
```

To use this script with shell wildcards, make sure to call the script with the desired pattern, for example:

```bash
./script_name.sh /path/to/files/*.mov
```

Make sure that the script file is executable:

```bash
chmod +x script_name.sh
```

The script checks if at least one file argument is provided, and it now iterates over all arguments instead of a hardcoded file pattern. It has also been modified to gracefully skip files that might lack a video or audio stream, printing a warning message instead of failing.

Please note that if you're handling files with special characters or spaces in the filenames, scanning through each file name with wildcards may require quoting or other shell-specific handling to ensure the filenames are passed correctly to the script.

