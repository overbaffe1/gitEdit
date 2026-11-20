"""Bounded deterministic payload for a manually dispatched GitHub Actions demo."""
from pathlib import Path
import csv,hashlib,io,json,math,os,re

def parse_inputs(env):
 motif=env.get('LAB_MOTIF','orbit');palette=env.get('LAB_PALETTE','night');raw=env.get('LAB_COUNT','24');flag=env.get('LAB_INCLUDE_CSV','true')
 if motif not in ('orbit','spiral'):raise ValueError('motif must be orbit or spiral')
 if palette not in ('night','paper'):raise ValueError('palette must be night or paper')
 if not re.fullmatch(r'[0-9]{1,3}',raw) or not 12<=int(raw)<=96:raise ValueError('count must be an integer from 12 to 96')
 if flag not in ('true','false'):raise ValueError('include_csv must be true or false')
 return {'motif':motif,'count':int(raw),'palette':palette,'include_csv':flag=='true'}

def coordinates(motif,count):
 points=[]
 for i in range(count):
  angle=(math.tau*i/count) if motif=='orbit' else i*math.pi*(3-math.sqrt(5))
  radius=205 if motif=='orbit' else 205*math.sqrt((i+1)/count)
  points.append((320+radius*math.cos(angle),260+radius*math.sin(angle)))
 return points

def build(params):
 points=coordinates(params['motif'],params['count']);bg,ink=('#142d38','#d6edab') if params['palette']=='night' else ('#f1e8d6','#214b59')
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="520" viewBox="0 0 640 520" role="img" aria-labelledby="title desc">','<title id="title">Native Actions experiment</title>',f'<desc id="desc">{params["count"]} points; {params["motif"]}; {params["palette"]}. Deterministic generated output, not a cloud-run screenshot.</desc>',f'<rect width="640" height="520" fill="{bg}"/>']
 for i,(x,y) in enumerate(points):parts.append(f'<circle cx="{x:.6f}" cy="{y:.6f}" r="{3+i%3}" fill="{ink}"/>')
 parts.append('</svg>');files={'drawing.svg':('\n'.join(parts)+'\n').encode()}
 if params['include_csv']:
  stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n');writer.writerow(['id','x','y'])
  for i,(x,y) in enumerate(points):writer.writerow([i+1,f'{x:.6f}',f'{y:.6f}'])
  files['coordinates.csv']=stream.getvalue().encode()
 hashes={name:hashlib.sha256(data).hexdigest() for name,data in files.items()}
 result={'parameters':params,'points':len(points),'bounds':[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)],'sha256':hashes,'scope':'Deterministic output. No claim that this was executed by GitHub Actions.'}
 files['result.json']=(json.dumps(result,indent=2)+'\n').encode()
 summary=f'''# Native lab: результат генератора

Это отчёт payload-скрипта. Сам по себе этот текст не доказывает облачный запуск: его можно получить и локально.

| Параметр | Значение |
|---|---|
| Расположение | {params['motif']} |
| Точки | {params['count']} |
| Палитра | {params['palette']} |
| CSV | {'yes' if params['include_csv'] else 'no'} |

## SHA-256 файлов

'''+''.join(f'- `{name}`: `{digest}`\n' for name,digest in hashes.items())+'''
SVG находится **в artifact**, а не встроен локальной ссылкой в эту страницу. Скачай `native-lab-result`, распакуй и открой drawing.svg. ZIP также содержит result.json и этот отчёт, а при включённом CSV — coordinates.csv.

Workflow не коммитит результат в репозиторий. Artifact временный; срок хранения в YAML — 3 дня с учётом политик GitHub. Для загрузки может требоваться вход и доступ к репозиторию.
'''
 files['summary.md']=summary.encode();return files

def execute(env):
 params=parse_inputs(env);files=build(params);output=Path(env.get('LAB_OUTPUT','/tmp/native-lab-result'))
 if output.exists() and any(output.iterdir()):raise ValueError('output directory must be empty; refusing stale or mixed results')
 output.mkdir(parents=True,exist_ok=True)
 for name,data in files.items():(output/name).write_bytes(data)
 summary=env.get('GITHUB_STEP_SUMMARY')
 if summary:
  with Path(summary).open('ab') as f:f.write(files['summary.md'])
 return output

if __name__=='__main__':
 try:print(execute(os.environ))
 except ValueError as e:raise SystemExit(str(e))
