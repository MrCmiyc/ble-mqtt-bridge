# BLE → MQTT Bridge

Because every BLE device ships with a proprietary app, no API, and just enough documentation to waste your entire weekend.

This fixes that.

---

## What this is

A bridge that:

- Connects to random BLE devices
- Figures out what their packets mean
- Publishes the data to MQTT
- Lets Home Assistant pretend it was supported all along

---

## What this is NOT

- A polished product  
- A beginner-friendly experience  
- Magic  

You will look at hex. You will guess wrong. You will question your life choices.

---

## Why this exists

Because:

- Vendors don't publish protocols  
- Existing tools almost work, but not quite  
- Writing one-off Python decoders for every device is dumb  

So instead:
**we describe the bytes once, in JSON, and move on with our lives.**

---

## The trick

If a device sends data over BLE, it is not special.

It is just bytes.

And bytes can be decoded.

---

## How it works (mentally)

1. Capture packets
2. Stare at them until patterns emerge
3. Map bytes → values
4. Save that as a template
5. Never think about that device again

---

## Decoder Wizard

This is the part that makes the whole thing viable.

Instead of writing code, you:

- click bytes
- assign meaning
- test guesses

It will feel like cheating. That's the point.

---

## Current state

- Works
- Probably breaks in weird edge cases
- Definitely written by someone who got annoyed enough to build it

---

## Usage

check [USAGE.md](USAGE.md) I guess

---

## Contributing

If you have:

- a weird BLE device
- packet captures
- or the patience to decode nonsense

you're already qualified.

---

## Philosophy

If you can capture it, you can decode it.

If you can decode it, you can automate it.

And if a vendor didn't want that to happen, they shouldn't have used BLE.
