cython_add_module_pyx(cmesh)
add_python_library(cmesh cmesh.cpp fmesh.f90)

set(PYTHON_INSTALL_PATH lib/python/site-packages)
set(PY_PATH ${PYTHON_INSTALL_PATH}/libqsnake)
install(TARGETS cmesh
            RUNTIME DESTINATION ${PY_PATH}
            ARCHIVE DESTINATION ${PY_PATH}
            LIBRARY DESTINATION ${PY_PATH}
        )
install(FILES __init__.py atom.py runtests.py
    DESTINATION ${PY_PATH}
    )
