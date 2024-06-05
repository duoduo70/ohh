import ohh.modules.json as json
import ohh.modules.jvm_bytecode as jvm_bytecode
import ohh.modules.stardand_string as standard_string

AUTO_EXTRACT_SOURCE = {
    ".json" : json.auto_extract_source,
    ".class": jvm_bytecode.auto_extract_source
}

REPLACE = {
    ".json": standard_string.replace,
    ".class": jvm_bytecode.replace
}

SEARCH = {
    ".json": standard_string.search,
    ".class": jvm_bytecode.search
}