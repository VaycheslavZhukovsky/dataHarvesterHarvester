from unittest.mock import MagicMock

from project.application.use_cases.restore_paginator import RecoveryProcessedDataCategoryUseCase


def test_restore_paginator_success():
    paginator = MagicMock()
    paginator.mark_processed.side_effect = lambda i: paginator

    paginator_factory = MagicMock()
    paginator_factory.create.return_value = paginator

    uc = RecoveryProcessedDataCategoryUseCase(paginator_factory)

    result = uc.execute("http://example.com", 10, [1, 2, 3])

    paginator_factory.create.assert_called_once_with("http://example.com", 10)
    assert result is paginator
    assert paginator.mark_processed.call_count == 3
