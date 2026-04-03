with open('/workspace/shop_vue/src/router/index.js', 'r') as f:
    content = f.read()

content = content.replace("    ]", "      // __GENERATED_ROUTES__\n    ]")

with open('/workspace/shop_vue/src/router/index.js', 'w') as f:
    f.write(content)
