import unittest,json,re,subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlparse
ROOT=Path(__file__).resolve().parent.parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.text=[];self.links=[];self.langs=[];self.h1=0;self.missing_alt=[]
 def handle_data(self,data):self.text.append(data)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if a.get('lang'):self.langs.append(a['lang'])
  if tag=='img' and not a.get('alt'):self.missing_alt.append(a)
  if tag in ['a','link','script','img']:
   for k in ['src','href']:
    if k in a:self.links.append(a[k])
def parse(s):p=Parser();p.feed(s);return p
def text(s):return re.sub(r'\s+','', ''.join(parse(s).text))
class SiteIntegrity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.articles=json.loads((ROOT/'content/articles.json').read_text())
  cls.original=subprocess.check_output(['git','show','eb02244:index.html'],cwd=ROOT,text=True)
 def test_all_eleven_articles_have_both_languages(self):
  self.assertEqual(len(self.articles),11)
  for a in self.articles:
   self.assertTrue(a['zh'] and a['en']);self.assertTrue((ROOT/'articles'/a['slug']/'index.html').is_file())
 def test_every_original_body_is_preserved(self):
  chunks=re.findall(r'<div class="page">(.*?)(?=<div class="page">|</body>)',self.original,re.S)
  for a,chunk in zip(self.articles,chunks):
   blocks=re.search(r'<div class="st-block">(.*?)</div>\s*<div class="tt-block">(.*?)</div>',chunk,re.S).groups()
   rendered=(ROOT/'articles'/a['slug']/'index.html').read_text()
   for lang,block in zip(['zh','en'],blocks):
    source=re.sub(r'<h3>.*?</h3>','',block,count=1,flags=re.S)
    self.assertEqual(text(source),text(a[lang]),f'{a["slug"]} {lang}')
    # Every paragraph/quotation and original source line appears in the rendered HTML.
    for part in re.findall(r'>([^<>]+)<',a[lang]):
     if part.strip():self.assertIn(text(part),text(rendered))
 def test_internal_links_and_images_resolve_in_project_subpath(self):
  for path in [ROOT/'index.html']+list((ROOT/'articles').rglob('index.html')):
   for link in parse(path.read_text()).links:
    u=urlparse(link)
    if u.scheme or u.netloc or not u.path:continue
    self.assertFalse(u.path.startswith('/'),f'Root-absolute link breaks project Pages: {link}')
    dest=path.parent/unquote(u.path)
    self.assertTrue(dest.exists(),f'{path.relative_to(ROOT)} -> {link}')
 def test_semantic_pages(self):
  for path in [ROOT/'index.html']+list((ROOT/'articles').rglob('index.html')):
   p=parse(path.read_text())
   self.assertEqual(p.h1,1);self.assertFalse(p.missing_alt)
   self.assertIn('zh-CN',p.langs)
   if '/articles/' in str(path):self.assertIn('en',p.langs)
 def test_images_are_local_and_web_ready(self):
  for a in self.articles:
   p=ROOT/a['image'];self.assertTrue(p.is_file());self.assertLess(p.stat().st_size,500_000)
 def test_sitemap_contains_all_reading_routes(self):
  sitemap=(ROOT/'sitemap.xml').read_text()
  self.assertEqual(sitemap.count('<url>'),12)
  for a in self.articles:self.assertIn(f'articles/{a["slug"]}/',sitemap)
 def test_rebuild_is_deterministic(self):
  paths=[ROOT/'index.html',ROOT/'sitemap.xml']+list((ROOT/'articles').rglob('index.html'))
  before={p:p.read_bytes() for p in paths}
  subprocess.run(['python3','scripts/build.py'],cwd=ROOT,check=True,capture_output=True)
  self.assertTrue(all(p.read_bytes()==b for p,b in before.items()))
if __name__=='__main__':unittest.main()
