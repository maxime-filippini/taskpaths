from taskpaths import InputStep
from taskpaths import LambdaStep


def test_simple_process():
    s = (
        InputStep(id_="x", value=5)
        >> LambdaStep(id_="y", lambda_=lambda x: x + 1)
        >> LambdaStep(id_="z", lambda_=lambda y: y ** 2)
    )

    s.run()

    assert s.value == 36
