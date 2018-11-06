#from conan.packager import ConanMultiPackager
from bincrafters import build_template_default
import platform
import os
from conanos.sdk.profile import filter
if platform.system() == 'Windows':
    os.environ['CONAN_VISUAL_VERSIONS']=os.environ.get('CONAN_VISUAL_VERSIONS','15')

if __name__ == "__main__":
    builder = build_template_default.get_builder()
    filter('zlib',builder)

    builder.run()
