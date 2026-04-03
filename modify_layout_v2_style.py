import re

with open('/workspace/shop_vue/src/components/LayoutV2.vue', 'r') as f:
    content = f.read()

# Make left sidebar hide when collapse is true
aside_pattern = r'<el-aside width="200px" class="left-sidebar">'
aside_replacer = r'<el-aside :width="isCollapse ? \'64px\' : \'200px\'" class="left-sidebar" style="transition: width 0.3s;">'
content = re.sub(aside_pattern, aside_replacer, content)

# Add custom active style to el-menu-item to look like Shows.mom
style_updates = """
.side-menu {
  border-right: none;
  flex: 1;
  overflow-y: auto;
  background-color: #fff;
}

:deep(.el-menu-item) {
  margin: 4px 8px;
  border-radius: 4px;
  height: 40px;
  line-height: 40px;
  color: #606266;
}

:deep(.el-menu-item.is-active) {
  color: #3e75f5 !important;
  background-color: #eef2fe !important;
  font-weight: 500;
}

:deep(.el-sub-menu__title) {
  color: #303133 !important;
  font-weight: 500;
}

:deep(.el-sub-menu__title:hover),
:deep(.el-menu-item:hover) {
  background-color: #f5f7fa !important;
  color: #3e75f5 !important;
}

.sidebar-title {
  font-size: 16px;
  white-space: nowrap;
  overflow: hidden;
}
"""

content = re.sub(r'\.side-menu \{[\s\S]*?:deep\(\.menu-html-container \.el-menu\) \{\n  background-color: #fff !important;\n\}', style_updates, content)

with open('/workspace/shop_vue/src/components/LayoutV2.vue', 'w') as f:
    f.write(content)
