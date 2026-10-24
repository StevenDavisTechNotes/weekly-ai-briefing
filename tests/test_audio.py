from weekly_ai_briefing.config import MAX_BITRATE_KBPS, MIN_BITRATE_KBPS
from weekly_ai_briefing.email_briefing.audio import choose_bitrate_kbps


def test_short_audio_uses_max_bitrate():
    assert choose_bitrate_kbps(10 * 60) == MAX_BITRATE_KBPS


def test_long_audio_lowers_bitrate():
    assert MIN_BITRATE_KBPS < choose_bitrate_kbps(4 * 3600) < MAX_BITRATE_KBPS


def test_very_long_audio_floors_at_min_bitrate():
    assert choose_bitrate_kbps(100 * 3600) == MIN_BITRATE_KBPS
