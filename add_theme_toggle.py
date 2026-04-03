import re

with open('/workspace/shop_vue/src/components/Layout.vue', 'r') as f:
    content = f.read()

# Add switch button icon to template
pattern = r'(<div class="header-actions">[\s\S]*?)<el-icon class="action-icon"><Search /></el-icon>'
replacer = r'\1<el-icon class="action-icon" @click="toggleTheme" title="切换到新版UI"><SwitchButton /></el-icon>\n            <el-icon class="action-icon"><Search /></el-icon>'
content = re.sub(pattern, replacer, content)

# Add SwitchButton to imports
import_pattern = r"import { (.*?) } from '@element-plus/icons-vue'"
def import_replacer(m):
    imports = m.group(1)
    if 'SwitchButton' not in imports:
        imports += ', SwitchButton'
    return f"import {{ {imports} }} from '@element-plus/icons-vue'"
content = re.sub(import_pattern, import_replacer, content)

# Add toggleTheme method
script_pattern = r'(const handleCommand = \(command\) => \{)'
toggle_method = """const toggleTheme = () => {
  localStorage.setItem('ui_theme', 'v2')
  window.location.reload()
}

"""
content = re.sub(script_pattern, toggle_method + r'\1', content)

with open('/workspace/shop_vue/src/components/Layout.vue', 'w') as f:
    f.write(content)
