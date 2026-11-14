# Records the REAL EvalLoop UI (sandbox providers) for scene 4, then extracts frames. Usage: python3 record_ui.py [fps]
import json, os, shutil, subprocess, sys, time, urllib.request, glob, tempfile
from playwright.sync_api import sync_playwright
fps = int(sys.argv[1]) if len(sys.argv) > 1 else 10; here = os.path.dirname(os.path.abspath(__file__)); port = 8783
data = tempfile.mkdtemp(); vid = tempfile.mkdtemp()
srv = subprocess.Popen(['node', os.path.join(here, '..', 'evalloop.mjs'), '--demo'], env={**os.environ, 'PORT': str(port), 'DATA_DIR': data}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    req = urllib.request.Request(f'http://localhost:{port}/api/demo', method='POST', headers={'x-evalloop': '1', 'content-type': 'application/json'})
    rid = json.load(urllib.request.urlopen(req))['runId']
    with sync_playwright() as p:
        b = p.chromium.launch(); c = b.new_context(viewport={'width': 1280, 'height': 720}, record_video_dir=vid, record_video_size={'width': 1280, 'height': 720})
        c.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const p=document.getElementById('pre'); if(p) p.remove();})")
        pg = c.new_page(); pg.goto(f'http://localhost:{port}/#/run/{rid}'); pg.wait_for_timeout(13500); c.close(); b.close()
    webm = glob.glob(os.path.join(vid, '*.webm'))[0]; out = os.path.join(here, 'clip'); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', webm, '-vf', f'fps={fps}', os.path.join(out, 'f%04d.png')], check=True)
    n = len(os.listdir(out)); json.dump({'dir': 'clip', 'fps': fps, 'n': n}, open(os.path.join(here, 'clip.json'), 'w')); print('frames:', n)
finally:
    srv.terminate()
