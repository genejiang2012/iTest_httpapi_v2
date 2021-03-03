
from httpapi import HttpAPI, Config, Step, RunRequest


class TestCaseBasic(HttpAPI):

    config = Config("login in web dev").base_url("https://httpbin.org/")

    teststeps = [
        Step(
            RunRequest("headers")
            .get("/headers")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.headers.Host", "httpbin.org")
        ),
        Step(
            RunRequest("user-agent")
            .get("/user-agent")
            .validate()
            .assert_equal("status_code", 200)
            .assert_startswith('body."user-agent"', "python-requests")
        )
    ]


if __name__ == "__main__":
    # print(TestCaseBasic().__dir__())
    TestCaseBasic().test_start()