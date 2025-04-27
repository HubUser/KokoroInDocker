from kokoro import KPipeline
import soundfile as sf
import numpy as np
import logging


pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sound(text, output_file, speed=1.0):
    logger.info(f"Generating sound for text: {text}")
    generator = pipeline(text, voice='af_heart', speed=speed)
    segments = [audio for _, _, audio in generator]
    logger.info(f"Generated {len(segments)} segments")
    full_audio = np.concatenate(segments)
    sf.write(output_file, full_audio, 24000)
    logger.info(f"Saved to {output_file}")