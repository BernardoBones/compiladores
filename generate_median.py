# generate_median.py
from llvmlite import ir, binding as llvm

# Inicializa binding (recomenda-se para operações com binding)
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# === 1) IR layer: construir o módulo e a função ===
int64 = ir.IntType(64)
fn_ty = ir.FunctionType(int64, (int64, int64, int64))

module = ir.Module(name="median_module")
module.triple = llvm.get_default_triple()  # opcional mas útil
fn = ir.Function(module, fn_ty, name="medianof3")
a, b, c = fn.args
a.name, b.name, c.name = "a", "b", "c"

entry = fn.append_basic_block("entry")
builder = ir.IRBuilder(entry)

# Método: encontrar max e min com selects, depois median = a+b+c - max - min
# (AVISO: soma a+b+c pode overflow int64; ver seção alternativa abaixo)
max_ab = builder.select(builder.icmp_signed('>', a, b), a, b, name="max_ab")
max_abc = builder.select(builder.icmp_signed('>', max_ab, c), max_ab, c, name="max_abc")

min_ab = builder.select(builder.icmp_signed('<', a, b), a, b, name="min_ab")
min_abc = builder.select(builder.icmp_signed('<', min_ab, c), min_ab, c, name="min_abc")

sum_ab = builder.add(a, b, name="sum_ab")
sum_abc = builder.add(sum_ab, c, name="sum_abc")
tmp = builder.sub(sum_abc, max_abc, name="tmp1")
median = builder.sub(tmp, min_abc, name="median")
builder.ret(median)

# === 2) Exportar textual (.ll) e bitcode (.bc) ===
llvm_ir = str(module)
with open("median.ll", "w") as f:
    f.write(llvm_ir)

# Para gerar bitcode: parse_assembly -> ModuleRef -> as_bitcode()
mod_ref = llvm.parse_assembly(llvm_ir)
mod_ref.verify()
bc = mod_ref.as_bitcode()
with open("median.bc", "wb") as f:
    f.write(bc)

print("Gerados: median.ll, median.bc")
print("Preview IR (primeiras linhas):")
print("\n".join(llvm_ir.splitlines()[:20]))
