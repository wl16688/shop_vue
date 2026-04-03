import re
with open('/workspace/shop_vue/src/components/Layout.vue', 'r') as f:
    content = f.read()

content = re.sub(r"vue-router\s+>'", "vue-router'", content)
content = re.sub(r"const router\s+> = useRouter\(\)", "const router = useRouter()", content)
content = re.sub(r"router\s+>\.push", "router.push", content)

with open('/workspace/shop_vue/src/components/Layout.vue', 'w') as f:
    f.write(content)
