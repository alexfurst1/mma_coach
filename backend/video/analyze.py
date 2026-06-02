import ollama 
import time

def full_batch_analysis(divided_frames:dict, sport:str, fight_type:str):
    divided_responses = []
    t0 = time.time()
    for batch, frames_list in divided_frames.items():
        t1 = time.time()
        divided_responses.append(analyze_video_general_batch(frames_list, sport, fight_type))
        print(f"llava {batch} time: {time.time() - t1:.1f}s")
    print(f'total llava time: {time.time() - t0:.1f}s')

    all_batches = "\n\n".join(
        f"=== BATCH {idx} ANALYSIS ===\n{response}"
        for idx, response in enumerate(divided_responses)
    )
    
    t0_2nd = time.time()
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{
            'role':'user',

            'content': (
            f"You are an expert {sport} coach writing the final fight report for a {fight_type}. "
            f"Below are separate technical analyses of consecutive short segments of the footage, "
            f"each produced from a small sequence of video frames. There are {len(divided_responses)} "
            f"segments total, presented in chronological order — segment 1 is the start of the footage, "
            f"the final segment is the end.\n\n"

            f"{all_batches}\n\n"

            f"Your job is to synthesize these per-segment analyses into ONE cohesive whole-fight report. "
            f"Do not simply restate each segment. Instead, reason ACROSS the segments to identify patterns, "
            f"changes, and trends over the course of the fight. Because the segments are in chronological "
            f"order, you can track how the fight develops from start to finish.\n\n"

            "Write the report in this structure:\n\n"

            "1. FIGHTER OVERVIEW\n"
            "   Identify each fighter using the consistent labels from the segment analyses "
            "   (e.g. 'Red Gloves', 'Blue Gloves'). Give a one-line summary of each fighter's overall showing. "
            "   If the segments label the fighters inconsistently, reconcile them as best you can and note it.\n\n"

            "2. FIGHT NARRATIVE\n"
            "   Describe how the fight developed from the early segments to the late ones. "
            "   Who controlled the early going? Did momentum shift at any point? "
            "   Note where in the footage the pattern clearly changed.\n\n"

            "3. EACH FIGHTER'S STRENGTHS\n"
            "   For each fighter, what did they consistently do well across multiple segments? "
            "   Prioritize patterns that show up in several segments over one-off moments in a single segment.\n\n"

            "4. EACH FIGHTER'S WEAKNESSES\n"
            "   For each fighter, what technical errors or openings recurred across segments? "
            "   Note whether a weakness was present throughout the footage or appeared only as the fight went on.\n\n"

            "5. CONDITIONING AND PACING\n"
            "   Based on how each fighter looked from the early segments to the late ones, did anyone fade, "
            "   slow down, or get hurt as the fight progressed? Did anyone pace themselves well?\n\n"

            "6. ACTIONABLE IMPROVEMENTS\n"
            "   Give each fighter 3-4 specific drills or adjustments to work on before their next "
            f"   {fight_type}, based on the weaknesses that showed up most consistently.\n\n"

            f"Keep the analysis specific, technical, and appropriate to {sport}. "
            f"If the segment analyses disagree or are unclear about something, say so rather than guessing. "
            f"Base everything only on what the segment analyses report — do not invent events that aren't mentioned."
        )
        }]
    )

    print(f"llama call time: {time.time() - t0_2nd:.1f}s")
    print(f"total analysis time: {time.time()-t0:.1f}s")
    return response['message']['content']

def analyze_video_general_batch(frames_filepaths: list, sport:str, fight_type:str):
    response = ollama.chat(
        model='llava:7b',
        messages=[{
        'role': 'user',
        'content': (
            f"You are an expert {sport} coach analyzing {fight_type} footage. "
            f"These images are a SHORT SEQUENCE of up to 10 frames sampled roughly 3 seconds apart, "
            f"covering only about 20-30 seconds from within a {sport} {fight_type}. "
            f"This is a small segment of the footage — NOT the whole fight. "
            f"Describe only what is visible in these specific frames.\n\n"

            f"Identify each fighter by their visible gear — glove color, shorts/trunks, and any of the following "
            f"that apply to {sport} and are visible in {fight_type}: headgear, elbow pads, shin guards. "
            f"For padwork, distinguish the striker from the pad holder. "
            f"Use consistent labels (e.g. 'Red Gloves', 'Blue Gloves') so this segment can be matched "
            f"to other segments later.\n\n"

            "Provide a structured analysis of THIS SEGMENT ONLY:\n\n"

            "1. FIGHTER IDENTIFICATION\n"
            f"   Describe each fighter (or striker and pad holder, if this is padwork) by their visible gear and clothing. "
            f"   Only reference gear that actually exists in {sport} and is visible in {fight_type} "
            f"   (e.g., no shin guards in boxing, no headgear in a professional bout).\n\n"

            "2. WHAT HAPPENS IN THESE FRAMES\n"
            f"   Describe the action across this short sequence in order — what each fighter does from the "
            f"   first frame to the last. Name strikes only if clearly identifiable and legal in {sport} "
            f"   (punches, and where applicable kicks, knees, elbows, clinch strikes). "
            f"   If the action is unclear in a frame, say so rather than guessing.\n\n"

            "3. TECHNICAL OBSERVATIONS\n"
            f"   For each fighter, note what is visible in these frames, relevant to {sport}:\n"
            "   - Stance and guard position\n"
            "   - Striking technique and mechanics on any strikes thrown\n"
            f"   - Grappling or clinch work if {sport} allows it and it appears here\n"
            "   - Defensive actions (blocks, parries, slips, checks, distance management — whichever apply)\n"
            f"   - Footwork and ring/cage control (or positioning relative to the pad holder, if this is padwork)\n\n"

            "4. NOTABLE STRENGTHS OR ERRORS\n"
            "   - Any technique executed well in this segment.\n"
            "   - Any visible error or opening left (dropped hands, square hips, lazy returns, off-balance).\n"
            "   - If nothing notable is visible, say so plainly.\n\n"

            f"Be specific and technical, and keep your analysis appropriate to {sport} and {fight_type}. "
            f"You may reference frame order (e.g. 'early frames show X, later frames show Y'). "
            f"Do NOT summarize the whole fight, do NOT judge who is winning, and do NOT "
            f"speculate about anything outside these {len(frames_filepaths)} frames — you are only seeing a small slice of the footage.\n\n"
            f"LENGTH REQUIREMENT: Keep your entire response under 150 words. Use short bullet fragments, "
            f"not full paragraphs. Skip sections where you have nothing notable to report rather than padding. "
            f"Brevity matters more than completeness."
        ),
    'images': frames_filepaths
    }],
    options={"num_predict":300}
    )
    
    print(f"length of response: {len(response['message']['content'].split())}")
    print(response['message']['content'])
    return response['message']['content']

def analyze_video_specific(frames_filepaths, sport:str, fight_type:str):
    t0 = time.time()
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

    print(f"Time for specific analysis: {time.time() - t0:.1f}s")
    print(len(response['message']['content'].split()))
    print(response['message']['content'])
    return response['message']['content']