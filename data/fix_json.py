#!/usr/bin/env python3
"""Fix json.dumps closing in add_d1_batch2.py"""
with open('/home/muatasr/.nanobot/workspace/fcle-study-app/data/add_d1_batch2.py') as f:
    content = f.read()

# Replace any occurrence of json.dumps ending with ]),
# The correct pattern is: json.dumps([...])  -- ending with ]),
# Wrong pattern: json.dumps([...),  -- ending with ),
# Also wrong: json.dumps([...]),  -- ending with ]]),

# Let's just do a targeted replacement:
# Replace all instances of: \"]),
# With: \"]),
# This is the correct closing: "string"]), closes string, array, function, dict

# Actually, the correct format is:
# "wrong_answers": json.dumps(["a", "b", "c"]),
# The \"]) closes: last string ", array ], function ), then dict ,

lines = content.split('\n')
fixed = []
for line in lines:
    if 'wrong_answers' in line and 'json.dumps' in line:
        stripped = line.rstrip()
        # Fix various wrong endings to the correct one: "]),
        if stripped.endswith(']),'):
            # Check if it's the correct pattern or has extra chars
            # Correct: ...last_string"]),
            # Wrong: ...last_string"]]), or ...last_string"),
            # Count brackets
            prefix = stripped[:stripped.rfind(')')]
            if prefix.endswith(']'),'):
                line = prefix[:-1] + '])\n'
            elif prefix.endswith('),'):
                # Missing ], add it before )
                line = prefix[:-1] + '])\n'
            # else it's fine
    fixed.append(line)
content = '\n'.join(fixed)
with open('/home/muatasr/.nanobot/workspace/fcle-study-app/data/add_d1_batch2.py','w') as f:
    f.write(content)
print('Done')
