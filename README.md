# xfani 动漫下载器

这是一个用于从指定动漫分享页自动下载动漫的工具。

## 项目地址

- **动漫分享页地址**: [https://dick.xfani.com/](https://dick.xfani.com/)
- **GitHub 项目地址**: [https://github.com/Eustia232/xfani](https://github.com/Eustia232/xfani)

## 使用方法

### 1. 下载动漫

1. 在 `status/todo.json` 文件中添加目标动漫的 ID。
2. 运行 `src/main.py`，程序将自动根据todo.json中的配置下载动漫内容。
3. 下载路径可以在 `status/download_config.json` 文件中进行配置。

### 2. 删除临时文件

- 运行 `src/remove_files.py` 来删除缓存中不再需要的临时文件。

## 获取动漫 ID

- 在动漫分享页中查询目标动漫，ID 可从 URL 中提取。

---

如果你在使用过程中遇到问题，欢迎提交 issue 或进行反馈。
