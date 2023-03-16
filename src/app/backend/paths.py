from pathlib import Path

class MyPaths():

    mod_path = Path(__file__).parent
    rel_path1 = '../../../url_lists'
    rel_path2 = '../../../csv_exports'
    urls_path = (mod_path / rel_path1).resolve()
    csv_path = (mod_path / rel_path2).resolve()

    rel_path3 = '../gui/resources/sc_icon2.png'
    rel_path4 = '../gui/resources/tab1b.png'
    rel_path5 = '../gui/resources/tab2b.png'
    rel_path6 = '../gui/resources/tab1s.png'
    rel_path7 = '../gui/resources/tab2s.png'

    icon_path = (mod_path / rel_path3).resolve()
    tab1b_path = (mod_path / rel_path4).resolve()
    tab2b_path = (mod_path / rel_path5).resolve()
    tab1s_path = (mod_path / rel_path6).resolve()
    tab2s_path = (mod_path / rel_path7).resolve()