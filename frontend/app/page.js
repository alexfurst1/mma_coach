"use client";

import Image from "next/image";
import React, { useEffect, useState } from 'react';

export default function Home() {
  const [file, setFile] = useState(null); // state for uploading files to cloud
  const [dropdownOpen, setDropdownOpen] = useState(false); // state for drop down video list
  const [videos, setVideos] = useState([]); // state (array) for holding all fetched videos
  const [selectedVideo, setSelectedVideo] = useState(null); // state for choosing which video to select
  const [videoUrl, setVideoUrl] = useState(null); // state for holding the current video url to be played

  useEffect(() => {
    fetch('http://localhost:8000/api/videos')
    .then(response => response.json())
    .then(data => setVideos(data));
    }, []
  );

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
      body:JSON.stringify({video_cfkey: selectedVideo.cloudflare_key, video_id: selectedVideo.id})
    });
  }
  
  
  const handleSubmit = async () => {
    if (!file) {
      alert('Select file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file',file);

    const response = await fetch("http://localhost:8000/upload", {
      method: 'POST',
      body: formData
    });

    const result = await response.json();
    console.log(result);

  };
  
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={100}
          height={20}
          priority
        />
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            Hello
          </h1>
          <input type='file' name='input' onChange={(e) => setFile(e.target.files[0])}/>
          <button onClick={handleSubmit}>Upload</button>
          
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
            </div>
          )}
      </main>
    </div>
  );
}
