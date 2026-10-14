"""Executable semantic-address and transport mapping subset for RFC-047/RFC-059."""
from __future__ import annotations

import re
from urllib.parse import quote, unquote

_ENTITY = re.compile(r"[A-Z][A-Za-z0-9]*\Z")
_ACTION = re.compile(r"[a-z0-9-]+\Z")
_STATE = re.compile(r"(?:requested|accepted|completed|failed|rejected|cancelled|x-[a-z0-9-]+)\Z")
_FORBIDDEN = set("* >+#/\\\\\t\r\n")


class InvalidSemanticAddress(ValueError):
    pass


def validate_address(address: str) -> str:
    if not isinstance(address, str) or not address or not address.isascii():
        raise InvalidSemanticAddress("address must be non-empty ASCII")
    if len(address.encode("ascii")) > 192:
        raise InvalidSemanticAddress("address exceeds 192 octets")
    if any(ch in _FORBIDDEN or ch.isspace() for ch in address):
        raise InvalidSemanticAddress("address contains a forbidden transport character")
    parts = address.split(".")
    if len(parts) != 3:
        raise InvalidSemanticAddress("address must contain exactly three dot-separated components")
    entity, action, state = parts
    if not 1 <= len(entity) <= 64 or not _ENTITY.fullmatch(entity):
        raise InvalidSemanticAddress("invalid entity component")
    if not 1 <= len(action) <= 64 or not _ACTION.fullmatch(action):
        raise InvalidSemanticAddress("invalid action component")
    if not 1 <= len(state) <= 64 or not _STATE.fullmatch(state):
        raise InvalidSemanticAddress("invalid state component")
    return address


def to_nats_subject(address: str) -> str:
    return validate_address(address)


def from_nats_subject(subject: str) -> str:
    return validate_address(subject)


def to_mqtt_topic(address: str) -> str:
    return validate_address(address).replace(".", "/")


def from_mqtt_topic(topic: str) -> str:
    if not isinstance(topic, str) or topic.count("/") != 2 or "." in topic:
        raise InvalidSemanticAddress("MQTT topic is not a reversible semantic-address mapping")
    return validate_address(topic.replace("/", "."))


def to_http_path(address: str) -> str:
    return "/v1/events/" + quote(validate_address(address), safe=".-")


def from_http_path(path: str) -> str:
    prefix = "/v1/events/"
    if not isinstance(path, str) or not path.startswith(prefix):
        raise InvalidSemanticAddress("HTTP path does not use the semantic event endpoint")
    encoded = path[len(prefix):]
    decoded = unquote(encoded, errors="strict")
    if "/" in decoded or quote(decoded, safe=".-") != encoded:
        raise InvalidSemanticAddress("HTTP path encoding is ambiguous or non-canonical")
    return validate_address(decoded)


def to_kafka_headers(address: str) -> dict[str, bytes]:
    return {"ubiq-name": validate_address(address).encode("ascii")}


def from_kafka_headers(headers: dict[str, bytes]) -> str:
    value = headers.get("ubiq-name")
    if not isinstance(value, bytes):
        raise InvalidSemanticAddress("Kafka ubiq-name header must be bytes")
    try:
        address = value.decode("ascii")
    except UnicodeDecodeError as exc:
        raise InvalidSemanticAddress("Kafka semantic address must be ASCII") from exc
    return validate_address(address)
