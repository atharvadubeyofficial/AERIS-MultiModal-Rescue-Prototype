from config.thresholds import SOS_TRIGGER_FRAME


def get_sos_state(frame_count):
    # Demo event. Replace with LoRa/GPS receiver integration in hardware.
    return frame_count >= SOS_TRIGGER_FRAME
