# 差异化说明：PaperMod 改造方案

> 目标：继承 PaperMod 的**底层架构**，但视觉层完全重写，让博客从外观看不出 PaperMod 的影子。
> 日期：2026-10-10

---

## 一、设计哲学（最重要）

**继承 ≠ 沿用外观**

| 维度 | 策略 |
|------|------|
| 架构层 | ✅ 完整继承（i18n、shortcode、RSS、sitemap、SEO defaults） |
| 视觉层 | ❌ 完全重写（颜色、字体、布局、组件、首页/详情/关于） |
| 交互层 | ⚠️ 部分继承（搜索、归档）+ 部分重写（TOC、阅读进度、主题切换） |

简单说：**你看到的所有「漂亮」的东西都是我写的，你看不见的基础设施是 PaperMod 的**。

---

## 二、具体差异化清单

### 1. 颜色系统（完全替换）

| 元素 | PaperMod 默认 | 本项目 |
|------|--------------|--------|
| 主品牌色 | 蓝色 `#3273dc` | **珊瑚橙 `#FF6E40`** |
| 强调 hover | 蓝色变深 | 橙红 `#EA580C` |
| 链接色 | 蓝色 | 橙红 + 下划线展开 |
| 浅色背景 | 纯白 `#FFFFFF` | 暖白 `#FAFAF9`（纸张感） |
| 暗色背景 | `#1d1d1d` | `#0F172A`（slate-900） |
| 代码块底 | `#272822` | `#0B1120`（slate-950） |

**反抄袭检查**：把 PaperMod 的任何截图和我们的放一起，颜色识别就能立刻区分。

### 2. 字体系统（完全替换）

| 元素 | PaperMod 默认 | 本项目 |
|------|--------------|--------|
| 全局字体 | 系统无衬线 | Inter |
| 标题 | 同上 | **Source Serif 4**（衬线，编辑感） |
| 代码 | Consolas / monospace | **JetBrains Mono** |
| 行高 | 1.6 | 1.75（更松弛） |
| 行长 | 不限 | 65–75 字符（`max-w-3xl`） |

**反抄袭检查**：衬线大标题是本项目最显眼的视觉特征。PaperMod 全部是无衬线。

### 3. 布局结构（完全重写）

| 页面 | PaperMod 默认 | 本项目 |
|------|--------------|--------|
| 首页 | 文章卡片平铺 | **Hero + 编辑精选 3 列 + 最新文章长列表 + 标签云 + Newsletter** |
| 文章页 | 单列 + 顶部 meta + 底部 footer | 居中正文 + 大标题（衬线）+ 阅读时长/作者 meta + 上下篇 |
| 关于页 | PaperMod 内置 profile 模式 | **自定义 layout**：头像区 + Now 区 + 工具栈 + 时间线 |
| 导航 | 中间 Logo + 右侧菜单 | **左 Logo + 中菜单 + 右操作**（含搜索/暗色切换） |
| 卡片样式 | 圆角 + 阴影 | **浅边框 + hover 微抬升 + 边框变品牌色** |
| 标签样式 | 普通链接 | **圆角胶囊 + 数量徽章** |

**反抄袭检查**：首页有「编辑精选」+「Newsletter」两个 PaperMod 没有的板块，结构性差异明显。

### 4. 组件样式（完全重写）

| 组件 | PaperMod 默认 | 本项目 |
|------|--------------|--------|
| 卡片 | 阴影 + 白底 | `border` + `hover:shadow-lift + hover:translate-y-[-2px]` |
| 按钮 | 蓝色实心 | 主品牌色 + active:scale-0.97 |
| 链接 | 单色下划线 | 渐变下划线 + 颜色 hover |
| 引用 blockquote | 左侧灰边 | **左侧橙边 + 浅橙背景 + 斜体** |
| 行内代码 | 灰底粉字 | JetBrains Mono + 暗色下自动适配 |
| 代码块 | highlight 默认样式 | 自定义 macOS 风格 + 语法高亮 |
| 表格 | 默认 | 斑马纹 + 表头加粗 |

### 5. 微交互（完全重写）

- **主题切换**：自定义 JS + localStorage 持久化（非 PaperMod 默认方式）
- **卡片 hover**：translate-y + border 变色 + shadow 升级（PaperMod 只有 shadow）
- **箭头位移**：右侧箭头 `transform: translateX(4px)`（PaperMod 无）
- **主题切换过渡**：所有元素 200ms 平滑过渡

### 6. 暗色模式（完全重写）

| 维度 | PaperMod | 本项目 |
|------|---------|--------|
| 触发方式 | 系统偏好（无手动按钮） | **系统偏好 + 手动按钮** |
| 持久化 | 无 | localStorage |
| 品牌色亮度 | 同样 `#3273dc` | 提升到 `#FB923C`（更柔和） |
| 背景 | 简单反色 | 重新设计的 slate token 系统 |
| 玻璃元素 | 透明效果差 | 自定义深色背景 |

---

## 三、继承清单（合理利用，避免重复造轮子）

| 资源 | 用途 |
|------|------|
| `i18n/*.yaml` | 47 个翻译文件，节省手动翻译 |
| `layouts/_shortcodes/` | Hugo 内置 shortcode 支持 |
| `assets/css/embed.torch.js` | Hugo 内置 JS 模块 |
| `assets/css/built-in/` | PaperMod 的 syntax highlight token |
| 默认 sitemap.xml 输出 | Hugo 标准输出 |
| 默认 RSS 输出 | Hugo 标准输出 |
| JSON feed 输出 | PaperMod 提供的 index.json |
| Search 页面 (`layouts/search.html`) | 借用了 PaperMod 的 Fuse.js 实现 |
| Archives 页面 (`layouts/archives.html`) | 借用了 PaperMod 的归档布局 |

---

## 四、配置上的差异化（hugo.toml）

在 `hugo.toml` 中**关闭了**所有可能暴露 PaperMod 身份的参数：

```toml
[params]
  ShowReadingTime = false      # 我们用 .ReadingTime 但不用 PaperMod 样式
  ShowShareButtons = false     # 我们用 SVG 自己实现
  ShowBreadCrumbs = false      # 自己实现
  ShowCodeCopyButtons = false  # 自己实现
  profileMode = false          # 关闭 PaperMod 主页 profile 模式
  socialIcons = []             # 关闭 PaperMod 内置社交图标
  homeInfoParams = ""          # 关闭 PaperMod 内置首页 hero
```

这些关闭项在视觉上避免了「这是 PaperMod 模板」的标志性特征。

---

## 五、未做差异化（明确决策）

以下元素我**没有**改，因为改了反而不好：

1. **Hugo 自身的 HTML 输出结构**——改了会导致 SEO 不友好
2. **PaperMod 的 syntax highlight token**——这是 Hugo 内置的，改它没有意义
3. **PaperMod 的 archive/sitemap/rss 输出**——这些是标准输出，Hugo 通用

---

## 六、视觉效果自检

完成改造后，从以下几个角度可以验证「看不出是 PaperMod」：

✅ 字体：Source Serif 4 衬线大标题（PaperMod 全 sans-serif）
✅ 主色：珊瑚橙（PaperMod 是蓝色）
✅ 首页结构：Hero + 编辑精选 + Newsletter（PaperMod 是平铺）
✅ 卡片：浅边框 + 微抬升（PaperMod 是大阴影）
✅ 关于页：自定义 layout（PaperMod 是 profile 模式）
✅ 暗色：slate token + 提亮的橙（PaperMod 是简单反色）

---

## 七、维护建议

如果你要继续在这个基础上迭代：

1. **优先改 `assets/css/extended/custom.css`**——所有视觉调整集中在这里
2. **修改菜单在 `hugo.toml`**——避免碰 PaperMod 的内部 partial
3. **新增内容用 Markdown**——所有 5 篇示例文章是模板
4. **不要启用 PaperMod 的参数开关**（如 profileMode）——会破坏差异化

如果你觉得当前差异化还不够，可以考虑：
- 完全去掉 `theme = "PaperMod"`，改成 `theme = "hn-custom"` 然后自建主题目录
- 但这会失去 i18n 等便利，需要权衡

---

## 八、对比文件清单

```
hugo-blog/
├── assets/css/extended/
│   └── custom.css           ← 本项目所有视觉样式（300+ 行）
├── layouts/                 ← 完全重写，覆盖 PaperMod
│   ├── index.html           ← Hero 首页（重写）
│   ├── _default/
│   │   ├── single.html      ← 文章详情（重写）
│   │   └── list.html        ← 列表页（重写）
│   ├── _partials/
│   │   ├── header.html      ← 顶部导航（重写）
│   │   └── footer.html      ← 页脚（重写）
│   └── about/single.html    ← 关于页（重写）
├── content/
│   ├── posts/               ← 5 篇示例 Markdown
│   └── about/index.md       ← 关于页内容
├── hugo.toml                ← 大量关闭 PaperMod 默认 UI
└── themes/PaperMod/         ← 仅继承，不修改
```
