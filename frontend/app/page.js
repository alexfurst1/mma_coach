"use client";

import Image from "next/image";
import React, { useEffect, useState } from 'react';

export default function Home() {
  const [file, setFile] = useState(null); // state for uploading files to cloud
  const [dropdownOpen, setDropdownOpen] = useState(false); // state for drop down video list
  const [fightType, setFightType] = useState("")
  const [sport, setSport] = useState("")
  const [videos, setVideos] = useState([]); // state (array) for holding all fetched videos
  const [selectedVideo, setSelectedVideo] = useState(null); // state for choosing which video to select
  const [videoUrl, setVideoUrl] = useState(null); // state for holding the current video url to be displayed
  const [startPos, setStartPos] = useState(0);
  const [endPos, setEndPos] = useState(0);
  const [generalSummaries, setGeneralSummaries] = useState([]);
  const [timestamps, setTimestamps] = useState([]);
  const [selectedSummary, setSelectedSummary] = useState(null);
  const [selectedTimestamp, setSelectedTimestamp] = useState(null);

  useEffect(() => {
    console.log('useEffect triggered for fetching video list')
    fetch('http://localhost:8000/api/videos')
    .then(response => response.json())
    .then(data => setVideos(data));
    }, []
  );

  useEffect(() => {
  if (selectedVideo) {
    console.log('useEffect triggered for selecting video, selectedVideo:', selectedVideo);
    fetch(`http://localhost:8000/getAnalysisGeneral/${selectedVideo.id}`)
      .then(response => response.json())
      .then(data => setGeneralSummaries(data));
    
    fetch(`http://localhost:8000/getAnalysisLocal/${selectedVideo.id}`)
      .then(response => response.json())
      .then(data => setTimestamps(data));
  }
}, [selectedVideo]);  // Runs when selectedVideo changes

  async function handleVideoSelect(video){ // handles which video is currently being displayed
    setSelectedVideo(video)
    setDropdownOpen(false)

    const response = await fetch(`http://localhost:8000/api/videos/${video.id}/url`);
    const data = await response.json();
    setVideoUrl(data.url)
  }

  async function handleGeneralAnalysis() {
    const response = await fetch("http://localhost:8000/api/analyzeGeneral", {
      method:'POST',
      headers:{'Content-Type': 'application/json'},
      body:JSON.stringify({video_cfkey: selectedVideo.cloudflare_key, video_id: selectedVideo.id, sport: selectedVideo.sport, fight_type: selectedVideo.fight_type})
    });
    console.log('Response received:', response.status);

    await response.json()

    const new_response = await fetch(`http://localhost:8000/getAnalysisGeneral/${selectedVideo.id}`)
    const data = await new_response.json()
    setGeneralSummaries(data)
  }

  async function handleLocalAnalysis() {
    console.log("Local analysis button clicked")
    if ((startPos && endPos) && (endPos < Number(selectedVideo.duration)) && (Number(endPos) > Number(startPos))){
      const response = await fetch(`http://localhost:8000/api/analyzeLocal`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body:JSON.stringify({video_cfkey: selectedVideo.cloudflare_key, video_id: selectedVideo.id, startPos: startPos, endPos: endPos, sport: selectedVideo.sport, fight_type:selectedVideo.fight_type})
      });
      console.log('Response received:', response.status);

      await response.json()

      const new_response = await fetch(`http://localhost:8000/getAnalysisLocal/${selectedVideo.id}`)
      const data = await new_response.json()
      setTimestamps(data)
    } else {
      console.log("local analysis failed the if statement.")
    }
  }
  
  
  const handleSubmit = async () => {
    if (!file) {
      alert('Select file first.');
      return;
    }
    if (fightType == "" || sport == ""){
      alert('Select fight type and sport first.');
      return;
    }

    const formData = new FormData();
    formData.append('fight_type',fightType);
    formData.append('sport',sport);
    formData.append('file',file);

    const response = await fetch("http://localhost:8000/upload", {
      method: 'POST',
      body: formData
    });

    console.log('Response received:', response.status);

    await response.json()

    const new_response = await fetch(`http://localhost:8000/api/videos`)
    const data = await new_response.json();
    setVideos(data);
    console.log(data);

  };
  
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col py-32 px-16 bg-white dark:bg-black gap-8">
        <div className="flex-1 flex flex-col gap-6">
          <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
            <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
              MMA Coaching Web App
            </h1>
            <input type='file' name='input' onChange={(e) => setFile(e.target.files[0])}/>
            <button onClick={handleSubmit}><strong>Upload</strong> (must fill out fight type and sport first)</button>
            <select 
              value={fightType} 
              onChange={(e) => setFightType(e.target.value)}
            >
              <option value="" disabled>Select fight type:</option>
              <option value="Spar">Spar</option>
              <option value="Padwork">Padwork</option>
              <option value="Amateur Fight">Amateur Fight</option>
              <option value="Professional Fight">Professional Fight</option>
            </select>

            <select 
              value={sport} 
              onChange={(e) => setSport(e.target.value)}
            >
              <option value="" disabled>Select sport:</option>
              <option value="Muay Thai">Muay Thai</option>
              <option value="MMA">MMA</option>
              <option value="Boxing">Boxing</option>
              <option value="Dutch Kickboxing">Dutch Kickboxing</option>
            </select>
          </div>
          <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
            <button onClick={() => setDropdownOpen(!dropdownOpen)}>
              Select video
            </button>
          </div>
          {dropdownOpen && (
            <div className = 'video_list'>
              this is the video list
              {
                videos.map((video) =>
                <div key={video.id} onClick={() => handleVideoSelect(video)}>
                  {video.cloudflare_key.replace('uploads/','')}
                  </div>
                  )}
            </div>
          )}
          {videoUrl && (
              <div style={{marginTop: '20px'}}>
                <h3>Now Playing: {selectedVideo.cloudflare_key}</h3>
                  <video 
                  src={videoUrl} 
                  controls 
                  width="800"
                  style={{maxWidth: '100%'}}
                >
                  Your browser doesn't support video playback.
                  </video>
                  <button onClick={handleGeneralAnalysis}>Analyze Displayed Video</button>
                  <br />
                  <button onClick={handleLocalAnalysis}>Analyze video within timestamps</button>
                  <br />
                  <label>Start Time: </label>
                    <input 
                      type='number'
                      value={startPos}
                      onChange={(e) => setStartPos(e.target.value)}
                      placeholder='0'
                      />
                    <br />
                    <label>End Time: </label>
                      <input 
                        type='number'
                        value={endPos}
                        onChange={(e) => setEndPos(e.target.value)}
                        placeholder={selectedVideo.duration}
                        />
                </div>
            )}
            </div>
                <div className="flex-1 flex flex-row gap-6 border-l border-gray-300 pl-8">
                  <h2 className="text-2xl font-semibold text-black dark:text-zinc-50">
                    Analyis results will appear here
                  </h2>
                  <br />
                </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">General Summaries</h3>
                  {videoUrl && generalSummaries && generalSummaries.length > 0 && (
                  <div>
                    {generalSummaries.map((summary) => (
                      <div key={summary.id}>
                        <div 
                          onClick={() => setSelectedSummary(
                            selectedSummary?.id === summary.id ? null : summary
                          )}
                          className="cursor-pointer hover:bg-gray-100 p-2 border-b"
                        >
                          <strong>Summary</strong> (click to {selectedSummary?.id === summary.id ? 'hide' : 'show'}) - created on {new Date(summary.created_at).toLocaleString()} 
                        </div>
                        
                        {selectedSummary?.id === summary.id && (
                          <div className="bg-gray-50 p-4 rounded mt-2">
                            <p>{selectedSummary.feedback}</p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div> 

              <div>
                <h3 className="text-xl font-semibold mb-2">Timestamped Summaries</h3>
                  {videoUrl && timestamps && (
                    <div>
                      {videoUrl && timestamps && timestamps.length > 0 && (
                        <div>
                          {timestamps.map((timestamp) => (
                            <div key={timestamp.id}>
                              <div 
                                onClick={() => setSelectedTimestamp(
                                  selectedTimestamp?.id === timestamp.id ? null : timestamp
                                )}
                                className="cursor-pointer hover:bg-gray-100 p-2 border-b"
                              >
                                <strong>{timestamp.t_start_seconds}s - {timestamp.t_end_seconds}</strong> (click to {selectedTimestamp?.id === timestamp.id ? 'hide' : 'show'}) - created on {new Date(timestamp.created_at).toLocaleString()} 
                              </div>

                              {selectedTimestamp?.id === timestamp.id && (
                                <div className="bg-gray-50 p-4 rounded mt-2">
                                  {selectedTimestamp.feedback}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
              </div>
              
        
      </main>
    </div>
  );
}
