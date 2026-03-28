"""Standalone Decoder Wizard - run independently of the bridge.

Usage: python3 decoder_standalone.py [--port 5001]
"""

import argparse
from flask import Flask, render_template_string, jsonify, request
import json
import os
from pathlib import Path

app = Flask(__name__, static_folder="static")

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BLE Decoder Wizard</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>

<header>
  <h1>BLE <span>Decoder</span> Wizard</h1>
  <div>Standalone Mode</div>
</header>

<div style="padding: 24px; max-width: 1200px; margin: 0 auto;">

  <div class="card">
    <h3>Load Capture</h3>
    <p style="color: var(--text2); margin-bottom: 12px;">
      Load a JSON capture file to begin mapping byte fields.
    </p>
    <button class="btn" onclick="loadCaptureFromFile()">Load Capture File</button>
    <button class="btn secondary" onclick="loadSample()">Load Sample Data</button>
  </div>

  <!-- Packet Header -->
  <div class="wizard-panel">
    <h3>Packet View</h3>
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
      <button class="btn small secondary" onclick="prevPacket()">◀ Prev</button>
      <span id="packet-counter">No packets loaded</span>
      <button class="btn small secondary" onclick="nextPacket()">Next ▶</button>
    </div>
    <div id="packet-view"></div>
  </div>

  <!-- Byte Diff -->
  <div class="wizard-panel">
    <h3>Byte Diff (changes highlighted)</h3>
    <div id="diff-view"></div>
  </div>

  <!-- Field Definitions -->
  <div class="wizard-panel">
    <h3>Field Definitions</h3>
    <p style="color: var(--text2); margin-bottom:8px; font-size:0.85rem;">
      Click a field row to select it, then click bytes in the hex view to set start/end positions.
    </p>
    <table class="field-table">
      <thead>
        <tr>
          <th>Name</th><th>Start</th><th>End</th><th>Type</th>
          <th>Scale</th><th>Unit</th><th>Preview</th><th></th>
        </tr>
      </thead>
      <tbody id="field-table-body"></tbody>
    </table>
    <div style="margin-top:12px; display:flex; gap:8px;">
      <button class="btn secondary" onclick="addField()">+ Add Field</button>
      <button class="btn secondary" onclick="testDecode()">Test Decode</button>
    </div>
  </div>

  <!-- Test Results -->
  <div class="wizard-panel">
    <h3>Test Decode Results</h3>
    <div id="test-results" style="overflow-x:auto;"></div>
  </div>

  <!-- Generate Template -->
  <div class="card">
    <h3>Generate Template</h3>
    <div class="form-row">
      <div class="form-group">
        <label>Template ID</label>
        <input id="tpl-id" placeholder="my_device">
      </div>
      <div class="form-group">
        <label>Name</label>
        <input id="tpl-name" placeholder="My Device">
      </div>
      <div class="form-group">
        <label>Manufacturer</label>
        <input id="tpl-manufacturer" placeholder="Brand">
      </div>
      <div class="form-group">
        <label>Model</label>
        <input id="tpl-model" placeholder="Model X">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>Characteristic UUID</label>
        <input id="tpl-characteristic" placeholder="0000xxxx-0000-1000-8000-00805f9b34fb">
      </div>
      <div class="form-group">
        <label>&nbsp;</label>
        <button class="btn" onclick="generateTemplate()">Download Template JSON</button>
      </div>
    </div>
  </div>

</div>

<div class="toast-container"></div>

<script src="/static/app.js"></script>
<script>
  window._templates = [];

  function loadSample() {
    const packets = [];
    // Generate sample Temtop-like packets for demo
    for (let i = 0; i < 10; i++) {
      const bytes = new Array(49).fill(0);
      // PM1.0 at bytes 20-21
      bytes[20] = 0; bytes[21] = 10 + i;
      // PM2.5 at bytes 22-23
      bytes[22] = 0; bytes[23] = 15 + i * 2;
      // PM10 at bytes 24-25
      bytes[24] = 0; bytes[25] = 25 + i * 3;
      // Temp at bytes 26-27 (signed, 245 = 24.5C)
      bytes[26] = 0; bytes[27] = 245 + i;
      // Humidity at bytes 28-29 (450 = 45.0%)
      bytes[28] = 1; bytes[29] = 194 + i * 5;

      packets.push({
        ts: (i * 3).toFixed(3),
        char: '00010203-0405-0607-0809-0a0b0c0d2b10',
        hex: bytes.map(b => b.toString(16).padStart(2, '0')).join(''),
        dec: bytes,
      });
    }
    loadCapture({ mac: 'AA:BB:CC:DD:EE:FF', ble_name: 'SAMPLE', packets: packets });
    toast('Sample data loaded', 'success');
  }
</script>

</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


@app.route("/api/templates", methods=["GET"])
def get_templates():
    return jsonify({"templates": []})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standalone BLE Decoder Wizard")
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    print(f"Decoder Wizard running at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=True)
