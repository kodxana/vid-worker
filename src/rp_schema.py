INPUT_SCHEMA = {
    "prompt": {
        "type": str,
        "required": True,
        "description": "Text prompt to generate video."
    },
    "negative_prompt": {
        "type": str,
        "required": False,
        "default": None,
        "description": "Text prompt to specify what you don't want in the video."
    },
    "width": {
        "type": int,
        "required": False,
        "default": 854,
        "description": "Width of the video in pixels."
    },
    "height": {
        "type": int,
        "required": False,
        "default": 480,
        "description": "Height of the video in pixels."
    },
    "video_length": {
        "type": int,
        "required": False,
        "default": 129,
        "description": "Length of the video in frames."
    },
    "infer_steps": {
        "type": int,
        "required": False,
        "default": 50,
        "description": "Number of inference steps."
    },
    "flow_shift": {
        "type": float,
        "required": False,
        "default": 7.0,
        "description": "Flow-shift parameter."
    },
    "embedded_guidance_scale": {
        "type": float,
        "required": False,
        "default": 6.0,
        "description": "Embedded guidance scale for generation."
    },
    "seed": {
        "type": int,
        "required": False,
        "default": None,
        "description": "Random seed for reproducibility."
    },
    "ulysses_degree": {
        "type": int,
        "required": False,
        "default": 1,
        "description": "Number of GPUs for Ulysses parallelism"
    },
    "ring_degree": {
        "type": int,
        "required": False,
        "default": 1,
        "description": "Number of GPUs for Ring parallelism"
    }
} 