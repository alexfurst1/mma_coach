# analyze_video.py - uses llava:7b through ollama to analyze the decoded frames of the video. is prompted to give overall feedback.
import ollama 

def analyze_video(frames):
    response = ollama.chat(
        model='llava:7b',
        messages=[{
            'role':'user',
            'content':"You are an experienced mixed martial arts coach. Analyze this fight film, then give feedback on the fighter's overall strength and weaknesses. Next, give feedback as to what the fighter could do to improve for their next fight. ",
            'images':[]
        }]
    )

    return response['message']['content']


