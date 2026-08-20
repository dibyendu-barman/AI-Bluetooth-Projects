import json
import os
from datetime import datetime

from google import genai


# ============================================================
# AI MUSIC & AUDIO ANALYZER
# STEP 18B - AI MUSIC INTERPRETATION
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 18B - AI MUSIC INTERPRETATION")
print("=" * 70)


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = os.path.join(
    "reports",
    "music_feature_summary.json"
)

OUTPUT_JSON = os.path.join(
    "reports",
    "music_ai_interpretation.json"
)

OUTPUT_TEXT = os.path.join(
    "reports",
    "music_ai_interpretation.txt"
)

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# CHECK GEMINI API KEY
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("\n❌ GEMINI_API_KEY not found.")
    print("\nSet your API key in PowerShell:")
    print('$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"')
    exit()

print("\n✅ Gemini API key detected.")


# ============================================================
# CHECK FEATURE FILE
# ============================================================

if not os.path.exists(INPUT_FILE):

    print("\n❌ Feature summary not found.")
    print(f"Expected: {INPUT_FILE}")

    print("\nRun Step 18A first:")
    print("python .\\music_feature_summary.py")

    exit()

print("✅ Feature package found.")


# ============================================================
# LOAD FEATURE PACKAGE
# ============================================================

try:

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        features = json.load(file)

    print("✅ Feature package loaded.")

except Exception as error:

    print("\n❌ Failed to load feature package.")
    print(f"Error: {error}")
    exit()


# ============================================================
# CREATE AI PROMPT
# ============================================================

prompt = f"""
You are an AI music analysis assistant.

Analyze the measured audio features below and create a
professional interpretation for an engineering/project report.

IMPORTANT RULES:

1. Use only the supplied measurements.
2. Do not invent the artist, song genre, instruments,
   vocals, lyrics, recording location, or production history.
3. Clearly distinguish measured facts from interpretation.
4. Treat the estimated musical key as an estimate.
5. Do not call the project health score an industry-standard
   audio quality measurement.
6. Explain important measurements in simple technical language.
7. Keep the response professional and concise.
8. Return ONLY valid JSON.
9. Do not use Markdown code fences.

Return exactly this JSON structure:

{{
    "track_summary": "",
    "sound_character": "",
    "frequency_analysis": "",
    "rhythm_analysis": "",
    "harmonic_analysis": "",
    "technical_quality": "",
    "key_observation": "",
    "important_findings": [],
    "limitations": [],
    "overall_interpretation": ""
}}

Measured feature data:

{json.dumps(features, indent=4)}
"""


# ============================================================
# CONNECT TO GEMINI
# ============================================================

try:

    print("\n🤖 Connecting to Gemini...")

    client = genai.Client(
        api_key=api_key
    )

    print("✅ Gemini client initialized.")

except Exception as error:

    print("\n❌ Gemini initialization failed.")
    print(f"Error: {error}")
    exit()


# ============================================================
# SEND FEATURES TO GEMINI
# ============================================================

try:

    print("\n🧠 Sending audio features to Gemini...")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    ai_text = response.text.strip()

    print("✅ AI interpretation received.")

except Exception as error:

    print("\n❌ Gemini API request failed.")
    print(f"Error: {error}")
    exit()


# ============================================================
# CLEAN AI RESPONSE
# ============================================================

if ai_text.startswith("```json"):

    ai_text = ai_text[len("```json"):]

    if ai_text.endswith("```"):
        ai_text = ai_text[:-3]

elif ai_text.startswith("```"):

    ai_text = ai_text[3:]

    if ai_text.endswith("```"):
        ai_text = ai_text[:-3]

ai_text = ai_text.strip()


# ============================================================
# VALIDATE JSON
# ============================================================

try:

    interpretation = json.loads(
        ai_text
    )

    print("✅ AI response validated as JSON.")

except json.JSONDecodeError as error:

    print("\n❌ AI response is not valid JSON.")
    print(f"Error: {error}")

    print("\nRaw AI response:")
    print(ai_text)

    exit()


# ============================================================
# BUILD FINAL RESULT
# ============================================================

result = {

    "project":
        "AI Music & Audio Analyzer",

    "step":
        "18B",

    "model":
        MODEL_NAME,

    "generated_at":
        datetime.now().isoformat(),

    "source_feature_file":
        "music_feature_summary.json",

    "measured_features":
        features,

    "ai_interpretation":
        interpretation
}


# ============================================================
# SAVE JSON REPORT
# ============================================================

try:

    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n✅ AI JSON report saved.")

except Exception as error:

    print("\n❌ Failed to save JSON report.")
    print(f"Error: {error}")
    exit()


# ============================================================
# SAVE HUMAN-READABLE REPORT
# ============================================================

try:

    with open(
        OUTPUT_TEXT,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "AI MUSIC & AUDIO ANALYZER\n"
        )

        file.write(
            "STEP 18B - AI MUSIC INTERPRETATION\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        sections = [
            (
                "TRACK SUMMARY",
                "track_summary"
            ),
            (
                "SOUND CHARACTER",
                "sound_character"
            ),
            (
                "FREQUENCY ANALYSIS",
                "frequency_analysis"
            ),
            (
                "RHYTHM ANALYSIS",
                "rhythm_analysis"
            ),
            (
                "HARMONIC ANALYSIS",
                "harmonic_analysis"
            ),
            (
                "TECHNICAL QUALITY",
                "technical_quality"
            ),
            (
                "KEY OBSERVATION",
                "key_observation"
            ),
            (
                "OVERALL INTERPRETATION",
                "overall_interpretation"
            )
        ]

        for title, key in sections:

            file.write(
                title + "\n"
            )

            file.write(
                "-" * 70 + "\n"
            )

            file.write(
                interpretation.get(
                    key,
                    ""
                )
            )

            file.write(
                "\n\n"
            )


        file.write(
            "IMPORTANT FINDINGS\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        for item in interpretation.get(
            "important_findings",
            []
        ):

            file.write(
                f"- {item}\n"
            )


        file.write(
            "\nLIMITATIONS\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        for item in interpretation.get(
            "limitations",
            []
        ):

            file.write(
                f"- {item}\n"
            )


    print(
        "✅ Human-readable AI report saved."
    )

except Exception as error:

    print(
        "\n❌ Failed to create text report."
    )

    print(
        f"Error: {error}"
    )

    exit()


# ============================================================
# DISPLAY AI INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("AI MUSIC INTERPRETATION")
print("=" * 70)


display_sections = [
    (
        "Track Summary",
        "track_summary"
    ),
    (
        "Sound Character",
        "sound_character"
    ),
    (
        "Frequency Analysis",
        "frequency_analysis"
    ),
    (
        "Rhythm Analysis",
        "rhythm_analysis"
    ),
    (
        "Harmonic Analysis",
        "harmonic_analysis"
    ),
    (
        "Technical Quality",
        "technical_quality"
    ),
    (
        "Key Observation",
        "key_observation"
    ),
    (
        "Overall Interpretation",
        "overall_interpretation"
    )
]


for title, key in display_sections:

    print(
        f"\n{title}:"
    )

    print(
        interpretation.get(
            key,
            ""
        )
    )


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 18B RESULT")
print("=" * 70)

print("✅ Feature package loaded.")
print("✅ Gemini AI connected.")
print("✅ Audio features sent to AI.")
print("✅ AI interpretation generated.")
print("✅ AI response validated.")
print("✅ Structured AI JSON generated.")
print("✅ Human-readable AI report generated.")

print("\nSaved files:")

print(
    f"   {OUTPUT_JSON}"
)

print(
    f"   {OUTPUT_TEXT}"
)

print("\n🎵 STEP 18B COMPLETE")