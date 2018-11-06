| Windows | Linux |
|:------:|:------:|
| [![Windows Build Status](https://ci.appveyor.com/api/projects/status/github/conanos/zlib?svg=true)](https://ci.appveyor.com/project/Mingyiz/zlib) |[![Linux Build Status](https://api.travis-ci.org/conanos/zlib.svg)](https://travis-ci.org/conanos/zlib)|

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
