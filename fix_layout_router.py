with open('/workspace/shop_vue/src/components/Layout.vue', 'r') as f:
    content = f.read()

content = content.replace("router\\n      >-view", "router-view")
content = content.replace("<router\\n      >", "<router-view>")

with open('/workspace/shop_vue/src/components/Layout.vue', 'w') as f:
    f.write(content)
