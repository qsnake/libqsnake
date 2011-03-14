set(PY_PATH ${PYTHON_INSTALL_PATH}/qsnake/mesh2d)
install(FILES __init__.py domain.py mesh.py plot.py solution.py
    triangulation.py
    DESTINATION ${PY_PATH}
    )
