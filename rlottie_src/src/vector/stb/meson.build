
source_file = ['stb_image.cpp']

if get_option('module') == true
    rlottie_image_loader_dir = get_option('moduledir') != '' ? get_option('moduledir') : get_option('libdir')
    rlottie_image_loader_lib = shared_module('rlottie-image-loader',
                                             source_file,
                                             include_directories : [include_directories('.'), config_dir],
                                             install : true,
                                             install_dir : rlottie_image_loader_dir,
                                             cpp_args : compiler_flags,
                                             gnu_symbol_visibility : 'hidden',
                                            )
    cc = meson.get_compiler('cpp')
    stb_dep = cc.find_library('dl', required : false)
else
    stb_dep = declare_dependency( include_directories : include_directories('.'),
                                  sources : source_file
                                 )
endif
