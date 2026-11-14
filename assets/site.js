(() => {
  'use strict';
  const search = document.querySelector('#search');
  if (search) {
    const cards = [...document.querySelectorAll('.story-card')];
    const filters = [...document.querySelectorAll('[data-filter]')];
    const clear = document.querySelector('.clear-search');
    let category = 'all';
    const normalize = value => value.normalize('NFKC').toLocaleLowerCase().trim();
    function update() {
      const words = normalize(search.value).split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        const haystack = normalize(card.dataset.search);
        const match = (category === 'all' || card.dataset.category === category) && words.every(word => /^[a-z0-9]+$/.test(word) ? new RegExp('\\b' + word + '\\b').test(haystack) : haystack.includes(word));
        card.hidden = !match;
        if (match) count++;
      });
      filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
      document.querySelector('#story-count').textContent = count;
      document.querySelector('#search-status').textContent = `找到 ${count} 篇作品`;
      document.querySelector('.empty-state').hidden = count > 0;
      clear.hidden = !search.value;
      const url = new URL(location.href);
      if (search.value.trim()) url.searchParams.set('q', search.value.trim()); else url.searchParams.delete('q');
      if (category !== 'all') url.searchParams.set('category', category); else url.searchParams.delete('category');
      history.replaceState(null, '', url.pathname + url.search + url.hash);
    }
    function restore() {
      const params = new URLSearchParams(location.search);
      search.value = params.get('q') || '';
      category = filters.some(button => button.dataset.filter === params.get('category')) ? params.get('category') : 'all';
      update();
    }
    search.addEventListener('input', update);
    filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; update(); }));
    clear.addEventListener('click', () => { search.value = ''; update(); search.focus(); });
    document.querySelector('.reset-search').addEventListener('click', () => { category = 'all'; search.value = ''; update(); search.focus(); });
    window.addEventListener('popstate', restore);
    restore();
  }
  if (document.body.classList.contains('reader-page')) {
    const modes = [...document.querySelectorAll('.read-modes button')];
    const status = document.querySelector('#reader-status');
    const storage = {
      get(key) { try { return localStorage.getItem(key); } catch { return null; } },
      set(key, value) { try { localStorage.setItem(key, value); } catch { /* Reading works with storage disabled. */ } }
    };
    function setMode(mode, announce = false) {
      if (!['both', 'zh', 'en'].includes(mode)) mode = 'both';
      document.body.dataset.mode = mode;
      const englishTitle = document.querySelector('.article-title-en');
      if (mode === 'en') {
        englishTitle.setAttribute('role', 'heading');
        englishTitle.setAttribute('aria-level', '1');
      } else {
        englishTitle.removeAttribute('role');
        englishTitle.removeAttribute('aria-level');
      }
      modes.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.mode === mode)));
      storage.set('bamin-reading-mode', mode);
      if (announce) status.textContent = `已切换为${mode === 'both' ? '中英对照' : mode === 'zh' ? '中文阅读' : 'English'}`;
      progress();
    }
    function setFont(value) {
      const size = Math.min(24, Math.max(16, Number(value) || 18));
      document.documentElement.style.setProperty('--reading-size', size + 'px');
      storage.set('bamin-reading-size', String(size));
      document.querySelector('[data-font=down]').disabled = size === 16;
      document.querySelector('[data-font=up]').disabled = size === 24;
      return size;
    }
    let font = setFont(storage.get('bamin-reading-size'));
    document.querySelectorAll('[data-font]').forEach(button => button.addEventListener('click', () => {
      font = setFont(font + (button.dataset.font === 'up' ? 2 : -2));
      status.textContent = `正文字号 ${font}`;
      progress();
    }));
    modes.forEach(button => button.addEventListener('click', () => setMode(button.dataset.mode, true)));
    const bar = document.querySelector('.reading-progress span');
    function progress() {
      const content = document.querySelector('.reading-content');
      const top = content.getBoundingClientRect().top + window.scrollY;
      const distance = content.offsetHeight - window.innerHeight + 68;
      const percentage = Math.max(0, Math.min(1, (window.scrollY - top + 68) / Math.max(1, distance)));
      bar.style.width = `${percentage * 100}%`;
    }
    setMode(storage.get('bamin-reading-mode') || 'both');
    window.addEventListener('scroll', progress, { passive: true });
    window.addEventListener('resize', progress);
    window.addEventListener('load', progress);
    document.querySelector('.copy-link').addEventListener('click', async event => {
      const button = event.currentTarget;
      try {
        if (!navigator.clipboard) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(location.href);
        button.textContent = '已复制';
        status.textContent = '文章链接已复制';
        setTimeout(() => { button.textContent = '复制链接'; }, 1800);
      } catch {
        status.textContent = '请从浏览器地址栏复制文章链接';
        button.textContent = '请复制地址栏链接';
      }
    });
  }
})();
