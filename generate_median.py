from llvmlite import ir, binding as llvm

# Inicialização LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# Tipos
int64 = ir.IntType(64)
fn_ty = ir.FunctionType(int64, (int64, int64, int64))

# Módulo e função
module = ir.Module(name="median_module_if")
fn = ir.Function(module, fn_ty, name="medianof3")
a, b, c = fn.args
a.name, b.name, c.name = "a", "b", "c"

# Bloco inicial
entry = fn.append_basic_block("entry")
builder = ir.IRBuilder(entry)

# Alocações para variáveis mutáveis
pmaior = builder.alloca(int64, name="maior")
pmenor = builder.alloca(int64, name="menor")

# Inicializa maior e menor com a
builder.store(a, pmaior)
builder.store(a, pmenor)

# ---- Atualiza maior ----
maior = builder.load(pmaior, "maior")
cond1 = builder.icmp_signed(">", b, maior)
with builder.if_then(cond1):
    builder.store(b, pmaior)

maior = builder.load(pmaior, "maior2")
cond2 = builder.icmp_signed(">", c, maior)
with builder.if_then(cond2):
    builder.store(c, pmaior)

# ---- Atualiza menor ----
menor = builder.load(pmenor, "menor")
cond3 = builder.icmp_signed("<", b, menor)
with builder.if_then(cond3):
    builder.store(b, pmenor)

menor = builder.load(pmenor, "menor2")
cond4 = builder.icmp_signed("<", c, menor)
with builder.if_then(cond4):
    builder.store(c, pmenor)

# ---- Calcula mediana ----
maior_final = builder.load(pmaior, "maior_final")
menor_final = builder.load(pmenor, "menor_final")

soma1 = builder.add(a, b, name="soma1")
soma2 = builder.add(soma1, c, name="soma2")
tmp = builder.sub(soma2, maior_final, name="tmp")
median = builder.sub(tmp, menor_final, name="median")

builder.ret(median)

# Exporta IR
print(module)


# BASICAMENTE ISSO AQUI
# a, b, c

# maior = a

# if b > a:
#     maior = b

# if c > maior:
#     maior = c