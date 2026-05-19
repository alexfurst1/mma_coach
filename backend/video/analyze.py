# analyze_video.py - uses llava:7b through ollama to analyze the decoded frames of the video. is prompted to give overall feedback.

import ollama 

def analyze_video_general(frames_filepaths, sport:str, fight_type:str):
    response = ollama.chat(
        model='llava:7b',
        messages=[{
    'role': 'user',
    'content': (
        f"You are an expert {sport} coach analyzing {fight_type} footage. "
        f"These images are sequential frames from one {sport} {fight_type}, sampled roughly 3 seconds apart, "
        f"so they represent the full arc of the session.\n\n"

        f"Identify each fighter by their visible gear — glove color, shorts/trunks, and any of the following "
        f"that apply to {sport} and are visible in {fight_type}: headgear, elbow pads, shin guards. "
        f"For padwork, distinguish the striker from the pad holder.\n\n"

        "Provide a structured analysis:\n\n"

        "1. FIGHTER IDENTIFICATION\n"
        f"   Describe each fighter (or striker and pad holder, if this is padwork) by their visible gear and clothing. "
        f"   Only reference gear that actually exists in {sport} and is visible in {fight_type} "
        f"   (e.g., no shin guards in boxing, no headgear in a professional bout).\n\n"

        "2. TECHNICAL ASSESSMENT\n"
        f"   For each fighter, evaluate only what is relevant to {sport}:\n"
        "   - Stance and guard position\n"
        f"   - Striking technique appropriate to {sport} (punches, and where applicable kicks, knees, elbows, clinch strikes)\n"
        f"   - Grappling or clinch work if {sport} allows it and it appears in the frames\n"
        "   - Defensive skills (blocks, parries, slips, checks, distance management — whichever apply)\n"
        f"   - Footwork and ring/cage control (or positioning relative to the pad holder, if this is padwork)\n"
        "   - Combinations, timing, and rhythm\n\n"

        "3. STRENGTHS\n"
        "   - What does each fighter do well?\n"
        "   - Which techniques are landing cleanly or being executed with the best mechanics?\n\n"

        "4. WEAKNESSES\n"
        "   - What technical errors appear consistently across frames?\n"
        "   - What openings are being left (dropped hands, square hips, lazy returns, predictable rhythm)?\n\n"

        "5. ACTIONABLE IMPROVEMENTS\n"
        f"   Give 3-4 specific drills or adjustments each fighter should practice before their next {fight_type}.\n\n"

        f"Be specific and technical, and keep your analysis appropriate to {sport} and {fight_type}. "
        "Reference frame patterns when relevant (e.g., 'early frames show X, later frames show Y') "
        "so the feedback is grounded in what is visible."
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
                f"You are assisting a {sport} coach reviewing {fight_type} footage. These are sequential frames "
                f"from a short, localized moment within a {sport} {fight_type} — a single exchange or sequence, "
                f"not the full session. Identify the people in the frames ONLY by visible gear — for a bout or "
                f"sparring, glove color (e.g. 'Red Gloves', 'Blue Gloves'); for padwork, 'Striker' and 'Pad Holder'. "
                f"If gear color is unclear, say so rather than guessing.\n\n"

                "Describe ONLY what is visibly happening across these frames. Do not infer intent, prior action "
                "before the first frame, or outcomes after the last frame. If something is unclear or out of "
                "frame, say so — do not guess.\n\n"

                "Report the following in short bullet points:\n"

                "1. Starting position — at the first frame, describe stance (orthodox/southpaw if visible), "
                f"distance between each person, guard and hand position, and ring/cage position if visible "
                f"(or for padwork, the striker's position relative to the pad holder).\n"

                "2. The exchange itself — describe the sequence of strikes, movement, or actions across the "
                f"frames in order. Name strikes ONLY if clearly identifiable and ONLY if legal in {sport} "
                f"(e.g. jab, cross, hook, uppercut, lead/rear roundhouse, low kick, teep, knee, elbow, clinch "
                f"strike, takedown attempt). If a strike is unclear, say 'strike unclear.' Note who initiated, "
                "who countered, and what landed vs. missed if visible.\n"

                "3. Defensive reactions — for each person, what defensive actions are visible (blocks, parries, "
                "slips, checks, level changes, footwork off the line). Note if defense is absent when a strike "
                "is coming.\n"

                "4. Weight, balance, and footwork through the sequence (loaded on lead leg, squared up, "
                "off-balance, posting on a leg, level change, stepping in/out, pivoting).\n"

                f"5. Sport-specific element if visible — for example, clinch entry and control in Muay Thai, "
                f"kick chambering or check in kickboxing, level change or grappling tie-up in MMA, head movement "
                f"or slip in boxing. Skip if not applicable to {sport} or not visible.\n"

                "6. One technical observation per person — strength OR weakness — grounded in what they did "
                "across this exchange (e.g. 'Red Gloves dropped rear hand after throwing the cross, "
                "leaving the chin exposed'). If nothing notable is visible, write 'no clear observation.'\n\n"

                "7. End state — at the final frame, where is each person, what is their guard doing, and is "
                "either person off-balance, out of position, or reset to a neutral stance.\n\n"

                f"Be concise. Reference frame order when useful (e.g. 'early frames', 'mid-sequence', 'final "
                f"frames'). Do not invent details. Do not give overall {fight_type} feedback — only this "
                f"exchange. Keep all observations appropriate to {sport} (do not reference techniques that are "
                f"illegal or not used in {sport}).",

            'images': frames_filepaths

        }]
    )

    return response['message']['content']