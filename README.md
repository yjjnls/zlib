| Version | Channel | Windows | Linux |
|:-------:|:-------:|:------:|:------:|
|  * | master | [![Windows Build Status](https://ci.appveyor.com/api/projects/status/github/conanos/zlib?svg=true&branch=master)](https://ci.appveyor.com/project/Mingyiz/zlib?branch=master) |[![Linux Build Status](https://api.travis-ci.org/conanos/zlib.svg?branch=master)](https://travis-ci.org/conanos/zlib?branch=master)|
|  1.2.11 | testing | [![Windows Build Status](https://ci.appveyor.com/api/projects/status/github/conanos/zlib?svg=true&branch=testing/1.2.11)](https://ci.appveyor.com/project/Mingyiz/zlib?branch=testing/1.2.11) |[![Linux Build Status](https://api.travis-ci.org/conanos/zlib.svg?branch=testing/1.2.11)](https://travis-ci.org/conanos/zlib?branch=testing/1.2.11)|
|  1.2.11 | stable | [![Windows Build Status](https://ci.appveyor.com/api/projects/status/github/conanos/zlib?svg=true&branch=stable/1.2.11)](https://ci.appveyor.com/project/Mingyiz/zlib?branch=stable/1.2.11) |[![Linux Build Status](https://api.travis-ci.org/conanos/zlib.svg?branch=stable/1.2.11)](https://travis-ci.org/conanos/zlib?branch=stable/1.2.11)|

# zlib


[Conan](https://bintray.com/conanos/stable/zlib%3Aconanos/1.2.11%3Astable) package for ZLIB library. 

This repo ported from https://github.com/conan-community/conan-zlib,
Thanks to Tim Lebedkov for the MinGW integration help! :)


## Basic setup

    $ conan install zlib/1.2.11@conan/stable
    
## Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    zlib/1.2.11@conan/stable

    [options]
    zlib:shared=True # False
    
    [generators]
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.cmake* with all the 
paths and variables that you need to link with your dependencies.
