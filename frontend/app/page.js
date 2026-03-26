"use client";

import Image from "next/image";
import React, { useState } from 'react';

export default function Home() {
  const [file, setFile] = useState(null);

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
          
          
        </div>
      </main>
    </div>
  );
}
