import json
import os

import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DRISHTI - LiDAR Visualization",
    page_icon="📡",
    layout="wide",
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# FIND FRAME JSON FILES
# ============================================================

POSSIBLE_LOCATIONS = [
    PROJECT_ROOT,
    os.path.join(PROJECT_ROOT, "person2_detection"),
]

FRAME_FILES = {}

for location in POSSIBLE_LOCATIONS:
    for frame_name in [
        "frame_001_output.json",
        "frame_002_output.json",
        "frame_003_output.json",
    ]:
        file_path = os.path.join(location, frame_name)

        if os.path.exists(file_path):
            FRAME_FILES[frame_name] = file_path


# ============================================================
# HELPER FUNCTION
# ============================================================

def load_json(file_path):
    """Load JSON data from a file."""

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# HEADER
# ============================================================

st.title("Adaptive Variable-Resolution 2.5D LiDAR Mapping")

st.caption(
    "DRISHTI - Dynamic Environment Perception and Adaptive Visualization"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Frame Selection")

if not FRAME_FILES:

    st.sidebar.error("No frame JSON files found.")

    st.error(
        "No frame output JSON files were found in the project directory."
    )

    st.stop()


frame_names = sorted(FRAME_FILES.keys())

selected_frame = st.sidebar.selectbox(
    "Select LiDAR Frame",
    frame_names,
)


selected_file = FRAME_FILES[selected_frame]


# ============================================================
# LOAD SELECTED FRAME
# ============================================================

try:

    data = load_json(selected_file)

except Exception as error:

    st.error(f"Unable to load JSON file: {error}")

    st.stop()


detections = data.get("detections", [])


if not isinstance(detections, list):
    detections = []


# ============================================================
# BASIC COUNTS
# ============================================================

total_objects = len(detections)

high_risk = 0
medium_risk = 0
low_risk = 0

high_resolution = 0
medium_resolution = 0
low_resolution = 0


for detection in detections:

    risk_level = detection.get(
        "risk_level",
        "LOW"
    )

    if isinstance(risk_level, str):
        risk_level = risk_level.upper()

    if risk_level == "HIGH":
        high_risk += 1

    elif risk_level == "MEDIUM":
        medium_risk += 1

    else:
        low_risk += 1


    resolution = detection.get(
        "recommended_resolution",
        "LOW"
    )

    if isinstance(resolution, str):
        resolution = resolution.upper()

    if resolution == "HIGH":
        high_resolution += 1

    elif resolution == "MEDIUM":
        medium_resolution += 1

    else:
        low_resolution += 1


# ============================================================
# SYSTEM STATUS
# ============================================================

st.subheader("System Status")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Frame",
        selected_frame.replace("_output.json", "")
    )


with col2:
    st.metric(
        "Detected Objects",
        total_objects
    )


with col3:
    st.metric(
        "High Risk Objects",
        high_risk
    )


with col4:
    st.metric(
        "High Resolution",
        high_resolution
    )


# ============================================================
# INTEGRATION STATUS
# ============================================================

st.subheader("Integration Status")

col1, col2, col3 = st.columns(3)


with col1:
    st.success("Detection\nConnected")


with col2:
    st.success("Tracking & Risk\nConnected")


with col3:
    st.success("Adaptive Resolution\nConnected")


# ============================================================
# 2.5D / 3D ENVIRONMENT VISUALIZATION
# ============================================================

st.subheader("2.5D LiDAR Environment")


fig = go.Figure()


# ------------------------------------------------------------
# OBJECT MARKERS
# ------------------------------------------------------------

for detection in detections:

    position = detection.get("position", {})

    x = position.get("x", 0)
    y = position.get("y", 0)
    z = position.get("z", 0)

    object_id = detection.get(
        "object_id",
        "Unknown"
    )

    class_name = detection.get(
        "class_name",
        "Unknown"
    )

    confidence = detection.get(
        "confidence",
        0
    )

    distance_data = detection.get(
        "distance",
        {}
    )

    if isinstance(distance_data, dict):

        distance = distance_data.get(
            "xy",
            distance_data.get("3d", 0)
        )

    else:

        distance = distance_data


    risk_level = detection.get(
        "risk_level",
        "UNKNOWN"
    )

    resolution = detection.get(
        "recommended_resolution",
        "UNKNOWN"
    )


    # Marker size based on resolution

    if resolution == "HIGH":
        marker_size = 18

    elif resolution == "MEDIUM":
        marker_size = 14

    else:
        marker_size = 10


    fig.add_trace(
        go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],

            mode="markers+text",

            text=[class_name],

            textposition="top center",

            marker=dict(
                size=marker_size,
                symbol="circle",
            ),

            name=str(object_id),

            hovertemplate=(
                "<b>%{text}</b><br>"
                "Object ID: " + str(object_id) + "<br>"
                "X: " + f"{x:.2f}" + "<br>"
                "Y: " + f"{y:.2f}" + "<br>"
                "Z: " + f"{z:.2f}" + "<br>"
                "Distance: " + f"{distance:.2f}" + " m<br>"
                "Confidence: " + f"{confidence:.2f}" + "<br>"
                "Risk: " + str(risk_level) + "<br>"
                "Resolution: " + str(resolution) +
                "<extra></extra>"
            ),
        )
    )


    # --------------------------------------------------------
    # VERTICAL LINE FROM GROUND TO OBJECT
    # --------------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=[x, x],
            y=[y, y],
            z=[0, z],

            mode="lines",

            line=dict(
                width=4
            ),

            showlegend=False,

            hoverinfo="skip",
        )
    )


# ============================================================
# LiDAR SENSOR REFERENCE
# ============================================================

fig.add_trace(
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],

        mode="markers+text",

        text=["LiDAR Sensor"],

        textposition="bottom center",

        marker=dict(
            size=8,
            symbol="diamond",
        ),

        name="LiDAR Sensor",
    )
)


# ============================================================
# GRAPH LAYOUT
# ============================================================

fig.update_layout(
    scene=dict(
        xaxis_title="X Position (m)",
        yaxis_title="Y Position (m)",
        zaxis_title="Height Z (m)",

        aspectmode="auto",
    ),

    height=600,

    margin=dict(
        l=0,
        r=0,
        t=20,
        b=0,
    ),

    legend=dict(
        orientation="h",
    ),
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# DETECTED OBJECTS
# ============================================================

st.subheader("Detected Objects")


table_rows = []


for detection in detections:

    position = detection.get(
        "position",
        {}
    )

    distance_data = detection.get(
        "distance",
        {}
    )

    if isinstance(distance_data, dict):

        distance = distance_data.get(
            "xy",
            distance_data.get("3d", 0)
        )

    else:

        distance = distance_data


    motion_data = detection.get(
        "motion",
        {}
    )

    if not isinstance(motion_data, dict):
        motion_data = {}


    risk_data = detection.get(
        "risk",
        {}
    )

    if not isinstance(risk_data, dict):
        risk_data = {}


    speed = motion_data.get(
        "speed",
        detection.get("speed", "N/A")
    )


    risk_score = risk_data.get(
        "risk_score",
        detection.get("risk_score", "N/A")
    )


    table_rows.append(
        {
            "Object ID": detection.get(
                "object_id",
                "Unknown"
            ),

            "Class": detection.get(
                "class_name",
                "Unknown"
            ),

            "Distance (m)": (
                round(distance, 2)
                if isinstance(distance, (int, float))
                else distance
            ),

            "Confidence": detection.get(
                "confidence",
                "N/A"
            ),

            "Speed": (
                round(speed, 2)
                if isinstance(speed, (int, float))
                else speed
            ),

            "Risk": detection.get(
                "risk_level",
                risk_data.get(
                    "risk_level",
                    "N/A"
                )
            ),

            "Risk Score": (
                round(risk_score, 2)
                if isinstance(risk_score, (int, float))
                else risk_score
            ),

            "Resolution": detection.get(
                "recommended_resolution",
                "N/A"
            ),
        }
    )


if table_rows:

    st.dataframe(
        table_rows,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("No detected objects in this frame.")


# ============================================================
# OBJECT DETAILS
# ============================================================

st.subheader("Object Details")


if detections:

    object_options = [
        detection.get(
            "object_id",
            f"Object {index + 1}"
        )
        for index, detection in enumerate(detections)
    ]


    selected_object_id = st.selectbox(
        "Select Object",
        object_options,
    )


    selected_object = None


    for detection in detections:

        if detection.get("object_id") == selected_object_id:

            selected_object = detection
            break


    if selected_object is not None:

        st.json(selected_object)


else:

    st.info("No object details available.")


# ============================================================
# MOTION & RISK
# ============================================================

st.subheader("Motion & Risk")


if detections:

    for detection in detections:

        object_id = detection.get(
            "object_id",
            "Unknown"
        )

        class_name = detection.get(
            "class_name",
            "Unknown"
        )


        motion = detection.get(
            "motion",
            {}
        )

        if not isinstance(motion, dict):
            motion = {}


        risk = detection.get(
            "risk",
            {}
        )

        if not isinstance(risk, dict):
            risk = {}


        speed = motion.get(
            "speed",
            "N/A"
        )

        direction = motion.get(
            "direction",
            "N/A"
        )

        risk_score = risk.get(
            "risk_score",
            detection.get(
                "risk_score",
                "N/A"
            )
        )

        ttc = risk.get(
            "ttc",
            "N/A"
        )

        risk_level = detection.get(
            "risk_level",
            risk.get(
                "risk_level",
                "N/A"
            )
        )


        with st.expander(
            f"{object_id} - {class_name}"
        ):

            col1, col2, col3, col4 = st.columns(4)


            with col1:

                if isinstance(speed, (int, float)):

                    st.metric(
                        "Speed",
                        f"{speed:.2f} m/s"
                    )

                else:

                    st.metric(
                        "Speed",
                        str(speed)
                    )


            with col2:

                if isinstance(direction, (int, float)):

                    st.metric(
                        "Direction",
                        f"{direction:.1f}°"
                    )

                else:

                    st.metric(
                        "Direction",
                        str(direction)
                    )


            with col3:

                if isinstance(risk_score, (int, float)):

                    st.metric(
                        "Risk Score",
                        f"{risk_score:.2f}"
                    )

                else:

                    st.metric(
                        "Risk Score",
                        str(risk_score)
                    )


            with col4:

                st.metric(
                    "Risk Level",
                    str(risk_level)
                )


            if isinstance(ttc, (int, float)):

                st.write(
                    f"**Time to Collision (TTC):** {ttc:.2f} seconds"
                )

            else:

                st.write(
                    "**Time to Collision (TTC):** "
                    + str(ttc)
                )


else:

    st.info("No motion or risk information available.")


# ============================================================
# ADAPTIVE RESOLUTION
# ============================================================

st.subheader("Adaptive Resolution")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "HIGH",
        high_resolution
    )


with col2:

    st.metric(
        "MEDIUM",
        medium_resolution
    )


with col3:

    st.metric(
        "LOW",
        low_resolution
    )


resolution_rows = []


for detection in detections:

    resolution = detection.get(
        "recommended_resolution",
        "N/A"
    )


    resolution_m = detection.get(
        "resolution_m",
        "N/A"
    )


    resolution_rows.append(
        {
            "Object ID": detection.get(
                "object_id",
                "Unknown"
            ),

            "Recommended Resolution": resolution,

            "Resolution Size (m)": (
                round(resolution_m, 2)
                if isinstance(
                    resolution_m,
                    (int, float)
                )
                else resolution_m
            ),
        }
    )


if resolution_rows:

    st.dataframe(
        resolution_rows,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# WHY PANEL
# ============================================================

st.subheader("Why Adaptive Resolution?")


for detection in detections:

    object_id = detection.get(
        "object_id",
        "Unknown"
    )

    class_name = detection.get(
        "class_name",
        "Unknown"
    )

    resolution = detection.get(
        "recommended_resolution",
        "N/A"
    )

    risk_level = detection.get(
        "risk_level",
        "N/A"
    )


    position = detection.get(
        "position",
        {}
    )


    distance_data = detection.get(
        "distance",
        {}
    )


    if isinstance(distance_data, dict):

        distance = distance_data.get(
            "xy",
            distance_data.get("3d", "N/A")
        )

    else:

        distance = distance_data


    if resolution == "HIGH":

        explanation = (
            "High resolution is being used for this object "
            "in the current adaptive output."
        )

    elif resolution == "MEDIUM":

        explanation = (
            "Medium resolution is being used for this object "
            "in the current adaptive output."
        )

    elif resolution == "LOW":

        explanation = (
            "Low resolution is being used for this object "
            "in the current adaptive output."
        )

    else:

        explanation = (
            "Resolution information is not available "
            "in the current output."
        )


    with st.expander(
        f"{object_id} - Why {resolution} Resolution?"
    ):

        st.write(
            f"**Object:** {class_name}"
        )

        if isinstance(distance, (int, float)):

            st.write(
                f"**Distance:** {distance:.2f} m"
            )

        else:

            st.write(
                f"**Distance:** {distance}"
            )


        st.write(
            f"**Risk Level:** {risk_level}"
        )

        st.write(
            f"**Recommended Resolution:** {resolution}"
        )

        st.info(explanation)


# ============================================================
# ADAPTIVE DECISION SUMMARY
# ============================================================

st.subheader("Adaptive Decision Summary")


st.write(
    "The adaptive-resolution system assigns different "
    "resolution levels to detected regions instead of "
    "using one uniform resolution everywhere."
)


summary_col1, summary_col2, summary_col3 = st.columns(3)


with summary_col1:

    st.metric(
        "High Resolution Regions",
        high_resolution
    )


with summary_col2:

    st.metric(
        "Medium Resolution Regions",
        medium_resolution
    )


with summary_col3:

    st.metric(
        "Low Resolution Regions",
        low_resolution
    )


# ============================================================
# ARCHITECTURE
# ============================================================

st.subheader("DRISHTI Processing Pipeline")


st.markdown(
    """
### LiDAR Input
↓  
### 2.5D Mapping
↓  
### Object Detection
↓  
### Tracking & Motion
↓  
### Risk Assessment
↓  
### Adaptive Resolution
↓  
### Adaptive 2.5D Map
↓  
### Visualization Dashboard
"""
)


# ============================================================
# DATA SOURCE NOTE
# ============================================================

st.info(
    "Prototype note: the currently available frame JSON files "
    "contain simulated/prototype detection outputs. "
    "The dashboard is designed to visualize structured outputs "
    "from the integrated DRISHTI pipeline."
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "DRISHTI | Adaptive Variable-Resolution 2.5D LiDAR Mapping"
)