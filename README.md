# Cuneiform

## 环境与依赖

Cuneiform 运行在 Python 3 上，依赖 [flask][1]、[Markdown][2] 以及 [LeanCloud Python SDK][3]。

## 在开始之前

Cuneiform 是一个 [LeanCloud][4] 应用。在部署上线之前，需要先做一些准备工作。

1. 在 [LeanCloud 控制台][5] 新建一个应用，并设置一个二级域名。
2. 在控制台中新增一个名为 `FLASK_SECRET_KEY` 的环境变量。（关于如何创建一个好的密钥，请参考 [这个 gist][6]）
3. 安装最新版的 [LeanCloud 命令行工具][7]。如果你无法访问 GitHub，请移步 [国内镜像](http://releases.leanapp.cn/#/leancloud/lean-cli/releases)。

## 部署方法

首先将 Cuneiform 的代码克隆到本地。在终端中打开项目所在目录，输入 `lean login`，然后 `lean checkout`，根据提示操作，就可以将本地的项目与刚刚在 LeanCloud 上创建的应用链接起来。

使用 [virtualenv][8] 来为这个应用创建一个隔离的 Python 运行环境。激活虚拟环境，然后用 `pip` 来安装所需的依赖。

用 `lean deploy` 命令将代码部署到 LeanCloud 上。部署完成之后，就可以在浏览器中输入刚才设置的域名，打开线上运行的网站了。

简单来讲：

```bash
$ git clone https://github.com/nervouna/Cuneiform.git && cd Cuneiform
$ virtualenv venv --python=python3 && source venv/bin/activate
$ (venv) pip install -r requirements.txt
$ (venv) lean login
$ (venv) lean checkout
$ (venv) lean deploy
```

## 怎样注册用户？

你可以在 [LeanCloud 控制台][5] 的数据管理中直接为 `_User` 表添加一条记录，输入用户名和密码即可。

## 我的数据在哪里？

在 [LeanCloud 控制台][5] 的数据管理一栏里查看数据。所有的帖子都存在 `Post` 表中，上传的图片在 `_File` 表，用户在 `_User` 表。

## 数据结构是怎样的？

Cuneiform 用到了五张表：`Post`、`Tag`、`TagPostMap`、`_User` 和 `_File`。他们的用途分别如下：

1. `Post` 表保存文章信息，包括标题、内容、作者，以及通过 markdown 渲染后的内容；
2. `Tag` 表保存标签信息；
3. `TagPostMap` 表保存文章和标签的关系；
4. `_User` 表是 LeanCloud 的默认表，保存的是作者的信息；
5. `_File` 表是 LeanCloud 的默认表，保存上传的文件。

## 如何调试？

在本地调试，请使用 `lean up` 命令。

## Miscellaneous

* License: [WTFPL][9]
* Author: GUAN Xiaoyu ([guanxy@me.com][10])

[1]: http://flask.pocoo.org
[2]: https://pythonhosted.org/Markdown/
[3]: https://github.com/leancloud/python-sdk
[4]: https://leancloud.cn/
[5]: https://leancloud.cn/dashboard/applist.html#/apps
[6]: https://gist.github.com/nervouna/cd58fb09c22826eaaff996793de72d85
[7]: https://github.com/leancloud/lean-cli/releases/latest
[8]: https://github.com/pypa/virtualenv
[9]: https://github.com/nervouna/Sniff/blob/master/LICENSE
[10]: mailto:guanxy@me.com
