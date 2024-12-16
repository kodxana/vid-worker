import os
import time
from pathlib import Path
import runpod
from runpod.serverless.utils import rp_cleanup
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.utils import upload_file_to_bucket

# Import the existing functions from predict.py
from predict import Predictor
from rp_schema import INPUT_SCHEMA

# Initialize the predictor
predictor = Predictor()
predictor.setup()

def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''
    
    # Validate the input
    validated_input = validate(event['input'], INPUT_SCHEMA)
    if 'errors' in validated_input:
        return {"error": validated_input['errors']}
    job_input = validated_input['validated_input']

    # Create results directory
    os.makedirs('/tmp/results', exist_ok=True)

    try:
        # Use the existing predict function
        output_path = predictor.predict(
            prompt=job_input.get('prompt'),
            negative_prompt=job_input.get('negative_prompt'),
            width=job_input.get('width', 854),
            height=job_input.get('height', 480),
            video_length=job_input.get('video_length', 129),
            infer_steps=job_input.get('infer_steps', 50),
            flow_shift=job_input.get('flow_shift', 7.0),
            embedded_guidance_scale=job_input.get('embedded_guidance_scale', 6.0),
            seed=job_input.get('seed'),
            ulysses_degree=job_input.get('ulysses_degree', 1),
            ring_degree=job_input.get('ring_degree', 1)
        )

        # Generate a unique filename
        timestamp = int(time.time())
        filename = f"video_{timestamp}.mp4"
        
        # Upload to S3 bucket
        video_url = upload_file_to_bucket(
            str(output_path),  # Local path
            filename,          # Remote filename
            "video/mp4"       # Content type
        )

        # Return the results
        return {
            "output": {
                "video_url": video_url,
                "seed": job_input.get('seed'),
                "parameters": job_input
            }
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        # Cleanup
        rp_cleanup.clean('/tmp/results')

runpod.serverless.start({"handler": handler}) 