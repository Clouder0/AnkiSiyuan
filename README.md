# AnkiSiyuan

同步[思源笔记](https://github.com/siyuan-note/siyuan)中的数据到 Anki 中。

[开发笔记](https://ld246.com/article/1627227554664) [AnkiLink 完全体构想](https://www.codein.icu/ankilink-complete/)

相关项目：[AnkiIn 导入 Anki 的 Python 工具库](https://github.com/Clouder0/AnkiIn) [AnkiLink Markdown 导入 Anki](https://github.com/Clouder0/AnkiLink)

- 按需导入
- 增量同步
- 勉强能用

尚在早期开发阶段，勉强能用。

## 安装

使用 pip 安装。

```bash
pip install AnkiSiyuan
```

基础使用方法：

```bash
python AnkiSiyuan/cli.py -p password
```

其中 password 为你的思源授权码。**似乎目前不输入也能用，可以忽略掉。**

请自行承担数据风险。

## 思源侧标记

需要对某个容器块进行标记，才会被同步到 Anki 中。

具体地，创建 `ankilink` 的属性，填写相应的配置。

如果对标题标记，则标题下的所有内容都会被同步。超级块同理，文档块亦同理。递归同步，请自行把控好范围。  
**尽量使用超级块，避免嵌套，以后可能有相关的调整。**

![例子](https://user-images.githubusercontent.com/41664195/127279369-c237fc31-4db9-4fe1-aef2-93b05ee0e88c.png)

有关的内容语法，请查看 [AnkiLink Wiki](https://github.com/Clouder0/AnkiLink/wiki) 与 [AnkiIn Wiki](https://github.com/Clouder0/AnkiIn/wiki)

## 同步范围

首次同步会消耗较长时间，之后会在执行目录下保存 `last_sync_time` 文件，保存上次同步的时间。

下一次同步时，只有上一次同步后被更新了的块才会被同步。

也就是说，只有新增、修改了的块才会被处理，以避免无谓的重复运算。
