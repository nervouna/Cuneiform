# Cuneiform

Cuneiform is a tiny blog. Written in Python, runs on [LeanEngine][1].

## Preparations

1. Create an app on [LeanCloud][2].
2. Get the latest [lean-cli][3].
3. Get yourself a [virtualenv][4].

## Getting Started

Clone this repo, cd into the directory, create a virtualenv and activate it:

```bash
virtualenv venv --python=python3
source ./venv/bin/activate
```

Then install the requirements:

```bash
pip install -r requirements.txt
```

Initialize the app with lean-cli. Type `lean login` and login with your user name and password. Then type `lean checkout` and follow the instructions.

Now your code is linked to the app on LeanCloud. Use `lean up` to debug on `localhost`, and use `lean deploy` to push it online. Don't forget to [set up a domain][5] :)

[1]: https://leancloud.cn/docs/leanengine_overview.html
[2]: https://leancloud.cn
[3]: https://github.com/leancloud/lean-cli/releases/latest
[4]: https://virtualenv.pypa.io/en/stable/installation/
[5]: https://leancloud.cn/cloud.html#/conf
