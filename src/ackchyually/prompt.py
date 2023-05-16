class Prompt:
    VERY_CRITICAL = """
I am going to present you with a video transcript from YouTube.
The transcript is too large for me to send you all at once.
I am going to send you each part separately following this message.
You must reply OK to every single transcript stub, until i ask for the final result.
When I ask for the final result you must output exactly the final result and nothing else.
I want you to be very critical of the material, as if you were a rigerous journalist.
The final result is a JSON object, which follows this structure (if you want to use double quotes in the JSON content please replace them with single quotes)
{
    "summary": "<your summary of the video. try to stay below 600 characters unless it's very important to the summary>",
    "score": "<0-1 based on the trustworthyness and overall quality of the information presented by the author.",
    "factcheck": {
        "false": [<list of mostly false claims by the author in the video>],
        "misleading": [<list of misleading statements by the author in the video>],
        "omission": [<list of very important facts left out of the video by the author to potentially create a false narative>],
        "bias": [<list of accurate statements presented by the author in a biased manner in the video>]
    }
}
Reply OK when you are ready.
"""
