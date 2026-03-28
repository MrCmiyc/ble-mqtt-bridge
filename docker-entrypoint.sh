#!/bin/bash
set -e

# Apply env vars to bridge.conf at startup
if [[ -f /app/bridge.conf ]]; then
    sed -i "s/^host = .*/host = ${MQTT_HOST:-localhost}/" /app/bridge.conf
    sed -i "s/^port = .*/port = ${MQTT_PORT:-1883}/" /app/bridge.conf
    sed -i "s/^username = .*/username = ${MQTT_USERNAME:-}/" /app/bridge.conf
    sed -i "s/^password = .*/password = ${MQTT_PASSWORD:-}/" /app/bridge.conf
fi

case "${MODE}" in
    bridge)
        exec python ble_mqtt_bridge.py
        ;;
    ui)
        exec python bridge_ui.py
        ;;
    decoder)
        exec python decoder_standalone.py --port 5001
        ;;
    bridge-ui)
        # Run both bridge and UI (default)
        python ble_mqtt_bridge.py &
        exec python bridge_ui.py
        ;;
    *)
        echo "Unknown MODE: ${MODE}"
        echo "Options: bridge, ui, decoder, bridge-ui"
        exit 1
        ;;
esac
