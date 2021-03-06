cmake_minimum_required(VERSION 2.6)

project(libqsnake)
enable_language(Fortran)

set(CMAKE_MODULE_PATH $ENV{SPKG_LOCAL}/share/qsnake/cmake)

if (CMAKE_Fortran_COMPILER_ID STREQUAL "GNU")
    # for gfortran, we need to use -fPIC
    set(CMAKE_Fortran_FLAGS "-fPIC")
endif ()

find_package(Python REQUIRED)
find_package(NumPy REQUIRED)
find_package(Cython REQUIRED)
include_directories(${PYTHON_INCLUDE_PATH} ${NUMPY_INCLUDE_PATH})

add_subdirectory(qsnake)

message("\n")
message("Configuration results")
message("---------------------")
message("Fortran compiler: ${CMAKE_Fortran_COMPILER}")
message("Fortran compiler flags: ${CMAKE_Fortran_FLAGS}")
message("Installation prefix: ${CMAKE_INSTALL_PREFIX}")
