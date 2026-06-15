import re

html_path = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════
# 1. CSS
# ══════════════════════════════════════════════

desktop_css = """
        .order-btn { flex: 0 0 100%; display: block; text-align: center; background: #25D366; color: #fff !important; font-family: 'Montserrat', sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; text-decoration: none; padding: 9px 0; margin-top: 10px; transition: background .2s; }
        .order-btn:hover { background: #20b958; }
        .lb { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.93); z-index: 500; align-items: center; justify-content: center; }
        .lb.open { display: flex; }
        .lb-inner { position: relative; display: flex; flex-direction: column; align-items: center; max-width: 96vw; }
        .lb img { max-width: 92vw; max-height: 82vh; object-fit: contain; display: block; background: transparent; padding: 0; }
        .lb-close { position: fixed; top: 14px; right: 18px; background: none; border: none; color: rgba(255,255,255,.75); font-size: 30px; cursor: pointer; z-index: 501; line-height: 1; padding: 4px 10px; }
        .lb-close:hover { color: #fff; }
        .lb-dots { display: flex; gap: 8px; margin-top: 14px; }
        .lb-dot { width: 8px; height: 8px; border-radius: 50%; border: 1.5px solid rgba(255,255,255,.5); padding: 0; background: transparent; cursor: pointer; transition: background .15s; }
        .lb-dot.active { background: #fff; border-color: #fff; }
        .card-gallery { cursor: zoom-in; }
        .card > img { cursor: zoom-in; }"""

mobile_css_new = "\n            .order-btn { font-size: 10px; padding: 8px 0; margin-top: 8px; }"

style_end = html.rfind('</style>')
if '.order-btn' not in html and style_end != -1:
    html = html[:style_end] + desktop_css + '\n    ' + html[style_end:]
    print("Desktop CSS added")

mobile_anchor = '            .gallery-dot { width: 6px; height: 6px; }'
if '.order-btn' not in html and mobile_anchor in html:
    html = html.replace(mobile_anchor, mobile_anchor + mobile_css_new)
    print("Mobile CSS added")

# card-footer: add flex-wrap so order-btn goes to new row on desktop too
html = html.replace(
    '.card-footer { padding: 14px 2px 14px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; }',
    '.card-footer { padding: 14px 2px 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; flex-wrap: wrap; }'
)

# ══════════════════════════════════════════════
# 2. Transform cards: <a class="card"> → <div>, add order-btn
# ══════════════════════════════════════════════
card_re = re.compile(r'(<a\b[^>]*class="card"[^>]*>)(.*?)(</a>)', re.DOTALL)

transformed = 0

def transform_card(m):
    global transformed
    open_tag = m.group(1)
    content = m.group(2)

    # Extract WA URL
    wa_m = re.search(r'href="(https://wa\.me/[^"]+)"', open_tag)
    wa_url = wa_m.group(1) if wa_m else '#'

    # New opening: <div ...> without href/target
    new_open = open_tag.replace('<a ', '<div ', 1)
    new_open = re.sub(r'\s*href="[^"]*"', '', new_open)
    new_open = re.sub(r'\s*target="[^"]*"', '', new_open)

    # Remove order-hint from card-overlay
    content = re.sub(r'<div class="order-hint">[^<]*</div>', '', content)

    # Add order-btn after price div, before closing card-footer </div>
    # card-footer always ends: ...<div class="price">X</div></div>
    btn = f'<a href="{wa_url}" target="_blank" class="order-btn">Заказать</a>'
    last_dd = content.rfind('</div></div>')
    if last_dd != -1:
        insert_pos = last_dd + len('</div>')
        content = content[:insert_pos] + btn + content[insert_pos:]

    transformed += 1
    return new_open + content + '</div>'

html = card_re.sub(transform_card, html)
print(f"Transformed {transformed} cards")

# ══════════════════════════════════════════════
# 3. Lightbox HTML (before </body>)
# ══════════════════════════════════════════════
lb_html = '''
<div id="lb" class="lb" onclick="if(event.target===this)lbClose()">
  <button class="lb-close" onclick="lbClose()">✕</button>
  <div class="lb-inner">
    <img id="lb-img" src="" alt="">
    <div id="lb-dots" class="lb-dots"></div>
  </div>
</div>'''

if 'id="lb"' not in html:
    html = html.replace('</body>', lb_html + '\n</body>', 1)
    print("Lightbox HTML added")

# ══════════════════════════════════════════════
# 4. Lightbox JS (before last </script>)
# ══════════════════════════════════════════════
lb_js = """
// ── Lightbox ──
(function(){
  var _imgs=[], _cur=0;
  function _show(){
    document.getElementById('lb-img').src=_imgs[_cur];
    var de=document.getElementById('lb-dots'); de.innerHTML='';
    if(_imgs.length>1){
      _imgs.forEach(function(_,i){
        var d=document.createElement('button');
        d.className='lb-dot'+(i===_cur?' active':'');
        d.onclick=function(){_cur=i;_show();};
        de.appendChild(d);
      });
    }
  }
  window.lbOpen=function(srcs,idx){
    _imgs=srcs; _cur=idx||0; _show();
    document.getElementById('lb').classList.add('open');
    document.body.style.overflow='hidden';
  };
  window.lbClose=function(){
    document.getElementById('lb').classList.remove('open');
    document.body.style.overflow='';
  };
  document.addEventListener('keydown',function(e){if(e.key==='Escape')lbClose();});
  var _sx=0;
  var _lbEl=document.getElementById('lb');
  _lbEl.addEventListener('touchstart',function(e){_sx=e.touches[0].clientX;},{passive:true});
  _lbEl.addEventListener('touchend',function(e){
    var dx=e.changedTouches[0].clientX-_sx;
    if(Math.abs(dx)<40||_imgs.length<2)return;
    if(dx<0&&_cur<_imgs.length-1){_cur++;_show();}
    else if(dx>0&&_cur>0){_cur--;_show();}
  });
  // Single img (no gallery)
  document.querySelectorAll('.card > img').forEach(function(img){
    img.addEventListener('click',function(){lbOpen([this.src],0);});
  });
  // Gallery
  document.querySelectorAll('.card-gallery').forEach(function(gal){
    gal.addEventListener('click',function(e){
      if(e.target.classList.contains('gallery-dot'))return;
      var srcs=Array.from(this.querySelectorAll('img')).map(function(i){return i.src;});
      var c=0;
      this.querySelectorAll('img').forEach(function(im,i){if(im.classList.contains('active'))c=i;});
      lbOpen(srcs,c);
    });
  });
})();
"""

if 'lbOpen' not in html:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + lb_js + html[last_script:]
        print("Lightbox JS added")

# ══════════════════════════════════════════════
# 5. Save
# ══════════════════════════════════════════════
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved.")
