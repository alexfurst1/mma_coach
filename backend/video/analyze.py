# analyze_video.py - uses llava:7b through ollama to analyze the decoded frames of the video. is prompted to give overall feedback.

import ollama 

def analyze_video_general(frames_filepaths):
    response = ollama.chat(
        model='llava:7b',
        messages=[{
            'role':'user',

            'content':(
                "You are an expert Muay Thai coach analyzing sparring footage. "
                "These images are sequential frames from one amateur Muay Thai bout. "
                "Identify each fighter by their glove, headgear, elbow pad, and shin guard color.\n\n"

                "Provide a structured analysis:\n\n"

                "1. FIGHTER IDENTIFICATION:"
                "Describe each fighter by glove, headgear, elblow pad, and shin guard color.\n\n"

                "2. TECHNICAL ASSESSMENT\n"
                "   For each fighter, evaluate:\n"
                "   - Stance and guard position\n"
                "   - Striking technique (jabs, crosses, kicks)\n"
                "   - Defensive skills (blocks, slips, movement)\n"
                "   - Footwork and ring control\n"
                "   - Combinations and timing\n\n"

                "3. STRENGTHS\n"
                "   - What does each fighter do well?\n"
                "   - Which techniques are most effective?\n\n"
                
                "4. WEAKNESSES\n"
                "   - What technical errors appear consistently?\n"
                "   - What openings are being left?\n\n"
                
                "5. ACTIONABLE IMPROVEMENTS\n"
                "   Give 3-4 specific drills or adjustments each fighter should practice before their next bout.\n\n"
                
                "Be specific and technical. Reference frame patterns when relevant (e.g., 'early frames show X, later frames show Y')."
            ),
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