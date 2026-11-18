#!/usr/bin/env python3
"""Strict educational Piet runner: colored blocks/black, six commands, no white/input.

It reads only the supplied PNG, never a compiled instruction list. This is NOT a
complete Piet implementation; unsupported commands/colors are explicit errors.
"""
import argparse
import json
from pathlib import Path
from PIL import Image

# Hue order: red, yellow, green, cyan, blue, magenta. Light/normal/dark.
COLORS=(
 ('#ffc0c0','#ffffc0','#c0ffc0','#c0ffff','#c0c0ff','#ffc0ff'),
 ('#ff0000','#ffff00','#00ff00','#00ffff','#0000ff','#ff00ff'),
 ('#c00000','#c0c000','#00c000','#00c0c0','#0000c0','#c000c0'),
)
RGB={tuple(bytes.fromhex(value[1:])):(h,l) for l,row in enumerate(COLORS) for h,value in enumerate(row)}
OPS={(0,1):'push',(0,2):'pop',(1,0):'add',(1,2):'multiply',(3,1):'pointer',(5,2):'outchar'}
DELTAS={name:delta for delta,name in OPS.items()}
DIRECTIONS=((1,0),(0,1),(-1,0),(0,-1))


def load(path,codel_size=1):
    if codel_size<1:raise ValueError('codel size must be positive')
    with Image.open(path) as image:
        if image.format!='PNG' or getattr(image,'n_frames',1)!=1:raise ValueError('single-frame PNG required')
        if image.mode not in ('RGB','RGBA'):raise ValueError('RGB/RGBA required')
        rgba=image.convert('RGBA')
        if rgba.getextrema()[3]!=(255,255):raise ValueError('transparency is not code')
        width,height=image.size
        if width%codel_size or height%codel_size:raise ValueError('image must be divisible by codel size')
        pixels=image.convert('RGB');grid=[]
        for y in range(0,height,codel_size):
            row=[]
            for x in range(0,width,codel_size):
                tile=pixels.crop((x,y,x+codel_size,y+codel_size))
                values=set(tile.get_flattened_data())
                if len(values)!=1:raise ValueError('each codel must be one flat color; no resampling')
                color=next(iter(values))
                if color!=(0,0,0) and color not in RGB:raise ValueError('unsupported color (white is not supported)')
                row.append(color)
            grid.append(row)
    return grid


def component(grid,point):
    x,y=point;color=grid[y][x];seen={point};todo=[point]
    while todo:
        x,y=todo.pop()
        for dx,dy in DIRECTIONS:
            p=(x+dx,y+dy);xx,yy=p
            if 0<=yy<len(grid) and 0<=xx<len(grid[0]) and p not in seen and grid[yy][xx]==color:
                seen.add(p);todo.append(p)
    return seen


def exit_point(block,dp,cc):
    dx,dy=DIRECTIONS[dp]
    # Max projection along DP; tie goes CC-left, relative to the current DP.
    lx,ly=dy,-dx
    sign=1 if cc==0 else -1
    return max(block,key=lambda p:(p[0]*dx+p[1]*dy,sign*(p[0]*lx+p[1]*ly)))


def execute(operation,area,stack,dp):
    if operation=='push':stack.append(area)
    elif operation=='pop':
        if stack:stack.pop()
    elif operation in ('add','multiply'):
        if len(stack)>=2:
            b=stack.pop();a=stack.pop();stack.append(a+b if operation=='add' else a*b)
    elif operation=='pointer':
        if stack:dp=(dp+stack.pop())%4
    elif operation=='outchar':
        if stack:
            code=stack.pop()
            if not 0<=code<=0x10ffff or 0xd800<=code<=0xdfff:raise ValueError('invalid Unicode output')
            return dp,chr(code)
    else:raise ValueError(f'unsupported instruction: {operation}')
    return dp,''


def run(grid,max_steps=1000):
    if not grid or not grid[0] or len({len(row) for row in grid})!=1:raise ValueError('rectangular nonempty grid required')
    if grid[0][0] not in RGB:raise ValueError('start must be a supported colored codel')
    point=(0,0);dp=0;cc=0;stack=[];output='';trace=[]
    for step in range(max_steps):
        block=component(grid,point);before=stack.copy();attempts=[];target=None
        for attempt in range(8):
            origin=exit_point(block,dp,cc);dx,dy=DIRECTIONS[dp];candidate=(origin[0]+dx,origin[1]+dy)
            x,y=candidate
            blocked=not(0<=y<len(grid) and 0<=x<len(grid[0])) or grid[y][x]==(0,0,0)
            attempts.append({'dp':dp,'cc':cc,'exit':list(origin),'blocked':blocked})
            if not blocked:target=candidate;break
            if attempt%2==0:cc=1-cc
            else:dp=(dp+1)%4
        if target is None:
            trace.append({'step':step,'operation':'halt','source':list(point),'area':len(block),
                          'block':[list(p) for p in sorted(block)],'attempts':attempts,
                          'stack_before':before,'stack_after':stack.copy(),'output':output,'dp':dp,'cc':cc})
            return {'output':output,'halted':True,'trace':trace,'stack':stack}
        src=RGB[grid[point[1]][point[0]]]
        color=grid[target[1]][target[0]]
        if color not in RGB:raise ValueError('white/unknown-color traversal is not supported')
        dest=RGB[color];delta=((dest[0]-src[0])%6,(dest[1]-src[1])%3)
        if delta not in OPS:raise ValueError(f'unsupported Piet color delta: {delta}')
        operation=OPS[delta];dp,char=execute(operation,len(block),stack,dp);output+=char
        trace.append({'step':step,'operation':operation,'source':list(point),'target':list(target),
                      'area':len(block),'block':[list(p) for p in sorted(block)],'attempts':attempts,
                      'stack_before':before,'stack_after':stack.copy(),'output':output,'dp':dp,'cc':cc})
        point=target
    return {'output':output,'halted':False,'trace':trace,'stack':stack}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image',type=Path)
    parser.add_argument('--codel-size',type=int,default=1)
    parser.add_argument('--max-steps',type=int,default=1000)
    parser.add_argument('--trace',type=Path)
    args=parser.parse_args()
    if args.max_steps<1:parser.error('--max-steps must be positive')
    try:result=run(load(args.image,args.codel_size),args.max_steps)
    except ValueError as e:parser.error(str(e))
    if args.trace:args.trace.write_text(json.dumps(result,indent=2)+'\n')
    print(result['output'],end='')
    if not result['halted']:raise SystemExit(2)
