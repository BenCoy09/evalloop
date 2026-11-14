# Renders the video. python3 render.py [--stills] ; env FPS (default 10 preview, use 30 for final), AUDIO=dir with s1.mp3..s8.mp3 (optional), CAPTIONS=0 to hide captions
import json, os, subprocess, sys
from playwright.sync_api import sync_playwright
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here); from script import build
fps = int(os.environ.get('FPS', 10)); real = json.load(open(os.path.join(here, 'real.json'))); timings = json.load(open(os.path.join(here, 'timings.json')))
audio = os.environ.get('AUDIO')
if audio:  # scene length = narration length + a short pause, so voice and picture always match
    for k in timings:
        f = os.path.join(audio, f'{k}.mp3')
        if os.path.exists(f): timings[k] = round(float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode()) + 0.6, 2)
clip = json.load(open(os.path.join(here, 'clip.json'))); script = build(real)
data = {'real': real, 'timings': timings, 'clip': clip, 'script': script, 'captions': os.environ.get('CAPTIONS', '1') != '0'}
open(os.path.join(here, 'script.md'), 'w').write('# EvalLoop demo narration (one file per scene for ElevenLabs: s1.mp3 ... s8.mp3)\n\n' + ''.join(f'## {k} ({timings[k]}s)\n{v}\n\n' for k, v in script.items()))
total = sum(timings.values())
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720}); pg.add_init_script(f'window.__DATA__ = {json.dumps(data)}')
    pg.goto('file://' + os.path.join(here, 'video.html')); pg.wait_for_timeout(400)
    if '--stills' in sys.argv:
        from PIL import Image
        t = 0; imgs = []
        for i, k in enumerate(timings):
            pg.evaluate('t => window.__frame(t)', t + timings[k] * 0.82); path = f'/tmp/still_{i+1}.png'; pg.screenshot(path=path); imgs.append(Image.open(path).resize((640, 360))); t += timings[k]
        sheet = Image.new('RGB', (1280, 1440)); [sheet.paste(im, ((i % 2) * 640, (i // 2) * 360)) for i, im in enumerate(imgs)]; sheet.save('/tmp/contact.png'); print('stills ok'); sys.exit(0)
    silent = os.path.join(here, 'demo_silent.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'veryfast', silent], stdin=subprocess.PIPE)
    n = int(total * fps)
    for i in range(n):
        pg.evaluate('t => window.__frame(t)', i / fps); ff.stdin.write(pg.screenshot(type='png'))
    ff.stdin.close(); ff.wait(); b.close()
final = os.path.join(here, 'demo.mp4')
if audio:
    parts = []; t = 0; cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', silent]; filt = []
    for i, k in enumerate(timings):
        f = os.path.join(audio, f'{k}.mp3')
        if os.path.exists(f): cmd += ['-i', f]; idx = len(parts) + 1; filt.append(f'[{idx}:a]adelay={int(t*1000)}|{int(t*1000)}[a{idx}]'); parts.append(f'[a{idx}]')
        t += timings[k]
    cmd += ['-filter_complex', ';'.join(filt) + ';' + ''.join(parts) + f'amix=inputs={len(parts)}:normalize=0[aout]', '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-shortest', final]
    subprocess.run(cmd, check=True); print('wrote', final)
else:
    print('wrote', silent, f'({total}s, {fps}fps)')
