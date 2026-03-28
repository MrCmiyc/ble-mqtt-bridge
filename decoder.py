"""Decoder module - decodes BLE packets using templates."""

from template import Template, TemplateField


def decode_packet(data: bytes, template: Template) -> dict:
    """Decode a raw BLE packet using a template.

    Returns dict with field keys mapped to decoded values.
    """
    return template.decode(data)


def decode_field(data: bytes, field: TemplateField) -> object:
    """Decode a single field from raw bytes."""
    return field.decode(data)


def validate_decode(data: bytes, template: Template) -> dict:
    """Decode and validate - flags implausible values."""
    decoded = template.decode(data)
    validated = {}
    for key, value in decoded.items():
        field = next((f for f in template.fields if f.key == key), None)
        status = "ok"
        if value is None:
            status = "decode_error"
        elif isinstance(value, float):
            if value != value:  # NaN
                status = "nan"
            elif abs(value) > 1e6:
                status = "out_of_range"
        validated[key] = {"value": value, "status": status, "field": field}
    return validated
