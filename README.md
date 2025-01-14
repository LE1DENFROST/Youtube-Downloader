### Fixes and Updates (v2025): <br>

1. **Switched from `pytube` to `yt_dlp` for enhanced stability and compatibility.** <br>
   Transitioned to `yt_dlp` to overcome frequent issues and limitations in `pytube`. <br>

2. **Updated `yt_dlp` to the 2025 version for improved performance and bug fixes.** <br>
   Ensures better download handling and added features from the latest release. <br>

3. **Added a batch script to check Python and library dependencies before running the app.** <br>
   Automatically installs missing libraries if not detected. <br>

4. **Implemented `pythonw` for running the application in the background (CMD window closes automatically).** <br>
   Ensures a seamless user experience. <br>

5. **Improved error handling to provide clearer messages for users.** <br>
   Added specific error messages for URL issues, network failures, and other exceptions. <br>

6. **Added support for Turkish characters in the batch script (UTF-8 encoding).** <br>
   Prevents encoding issues in Turkish-based systems. <br>

7. **Cleaned up unnecessary imports and redundant code for better maintainability.** <br>
   Streamlined the codebase by removing unused dependencies. <br>

8. **Ensured directories (`indirilen_mp3`, `indirilen_videolar`) are created if missing.** <br>
   Added checks to avoid folder-related errors during downloads. <br>

9. **Enhanced user feedback and UI messages for a smoother experience.** <br>
   Informative prompts are provided at each step of the process. <br>

10. **Improved overall download performance by leveraging optimized `yt_dlp` configurations.** <br>
    Configured for faster and more reliable downloads. <br>
