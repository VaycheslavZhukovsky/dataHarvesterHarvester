import pytest

from project.domain.value_objects.page_state import PageProcessingState


def test_initial_state():
    state = PageProcessingState(total_pages=5)
    assert state.total_pages == 5
    assert state.processed_pages == []
    assert state.current_page() == 1
    assert state.is_finished() is False


def test_add_processed_updates_state():
    state = PageProcessingState(total_pages=5)
    state = state.add_processed(1)
    state = state.add_processed(3)

    assert state.processed_pages == [1, 3]
    assert state.current_page() == 2
    assert state.is_finished() is False


def test_completed_state():
    state = PageProcessingState(total_pages=3)
    state = state.add_processed(1).add_processed(2).add_processed(3)

    assert state.is_finished() is True
    assert state.current_page() is None


def test_immutable_behavior():
    state1 = PageProcessingState(total_pages=3)
    state2 = state1.add_processed(1)

    assert state1.processed_pages == []
    assert state2.processed_pages == [1]


def test_unique_pages_stored():
    state = PageProcessingState(total_pages=3)
    state = state.add_processed(1).add_processed(1)

    assert state.processed_pages == [1]


def test_out_of_range_page_raises_error():
    state = PageProcessingState(total_pages=3)
    with pytest.raises(ValueError):
        state.add_processed(0)

    with pytest.raises(ValueError):
        state.add_processed(4)
