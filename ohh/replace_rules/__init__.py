import ohh.replace_rules.json as json
import ohh.replace_rules.class_ as class_

auto_extract_source = {
    ".json" : json.auto_extract_source
}

replace = {
    ".json": json.replace,
    ".class": class_.replace
}

search = {
    ".json": json.search,
    ".class": class_.search
}