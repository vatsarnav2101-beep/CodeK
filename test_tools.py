from app.tools.workspace import Workspace, WorkspaceError


def test_workspace_lists_and_reads(tmp_path):
    (tmp_path / "hello.py").write_text("print('hello')", encoding="utf-8")
    workspace = Workspace(tmp_path)
    assert "hello.py" in workspace.list_files()
    assert "hello" in workspace.read_file("hello.py")


def test_workspace_blocks_escape(tmp_path):
    workspace = Workspace(tmp_path)
    try:
        workspace.read_file("../outside.txt")
    except WorkspaceError:
        pass
    else:
        raise AssertionError("Expected path traversal to be blocked")
