from pathlib import Path
import sys
from steven_melina import RESPONSE_DELIMITER, SPEAKER_DELIMITER, SPEAKER_VOICES
import text_to_audio

log_file = Path(__file__).parent / "gpt_usage_last_conver.txt"

with open(log_file, "r") as file:
    log_data = file.read()

log_strings = log_data.split(RESPONSE_DELIMITER)
processed_logs_1 = []
for string in log_strings:
    if string == "":
        continue
    else:
        # string = string.strip()
        processed_logs_1.append(string)

speakers_strings = []
responses = []

for log_string in processed_logs_1:
    processed_log = log_string.split(SPEAKER_DELIMITER)
    speakers_strings.append(processed_log[0])
    responses.append(processed_log[1])

speakers = []
for speaker in speakers_strings:
    if speaker.strip() == "Talker_Steven:":
        speakers.append(SPEAKER_VOICES[0])


    elif speaker.strip() == "Talker_Melina:":
        speakers.append(SPEAKER_VOICES[1])

    else:
        raise ValueError("Speaker not recognized")

for i, response in enumerate(responses):
    text_to_audio.main(response, speakers[i], counter=i)
    print(f"Speech{i}.mp3 created")