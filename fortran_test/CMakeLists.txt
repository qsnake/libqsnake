project(fortran_test)

cmake_minimum_required(VERSION 2.6)
enable_language(Fortran)
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

set(CMAKE_Fortran_FLAGS "-W -Wall ${CMAKE_Fortran_FLAGS}")
set(CMAKE_C_FLAGS "-W -Wall ${CMAKE_C_FLAGS}")

include(UseCython)
find_package(PythonLibs REQUIRED)
find_package(NumPy REQUIRED)

include_directories(${PYTHON_INCLUDE_PATH} ${NUMPY_INCLUDE_PATH})


add_subdirectory(lib)

message("\nConfiguration results (these options can be set on the commandline)")
message("---------------------")
message("Fortran compiler: ${CMAKE_Fortran_COMPILER}")
message("Fortran compiler flags: ${CMAKE_Fortran_FLAGS}")
message("C compiler: ${CMAKE_C_COMPILER}")
message("C compiler flags: ${CMAKE_C_FLAGS}")
message("Installation prefix: ${CMAKE_INSTALL_PREFIX}")
message("\n")
