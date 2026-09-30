import pytest
from app.core.graph import TaskGraph
from app.core.models import Task


def test_topological_order():
    graph = TaskGraph()
    graph.add_task(Task("a", "A", "x"))
    graph.add_task(Task("b", "B", "x", depends_on=["a"]))
    graph.add_task(Task("c", "C", "x", depends_on=["b"]))
    assert graph.topological_order() == ["a", "b", "c"]


def test_cycle_is_rejected():
    graph = TaskGraph()
    graph.add_task(Task("a", "A", "x"))
    graph.add_task(Task("b", "B", "x", depends_on=["a"]))
    # Directly corrupting the graph here lets us test the detector itself.
    graph.edges["b"].append("a")
    assert graph.has_cycle()
    with pytest.raises(ValueError):
        graph.topological_order()
