import sys
import pandas as pd
from pydub import AudioSegment, silence

def load_audio_and_split_channels(file_path):
    """Load an audio file and split it into left and right channels."""
    audio = AudioSegment.from_file(file_path)
    return audio.split_to_mono()

def detect_nonsilent_chunks(audio_channel, min_silence_len=1000, silence_thresh=-50):
    """Detect non-silent chunks in an audio channel."""
    return silence.detect_nonsilent(audio_channel, min_silence_len, silence_thresh)

def convert_chunks_to_time_format(chunks):
    """Convert chunk time from milliseconds to seconds."""
    return [(start / 1000, end / 1000) for start, end in chunks]

# Function to convert timestamps to milliseconds
def convert_timestamp_to_milliseconds(timestamp):
    hours, minutes, seconds = [float(part) for part in timestamp.split(':')]
    return int((hours * 3600 + minutes * 60 + seconds) * 1000)

def read_webvtt_content(file_path):
    """Read and return the content of a WEBVTT file."""
    with open(file_path, 'r', encoding="utf8") as file:
        return file.read()

def create_dataframe_from_webvtt(webvtt_content):
    """Create a DataFrame from WEBVTT content with timestamps and contents."""
    df = pd.DataFrame(columns=["Start Time", "End Time", "Channel", "TimeStamp", "Content"])
    current_content = ""
    for line in webvtt_content.split('\n'):
        if '-->' in line:
            if current_content.strip() != "":
                df.at[len(df) - 1, "Content"] = current_content.strip()
                current_content = ""
            start_time, end_time = line.split(' --> ')
            start_ms = convert_timestamp_to_milliseconds(start_time)
            end_ms = convert_timestamp_to_milliseconds(end_time)
            df = df.append({"Start Time": start_ms, "End Time": end_ms, "Channel": None, "TimeStamp": line, "Content": ""}, ignore_index=True)
        else:
            current_content += line + " "
    if current_content.strip() != "":
        df.at[len(df) - 1, "Content"] = current_content.strip()
    return df

def calculate_duration_in_range(chunks, start_ms, end_ms):
    """Calculate the duration of non-silent chunks within a specified time range."""
    duration = 0
    for chunk_start, chunk_end in chunks:
        chunk_start_ms, chunk_end_ms = chunk_start * 1000, chunk_end * 1000
        if chunk_start_ms < end_ms and chunk_end_ms > start_ms:
            overlap_start, overlap_end = max(chunk_start_ms, start_ms), min(chunk_end_ms, end_ms)
            duration += overlap_end - overlap_start
    return duration

def update_dataframe_with_channel(df, nonsilent_left, nonsilent_right):
    """Update DataFrame with the determined channel."""
    for index, row in df.iterrows():
        duration_left = calculate_duration_in_range(nonsilent_left, row['Start Time'], row['End Time'])
        duration_right = calculate_duration_in_range(nonsilent_right, row['Start Time'], row['End Time'])
        channel = 'L' if duration_left > duration_right else 'R' if duration_right > duration_left else 'None'
        df.at[index, 'Channel'] = channel
    return df

# Main execution
def tagging_main(audio_file, webvtt_file):
    left_channel, right_channel = load_audio_and_split_channels(audio_file)
    nonsilent_left = convert_chunks_to_time_format(detect_nonsilent_chunks(left_channel))
    nonsilent_right = convert_chunks_to_time_format(detect_nonsilent_chunks(right_channel))

    webvtt_content = read_webvtt_content(webvtt_file)
    df = create_dataframe_from_webvtt(webvtt_content)
    df = update_dataframe_with_channel(df, nonsilent_left, nonsilent_right)

    return df

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ch_tagger.py <audio_file_path> <webvtt_file_path>")
    else:
        audio_file_path = sys.argv[1]
        webvtt_file_path = sys.argv[2]
        df = tagging_main(audio_file_path, webvtt_file_path)
        print(df)
