# -*- coding: utf-8 -*-
import os
css = """
:root{--primary:#2563eb;--primary-h:#1d4ed8;--bg:#f1f5f9;--card:#ffffff;--text:#1e293b;--sub:#64748b;--muted:#94a3b8;--hero-s:#0f172a;--hero-e:#1e293b;--border:#e2e8f0;--border2:#cbd5e1;--green:#10b981;--amber:#f59e0b;--red:#ef4444;--sh:0 2px 8px rgba(0,0,0,.07);--sh2:0 4px 24px rgba(0,0,0,.10);--r:12px;--r2:8px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,"PingFang SC","Microsoft YaHei","Segoe UI Emoji","Inter",sans-serif;background:var(--bg);color:var(--text);font-size:14px;line-height:1.5;min-height:100vh;-webkit-font-smoothing:antialiased}
.hero-s{display:flex;width:100%;margin-bottom:.75rem;align-items:stretch;gap:8px}
.hero{background:linear-gradient(135deg,var(--hero-s),var(--hero-e));border-radius:var(--r);padding:.6rem 1rem;box-shadow:0 4px 12px rgba(0,0,0,.2);display:flex;align-items:center;flex:1 1 0;min-height:52px;position:relative;overflow:hidden}
.hero::after{content:"PH";position:absolute;right:3%;bottom:-10px;font-size:3.5rem;font-weight:900;color:rgba(255,255,255,.07);pointer-events:none;z-index:1}
.hero-content{position:relative;z-index:2;width:100%}
.hero-date{font-size:.7rem;color:rgba(255,255,255,.55);margin-bottom:.2rem;letter-spacing:.04em}
.hero-title{font-size:1rem;font-weight:800;color:#fff;margin-bottom:.08rem;letter-spacing:.02em}
.hero-sub{font-size:.72rem;color:rgba(255,255,255,.45)}
.hero-r{margin-left:auto;display:flex;flex-direction:column;align-items:flex-end;gap:.15rem;padding-left:1rem}
.hero-stats{display:flex;gap:.45rem;flex-wrap:wrap;justify-content:flex-end}
.hero-stat{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:6px;padding:.18rem .5rem;font-size:.68rem;color:rgba(255,255,255,.7)}
.hero-stat strong{color:#fff;font-weight:700}
.logo-wrap{flex:0 0 44px;display:flex;justify-content:center;align-items:center}
.logo{height:32px;width:auto;object-fit:contain}
.container{max-width:1280px;margin:0 auto;padding:.875rem;padding-bottom:2rem}
.app-body{display:grid;grid-template-columns:210px 1fr;gap:.875rem;align-items:start}
@media(max-width:900px){.app-body{grid-template-columns:1fr}}
.sidebar{background:var(--card);border-radius:var(--r);border:1px solid var(--border);box-shadow:var(--sh);overflow:hidden;position:sticky;top:.875rem}
.sidebar-toggle{display:flex;align-items:center;justify-content:space-between;padding:.6rem .875rem;background:var(--hero-s);color:rgba(255,255,255,.7);font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;cursor:pointer;border-bottom:1px solid rgba(255,255,255,.08)}
.sidebar-toggle:hover{background:#1a2540}
.nav-items{padding:.5rem}
.nav-items.collapsed{display:none}
.nav-item{display:flex;align-items:center;gap:.5rem;width:100%;text-align:left;padding:.5rem .625rem;border:1px solid transparent;border-radius:var(--r2);font-size:.82rem;color:var(--sub);background:transparent;cursor:pointer;transition:all .15s;margin-bottom:.12rem}
.nav-item:hover{background:var(--bg);color:var(--text);border-color:var(--border)}
.nav-item.active{background:#eff6ff;border-color:#bfdbfe;color:var(--primary);font-weight:600}
.nav-icon{font-size:.95rem;width:18px;text-align:center;flex-shrink:0;line-height:1}
.nav-label{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nav-count{background:var(--bg);border-radius:10px;padding:.08rem .38rem;font-size:.62rem;color:var(--muted);min-width:20px;text-align:center;flex-shrink:0}
.nav-item.active .nav-count{background:#dbeafe;color:var(--primary)}
.main{display:flex;flex-direction:column;gap:.875rem}
.search-bar{background:var(--card);border-radius:var(--r);border:1px solid var(--border);box-shadow:var(--sh);padding:.65rem 1rem;display:flex;align-items:center;gap:.75rem}
.search-title{font-size:.82rem;font-weight:700;color:var(--text);white-space:nowrap;display:flex;align-items:center;gap:.35rem}
.search-count{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:.12rem .5rem;font-size:.68rem;color:var(--sub);font-weight:400}
.search-wrap{flex:1;max-width:300px;position:relative}
.search-wrap input{width:100%;padding:.4rem .7rem .4rem 2rem;background:var(--bg);border:1px solid var(--border);border-radius:var(--r2);color:var(--text);font-size:.82rem;transition:border .15s}
.search-wrap input:focus{outline:none;border-color:var(--primary);background:#fff}
.search-wrap input::placeholder{color:var(--muted)}
.search-icon{position:absolute;left:.55rem;top:50%;transform:translateY(-50%);color:var(--muted);font-size:.82rem;pointer-events:none}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.875rem}
@media(max-width:900px){.grid{grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:.9rem 1rem;display:flex;flex-direction:column;gap:.6rem;transition:box-shadow .2s,border-color .2s,transform .2s}
.card:hover{box-shadow:var(--sh2);border-color:var(--border2);transform:translateY(-2px)}
.card-top{display:flex;align-items:center;gap:.5rem}
.badge{padding:.18rem .5rem;border-radius:5px;font-size:.62rem;font-weight:700;white-space:nowrap;flex-shrink:0}
.bg-h{background:#eef2ff;color:#6366f1}
.bg-x{background:#fdf4ff;color:#a855f7}
.bg-y{background:#f0fdf4;color:#16a34a}
.bg-t{background:#eff6ff;color:#2563eb}
.bg-q{background:#fffbeb;color:#d97706}
.title{font-size:.875rem;font-weight:700;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--text)}
.content{font-size:.8rem;color:var(--sub);line-height:1.65;white-space:pre-wrap;word-break:break-all;flex:1;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.content.expanded{display:block;-webkit-line-clamp:unset;overflow:visible}
.expand{font-size:.7rem;color:var(--primary);cursor:pointer;user-select:none;display:inline-flex;align-items:center;gap:.2rem}
.expand:hover{text-decoration:underline}
.footer{display:flex;align-items:center;gap:.4rem;border-top:1px solid var(--border);padding-top:.6rem;margin-top:auto}
.date{font-size:.65rem;color:var(--muted);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.btn{display:inline-flex;align-items:center;gap:.2rem;padding:.28rem .55rem;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--sub);font-size:.72rem;cursor:pointer;transition:all .15s;white-space:nowrap}
.btn:hover{background:var(--bg);border-color:var(--border2);color:var(--text)}
.btn-copy:hover{border-color:#86efac;color:var(--green)}
.btn-copy.copied{border-color:#86efac;color:var(--green);background:#f0fdf4}
.btn-like{font-size:.75rem}
.btn-like:hover{border-color:#93c5fd;color:var(--primary)}
.btn-like.liked{border-color:#93c5fd;color:var(--primary);background:#eff6ff}
.like-num{font-weight:700}
.btn-del:hover{border-color:#fca5a5;color:var(--red)}
.demand{background:var(--card);border:1px solid var(--border);border-radius:var(--r);box-shadow:var(--sh);overflow:hidden}
.demand-h{display:flex;align-items:center;gap:.6rem;padding:.7rem 1rem;cursor:pointer;background:linear-gradient(135deg,#fffbeb,#fefce8);border-bottom:1px solid #fde68a}
.demand-h:hover{background:linear-gradient(135deg,#fef9c3,#fef9c3)}
.demand-title{font-size:.82rem;font-weight:800;color:var(--amber);display:flex;align-items:center;gap:.35rem}
.demand-badge{background:rgba(245,158,11,.12);color:var(--amber);border-radius:10px;padding:.08rem .4rem;font-size:.62rem;font-weight:700}
.demand-tog{margin-left:auto;font-size:.68rem;color:var(--muted);display:flex;align-items:center;gap:.2rem}
.demand-b{padding:.75rem 1rem}
.demand-b.collapsed{display:none}
.demand-r{display:flex;gap:.6rem;overflow-x:auto;padding-bottom:.2rem;scrollbar-width:thin;scrollbar-color:var(--border2) transparent}
.demand-r::-webkit-scrollbar{height:3px}
.demand-r::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
.demand-card{flex-shrink:0;width:210px;background:var(--bg);border:1px solid var(--border);border-radius:var(--r2);padding:.65rem .8rem;display:flex;flex-direction:column;gap:.3rem}
.demand-rr{display:flex;align-items:center;gap:.4rem}
.rank{width:20px;height:20px;border-radius:50%;background:#fef3c7;color:var(--amber);font-size:.65rem;font-weight:800;display:flex;align-items:center;justify-content:center}
.rank.top3{background:var(--amber);color:#fff}
.rank-title{font-size:.78rem;font-weight:700;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rank-c{font-size:.72rem;color:var(--sub);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.rank-l{display:flex;align-items:center;gap:.25rem;font-size:.68rem;color:var(--amber);font-weight:700}
.form-section{display:grid;grid-template-columns:1fr 1fr;gap:.875rem}
@media(max-width:700px){.form-section{grid-template-columns:1fr}}
.form-block{background:var(--card);border:1px solid var(--border);border-radius:var(--r);box-shadow:var(--sh);padding:.875rem 1rem}
.form-title{font-size:.7rem;font-weight:700;color:var(--sub);text-transform:uppercase;letter-spacing:.07em;margin-bottom:.6rem;display:flex;align-items:center;gap:.3rem}
.form-title::before{content:"";display:block;width:3px;height:11px;border-radius:2px;background:var(--primary)}
.form-title.demand::before{background:var(--amber)}
.f-row{display:flex;gap:.5rem;align-items:flex-start}
.f-col{flex:1;display:flex;flex-direction:column;gap:.4rem}
.f-input,.f-select,.f-textarea{width:100%;padding:.42rem .6rem;background:var(--bg);border:1px solid var(--border);border-radius:7px;color:var(--text);font-size:.8rem;font-family:inherit;transition:border .15s}
.f-input:focus,.f-select:focus,.f-textarea:focus{outline:none;border-color:var(--primary);background:#fff}
.f-input::placeholder,.f-textarea::placeholder{color:var(--muted)}
.f-select{cursor:pointer}
.f-select option{background:var(--card)}
.f-textarea{resize:vertical;min-height:54px;max-height:88px}
.btn-submit{flex-shrink:0;padding:.42rem .85rem;background:var(--primary);color:#fff;border:none;border-radius:7px;font-size:.8rem;font-weight:700;cursor:pointer;transition:background .15s,transform .1s;align-self:flex-end;white-space:nowrap}
.btn-submit:hover{background:var(--primary-h)}
.btn-submit:active{transform:scale(.97)}
.btn-submit:disabled{opacity:.5;cursor:not-allowed}
.btn-submit-demand{background:var(--amber)}
.btn-submit-demand:hover{background:#d97706}
.empty{text-align:center;padding:2.5rem 1rem;color:var(--sub)}
.empty .empty-icon{font-size:2.5rem;margin-bottom:.6rem}
.empty p{font-size:.85rem}
.loading{text-align:center;padding:1.5rem;color:var(--sub);font-size:.82rem}
#toast{position:fixed;bottom:1.5rem;right:1.5rem;background:var(--card);border:1px solid var(--border2);color:var(--text);padding:.6rem 1rem;border-radius:10px;font-size:.8rem;box-shadow:var(--sh2);opacity:0;transform:translateY(8px);transition:all .2s;z-index:9999;pointer-events:none;max-width:260px}
#toast.show{opacity:1;transform:translateY(0)}
#toast.toast-success{border-color:#86efac}
#toast.toast-error{border-color:#fca5a5}
"""
print(f"CSS: {len(css)} chars")
