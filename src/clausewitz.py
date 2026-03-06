import re


def fmt(v):
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, str) and (" " in v or not v):
        return f'"{v}"'
    return str(v)


def to_clausewitz(data, indent=0):
    pad = "\t" * indent
    out = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(key, str) and key.startswith("_"):
                continue
            key = str(key)
            if isinstance(value, list) and value and isinstance(value[0], dict):
                for item in value:
                    out.append(f"{pad}{key} = {{")
                    out.append(to_clausewitz(item, indent + 1))
                    out.append(f"{pad}}}")
            elif isinstance(value, list):
                out.append(f"{pad}{key} = {{ {' '.join(fmt(v) for v in value)} }}")
            elif isinstance(value, dict):
                out.append(f"{pad}{key} = {{")
                out.append(to_clausewitz(value, indent + 1))
                out.append(f"{pad}}}")
            else:
                out.append(f"{pad}{key} = {fmt(value)}")
    return "\n".join(filter(None, out))


def parse_clausewitz(text):
    text = re.sub(r'#[^\n]*', '', text)
    tokens = re.findall(r'"[^"]*"|\{|\}|[^\s{}]+', text)
    pos = [0]

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def consume():
        t = peek(); pos[0] += 1; return t

    def parse_block():
        result = {}
        while peek() and peek() != "}":
            key = consume()
            if peek() == "=":
                consume()
                if peek() == "{":
                    consume(); val = parse_block(); consume()
                else:
                    raw = consume(); val = raw.strip('"')
                    if val == "yes": val = True
                    elif val == "no": val = False
                    else:
                        try: val = int(val)
                        except ValueError:
                            try: val = float(val)
                            except ValueError: pass
            else:
                val = True
            if key in result:
                if not isinstance(result[key], list):
                    result[key] = [result[key]]
                result[key].append(val)
            else:
                result[key] = val
        return result

    return parse_block()
