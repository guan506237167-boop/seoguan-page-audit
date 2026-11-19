# 本地脚本使用

依赖：Python 3.10 或以上。除图片工具外只使用Python标准库。先将工作目录切到本Skill文件夹，或把命令中的相对路径替换为实际绝对路径。下述输出文件/目录必须尚不存在；重试时使用新路径，原输入和旧结果都保留。

```sh
python scripts/audit_html.py references/page.html --url https://example.com/p1 --output page-result.json
```

## 输入与示例预期

输入UTF-8 HTML快照，--url填写快照原页面完整URL。示例应发现noindex和多canonical；H1和描述存在；空alt需要判断图片用途，不能一律报错。

## 能力边界

不联网、不执行JS；动态站点优先由浏览器导出实际渲染HTML。HTTP头、robots.txt、索引和速度均不在本脚本检测范围内。

所有样例使用example.com及虚构资料，不能当客户实测。脚本不含遥测或付费API，不会发布内容。发现问题会写入报告，不代表执行异常；命令参数或输入格式错误返回退出码2。图片工具有文件处理失败时返回1并保留manifest；跳过动画会记录原因。
