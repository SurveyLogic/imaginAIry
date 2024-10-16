import replicate

from dotenv import load_dotenv

load_dotenv()


def flux_dev(prompt):
    output = replicate.run(
        "black-forest-labs/flux-dev",
        input={
            "prompt": prompt,
            "go_fast": True,
            "guidance": 3.5,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "webp",
            "output_quality": 80,
            "prompt_strength": 0.8,
            "num_inference_steps": 28,
        },
    )
    return output

def flux_schnell(prompt):
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
            "go_fast": True,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "webp",
            "output_quality": 80,
            "num_inference_steps": 4
        }
    )
    return output