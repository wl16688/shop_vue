with open('/workspace/shop_vue/src/components/Layout.vue', 'r') as f:
    content = f.read()

content = content.replace("vue-router\\n      >'", "vue-router'")
content = content.replace("const router\\n      > = useRouter()", "const router = useRouter()")

with open('/workspace/shop_vue/src/components/Layout.vue', 'w') as f:
    f.write(content)
