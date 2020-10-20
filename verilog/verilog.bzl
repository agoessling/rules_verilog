VerilogModuleInfo = provider(
    doc = "Info pertaining to Verilog module.",
    fields = {
        "top": "Top module name.",
        "files": "A depset of all necessary Verilog files.",
    },
)

def _verilog_module_impl(ctx):
    return [
        VerilogModuleInfo(
            top = ctx.attr.top,
            files = depset(
                direct = ctx.files.srcs,
                transitive = [dep[VerilogModuleInfo].files for dep in ctx.attr.deps],
            ),
        )
    ]

verilog_module = rule(
    implementation = _verilog_module_impl,
    doc = "Verilog module.",
    attrs = {
        "srcs": attr.label_list(
            doc = "(System) verilog source files.",
            allow_files = [".v", ".sv"],
        ),
        "top": attr.string(
            doc = "Top module name.",
            mandatory = True,
        ),
        "deps": attr.label_list(
            doc = "Verilog module dependencies.",
            providers = [VerilogModuleInfo],
        ),
    },
)
