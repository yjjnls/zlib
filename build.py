#from conan.packager import ConanMultiPackager
from bincrafters import build_template_default
import platform
import os

os.environ['CONAN_USERNAME'] = os.environ.get('CONAN_USERNAME','conanos')

if __name__ == "__main__":
    #builder = ConanMultiPackager()
    #builder.add_common_builds(shared_option_name="zlib:shared", pure_c=True)
    builder = build_template_default.get_builder()
    if os.environ.get('EMSCRIPTEN_VERSIONS'):
        for version in os.environ['EMSCRIPTEN_VERSIONS'].split(','):
            for build_type in os.environ.get('CONAN_BUILD_TYPES','Debug').split(','):
                builder.add(settings={
                    "arch": "any", 
                    "compiler": "emcc",
                    "compiler.libcxx":'libcxxabi',
                    "build_type": build_type, 
                    "compiler.version": version
                    },
                    options={'zlib:shared':True}, env_vars={}, build_requires={})

        items = []
        for item in builder.items:
            if not os.environ.get('CONAN_GCC_VERSIONS') and item.settings['compiler'] == 'gcc':
                continue  
            if not os.environ.get('CONAN_CLANG_VERSIONS') and item.settings['compiler'] == 'clang':
                continue 
            items.append(item)

        builder.items = items


    builder.run()
