# AnkiSiyuan

同步[思源笔记](https://github.com/siyuan-note/siyuan)中的数据到 Anki 中。

[开发笔记](https://ld246.com/article/1627227554664) [AnkiLink 完全体构想](https://www.codein.icu/ankilink-complete/)

相关项目：[AnkiIn 导入 Anki 的 Python 工具库](https://github.com/Clouder0/AnkiIn) [AnkiLink Markdown 导入 Anki](https://github.com/Clouder0/AnkiLink)

- 按需导入
- 增量同步
- 勉强能用

更新了 v0.1.0，对同步代码进行大幅重构，优化了性能。

现在初次同步的速度应该很快了。

## 安装

使用 pip 安装。

```bash
pip install ankisiyuan
```

需要在 Anki 中安装 anki-connect 拓展。

基础使用方法：

```bash
python -m ankisiyuan
```

**需要在 Anki 与思源笔记同时运行时使用。**

需要在运行目录下保存 `config.toml` 文件，大致形式如下：

```toml
[siyuan]
assets_replacement = "http://127.0.0.1:6806/assets/"
api_token = "your_api_token"
```

如果希望在其他设备上也能看到图片，可以将 `http://127.0.0.1:6806/assets` 替换成思源的图床地址。

请自行承担数据风险。

## 更新

一个较为稳妥的方式是卸载后再次安装。  
需要注意，v0.1.0 之前的版本名称为 `AnkiSiyuan`，以后的版本为 `ankisiyuan`，大小写可能敏感。

```bash
pip uninstall ankisiyuan
pip install ankisiyuan
```

另一种方式：

```bash
pip install ankisiyuan --upgrade
```

## 思源侧标记

需要对某个容器块进行标记，才会被同步到 Anki 中。

具体地，创建 `ankilink` 的属性，填写相应的配置。

推荐使用标题的形式。

> ## 背诵内容(在这里设置属性)
>
> Card1  
> Ans

事实上，只要在目标卡片块的父亲块上打标记即可。比如说使用超级块打标记也是可以的。

![例子](https://user-images.githubusercontent.com/41664195/131253057-a6ae22d0-02ce-4ad7-9757-43f7b1fb5c28.png)

有关的内容语法，请查看 [AnkiLink Wiki](https://github.com/Clouder0/AnkiLink/wiki) 与 [AnkiIn Wiki](https://github.com/Clouder0/AnkiIn/wiki)  

## 同步范围

每次同步都是增量同步，会在运行目录下保存上次同步的时间 `last_sync_time` 文件。

也就是说，只有新增、修改了的块才会被处理，以避免无谓的重复运算。

## 图片

在运行思源的设备上，可以通过 `http://127.0.0.1:6806/assets` 访问到图片。

也可以通过思源提供的图床嵌入到 Anki 中。

在运行目录下创建 `config.toml` 文件，写入：

```ini
[siyuan]
assets_replacement = "https://b3logfile.com/siyuan/1609132319768/assets"
```

请将 `1609132319768` 替换为你的图床链接中对应的 id.
