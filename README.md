# shop_vue（管理端前端）

本项目为商城管理端前端，基于 Vue 3 + Vite。

## 环境要求

- Node.js：`^20.19.0 || >=22.12.0`（见 [package.json](file:///workspace/shop_vue/package.json#L26-L28)）
- npm：建议使用 Node 自带的 npm 版本

## 启动前说明

- 本项目默认通过 Vite 代理 `/api` 到后端：`http://localhost:8081`（见 [vite.config.js](file:///workspace/shop_vue/vite.config.js#L16-L27)）
- 启动前请先确保后端 `shop_java` 已运行在 `8081` 端口

## 安装依赖

```bash
npm install
```

## 本地开发启动

```bash
npm run dev
```

启动后访问地址：

- 管理端前端：http://localhost:5173/
- 通过代理访问后端接口（示例）：http://localhost:5173/api/admin/

## 打包构建

```bash
npm run build
```
