with open('/workspace/shop_vue/src/components/LayoutV2.vue', 'r') as f:
    content = f.read()

content = content.replace("\\'", "'")

with open('/workspace/shop_vue/src/components/LayoutV2.vue', 'w') as f:
    f.write(content)
