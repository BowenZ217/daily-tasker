## 0. 环境准备

推荐使用 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 管理 Python 环境。

可从以下链接下载并安装 Miniconda:

* [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

---

## 1. 克隆项目

```bash
git clone https://github.com/BowenZ217/daily-tasker.git
cd daily-tasker
```

---

## 2. 创建并激活 Conda 环境

```bash
conda create -n daily-tasker python=3.12 -y
conda activate daily-tasker
```

---

## 3. 安装开发依赖

使用 `pip` 安装项目及其开发依赖:

```bash
pip install -e .[dev]
```

---

## 4. 安装 pre-commit 钩子

本项目使用 [pre-commit](https://pre-commit.com/) 管理提交前的代码检查工具。

首次使用时执行:

```bash
pre-commit install
```

可使用以下命令在全部文件上手动运行:

```bash
pre-commit run --all-files
```

---

## 5. 提交规范

本项目遵循 [Conventional Commits](https://www.conventionalcommits.org/) 提交规范, 格式如下:

```
<type>(<scope>): <description>
```

### 常用类型

* `feat`: 添加新功能
* `fix`: 修复问题
* `docs`: 修改文档
* `style`: 代码格式调整 (不影响功能)
* `refactor`: 代码重构 (非功能性变更)
* `test`: 添加或修改测试
* `chore`: 构建过程或辅助工具的变更

### 示例

```bash
git commit -m "feat(cli): add clean command for cache/logs"
git commit -m "fix(xxx): xxxxx"
```

---

## 6. 版本管理与日志生成

使用 [`commitizen`](https://github.com/commitizen-tools/commitizen) 管理版本与生成变更日志:

```bash
cz bump
```

该命令将根据提交信息:

* 自动更新版本号
* 生成或更新 `CHANGELOG.md`
* 创建对应的 Git 标签
