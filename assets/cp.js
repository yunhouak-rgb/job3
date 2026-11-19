(function(){
  var boxes=document.querySelectorAll('.cp-box[data-cp]');
  if(!boxes.length) return;
  var OK=['https://link.coupang.com/','https://bestmore.net/click.php'];
  function lab(t){return t.replace(/\s*보기$/,'').replace(/\s*보기\s*\(/,' (');}
  fetch('/cp-links.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){
    var it=(d&&d.items)||{};
    boxes.forEach(function(b){
      var keys=b.getAttribute('data-cp').split(',');
      var html='', cp=false, lp=false, n=0;
      keys.forEach(function(k){
        k=k.trim(); var x=it[k];
        if(!x||!x.url||!OK.some(function(p){return x.url.indexOf(p)===0;})) return;
        var isLp=x.src==='linkprice'; if(isLp) lp=true; else cp=true; n++;
        html+='<a href="'+x.url+'" target="_blank" rel="sponsored nofollow noopener" data-cpk="'+k+'" style="display:flex;align-items:center;gap:12px;padding:12px 14px;background:var(--white,#fff);border:1.5px solid var(--gray-200,#e5e5e5);border-radius:12px;color:var(--text,#222);text-decoration:none;">'
          +'<span style="font-size:1.6rem;line-height:1;flex:none;">'+(x.icon||(isLp?'🎓':'🛒'))+'</span>'
          +'<span style="flex:1;min-width:0;"><b style="display:block;font-size:.93rem;">'+lab(x.label)+'</b>'+(x.note?'<span style="display:block;font-size:.8rem;color:var(--text-sub,#666);margin-top:2px;line-height:1.45;">'+x.note+'</span>':'')+'</span>'
          +'<span style="flex:none;font-size:.8rem;font-weight:800;color:#fff;background:'+(isLp?'#5624d0':'#e52528')+';padding:7px 10px;border-radius:8px;white-space:nowrap;">'+(isLp?'강의 보기':'가격 보기')+'</span></a>';
      });
      if(!html) return;
      var disc=(cp?'쿠팡 파트너스 활동으로 일정액의 수수료를 받습니다. ':'')+(lp?'일부 링크는 링크프라이스 제휴 링크로, 구매 시 수수료를 받을 수 있습니다.':'');
      b.innerHTML='<div style="font-size:.95rem;font-weight:900;color:var(--black,#111);margin-bottom:10px;">'+(b.getAttribute('data-title')||'준비물 한 번에 보기')+'</div>'
        +'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px;">'+html+'</div>'
        +'<p style="margin:10px 0 0;font-size:.72rem;line-height:1.6;color:var(--text-muted,#999);">'+disc+'</p>';
      b.style.cssText='border:1.5px solid #f3d9a6;background:#fffdf7;border-radius:14px;padding:16px;margin:26px 0;';
      if(window.gtag) gtag('event','cp_view',{page:location.pathname,items:n});
      b.addEventListener('click',function(e){var a=e.target.closest('a[data-cpk]'); if(a&&window.gtag) gtag('event','cp_click',{item:a.getAttribute('data-cpk'),page:location.pathname});});
    });
  }).catch(function(){});
})();
