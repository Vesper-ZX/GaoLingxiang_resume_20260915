# 从所有页面提取用到的字符并做字体子集化
import glob
import subprocess
import sys

# 收集所有 HTML 文件的字符
chars = set()
for f in glob.glob('*.html') + glob.glob('awards/*.html'):
    with open(f, encoding='utf-8') as fh:
        chars.update(fh.read())

# 补充：ASCII 可打印字符 + 常用中文标点
chars.update(chr(c) for c in range(0x20, 0x7F))
chars.update('，。！？；：、“”‘’（）《》〈〉【】—…·～￥「」『』、')
chars.discard('\n')

text = ''.join(sorted(chars))
with open('fonts_src/chars.txt', 'w', encoding='utf-8') as fh:
    fh.write(text)
print('unique chars:', len(chars))

jobs = [
    ('fonts_src/smiley/SmileySans-Oblique.ttf', 'fonts/SmileySans-Oblique.subset.woff2'),
    ('fonts_src/LXGWWenKai-Regular.ttf', 'fonts/LXGWWenKai-Regular.subset.woff2'),
]
for src, dst in jobs:
    r = subprocess.run([
        sys.executable, '-m', 'fontTools.subset', src,
        '--text-file=fonts_src/chars.txt',
        '--flavor=woff2',
        f'--output-file={dst}',
        '--layout-features=*',
        '--glyph-names',
        '--symbol-cmap',
        '--legacy-cmap',
        '--notdef-glyph',
        '--notdef-outline',
        '--recommended-glyphs',
        '--name-IDs=*',
        '--name-legacy',
        '--name-languages=*',
    ], capture_output=True, text=True)
    print(dst, 'rc=', r.returncode)
    if r.returncode != 0:
        print(r.stderr[-2000:])
