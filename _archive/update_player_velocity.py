import re
from pathlib import Path
path = Path('base/ships.tbl')
text = path.read_text(encoding='utf8')
lines = text.splitlines()
flag_pattern = re.compile(r'\$Flags\s*:\s*\(.*\bplayer_ship\b.*\)', re.IGNORECASE)
max_pattern = re.compile(r'^(?P<indent>\s*\$Max Velocity\s*:\s*)(?P<vals>[^;]+?)(?P<comment>\s*;;.*)?$')
rear_pattern = re.compile(r'^(?P<indent>\s*\$Rear Velocity\s*:\s*)(?P<val>[^;]+?)(?P<comment>\s*;;.*)?$')
changes = []
for idx,line in enumerate(lines):
    if flag_pattern.search(line):
        max_idx = None
        rear_idx = None
        for j in range(idx-1, max(idx-51, -1), -1):
            if max_idx is None and max_pattern.match(lines[j]):
                max_idx = j
            if rear_idx is None and rear_pattern.match(lines[j]):
                rear_idx = j
            if max_idx is not None and rear_idx is not None:
                break
        if max_idx is None:
            for j in range(idx+1, min(idx+51, len(lines))):
                if max_pattern.match(lines[j]):
                    max_idx = j
                    break
        if rear_idx is None:
            for j in range(idx+1, min(idx+51, len(lines))):
                if rear_pattern.match(lines[j]):
                    rear_idx = j
                    break
        if max_idx is None or rear_idx is None:
            continue
        max_line = lines[max_idx]
        m = max_pattern.match(max_line)
        vals = m.group('vals').strip()
        parts = [p.strip() for p in vals.split(',') if p.strip() != '']
        if len(parts) < 3:
            continue
        try:
            z = float(parts[2])
        except ValueError:
            continue
        half = z/2
        new_vals = f"{half:g}, {half:g}, {parts[2]}"
        lines[max_idx] = f"{m.group('indent')}{new_vals}{m.group('comment') or ''}"
        rear_line = lines[rear_idx]
        m2 = rear_pattern.match(rear_line)
        lines[rear_idx] = f"{m2.group('indent')}{half:g}{m2.group('comment') or ''}"
        changes.append((max_idx+1, rear_idx+1, z, half))
if not changes:
    print('No player_ship entries updated.')
else:
    print(f'Updated {len(changes)} player_ship entries:')
    for max_line, rear_line, z, half in changes:
        print(f'  Max @ line {max_line}, Rear @ line {rear_line}: z={z} -> half={half}')
path.write_text('\n'.join(lines) + ('\n' if text.endswith('\n') else ''), encoding='utf8')
