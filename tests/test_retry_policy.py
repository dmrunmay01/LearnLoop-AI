def route(report, attempt, max_retries):
    if report["overall_pass"]:
        return "publish"
    if attempt >= max_retries:
        return "reject"
    return "improve"

def test_pass_publishes_immediately():
    assert route({"overall_pass": True}, 0, 2) == "publish"

def test_failure_retries_until_limit():
    assert route({"overall_pass": False}, 0, 2) == "improve"
    assert route({"overall_pass": False}, 1, 2) == "improve"
    assert route({"overall_pass": False}, 2, 2) == "reject"

def test_zero_retry_rejects_first_failure():
    assert route({"overall_pass": False}, 0, 0) == "reject"
