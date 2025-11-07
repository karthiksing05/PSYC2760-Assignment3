import os
import random
import subprocess

WORDS = ["pabiku", "tibudo", "lagome"]
SYLLABLES = ["pa", "bi", "ku", "ti", "bu", "do", "la", "go", "me"]

def generate_audio_with_say(text, output_file):
    subprocess.run(["say", "-v", "Samantha", "-r", "120", text, "-o", output_file])

def generate_familiarization(words, duration_seconds=130, output_file="familiarization.wav"):
    """Create a 2-minute familiarization stream of fake words."""
    sequence = []
    while len(" ".join(sequence)) < duration_seconds * 10:
        sequence.append(random.choice(words))
    text = " ".join(sequence)

    print("Generating familiarization audio (this may take ~1 minute)...")
    temp_aiff = "familiarization.aiff"
    generate_audio_with_say(text, temp_aiff)

    subprocess.run(["ffmpeg", "-y", "-i", temp_aiff, "-t", str(duration_seconds), output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(temp_aiff)
    print(f"✅ Familiarization audio saved as {output_file}")

def generate_test_stimulus(word, output_file, length):
    text = " ".join([word] * length)
    temp_aiff = output_file.replace(".wav", ".aiff")
    generate_audio_with_say(text, temp_aiff)
    subprocess.run(["ffmpeg", "-y", "-i", temp_aiff, output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(temp_aiff)
    print(f"Test stimulus saved as {output_file}")

def main():
    generate_familiarization(WORDS, 120, "familiarization.wav")

    old_word = random.choice(WORDS)
    generate_test_stimulus(old_word, "old.wav", 350)

    new_word = "".join(random.sample(SYLLABLES, 3))
    while new_word in WORDS:
        new_word = "".join(random.sample(SYLLABLES, 3))
    generate_test_stimulus(new_word, "new.wav", 350)

    print(f"\nOld word used: {old_word}")
    print(f"New (nonexistent) word: {new_word}")

if __name__ == "__main__":
    main()
