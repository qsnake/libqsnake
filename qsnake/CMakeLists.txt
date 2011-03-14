cython_add_module_pyx(cmesh)
add_python_library(cmesh cmesh.cpp fmesh_wrapper.f90 fmesh.f90)

set(PY_PATH ${PYTHON_INSTALL_PATH}/qsnake)
install(TARGETS cmesh
            RUNTIME DESTINATION ${PY_PATH}
            ARCHIVE DESTINATION ${PY_PATH}
            LIBRARY DESTINATION ${PY_PATH}
        )
install(FILES __init__.py atom.py runtests.py mesh.py atoms.py
    DESTINATION ${PY_PATH}
    )

add_subdirectory(data)
add_subdirectory(mesh2d)
add_subdirectory(tests)
