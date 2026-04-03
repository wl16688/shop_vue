with open('/workspace/shop_vue/src/components/Layout.vue', 'r') as f:
    content = f.read()

content = content.replace("useRouter\\n      >", "useRouter")
content = content.replace("'vue-router\\n      >'", "'vue-router'")
content = content.replace("router\\n      >\\n      >.push", "router.push")

with open('/workspace/shop_vue/src/components/Layout.vue', 'w') as f:
    f.write(content)
