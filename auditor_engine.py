import os
import time
from google import genai
from google.genai import types

class MultimodalCodeAuditor:
    def __init__(self, api_key=None):
        self.client= genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))
        self.model= "gemini-2.0-flash"

    def analyse_video_walkthrough(self, video_path):
        print(f"Uploading video file '{video_path}' to Gemini API")

        video_file=self.client.files.upload(file=video_path)
        print(f"Video Uploaded! File URI: {video_file.uri}")

        while video_file.state.name == "PROCESSING":
            print("Waiting for video processing to complete")
            time.sleep(3)
            video_file= self.client.files.get(name=video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(f"Video processing failed: {video_file.error.message}")

        print("Analysing Video Frames & Audio Stream with Gemini 2.0 Flash")

        prompt="""
        You are an elite Senior Staff Engineer performing a Multimodal Code Review and Security Audit on this video walkthrough.

        Perform the following steps carefully:
        1. **Summary of Video Walkthrough**: Briefly summarize what the speaker/video is demonstrating or what bug is being reported.
        2. **Visual Code Extraction**: Identify key code snippets shown on screen during the video.
        3. **Bug & Defect Analysis**: Pinpoint logical errors, race conditions, security vulnerabilities, or anti-patterns shown or spoken about.
        4. **Proposed Fix / Git Diff**: Write a clean, corrected version of the code or a unified Git patch that fixes the issue.

        Format the output clearly using structured Markdown headings.
        """

        response=self.client.models.generate_content(
            model= self.model,
            contents=[video_file, prompt]
        )

        try:
            self.client.files.delete(name=video_file.name)
            print("Cleaned up temporary video file from cloud.")
        except Exception as e:
            print(f"Warning cleaning files: {e}")

        return response.text