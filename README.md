# 八闽传真 · Bamin Dispatch

谢雨泉的福建文旅新闻英译作品集，收录 11 篇中英对照译作。

**线上地址：** https://yuquanhsieh.github.io/BaminDispatch.github.io/

## 本地预览

无需安装前端依赖，直接使用 Python 3：

```sh
python3 -m http.server 8769 --bind 127.0.0.1
```

浏览器打开 http://127.0.0.1:8769/ 。

## 修改内容

- `content/articles.json`：文章标题、分类、原文、译文及原配图地址。
- `assets/`：本地 WebP 配图、样式与交互脚本。
- `scripts/build.py`：生成首页、11 个独立文章页与 sitemap。

修改内容后重新生成并检查：

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

首页支持主题筛选和中英文正文搜索；文章支持中英对照、单语言阅读与字号设置。阅读偏好保存在浏览器本地，不收集个人数据。

## 发布与回滚

GitHub Pages 从 `main` 分支发布仓库根目录。构建产物随源码一起提交；推送 `main` 后等待仓库内 **pages build and deployment** 成功。

2026-11-14 改版前版本：`eb02244fa44d90035b6605e90e6c11fcd64eb363`。需要回滚时对改版提交执行 `git revert` 并推送，保留可追溯历史。

新闻正文及图片版权归原作者，译文为个人翻译作品。图片沿用旧站素材并本地压缩，来源地址保留于 `content/articles.json`。新增图片请先确认使用范围。
