### 项目名称

**题目收集器**

### 项目简介

这是一个用于从网页中收集题目和答案的工具。它可以解析指定网址中的题目内容，并根据用户的选择，将题目和答案输出到文本文件或HTML文件中，以便用户进一步处理或导入到其他应用程序中。

### 安装依赖

在运行该项目之前，请确保已安装以下依赖：

```bash
pip install requests
pip install beautifulsoup4
```

###如何使用
使用命令行界面来运行该项目。下面是使用说明：

```
python exam.py -u URL_FILE [--output OUTPUT_FILE] [-m MODE]
```
- `-u` 或 `--url_file`：指定包含待解析网址的文件路径。
- `--output` 或 `-o`：指定输出文件的路径。如果未提供，则会在当前目录下生成一个默认文件名。
- `-m` 或 `--mode`：选择输出模式。可选值为 `txt` 或 `anki`。默认为 `anki`。

### 输出模式

- `txt` 模式：将题目和答案输出为文本格式。
- `anki` 模式：将题目和答案输出为适用于 Anki 软件的格式。

### 许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)。
