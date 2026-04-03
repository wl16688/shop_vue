import re
with open('/workspace/shop_vue/src/components/Layout.vue', 'r') as f:
    content = f.read()

content = re.sub(r'<router\s+>-view', '<router-view', content)
content = re.sub(r'</router\s+>-view>', '</router-view>', content)

with open('/workspace/shop_vue/src/components/Layout.vue', 'w') as f:
    f.write(content)
