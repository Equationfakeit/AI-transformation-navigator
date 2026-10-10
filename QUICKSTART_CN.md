# 从零开始：AI Transformation Navigator

## 第一步：本地运行（Mac）

1. 下载并解压整个项目压缩包。建议把解压出的 `ai-transformation-navigator` 文件夹放在“下载”目录中。
2. 打开 **Terminal（终端）**，逐行复制执行以下命令：

```bash
cd ~/Downloads/ai-transformation-navigator
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

3. `python3 --version` 应显示 Python 3.10 或更高版本。如果提示没有 Python，先从 https://www.python.org/downloads/ 安装。
4. 终端会显示一个以 `localhost:8501` 为例的本地网址。在浏览器中打开它，就能看到你的网站。
5. 停止网站：返回终端，按 `Control + C`。

### 测试代码是否正确

在已激活 `.venv` 的终端执行：

```bash
python3 -m unittest discover -s tests -v
```

## 第二步：上传 GitHub

1. 打开 https://github.com/new 。
2. **Repository name** 填 `ai-transformation-navigator`。
3. 建议选 **Public**（面试时方便展示）。不要勾选初始化 README，因为项目里已经有。
4. 点击 **Create repository**。
5. 回到终端，确保自己在项目目录，逐行执行：

```bash
cd ~/Downloads/ai-transformation-navigator
git init
git add .
git commit -m "Build AI transformation strategy MVP"
git branch -M main
git remote add origin https://github.com/Equationfakeit/ai-transformation-navigator.git
git push -u origin main
```

如果 Git 让你登录，按 GitHub 的提示通过浏览器或凭据管理器完成认证。GitHub 密码不能直接当作 Git 操作的凭据。

## 第三步：正式发布网站

1. 打开 https://share.streamlit.io 。
2. 用 GitHub 登录，点击 **Create app**。
3. 选择从已有 GitHub 仓库部署（existing app/repository）。
4. 填写：

```text
Repository: Equationfakeit/ai-transformation-navigator
Branch: main
Main file path: app.py
```

5. 点击 **Deploy**。成功以后会出现你自己的 `*.streamlit.app` 网址。
6. 把这个网址加入你已有的 `my-website/index.html`，作为“Projects / AI Transformation Navigator”的链接。不要覆盖原有页面。

## 第四步：练习面试演示

- 在 **Diagnose** 调低 `Data & governance`，观察 AI Readiness 评分变化。
- 在 **Prioritize** 查看推荐场景排序及风险控制措施。
- 在 **ROI simulator** 将 adoption rate 从 60% 调到 30%，观察回报变化。
- 在 **Strategy report** 下载建议报告。

**讲解时注意：** 评分来自透明的规则模型，所有示例是假设数据；此版本没有连接生成式 AI API。ROI 中的劳动时间价值不等于实际节省的现金。这些限制应该主动讲清楚。
