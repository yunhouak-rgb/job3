(function(){
  var boxes=document.querySelectorAll('.cp-box[data-cp]');
  if(!boxes.length) return;
  var OK=['https://link.coupang.com/','https://bestmore.net/click.php'];
  fetch('/cp-links.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){
    var it=(d&&d.items)||{};
    boxes.forEach(function(b){
      var keys=b.getAttribute('data-cp').split(',');
      var html='', cp=false, lp=false;
      keys.forEach(function(k){
        var x=it[k.trim()];
        if(!x||!x.url||!OK.some(function(p){return x.url.indexOf(p)===0;})) return;
        var isLp=x.src==='linkprice'; if(isLp) lp=true; else cp=true;
        html+='<a href="'+x.url+'" target="_blank" rel="sponsored nofollow noopener" data-cpk="'+k.trim()+'" style="display:inline-block;margin:4px 8px 4px 0;padding:9px 14px;background:var(--white,#fff);border:1.5px solid var(--gray-200,#ddd);border-radius:10px;color:var(--text,#222);font-size:.88rem;font-weight:700;text-decoration:none;">'+(isLp?'🎓 ':'🛒 ')+x.label+' →</a>';
      });
      if(!html) return;
      var disc=(cp?'이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다. ':'')+(lp?'일부 링크는 제휴 마케팅(링크프라이스) 링크로, 구매 시 일정액의 수수료를 받을 수 있습니다.':'');
      b.innerHTML='<div style="font-size:.8rem;font-weight:700;color:var(--text-sub,#666);margin-bottom:8px;">'+(b.getAttribute('data-title')||'준비물 한 번에 보기')+'</div>'+html+'<p style="margin:10px 0 0;font-size:.75rem;line-height:1.6;color:var(--text-muted,#999);">'+disc+'</p>';
      b.style.cssText='background:var(--gray-50,#f7f7f7);border-radius:12px;padding:16px 18px;margin:26px 0;';
      b.addEventListener('click',function(e){var a=e.target.closest('a[data-cpk]'); if(a&&window.gtag) gtag('event','cp_click',{item:a.getAttribute('data-cpk'),page:location.pathname});});
    });
  }).catch(function(){});
})();
