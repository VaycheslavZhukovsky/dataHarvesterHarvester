import pytest

from project.application.retry_policy import RetryPolicy


def test_initial_state_allows_retry():
    policy = RetryPolicy()
    assert policy.should_retry() is True
    assert policy.current == 0


def test_register_failure_increments_counter():
    policy = RetryPolicy()
    policy.register_failure()
    assert policy.current == 1
    assert policy.should_retry() is True


def test_reaching_max_failures_disables_retry():
    policy = RetryPolicy(max_consecutive_failures=3)

    policy.register_failure()
    policy.register_failure()
    policy.register_failure()

    assert policy.current == 3
    assert policy.should_retry() is False


def test_more_than_max_failures_still_disables_retry():
    policy = RetryPolicy(max_consecutive_failures=2)

    policy.register_failure()
    policy.register_failure()
    policy.register_failure()

    assert policy.current == 3
    assert policy.should_retry() is False


def test_register_success_resets_counter():
    policy = RetryPolicy(max_consecutive_failures=2)

    policy.register_failure()
    policy.register_failure()
    assert policy.should_retry() is False

    policy.register_success()
    assert policy.current == 0
    assert policy.should_retry() is True


@pytest.mark.parametrize(
    "failures, max_failures, expected",
    [
        (0, 3, True),
        (1, 3, True),
        (2, 3, True),
        (3, 3, False),
        (4, 3, False),
    ],
)
def test_should_retry_parametrized(failures, max_failures, expected):
    policy = RetryPolicy(max_consecutive_failures=max_failures)

    for _ in range(failures):
        policy.register_failure()

    assert policy.should_retry() is expected
