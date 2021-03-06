from conans.model.conan_file import ConanFile, tools
from conans import CMake
import os
import platform


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def is_emscripten(self):
        try:
            return self.settings.compiler == 'emcc'
        except:
            return False

    def configure(self):
        del self.settings.compiler.libcxx
        if self.is_emscripten():
            del self.settings.os
            del self.settings.arch

    def build(self):

        # Compatibility with Conan < 1.0 (#2234)
        generator = "Unix Makefiles" if platform.system() != "Windows" else None
        cmake = CMake(self, generator=generator)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        if self.is_emscripten():
            self.run('node bin/test.js')
            return

        if not tools.cross_building(self.settings):
            self.run("cd bin && .%stest" % os.sep)
        assert os.path.exists(os.path.join(
            self.deps_cpp_info["zlib"].rootpath, "LICENSE"))
