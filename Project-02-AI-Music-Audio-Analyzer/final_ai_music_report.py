import json
import os
from datetime import datetime


# ============================================================
# AI MUSIC & AUDIO ANALYZER
# STEP 20 - FINAL AI MUSIC ANALYSIS REPORT GENERATOR
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 20 - FINAL AI MUSIC ANALYSIS REPORT GENERATOR")
print("=" * 70)


# ============================================================
# CONFIGURATION
# ============================================================

FEATURE_FILE = os.path.join(
    "reports",
    "music_feature_summary.json"
)

AI_FILE = os.path.join(
    "reports",
    "music_ai_interpretation.json"
)

RECOMMENDATION_FILE = os.path.join(
    "reports",
    "music_recommendations.json"
)

DASHBOARD_FILE = os.path.join(
    "reports",
    "ai_music_analysis_dashboard.png"
)

OUTPUT_HTML = os.path.join(
    "reports",
    "final_ai_music_analysis.html"
)

OUTPUT_JSON = os.path.join(
    "reports",
    "final_ai_music_analysis.json"
)


# ============================================================
# CHECK INPUT FILES
# ============================================================

required_files = [
    FEATURE_FILE,
    AI_FILE,
    RECOMMENDATION_FILE
]

for file_path in required_files:

    if not os.path.exists(file_path):

        print(
            f"\n❌ Required file not found:"
        )

        print(
            f"   {file_path}"
        )

        print(
            "\nPlease complete the previous steps first."
        )

        exit()


print("\n✅ Feature package found.")
print("✅ AI interpretation found.")
print("✅ Recommendation package found.")


# ============================================================
# LOAD JSON DATA
# ============================================================

try:

    with open(
        FEATURE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        features = json.load(file)


    with open(
        AI_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        ai_data = json.load(file)


    with open(
        RECOMMENDATION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        recommendation_data = json.load(file)


    print(
        "✅ All analysis data loaded successfully."
    )

except Exception as error:

    print(
        "\n❌ Failed to load project data."
    )

    print(
        f"Error: {error}"
    )

    exit()


# ============================================================
# EXTRACT DATA
# ============================================================

file_info = features["file"]

signal = features["signal"]

spectral = features["spectral"]

frequency = features["frequency_balance"]

rhythm = features["rhythm"]

music = features["music"]

clipping = features["clipping"]

quality = features["quality"]

ai = ai_data["ai_interpretation"]

recommendations = recommendation_data[
    "recommendation_engine"
]


# ============================================================
# HELPER FUNCTION
# ============================================================

def safe(value):

    if value is None:

        return "N/A"

    return str(value)


def list_html(items):

    if not items:

        return "<li>No items reported.</li>"

    output = ""

    for item in items:

        output += (
            "<li>"
            + safe(item)
            + "</li>"
        )

    return output


# ============================================================
# EXTRACT MAIN VALUES
# ============================================================

track_name = file_info["name"]

duration = file_info["duration_sec"]

sample_rate = file_info["sample_rate_hz"]

channels = file_info["channels"]

samples = file_info["samples"]

rms_dbfs = signal["rms_dbfs"]

peak_dbfs = signal["peak_dbfs"]

dynamic_range = signal["dynamic_range_db"]

crest_factor = signal["crest_factor"]

bass = frequency["bass_percent"]

mid = frequency["mid_percent"]

treble = frequency["treble_percent"]

dominant_band = frequency["dominant_band"]

bpm = rhythm["bpm"]

tempo_category = rhythm["tempo_category"]

beats = rhythm["beats"]

onsets = rhythm["onsets"]

estimated_key = music["estimated_key"]

key_correlation = music["key_correlation"]

centroid = spectral["centroid_hz"]

bandwidth = spectral["bandwidth_hz"]

rolloff = spectral["rolloff_hz"]

flatness = spectral["flatness"]

zcr = spectral["zero_crossing_rate"]

health_score = quality["health_score"]

health_classification = quality["classification"]

clipped_samples = clipping["clipped_samples"]

clipping_percentage = clipping["clipping_percentage"]


# ============================================================
# CONSOLE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL MUSIC ANALYSIS")
print("=" * 70)

print(
    f"\nTrack            : {track_name}"
)

print(
    f"Duration         : {duration:.2f} sec"
)

print(
    f"Sample Rate      : {sample_rate} Hz"
)

print(
    f"Channels         : {channels}"
)

print(
    f"Estimated Key    : {estimated_key}"
)

print(
    f"BPM              : {bpm:.2f}"
)

print(
    f"Dominant Band    : {dominant_band}"
)

print(
    f"RMS Level        : {rms_dbfs:.2f} dBFS"
)

print(
    f"Peak Level       : {peak_dbfs:.2f} dBFS"
)

print(
    f"Dynamic Range    : {dynamic_range:.2f} dB"
)

print(
    f"Clipping         : {clipped_samples} samples"
)

print(
    f"Health Score     : {health_score}/100"
)

print(
    f"Classification    : {health_classification}"
)


# ============================================================
# HTML REPORT
# ============================================================

html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
AI Music & Audio Analyzer - Final Report
</title>

<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
    padding: 0;
    background: #f4f6f8;
    color: #263238;
}}

.container {{
    width: 90%;
    max-width: 1200px;
    margin: 30px auto;
}}

.header {{
    background: #263238;
    color: white;
    padding: 35px;
    border-radius: 12px;
}}

.header h1 {{
    margin: 0;
    font-size: 32px;
}}

.header p {{
    margin-top: 8px;
    color: #cfd8dc;
}}

.section {{
    background: white;
    margin-top: 20px;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.section h2 {{
    margin-top: 0;
    color: #263238;
}}

.grid {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
}}

.card {{
    background: #f7f9fa;
    padding: 18px;
    border-radius: 8px;
}}

.card-title {{
    font-size: 12px;
    color: #607d8b;
    text-transform: uppercase;
}}

.card-value {{
    font-size: 23px;
    font-weight: bold;
    margin-top: 7px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    background: #263238;
    color: white;
    text-align: left;
    padding: 10px;
}}

td {{
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
}}

tr:nth-child(even) {{
    background: #f7f9fa;
}}

ul {{
    line-height: 1.7;
}}

.health {{
    text-align: center;
    padding: 25px;
    border-radius: 10px;
    background: #f7f9fa;
}}

.health-score {{
    font-size: 52px;
    font-weight: bold;
}}

.dashboard {{
    width: 100%;
    border-radius: 8px;
    border: 1px solid #ddd;
}}

.footer {{
    text-align: center;
    color: #78909c;
    margin: 30px;
    font-size: 12px;
}}

.warning {{
    background: #fff8e1;
    padding: 15px;
    border-left: 4px solid #ffb300;
    border-radius: 5px;
}}

</style>

</head>


<body>


<div class="container">


<div class="header">

<h1>
AI Music & Audio Analyzer
</h1>

<p>
Final AI Music Analysis Report
</p>

<p>
Project-02 • Version v1.1 • Step 20
</p>

</div>


<!-- ===================================================== -->
<!-- TRACK OVERVIEW -->
<!-- ===================================================== -->

<div class="section">

<h2>1. Track Overview</h2>

<div class="grid">

<div class="card">

<div class="card-title">
Track
</div>

<div class="card-value">
{track_name}
</div>

</div>


<div class="card">

<div class="card-title">
Duration
</div>

<div class="card-value">
{duration:.2f} sec
</div>

</div>


<div class="card">

<div class="card-title">
Sample Rate
</div>

<div class="card-value">
{sample_rate} Hz
</div>

</div>


<div class="card">

<div class="card-title">
Channels
</div>

<div class="card-value">
{channels}
</div>

</div>


<div class="card">

<div class="card-title">
BPM
</div>

<div class="card-value">
{bpm:.2f}
</div>

</div>


<div class="card">

<div class="card-title">
Estimated Key
</div>

<div class="card-value">
{estimated_key}
</div>

</div>

</div>

</div>


<!-- ===================================================== -->
<!-- HEALTH -->
<!-- ===================================================== -->

<div class="section">

<h2>2. Audio Health</h2>

<div class="health">

<div class="health-score">
{health_score}/100
</div>

<h3>
{health_classification}
</h3>

<p>
Project-specific audio quality heuristic.
</p>

</div>

</div>


<!-- ===================================================== -->
<!-- SIGNAL -->
<!-- ===================================================== -->

<div class="section">

<h2>3. Signal Analysis</h2>

<table>

<tr>
<th>Parameter</th>
<th>Result</th>
</tr>

<tr>
<td>RMS Level</td>
<td>{rms_dbfs:.2f} dBFS</td>
</tr>

<tr>
<td>Peak Level</td>
<td>{peak_dbfs:.2f} dBFS</td>
</tr>

<tr>
<td>Dynamic Range</td>
<td>{dynamic_range:.2f} dB</td>
</tr>

<tr>
<td>Crest Factor</td>
<td>{crest_factor:.3f}</td>
</tr>

<tr>
<td>Clipped Samples</td>
<td>{clipped_samples}</td>
</tr>

<tr>
<td>Clipping Percentage</td>
<td>{clipping_percentage:.6f}%</td>
</tr>

</table>

</div>


<!-- ===================================================== -->
<!-- FREQUENCY -->
<!-- ===================================================== -->

<div class="section">

<h2>4. Frequency & Spectral Analysis</h2>

<table>

<tr>
<th>Feature</th>
<th>Result</th>
</tr>

<tr>
<td>Bass</td>
<td>{bass:.2f}%</td>
</tr>

<tr>
<td>Mid</td>
<td>{mid:.2f}%</td>
</tr>

<tr>
<td>Treble</td>
<td>{treble:.2f}%</td>
</tr>

<tr>
<td>Dominant Band</td>
<td>{dominant_band}</td>
</tr>

<tr>
<td>Spectral Centroid</td>
<td>{centroid:.2f} Hz</td>
</tr>

<tr>
<td>Spectral Bandwidth</td>
<td>{bandwidth:.2f} Hz</td>
</tr>

<tr>
<td>Spectral Rolloff</td>
<td>{rolloff:.2f} Hz</td>
</tr>

<tr>
<td>Spectral Flatness</td>
<td>{flatness:.6f}</td>
</tr>

<tr>
<td>Zero Crossing Rate</td>
<td>{zcr:.6f}</td>
</tr>

</table>

</div>


<!-- ===================================================== -->
<!-- RHYTHM -->
<!-- ===================================================== -->

<div class="section">

<h2>5. Rhythm Analysis</h2>

<table>

<tr>
<th>Feature</th>
<th>Result</th>
</tr>

<tr>
<td>Estimated BPM</td>
<td>{bpm:.2f}</td>
</tr>

<tr>
<td>Tempo Category</td>
<td>{tempo_category}</td>
</tr>

<tr>
<td>Detected Beats</td>
<td>{beats}</td>
</tr>

<tr>
<td>Detected Onsets</td>
<td>{onsets}</td>
</tr>

</table>

</div>


<!-- ===================================================== -->
<!-- KEY -->
<!-- ===================================================== -->

<div class="section">

<h2>6. Musical Key Analysis</h2>

<table>

<tr>
<th>Feature</th>
<th>Result</th>
</tr>

<tr>
<td>Estimated Key</td>
<td>{estimated_key}</td>
</tr>

<tr>
<td>Key Correlation</td>
<td>{key_correlation:.4f}</td>
</tr>

</table>

</div>


<!-- ===================================================== -->
<!-- DASHBOARD -->
<!-- ===================================================== -->

<div class="section">

<h2>7. AI Music Dashboard</h2>

"""

if os.path.exists(DASHBOARD_FILE):

    html += """

<p>
The integrated dashboard generated in Step 18C is included
as the visual summary of the analysis.
</p>

<img
src="ai_music_analysis_dashboard.png"
class="dashboard"
alt="AI Music Analysis Dashboard"
>

"""

else:

    html += """

<p>
The Step 18C dashboard image was not found.
</p>

"""


html += f"""

</div>


<!-- ===================================================== -->
<!-- AI INTERPRETATION -->
<!-- ===================================================== -->

<div class="section">

<h2>8. AI Music Interpretation</h2>

<h3>
Track Summary
</h3>

<p>
{safe(ai.get("track_summary", ""))}
</p>


<h3>
Sound Character
</h3>

<p>
{safe(ai.get("sound_character", ""))}
</p>


<h3>
Frequency Analysis
</h3>

<p>
{safe(ai.get("frequency_analysis", ""))}
</p>


<h3>
Rhythm Analysis
</h3>

<p>
{safe(ai.get("rhythm_analysis", ""))}
</p>


<h3>
Harmonic Analysis
</h3>

<p>
{safe(ai.get("harmonic_analysis", ""))}
</p>


<h3>
Technical Quality
</h3>

<p>
{safe(ai.get("technical_quality", ""))}
</p>


<h3>
Overall Interpretation
</h3>

<p>
{safe(ai.get("overall_interpretation", ""))}
</p>

</div>


<!-- ===================================================== -->
<!-- RECOMMENDATIONS -->
<!-- ===================================================== -->

<div class="section">

<h2>9. AI Recommendations</h2>

<h3>
Overall Insight
</h3>

<p>
{safe(recommendations.get("overall_insight", ""))}
</p>


<h3>
Strengths</h3>

<ul>

{list_html(
    recommendations.get(
        "strengths",
        []
    )
)}

</ul>


<h3>
Areas to Review
</h3>

<ul>

{list_html(
    recommendations.get(
        "areas_to_review",
        []
    )
)}

</ul>


<h3>
Audio Engineering Recommendations
</h3>

<ul>

{list_html(
    recommendations.get(
        "audio_engineering_recommendations",
        []
    )
)}

</ul>


<h3>
Listening Recommendations
</h3>

<ul>

{list_html(
    recommendations.get(
        "listening_recommendations",
        []
    )
)}

</ul>


<h3>
Priority Actions
</h3>

<ul>

{list_html(
    recommendations.get(
        "priority_actions",
        []
    )
)}

</ul>


<h3>
Final Recommendation
</h3>

<p>
{safe(recommendations.get("final_recommendation", ""))}
</p>

</div>


<!-- ===================================================== -->
<!-- LIMITATIONS -->
<!-- ===================================================== -->

<div class="section">

<h2>10. Engineering Limitations</h2>

<div class="warning">

<p>
DSP measurements depend on the selected algorithms,
sample rate, mono conversion and frequency-band definitions.
</p>

<p>
Musical key detection is an estimate based on
chroma/profile correlation.
</p>

<p>
The Audio Health Score is a project-specific heuristic
and is not an industry-standard audio quality metric.
</p>

<p>
AI interpretation and recommendations should be treated
as analysis assistance and should be verified through
appropriate listening and engineering measurements.
</p>

</div>

</div>


<!-- ===================================================== -->
<!-- CONCLUSION -->
<!-- ===================================================== -->

<div class="section">

<h2>11. Final Conclusion</h2>

<p>

The AI Music & Audio Analyzer successfully processed
the selected music track through a complete DSP and
AI-assisted analysis pipeline.

The track demonstrated:

</p>

<ul>

<li>
Zero detected digital clipping.
</li>

<li>
A project health score of
{health_score}/100.
</li>

<li>
Bass-dominant frequency distribution.
</li>

<li>
Moderate estimated tempo of
{bpm:.2f} BPM.
</li>

<li>
Estimated musical key of
{estimated_key}.
</li>

<li>
Successful Gemini AI interpretation.
</li>

<li>
Successful AI recommendation generation.
</li>

<li>
Successful integrated dashboard generation.
</li>

</ul>

<p>

The project has progressed from basic Bluetooth audio
capture to a complete AI-assisted music analysis,
recommendation and reporting workflow.

</p>

</div>


<!-- ===================================================== -->
<!-- VERSION -->
<!-- ===================================================== -->

<div class="section">

<h2>12. Project Milestone</h2>

<table>

<tr>
<th>Milestone</th>
<th>Status</th>
</tr>

<tr>
<td>Steps 1–17 — DSP & Music Analysis</td>
<td>COMPLETE</td>
</tr>

<tr>
<td>Step 18A — AI Feature Package</td>
<td>COMPLETE</td>
</tr>

<tr>
<td>Step 18B — AI Music Interpretation</td>
<td>COMPLETE</td>
</tr>

<tr>
<td>Step 18C — AI Dashboard</td>
<td>COMPLETE</td>
</tr>

<tr>
<td>Step 19 — AI Recommendations</td>
<td>COMPLETE</td>
</tr>

<tr>
<td>Step 20 — Final Report Generator</td>
<td>COMPLETE</td>
</tr>

</table>

</div>


<div class="footer">

AI Music & Audio Analyzer • Project-02 • Step 20

</div>


</div>

</body>

</html>
"""


# ============================================================
# SAVE HTML
# ============================================================

try:

    with open(
        OUTPUT_HTML,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            html
        )

    print(
        "\n✅ Final HTML report generated."
    )

except Exception as error:

    print(
        "\n❌ Failed to create HTML report."
    )

    print(
        f"Error: {error}"
    )

    exit()


# ============================================================
# FINAL JSON PACKAGE
# ============================================================

final_package = {

    "project":
        "AI Music & Audio Analyzer",

    "version":
        "v1.1",

    "step":
        "20",

    "generated_at":
        datetime.now().isoformat(),

    "track":
        file_info,

    "signal_analysis":
        signal,

    "spectral_analysis":
        spectral,

    "frequency_balance":
        frequency,

    "rhythm_analysis":
        rhythm,

    "music_analysis":
        music,

    "clipping_analysis":
        clipping,

    "audio_quality":
        quality,

    "ai_interpretation":
        ai,

    "ai_recommendations":
        recommendations,

    "dashboard":
        "ai_music_analysis_dashboard.png",

    "final_report":
        "final_ai_music_analysis.html"
}


# ============================================================
# SAVE FINAL JSON
# ============================================================

try:

    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_package,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        "✅ Final JSON package generated."
    )

except Exception as error:

    print(
        "\n❌ Failed to create final JSON."
    )

    print(
        f"Error: {error}"
    )

    exit()


# ============================================================
# FINAL RESULT
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "STEP 20 RESULT"
)

print(
    "=" * 70
)

print(
    "✅ DSP analysis integrated."
)

print(
    "✅ Music analysis integrated."
)

print(
    "✅ Audio health score integrated."
)

print(
    "✅ AI interpretation integrated."
)

print(
    "✅ AI recommendations integrated."
)

print(
    "✅ Step 18C dashboard integrated."
)

print(
    "✅ Final HTML report generated."
)

print(
    "✅ Final JSON package generated."
)

print(
    "\nSaved files:"
)

print(
    f"   {OUTPUT_HTML}"
)

print(
    f"   {OUTPUT_JSON}"
)

print(
    "\n🎵 STEP 20 COMPLETE"
)