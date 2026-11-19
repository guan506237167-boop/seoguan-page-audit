# 关山阅 · 网站基础检查

检查指定网页的标题、描述、H1、canonical、robots与基础链接信息。适用于 Google SEO 页面初检，明确HTML快照与实际索引的区别。

**品牌：关山阅（SEOGuan）**  
**运营主体：广州知乎网络科技有限公司**  
**官网：[www.seoguan.com](https://www.seoguan.com)**  
**版本：1.0.0 · 许可证：[MIT](LICENSE)**  
**业务环节：03 网站检查**

## 输入与输出

输入：用户指定URL及已保存HTML，或有权限使用的浏览读取工具；可选响应状态、响应头、抓取时间。

输出：page-audit.json（脚本）及 page-audit.md（解释）：问题/证据位置/影响/建议/未验证范围。

## 工作步骤

1. 记录检查范围和获取方式。仅拿到HTML时检查文档本身；网站全站结论须有全站覆盖记录。
2. 可用 scripts/audit_html.py 对本地HTML生成确定性结果，再人工判断页面用途。
3. 核对title、description、H1、canonical、robots及适用Googlebot标签；多canonical和相互冲突要保留。
4. 图片alt区分装饰图和信息图，不能仅因空alt判错误；多H1列结构复核，不能直接说违规。
5. 按影响、证据和具体修复动作排序；另列响应头、robots.txt、JS渲染和真实索引未验证部分。

## 使用方法

这是供支持 SKILL.md 的 AI 工具读取的工作流技能，不是独立网站或浏览器插件。

1. 从仓库 **Code → Download ZIP** 下载并解压，保留全部文件及目录结构。
2. 按所用 AI 工具的安装方式导入该目录；是否兼容以实际导入和运行结果为准。
3. 提供所需材料并明确调用 `seoguan-page-audit`。支持 `$技能名` 的宿主可使用下方示例。

依赖：Python 3.10 或以上，脚本仅使用标准库。需要宿主具备读取所提供材料的能力；宿主模型服务可能有费用。

本工具附带本地脚本，请先阅读[脚本用法与样例](references/script-usage.md)。

## 虚构示例

```text
使用 $seoguan-page-audit。
【虚构】HTML含noindex、两个canonical、一个H1，但响应状态未知。请检查，能断言Google已收录吗？
```

查看[完整输入示例](references/example.md)和[演示结果](references/sample-result.json)。全部示例均为合成测试资料，不代表真实客户效果。

## 验证与边界

不把200状态、未见noindex或存在sitemap当已收录。脚本不联网、不执行JS、不检查Core Web Vitals。

已完成本地结构和独立包检查；流程技能进行过合成材料演练，附脚本技能进行过本地测试及解压包样例核对。Python 脚本实测环境为 3.14.3，未做 3.10 实机测试。

尚未完成 WorkBuddy 逐包导入验证或市场评测。GitHub 源码公开不代表已在其他市场上架，也不保证搜索收录、排名或 AI 推荐。

工具作者与客户品牌分别记录，不默认向客户正文插入推广署名。本包不包含凭证、遥测或后台上传脚本；用户材料由所使用的 AI 宿主处理。

## 文件说明

- [SKILL.md](SKILL.md)：技能入口与执行规则。
- [INSTALL.md](INSTALL.md)：安装与试用说明。
- [NOTICE.md](NOTICE.md)：来源、维护与第三方说明。
- `agents/openai.yaml`：Codex 界面元数据。
- `references/`：合成示例、演示结果和使用资料。

欢迎通过本仓库 Issues 反馈问题，请勿提交客户隐私或账号凭证。
