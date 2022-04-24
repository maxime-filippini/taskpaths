import pytest
from hypothesis import given
from hypothesis.strategies import floats
from hypothesis.strategies import integers

from taskpaths.process import InputStep
from taskpaths.process import Step


regular_floats = floats(allow_infinity=False, allow_nan=False)
regular_numbers = integers() | regular_floats


@pytest.fixture(scope="session")
def sum_step():
    class SimpleSumStep(Step):
        def instruction(self, x, y):
            return x + y

    return SimpleSumStep


@pytest.fixture(scope="session")
def product_step():
    class SimpleProductStep(Step):
        def instruction(self, x, y):
            return x * y

    return SimpleProductStep


@given(x=regular_numbers, y=regular_numbers)
def test_simple_sums(sum_step, x, y):
    s_x = InputStep(id_="x", value=x)
    s_y = InputStep(id_="y", value=y)

    step = sum_step(id_="sum", precedents=[s_x, s_y])
    step.run()

    assert step.value == s_x.value + s_y.value


@given(x=regular_numbers, y=regular_numbers)
def test_simple_products(product_step, x, y):
    s_x = InputStep(id_="x", value=x)
    s_y = InputStep(id_="y", value=y)

    step = product_step(id_="product", precedents=[s_x, s_y])
    step.run()

    assert step.value == s_x.value * s_y.value


@given(x=regular_numbers, y=regular_numbers, z=regular_numbers, k=regular_numbers)
def test_complex_process(sum_step, product_step, x, y, z, k):

    process = product_step(
        id_="product",
        precedents=[
            sum_step(
                id_="x",
                precedents=[InputStep(id_="x", value=x), InputStep(id_="y", value=y)],
            ),
            sum_step(
                id_="y",
                precedents=[InputStep(id_="x", value=z), InputStep(id_="y", value=k)],
            ),
        ],
    )

    process.run()

    assert process.value == (x + y) * (z + k)
