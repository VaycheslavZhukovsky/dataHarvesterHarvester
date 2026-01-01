from project.infrastructure.adapters.file_html_reader import FileHtmlReader


def test_file_html_reader_reads_file(tmp_path):
    file = tmp_path / "page.html"
    file.write_text("<html>test</html>", encoding="utf-8")

    content = FileHtmlReader.read(file)
    assert content == "<html>test</html>"
