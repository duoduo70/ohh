import ohh.modules.json as json
import ohh.modules.jvm_bytecode as jvm_bytecode
import ohh.modules.stardand_string as stardand_string

auto_extract_source = {
    ".json" : json.auto_extract_source,
    ".java": stardand_string.auto_extract_source,
    ".class": jvm_bytecode.auto_extract_source
}

replace = {
    ".json": stardand_string.replace,
    ".class": jvm_bytecode.replace
}

search = {
    ".json": stardand_string.search,
    ".class": jvm_bytecode.search
}