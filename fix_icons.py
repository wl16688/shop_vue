import re

with open('/workspace/shop_vue/src/components/LayoutV2.vue', 'r') as f:
    content = f.read()

# Replace missing icons import
import_icons = "import { Search, FullScreen, Bell, ArrowDown, SwitchButton, RefreshRight, Fold, Expand, Menu, User, Star, Goods, List, Setting, DataLine, DataAnalysis, Message, ChatDotRound, Location, Picture, Camera, VideoCamera, Headset, Phone, More, Share, Ticket, Money, Coin, Wallet, Discount, PriceTag, News, Guide, Position, Connection, Link, Monitor, Cpu, Collection, Folder, Document, Files, Box, OfficeBuilding, School, House, Shop, ShoppingCart, ShoppingCartFull, Sell, SoldOut, Present, Gift, Medal, Trophy, Reading, Notebook, MapLocation, Grid, HomeFilled, Management, Histogram, TrendCharts, Briefcase, Postcard, CreditCard } from '@element-plus/icons-vue'"

content = re.sub(r"import \{ .*? \} from '@element-plus/icons-vue'", import_icons, content)

with open('/workspace/shop_vue/src/components/LayoutV2.vue', 'w') as f:
    f.write(content)
