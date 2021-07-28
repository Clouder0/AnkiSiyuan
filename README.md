# AnkiSiyuan

同步[思源笔记](https://github.com/siyuan-note/siyuan)中的数据到 Anki 中。

[开发笔记](https://ld246.com/article/1627227554664) [AnkiLink 完全体构想](https://www.codein.icu/ankilink-complete/)

相关项目：[AnkiIn 导入 Anki 的 Python 工具库](https://github.com/Clouder0/AnkiIn) [AnkiLink Markdown 导入 Anki](https://github.com/Clouder0/AnkiLink)

- 按需导入
- 增量同步
- 勉强能用

尚在早期开发阶段，勉强能用。

## 安装

使用 pip 安装 [AnkiIn](https://github.com/Clouder0/AnkiIn) 依赖。

基础使用方法：

```bash
python AnkiSiyuan/cli.py -p password
```

其中 password 为你的思源授权码。

请自行承担数据风险。

## 思源侧标记

需要对某个容器块进行标记，才会被同步到 Anki 中。

具体地，创建 `ankilink` 的属性，值随意填写。

如果对标题标记，则标题下的所有内容都会被同步。超级块同理，文档块亦同理。递归同步，请自行把控好范围。

![例子](https://user-images.githubusercontent.com/41664195/127279369-c237fc31-4db9-4fe1-aef2-93b05ee0e88c.png)

有关的内容语法，请查看 [AnkiLink Wiki](https://github.com/Clouder0/AnkiLink/wiki) 与 [AnkiIn Wiki](https://github.com/Clouder0/AnkiIn/wiki)
