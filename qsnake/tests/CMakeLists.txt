set(PY_PATH ${PYTHON_INSTALL_PATH}/qsnake/tests)
install(FILES test_atom.py test_elk.py test_atoms.py test_phaml.py
    DESTINATION ${PY_PATH}
    )
install(FILES
    phaml_data/domain.edge
    phaml_data/domain.ele
    phaml_data/domain.neigh
    phaml_data/domain.node
    DESTINATION ${PY_PATH}/phaml_data
    )
