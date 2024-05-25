import os
import subprocess

def compress_video(video_path, output_path):
    full_video_path = os.path.join(os.getcwd(), video_path)
    full_output_path = os.path.join(os.getcwd(), output_path)
    command = f'ffmpeg -i "{full_video_path}" -vcodec libx264 -crf 28 "{full_output_path}"'
    subprocess.call(command, shell=True)

def main():
    video_directory = r"C:\Users\kenne\Videos\Captures"
    os.chdir(video_directory)
    total_files = len([filename for filename in os.listdir(video_directory) if filename.endswith(".mp4") and not filename.endswith("_small.mp4")])
    completed_files = 0
    for filename in os.listdir(video_directory):
        if filename.endswith(".mp4") and not filename.endswith("_small.mp4"):
            compressed_filename = f"{os.path.splitext(filename)[0]}_small.mp4"
            if not os.path.exists(compressed_filename):
                compress_video(filename, compressed_filename)
                completed_files += 1
                print(f"Completed {completed_files} of {total_files} files ({completed_files/total_files*100:.2f}%)")
    print("Compression complete!")

if __name__ == "__main__":
    main()