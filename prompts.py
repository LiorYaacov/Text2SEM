def build_prompt(instruction):
    return f"""
You are an intelligent assistant. Given a natural language instruction about moving a shape, convert it into a valid JSON object enclosed in curly brackets.

Always include these fields:
- action
- shape
- direction
- distance

Be tolerant to typos and case inconsistencies.
Always return a complete and valid JSON object, nothing else.

Examples:

Instruction: Move the red triangle down by 10 pixels.
Output:
{{"action": "move", "shape": "triangle", "direction": "down", "distance": 10}}

Instruction: shift the BIGGEST Circle Left by 20.
Output:
{{"action": "move", "shape": "circle", "direction": "left", "distance": 20}}

Instruction: slide teh blu sqare TO the right by 5 pixelz.
Output:
{{"action": "move", "shape": "square", "direction": "right", "distance": 5}}

Instruction: move the line 5 pixels up
Output:
{{"action": "move", "shape": "line", "direction": "up", "distance": 5}}



Instruction: {instruction}
Output:
"""
