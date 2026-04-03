with open('/workspace/update_generator.py', 'r') as f:
    content = f.read()

content = content.replace("re.sub(r'// __GENERATED_ROUTES__.*', '// __GENERATED_ROUTES__\\n' + router_imports_str, router_content, flags=re.DOTALL)", 
                          "router_content.replace('// __GENERATED_ROUTES__', router_imports_str)")

with open('/workspace/update_generator.py', 'w') as f:
    f.write(content)
