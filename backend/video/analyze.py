# analyze_video.py - uses llava:7b through ollama to analyze the decoded frames of the video. is prompted to give overall feedback.

import ollama 

def analyze_video_general(frames_filepaths, sport:str, fight_type:str):
    response = ollama.chat(
        model='llava:7b',
        messages=[{
            'role':'user',

            'content':(
                f"You are an expert {sport} coach analyzing {fight_type} footage. "
                f"These images are sequential frames from one amateur {sport} bout. "
                "Identify each fighter by their glove, headgear, elbow pad, and shin guard color.\n\n"

                "Provide a structured analysis:\n\n"

                "1. FIGHTER IDENTIFICATION:"
                "Describe each fighter by glove, headgear, elblow pad, or shin guard color.\n\n"

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

def analyze_video_specific(frames_filepaths, sport:str, fight_type:str):
    response = ollama.chat(
        model='llava:7b',
        messages=[{
            'role':'user',

            'content':
                f"You are assisting a {sport} coach reviewing {fight_type} footage. This is a single still frame "
                f"from a {sport} bout. Two fighters are present, identified ONLY by glove color "
                "(e.g. 'Red Gloves', 'Blue Gloves').\n\n"
                "Describe ONLY what is visibly happening in THIS frame. Do not infer intent, prior action, "
                "or outcomes. If something is unclear or out of frame, say so — do not guess.\n\n"
                "Report the following in short bullet points:\n"
                "1. Stance and position of each fighter (orthodox/southpaw if visible, distance between them, "
                "ring position if visible).\n"
                "2. Guard and hand position of each fighter (high, low, hands down, hands extended).\n"
                "3. Any strike being thrown or landing in this frame — name the strike only if clearly "
                "identifiable (jab, cross, lead/rear roundhouse, teep, knee, elbow, clinch). If unclear, "
                "say 'strike unclear.'\n"
                "4. Weight distribution and balance if visible (loaded on lead leg, squared up, off-balance).\n"
                "5. One visible technical observation per fighter — strength OR weakness — based STRICTLY on "
                "this frame (e.g. 'Red Gloves' rear hand is dropped below chin'). If nothing notable is "
                "visible, write 'no clear observation.'\n\n"
                "Be concise. Do not invent details. Do not give overall fight feedback — only this frame.",

            'images': frames_filepaths

        }]
    )

    return response['message']['content']