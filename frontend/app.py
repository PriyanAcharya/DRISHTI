import streamlit as st
import json
import os
import plotly.graph_objects as go

st.set_page_config(
    page_title="DRISHTI",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ DRISHTI")
st.subheader("Adaptive Variable-Resolution 2.5D LiDAR Mapping")

# --------------------------------------------------
# FIND PROJECT ROOT
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

FRAME_FILES = [
    "frame_001_output.json",
    "frame_002_output.json",
    "frame_003_output.json"
]


# --------------------------------------------------
# LOAD FRAME
# --------------------------------------------------

def load_frame(filename):
    possible_paths = [
        os.path.join(PROJECT_ROOT, filename),
        os.path.join(PROJECT_ROOT, "person2_detection", filename)
    ]

    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)

    return None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("🎞️ Frame Selection")

selected_frame = st.sidebar.selectbox(
    "Select LiDAR Frame",
    FRAME_FILES
)

data = load_frame(selected_frame)

if data is None:
    st.error(f"{selected_frame} could not be found.")
    st.stop()

detections = data.get("detections", [])


# --------------------------------------------------
# SYSTEM STATUS
# --------------------------------------------------

st.header("📊 System Status")

high_risk = sum(
    1 for d in detections
    if d.get("risk_level", "").upper() == "HIGH"
)

medium_risk = sum(
    1 for d in detections
    if d.get("risk_level", "").upper() == "MEDIUM"
)

low_risk = sum(
    1 for d in detections
    if d.get("risk_level", "").upper() == "LOW"
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Frame",
    data.get("frame_id", selected_frame)
)

c2.metric(
    "Detected Objects",
    len(detections)
)

c3.metric(
    "High Risk",
    high_risk
)

c4.metric(
    "Medium Risk",
    medium_risk
)


# --------------------------------------------------
# 3D MAP
# --------------------------------------------------

st.header("🌐 2.5D LiDAR Environment")

fig = go.Figure()

for detection in detections:

    position = detection.get("position", {})

    x = position.get("x", 0)
    y = position.get("y", 0)
    z = position.get("z", 0)

    object_id = detection.get("object_id", "Unknown")
    class_name = detection.get("class_name", "Unknown")

    distance_data = detection.get("distance", {})
    distance = distance_data.get("xy", 0)

    risk = detection.get("risk_level", "UNKNOWN")
    resolution = detection.get(
        "recommended_resolution",
        "UNKNOWN"
    )

    confidence = detection.get(
        "confidence",
        0
    )

    # Bigger marker = higher recommended resolution
    if resolution.upper() == "HIGH":
        marker_size = 20
    elif resolution.upper() == "MEDIUM":
        marker_size = 15
    else:
        marker_size = 10

    label = (
        f"{class_name}<br>"
        f"{object_id}<br>"
        f"Distance: {distance:.2f} m<br>"
        f"Risk: {risk}<br>"
        f"Resolution: {resolution}"
    )

    fig.add_trace(
        go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode="markers+text",
            text=[class_name],
            textposition="top center",
            hovertext=[label],
            hoverinfo="text",
            marker=dict(
                size=marker_size,
                symbol="circle"
            ),
            name=class_name
        )
    )

    # Add a vertical line from ground to object
    fig.add_trace(
        go.Scatter3d(
            x=[x, x],
            y=[y, y],
            z=[0, z],
            mode="lines",
            showlegend=False,
            hoverinfo="skip"
        )
    )


# Add sensor/reference point
fig.add_trace(
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode="markers+text",
        text=["LiDAR"],
        textposition="bottom center",
        marker=dict(
            size=12,
            symbol="diamond"
        ),
        name="LiDAR Sensor"
    )
)


fig.update_layout(
    height=650,
    scene=dict(
        xaxis_title="X (meters)",
        yaxis_title="Y (meters)",
        zaxis_title="Elevation Z (meters)",
        camera=dict(
            eye=dict(
                x=1.6,
                y=1.6,
                z=1.2
            )
        )
    ),
    margin=dict(
        l=0,
        r=0,
        t=30,
        b=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# DETECTED OBJECTS
# --------------------------------------------------

st.header("🎯 Detected Objects")

table_data = []

for detection in detections:

    position = detection.get("position", {})
    distance = detection.get("distance", {})

    table_data.append({
        "Object ID": detection.get(
            "object_id",
            "-"
        ),

        "Class": detection.get(
            "class_name",
            "-"
        ),

        "Distance (m)": round(
            distance.get("xy", 0),
            2
        ),

        "Confidence": round(
            detection.get(
                "confidence",
                0
            ),
            2
        ),

        "Motion": round(
            detection.get(
                "motion_score",
                0
            ),
            2
        ),

        "Risk": detection.get(
            "risk_level",
            "-"
        ),

        "Resolution": detection.get(
            "recommended_resolution",
            "-"
        ),

        "X": round(
            position.get("x", 0),
            2
        ),

        "Y": round(
            position.get("y", 0),
            2
        ),

        "Z": round(
            position.get("z", 0),
            2
        )
    })


st.dataframe(
    table_data,
    use_container_width=True
)


# --------------------------------------------------
# OBJECT DETAILS
# --------------------------------------------------

st.header("🔎 Object Details")

if detections:

    object_names = [
        d.get(
            "object_id",
            "Unknown"
        )
        for d in detections
    ]

    selected_object = st.selectbox(
        "Select detected object",
        object_names
    )

    selected_data = next(
        d for d in detections
        if d.get("object_id") == selected_object
    )

    st.json(selected_data)


# --------------------------------------------------
# ADAPTIVE RESOLUTION
# --------------------------------------------------

st.header("⚡ Adaptive Resolution")

resolution_counts = {}

for detection in detections:

    resolution = detection.get(
        "recommended_resolution",
        "UNKNOWN"
    )

    resolution_counts[resolution] = (
        resolution_counts.get(
            resolution,
            0
        ) + 1
    )


r1, r2, r3 = st.columns(3)

r1.metric(
    "HIGH Resolution",
    resolution_counts.get(
        "HIGH",
        0
    )
)

r2.metric(
    "MEDIUM Resolution",
    resolution_counts.get(
        "MEDIUM",
        0
    )
)

r3.metric(
    "LOW Resolution",
    resolution_counts.get(
        "LOW",
        0
    )
)


# --------------------------------------------------
# ADAPTIVE DECISION SUMMARY
# --------------------------------------------------

st.header("🧠 Adaptive Decision Summary")

for detection in detections:

    object_id = detection.get(
        "object_id",
        "Unknown"
    )

    class_name = detection.get(
        "class_name",
        "Unknown"
    )

    risk = detection.get(
        "risk_level",
        "UNKNOWN"
    )

    resolution = detection.get(
        "recommended_resolution",
        "UNKNOWN"
    )

    distance = detection.get(
        "distance",
        {}
    ).get("xy", 0)

    st.write(
        f"**{object_id} ({class_name})** → "
        f"Distance: **{distance:.2f} m** | "
        f"Risk: **{risk}** | "
        f"Resolution: **{resolution}**"
    )


st.caption(
    "Visualization uses the team's JSON detection output. "
    "Current JSON data represents prototype/simulated frames."
)