#!/usr/bin/env python3
"""Build a dependency-free, directly deployable GitHub Pages portfolio."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json,re,math
ROOT=Path(__file__).resolve().parent.parent
ARTICLES=json.loads((ROOT/'content/articles.json').read_text())
BASE='https://yuquanhsieh.github.io/BaminDispatch.github.io/'
class Text(HTMLParser):
 def __init__(self): super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
def plain(s):
 p=Text();p.feed(s);return ' '.join(' '.join(p.parts).split())
def icon(name):
 paths={'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>','back':'<path d="M19 12H5m6-6-6 6 6 6"/>','search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/>','close':'<path d="m6 6 12 12M18 6 6 18"/>','up':'<path d="m6 14 6-6 6 6"/>'}
 return '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'+paths[name]+'</svg>'
def head(title,description,prefix='',path='',image='assets/story-10.webp'):
 return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}">
<meta name="theme-color" content="#f7f5ee"><link rel="canonical" href="{BASE+path}">
<meta property="og:type" content="{'article' if path else 'website'}"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:image" content="{BASE+image}"><meta property="og:url" content="{BASE+path}">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}assets/style.css"><script defer src="{prefix}assets/site.js"></script></head>'''
def header(prefix='',reader=False):
 return f'''<a class="skip-link" href="#main">跳到正文</a><header class="site-header"><div class="header-inner"><a class="brand" href="{prefix}index.html" aria-label="八闽传真首页"><span class="brand-mark" aria-hidden="true">闽</span><span>八闽传真<span class="brand-en" lang="en">Bamin Dispatch</span></span></a><nav aria-label="主导航"><a href="{prefix}index.html#works">作品</a><a href="{prefix}index.html#about">关于</a></nav></div></header>'''
def footer(prefix=''):
 return f'''<footer class="site-footer"><a class="footer-brand" href="{prefix}index.html">八闽传真</a><span>© {2026} 谢雨泉</span><a href="#top">回到顶部 {icon('up')}</a></footer>'''
def card(a):
 searchable=plain(a['zh']+' '+a['en'])
 return f'''<article class="story-card" data-category="{a['category']}" data-search="{escape(a['title']+' '+a['englishTitle']+' '+a['place']+' '+searchable,quote=True)}"><a class="story-image" href="articles/{a['slug']}/"><img src="{a['image']}" alt="{a['title']}" loading="lazy" width="720" height="480"><span class="image-arrow">{icon('arrow')}</span></a><div class="card-meta"><span>{a['place']}</span><span>{a['category']}</span></div><h3><a href="articles/{a['slug']}/">{a['title']}</a></h3><p class="card-english" lang="en">{a['englishTitle']}</p></article>'''
def build_home():
 # Lead with heritage and everyday life; preserve original article numbers in source data.
 order=[9,8,1,3,7,2,0,6,5,10,4]
 cards='\n'.join(card(ARTICLES[i]) for i in order)
 cats=''.join(f'<button type="button" data-filter="{c}" aria-pressed="false">{c}</button>' for c in ['山海漫游','烟火风味','文化寻踪','城市新事'])
 s=head('八闽传真 Bamin Dispatch · 福建文旅新闻英译作品集','谢雨泉的福建文旅新闻英译作品集。11篇中英双语译作，从山海、风味与地方文化读懂福建。')
 s+='''<body id="top">'''+header()+f'''<main id="main"><section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><h1 id="hero-title">把福建的故事，<br>说给<span>世界</span>听。</h1><p>在山海、烟火与人情之间，<br>用两种语言，记录一方风土。</p><a class="text-link" href="#works">翻阅作品 {icon('arrow')}</a></div><a class="hero-photo" href="articles/xianyou-old-street/" aria-label="阅读仙游千年古街"><img src="assets/story-10.webp" width="1440" height="1000" alt="俯瞰仙游古街的红瓦屋顶与巷陌" fetchpriority="high"><div class="hero-caption"><h2>千年古街，<br>烟火未央。</h2><span class="hero-photo-arrow">{icon('arrow')}</span></div></a></section>
<section class="works section-shell" id="works" aria-labelledby="works-title"><div class="section-heading"><h2 id="works-title">文旅译作<span id="story-count">11</span></h2><label class="search-box">{icon('search')}<input id="search" type="search" aria-label="搜索作品" placeholder="搜索作品、地点" autocomplete="off"><button class="clear-search" type="button" aria-label="清除搜索" hidden>{icon('close')}</button></label></div><div class="filters" role="group" aria-label="按主题筛选"><button type="button" data-filter="all" aria-pressed="true">全部作品</button>{cats}</div><p class="sr-only" id="search-status" role="status" aria-live="polite"></p><div class="story-grid">{cards}</div><div class="empty-state" hidden><p>没有找到相关作品</p><button class="reset-search" type="button">查看全部作品 {icon('arrow')}</button></div></section>
<section class="about section-shell" id="about" aria-labelledby="about-title"><div class="about-heading"><span class="about-mark" aria-hidden="true">闽</span><h2 id="about-title">立足八闽，<br>让地方故事被看见。</h2></div><div class="about-copy"><p>「八闽传真」是谢雨泉的福建文旅新闻英译作品集，收录 11 篇中英对照译作。循着一碗冰饭、一场民俗、一条古街，走近福建的日常与新生。</p><p>中文新闻与配图版权归原作者，译文为个人翻译作品。</p><a class="text-link" href="https://github.com/YuquanHsieh/BaminDispatch.github.io" target="_blank" rel="noopener noreferrer">查看项目 {icon('arrow')}</a></div></section></main>'''+footer()+'''</body></html>'''
 (ROOT/'index.html').write_text(s)
def build_article(a,i):
 prefix='../../'; path=f'articles/{a["slug"]}/'
 zh=a['zh'];en=a['en']
 # Subheadings belong below the article title, with no modifications to the prose.
 meta_zh=re.search(r'<p class="meta-info">(.*?)</p>',zh,re.S)
 meta_en=re.search(r'<p class="meta-info">(.*?)</p>',en,re.S)
 if meta_zh:zh=zh.replace(meta_zh.group(0),'',1)
 if meta_en:en=en.replace(meta_en.group(0),'',1)
 zh_meta=f'<p class="article-source">{meta_zh.group(1)}</p>' if meta_zh else ''
 en_meta=f'<p class="article-source" lang="en">{meta_en.group(1)}</p>' if meta_en else ''
 s=head(a['title']+' · 八闽传真',a['summary'],prefix,path,a['image'])+f'''<body id="top" class="reader-page" data-mode="both">'''+header(prefix,True)
 s+=f'''<main id="main"><div class="article-intro section-shell"><a class="back-link" href="../../index.html#works">{icon('back')} 全部作品</a><div class="article-category">{a['place']}<span>·</span>{a['category']}</div><h1>{a['title']}</h1><p class="article-title-en" lang="en">{a['englishTitle']}</p></div><figure class="article-cover section-shell"><img src="{prefix+a['image']}" alt="{a['title']}" width="1440" height="800" fetchpriority="high"></figure><div class="reader-toolbar"><div class="toolbar-inner"><div class="read-modes" role="group" aria-label="阅读语言"><button type="button" data-mode="both" aria-pressed="true">中英对照</button><button type="button" data-mode="zh" aria-pressed="false">中文</button><button type="button" data-mode="en" aria-pressed="false">English</button></div><div class="reader-actions"><button type="button" data-font="down" aria-label="缩小正文字号">A−</button><button type="button" data-font="up" aria-label="放大正文字号">A+</button><button class="copy-link" type="button">复制链接</button></div></div><div class="reading-progress" aria-hidden="true"><span></span></div></div><div class="reading-content section-shell"><section class="language-column zh-column" lang="zh-CN" aria-labelledby="zh-label"><h2 class="language-label" id="zh-label">中文原文</h2>{zh_meta}<div class="prose">{zh}</div></section><section class="language-column en-column" lang="en" aria-labelledby="en-label"><h2 class="language-label" id="en-label">English translation</h2>{en_meta}<div class="prose">{en}</div></section></div><p class="sr-only" role="status" id="reader-status" aria-live="polite"></p><nav class="article-pagination section-shell" aria-label="更多作品">'''
 for offset,label in [(-1,'上一篇'),(1,'下一篇')]:
  n=i+offset
  if 0<=n<len(ARTICLES):
   other=ARTICLES[n]
   s+=f'<a href="../{other["slug"]}/"><span>{label}</span><strong>{other["title"]}</strong>{icon("back" if offset<0 else "arrow")}</a>'
  else:s+='<div></div>'
 s+='</nav></main>'+footer(prefix)+'</body></html>'
 d=ROOT/path;d.mkdir(parents=True,exist_ok=True);(d/'index.html').write_text(s)
if __name__=='__main__':
 build_home()
 for i,a in enumerate(ARTICLES):build_article(a,i)
 (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in ['']+[f'articles/{a["slug"]}/' for a in ARTICLES])+'</urlset>\n')
 print(f'Built home + {len(ARTICLES)} bilingual articles.')
