from project.domain.entities.file_name_keeper import FileNameKeeper
from project.domain.value_objects.file_name_keeper import FileName


def test_keeper():
    keeper = FileNameKeeper()

    keeper.add(FileName(name="index.html"))
    keeper.add(FileName(name="index.html"))

    assert keeper.exists(FileName(name="index.html"))
    assert not keeper.exists(FileName(name="other.html"))

    assert len(keeper.filenames) == 1
