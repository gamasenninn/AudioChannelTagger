# Audio Channel Tagger

## Overview
The Audio Channel Tagger is a Python script designed to analyze stereo audio files and corresponding WEBVTT files to determine which channel (left or right) is dominant in each segment of the audio. This tool is particularly useful for applications such as audio transcription, where identifying the predominant channel can enhance the accuracy of the transcription process.

## Features
- Load and split stereo audio files into left and right channels.
- Detect non-silent segments in each audio channel.
- Read and process WEBVTT files to align audio segments with text.
- Calculate the duration of non-silent audio within specified time ranges.
- Determine the dominant audio channel (left or right) for each segment.
- Output results in a structured DataFrame.

## Requirements
- Python 3.x
- `pandas` library
- `pydub` library

## Installation
Ensure you have Python 3 installed on your system. You can install the required libraries using pip:

```
pip install pandas pydub
```

## Usage
The script can be run from the command line by providing the paths to the audio file and the corresponding WEBVTT file:

```
python ch_tagger.py <audio_file_path> <webvtt_file_path>
```

Replace `<audio_file_path>` and `<webvtt_file_path>` with the actual paths to your audio file and WEBVTT file, respectively.

## Example
```
python ch_tagger.py my_audio.m4a my_transcript.vtt
```

## Output
The script outputs a DataFrame with the following columns:

- Start Time: The starting time of the audio segment in milliseconds.
- End Time: The ending time of the audio segment in milliseconds.
- Channel: The dominant audio channel for the segment ('L' for left, 'R' for right, or 'None').
- TimeStamp: The original timestamp from the WEBVTT file.
- Content: The corresponding text content from the WEBVTT file.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


