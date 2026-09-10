#!/usr/bin/env python3
"""Gera ../artifact.html: HTML unico com fotos, logos e GSAP embutidos (para publicar como Artifact)."""
import base64,re,os,mimetypes
here=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(here,'index.html'),encoding='utf-8').read()
def data_uri(path):
    mt=mimetypes.guess_type(path)[0] or 'application/octet-stream'
    return 'data:%s;base64,%s'%(mt,base64.b64encode(open(path,'rb').read()).decode())
# assets
s=re.sub(r'(src|href|data-src)="(assets/[^"]+)"',lambda m:'%s="%s"'%(m.group(1),data_uri(os.path.join(here,m.group(2)))),s)
# vendor scripts inline
def inline_js(m):
    js=open(os.path.join(here,m.group(1)),encoding='utf-8').read()
    return '<script>'+js+'</script>'
s=re.sub(r'<script src="(vendor/[^"]+)"></script>',inline_js,s)
# strip document wrapper (artifact adds its own)
s=re.sub(r'^\s*<!doctype html>\s*<html[^>]*>\s*<head>\s*','',s,flags=re.I)
s=re.sub(r'</head>\s*<body>\s*','',s,flags=re.I)
s=re.sub(r'\s*</body>\s*</html>\s*$','\n',s,flags=re.I)
# titulo curto so no artifact (a tag <title> do index.html continua otimizada para SEO)
s=re.sub(r'<title>[^<]*</title>','<title>Minas Brasil Piscinas</title>',s,count=1)
out=os.path.join(here,'..','artifact.html')
open(out,'w',encoding='utf-8').write(s)
print('ok',out,round(os.path.getsize(out)/1e6,2),'MB')
