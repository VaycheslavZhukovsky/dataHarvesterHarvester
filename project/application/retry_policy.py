class RetryPolicy:
    def __init__(self, max_consecutive_failures: int = 3):
        self.max = max_consecutive_failures
        self.current = 0

    def register_failure(self):
        self.current += 1

    def register_success(self):
        self.current = 0

    def should_retry(self) -> bool:
        return self.current < self.max
