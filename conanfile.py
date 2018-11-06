from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
from conans.util import files
import os

try:
    import conanos.conan.hacks.cmake
except:
    if os.environ.get('EMSCRIPTEN_VERSIONS'):
        raise Exception(
            'Please use pip install conanos to patch conan for emscripten binding !')


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    ZIP_FOLDER_NAME = "zlib-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]    }
    default_options = "shared=True"
    exports_sources = ["CMakeLists.txt"]
    url = "http://github.com/conanos/zlib"
    license = "Zlib"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"

    def is_emscripten(self):
        try:
            return self.settings.compiler == 'emcc'
        except:
            return False

    def config_options(self):
        if self.is_emscripten():
            self.options.remove("fPIC")
            self.options.remove("shared")

    def configure(self):
        
        del self.settings.compiler.libcxx
        if self.is_emscripten():
            del self.settings.os
            del self.settings.arch

    def source(self):
        z_name = "zlib-%s.tar.gz" % self.version
        tools.download("https://zlib.net/zlib-%s.tar.gz" %
                       self.version, z_name)
        tools.unzip(z_name)
        os.unlink(z_name)
        files.rmdir("%s/contrib" % self.ZIP_FOLDER_NAME)
        if not tools.os_info.is_windows:
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):
        with tools.chdir(os.path.join(self.source_folder, self.ZIP_FOLDER_NAME)):
            for filename in ['zconf.h', 'zconf.h.cmakein', 'zconf.h.in']:
                tools.replace_in_file(filename,
                                      '#ifdef HAVE_UNISTD_H    /* may be set to #if 1 by ./configure */',
                                      '#if defined(HAVE_UNISTD_H) && (1-HAVE_UNISTD_H-1 != 0)')
                tools.replace_in_file(filename,
                                      '#ifdef HAVE_STDARG_H    /* may be set to #if 1 by ./configure */',
                                      '#if defined(HAVE_STDARG_H) && (1-HAVE_STDARG_H-1 != 0)')
            if self.is_emscripten():
                tools.replace_in_file('CMakeLists.txt',
                                      'add_library(zlibstatic STATIC ${ZLIB_SRCS} ${ZLIB_ASMS} ${ZLIB_PUBLIC_HDRS} ${ZLIB_PRIVATE_HDRS})',
                                      '#iadd_library(zlibstatic STATIC ${ZLIB_SRCS} ${ZLIB_ASMS} ${ZLIB_PUBLIC_HDRS} ${ZLIB_PRIVATE_HDRS})')
                tools.replace_in_file('CMakeLists.txt',
                                      'set_target_properties(zlib zlibstatic PROPERTIES OUTPUT_NAME z)',
                                      'set_target_properties(zlib PROPERTIES OUTPUT_NAME z)')
                tools.replace_in_file('CMakeLists.txt',
                                      'install(TARGETS zlib zlibstatic',
                                      'install(TARGETS zlib ')

            files.mkdir("_build")
            with tools.chdir("_build"):
                if not tools.os_info.is_windows and not self.is_emscripten():
                    env_build = AutoToolsBuildEnvironment(self)
                    if self.settings.arch in ["x86", "x86_64"] and self.settings.compiler in ["apple-clang", "clang", "gcc"]:
                        env_build.flags.append('-mstackrealign')

                    env_build.fpic = True

                    if self.settings.os == "Macos":
                        old_str = '-install_name $libdir/$SHAREDLIBM'
                        new_str = '-install_name $SHAREDLIBM'
                        tools.replace_in_file("../configure", old_str, new_str)

                    if self.settings.os == "Windows":  # Cross building to Linux
                        tools.replace_in_file(
                            "../configure", 'LDSHAREDLIBC="${LDSHAREDLIBC--lc}"', 'LDSHAREDLIBC=""')
                    # Zlib configure doesnt allow this parameters

                    if self.settings.os == "iOS":
                        tools.replace_in_file(
                            "../gzguts.h", '#ifdef _LARGEFILE64_SOURCE', '#include <unistd.h>\n\n#ifdef _LARGEFILE64_SOURCE')

                    if self.settings.os == "Windows" and tools.os_info.is_linux:
                        # Let our profile to declare what is needed.
                        tools.replace_in_file(
                            "../win32/Makefile.gcc", 'LDFLAGS = $(LOC)', '')
                        tools.replace_in_file(
                            "../win32/Makefile.gcc", 'AS = $(CC)', '')
                        tools.replace_in_file(
                            "../win32/Makefile.gcc", 'AR = $(PREFIX)ar', '')
                        tools.replace_in_file(
                            "../win32/Makefile.gcc", 'CC = $(PREFIX)gcc', '')
                        tools.replace_in_file(
                            "../win32/Makefile.gcc", 'RC = $(PREFIX)windres', '')
                        self.run("cd .. && make -f win32/Makefile.gcc")
                    else:
                        _args = ["--prefix=%s/build"%(os.getcwd())]
                        if not self.options.shared:
                            _args.extend(['--static'])
                        env_build.configure(
                            "../", build=False, host=False, target=False, args=_args)
                        env_build.make()
                        env_build.install()

                else:
                    cmake = CMake(self)
                    cmake.configure(build_dir=".")
                    cmake.build(build_dir=".")

    def package(self):
        self.output.warn("local cache: %s" % self.in_local_cache)
        self.output.warn("develop: %s" % self.develop)
        # Extract the License/s from the header to a file
        with tools.chdir(os.path.join(self.source_folder, self.ZIP_FOLDER_NAME)):
            tmp = tools.load("zlib.h")
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        # Copy the license files
        self.copy("LICENSE", src=self.ZIP_FOLDER_NAME, dst=".")

        if not tools.os_info.is_linux:
            # Copy pc file
            self.copy("*.pc", dst="", keep_path=False)
            # Copying zlib.h, zutil.h, zconf.h
            self.copy("*.h", "include", "%s" %
                      self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy("*.h", "include", "%s" % "_build", keep_path=False)

        # Copying static and dynamic libs
        build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build")
        lib_path = os.path.join(self.package_folder, "lib")
        suffix = "d" if self.settings.build_type == "Debug" else ""
        if self.is_emscripten():
            self.copy(pattern="*.so*", dst="lib",
                      src=build_dir, keep_path=False)
            return

        if self.settings.os == "Windows":
            if self.options.shared:
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build")
                self.copy(pattern="*.dll", dst="bin",
                          src=build_dir, keep_path=False)
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build/lib")
                self.copy(pattern="*zlibd.lib", dst="lib",
                          src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib",
                          src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib",
                          src=build_dir, keep_path=False)
                if tools.os_info.is_linux:
                    self.copy(pattern="*libz.dll.a", dst="lib",
                              src=self.ZIP_FOLDER_NAME)
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(lib_path, "zlib%s.lib" % suffix)
                    os.rename(current_lib, os.path.join(lib_path, "zlib.lib"))
            else:
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build/lib")
                if self.settings.os == "Windows":
                    if tools.os_info.is_windows:
                        # MinGW
                        self.copy(pattern="libzlibstaticd.a",
                                  dst="lib", src=build_dir, keep_path=False)
                        self.copy(pattern="libzlibstatic.a", dst="lib",
                                  src=build_dir, keep_path=False)
                        # Visual Studio
                        self.copy(pattern="zlibstaticd.lib", dst="lib",
                                  src=build_dir, keep_path=False)
                        self.copy(pattern="zlibstatic.lib", dst="lib",
                                  src=build_dir, keep_path=False)
                    if tools.os_info.is_linux:
                        self.copy(pattern="libz.a", dst="lib",
                                  src=self.ZIP_FOLDER_NAME, keep_path=False)
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(
                        lib_path, "zlibstatic%s.lib" % suffix)
                    os.rename(current_lib, os.path.join(lib_path, "zlib.lib"))
                elif self.settings.compiler == "gcc":
                    if not tools.os_info.is_linux:
                        current_lib = os.path.join(lib_path, "libzlibstatic.a")
                        os.rename(current_lib, os.path.join(
                            lib_path, "libzlib.a"))
        elif tools.os_info.is_linux:
            if self.options.shared:
                os.remove('%s/_build/build/lib/libz.a'%(self.ZIP_FOLDER_NAME))
            self.copy("*", src="%s/_build/build"%(self.ZIP_FOLDER_NAME))
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib",
                              src=build_dir, keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib",
                              src=build_dir, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib",
                          src=build_dir, keep_path=False)

    def package_info(self):
        if self.is_emscripten():
            self.cpp_info.libs = ['z']
            return
        if self.settings.os == "Windows" and not tools.os_info.is_linux:
            self.cpp_info.libs = ['zlib']
        else:
            self.cpp_info.libs = ['z']
