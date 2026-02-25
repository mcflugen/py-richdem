#!/usr/bin/env python3

dtypes = [
    "float",
    "double",
    "int8_t",
    "int16_t",
    "int32_t",
    "int64_t",
    "uint8_t",
    "uint16_t",
    "uint32_t",
    "uint64_t",
]

with open("Array2D_wrapper.hpp.template") as f:
    template = f.read()

with open("Array2D_wrapper.hpp", "w") as f:
    for T in dtypes:
        rendered_T = template.replace("@T@", T)

        if "@U@" in rendered_T:
            for U in dtypes:
                f.write(rendered_T.replace("@U@", U))
        else:
            f.write(rendered_T)
