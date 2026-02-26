# analyze_video.py - uses llava:7b through ollama to analyze the decoded frames of the video. is prompted to give overall feedback.

import ollama 

def analyze_video_general(frames_filepaths):
    response = ollama.chat(
        model='llava:7b',
        messages=[{
            'role':'user',

            'content':"You are an experienced Muay Thai kickboxing coach. You will analyze ~50 images, all still frames from one"
            " Muay Thai kickboxing fight, then give feedback on each fighter's overall strength and weaknesses. Next, give feedback "
            "as to what each fighter could do to improve for their next fight. Identify each fighter by the color of their "
            "kickboxing gloves. This fight is held under the amateur muay thai ruleset.",

            'images': frames_filepaths
        }]
    )

    return response['message']['content']

def analyze_video_specific(frames_filepaths):
    response = ollama.chat(
        model='llava:7b',
        messages=[{
            'role':'user',

            'content':"You are an experienced Muay Thai kickboxing coach. You will analyze ~50 images, all still frames from a clip from"
            "a Muay Thai kickboxing fight. You will first give each fighter's overall strengths and weaknesses. Next, you will give"
            "feedback as to what each fighter could do to improve for their next fight. Identify each fighter by the color of their"
            "kickboxing gloves. This fight is held under the amateur muay thai ruleset.",

            'images': frames_filepaths

        }]
    )

    return response['message']['content']