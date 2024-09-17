import abstra.forms as af
import abstra.ai as ai
import json

@af.reactive
def upload_page(p):
    global datasheet_file
    datasheet_file = p.read_file("Upload the Datasheet", accepted_formats=[".png"])
    p.display_file("datasheet.png", download_text="Here's an example if you prefer")

upload_page.run()

# Define common prompt and instructions
common_prompt = "This datasheet is a technical document that provides detailed specifications and dimensions for a series of electric motors. It includes information about the electrical characteristics, mechanical dimensions, and performance metrics for different models. The data is essential for engineers and designers to select the appropriate motor for their specific applications, ensuring compatibility and optimal performance."
def process_response(response):
    if isinstance(response, str):
        # Handle the case where the response is a string (likely an error message)
        print("Error response from AI service:", response)
        return None

result = ai.prompt(
    [common_prompt, datasheet_file],
    format={
        "result": {
            "measurements": "object",
            "description": "Record of device measurements, each key is the device name",
            "additionalProperties": {
                "type": "object",
                "description": "Record of device metrics, each key is the measurement name and its unit.",
                "additionalProperties": {
                    "oneOf": [
                        { "type": "number", "description": "Numerical measurement values" },
                        { "type": "string", "description": "All other measurement values" },
                    ]
                }
            }
        }
    }
)["result"]


af.read_code("Here is the result", initial_value=json.dumps(result, indent=2), language='json')
