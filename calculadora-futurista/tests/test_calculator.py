"""Testes da lógica da calculadora (não dependem da interface)."""

from decimal import Decimal

import pytest

from calculator import Calculator, CalculatorError


def press(calc: Calculator, keys: str) -> Calculator:
    """Atalho para simular teclas: dígitos, . + - * / = % n(±) c(limpar) <(apagar)."""
    for key in keys:
        if key.isdigit():
            calc.input_digit(key)
        elif key == ".":
            calc.input_decimal()
        elif key in "+-*/":
            calc.set_operator(key)
        elif key == "=":
            calc.calculate()
        elif key == "%":
            calc.percent()
        elif key == "n":
            calc.toggle_sign()
        elif key == "c":
            calc.clear()
        elif key == "<":
            calc.backspace()
    return calc


@pytest.fixture
def calc() -> Calculator:
    return Calculator()


# ---- operações básicas -------------------------------------------------------
@pytest.mark.parametrize("keys, expected", [
    ("2+3=", "5"), ("9-4=", "5"), ("5-9=", "-4"),
    ("6*7=", "42"), ("8/2=", "4"), ("1/4=", "0.25"),
])
def test_basic_operations(calc, keys, expected):
    assert press(calc, keys).display == expected


def test_static_operations():
    assert Calculator.add(Decimal(1), Decimal(2)) == 3
    assert Calculator.subtract(Decimal(1), Decimal(2)) == -1
    assert Calculator.multiply(Decimal(3), Decimal(4)) == 12
    assert Calculator.divide(Decimal(9), Decimal(3)) == 3


# ---- divisão por zero e erros -------------------------------------------------
def test_division_by_zero_shows_error(calc):
    press(calc, "5/0=")
    assert calc.has_error
    assert calc.display == "Divisão por zero"


def test_divide_function_raises_on_zero():
    with pytest.raises(CalculatorError):
        Calculator.divide(Decimal(1), Decimal(0))


def test_chained_division_by_zero(calc):
    press(calc, "5/0+")
    assert calc.has_error


def test_recovers_from_error_when_typing(calc):
    press(calc, "5/0=7")
    assert not calc.has_error
    assert calc.display == "7"


def test_operator_ignored_during_error(calc):
    press(calc, "5/0=+")
    assert calc.has_error


def test_result_too_large(calc):
    press(calc, "999999999999999*999999999999999=")
    assert calc.display == "Resultado muito grande"


def test_invalid_digit_and_operator(calc):
    with pytest.raises(ValueError):
        calc.input_digit("a")
    with pytest.raises(ValueError):
        calc.set_operator("^")


def test_equals_without_operation(calc):
    assert press(calc, "=").display == "0"
    assert press(Calculator(), "5=").display == "5"


# ---- porcentagem ---------------------------------------------------------------
def test_percent_alone(calc):
    assert press(calc, "50%").display == "0.5"


def test_percent_with_addition(calc):
    assert press(calc, "200+10%=").display == "220"


def test_percent_with_multiplication(calc):
    assert press(calc, "50*10%=").display == "5"


# ---- negativos e decimais -------------------------------------------------------
def test_toggle_sign(calc):
    assert press(calc, "5n").display == "-5"
    assert press(calc, "n").display == "5"


def test_sign_on_zero_does_nothing(calc):
    assert press(calc, "n").display == "0"


def test_negative_operations(calc):
    assert press(calc, "5n+3=").display == "-2"
    assert press(Calculator(), "5n*2=").display == "-10"


def test_decimal_precision(calc):
    assert press(calc, "0.1+0.2=").display == "0.3"
    assert press(Calculator(), "1.5+2.25=").display == "3.75"


def test_only_one_decimal_point(calc):
    assert press(calc, "1..5").display == "1.5"


def test_decimal_first(calc):
    assert press(calc, ".").display == "0."
    assert press(calc, "5").display == "0.5"


def test_repeating_decimal_is_rounded(calc):
    assert press(calc, "1/3=").display.startswith("0.333333")


# ---- limpeza e apagar ----------------------------------------------------------
def test_clear(calc):
    press(calc, "123+4c")
    assert calc.display == "0"
    assert calc.expression == ""


def test_backspace(calc):
    assert press(calc, "123<").display == "12"
    assert press(Calculator(), "1<").display == "0"
    assert press(Calculator(), "5n<").display == "0"


def test_backspace_does_not_edit_result(calc):
    assert press(calc, "2+3=<").display == "5"


# ---- operações consecutivas e entrada -----------------------------------------
def test_chained_operations_left_to_right(calc):
    assert press(calc, "2+3+4=").display == "9"
    assert press(Calculator(), "2+3*4=").display == "20"


def test_continue_after_result(calc):
    assert press(calc, "2+3=*4=").display == "20"


def test_new_number_after_result(calc):
    press(calc, "2+3=7")
    assert calc.display == "7"
    assert calc.expression == ""


def test_replace_operator(calc):
    assert press(calc, "5+*3=").display == "15"


def test_leading_zeros_and_limit(calc):
    assert press(calc, "007").display == "7"
    assert len(press(Calculator(), "1" * 20).display) == 15


def test_expression_text(calc):
    assert press(calc, "2+").expression == "2 +"
    assert press(Calculator(), "6*7=").expression == "6 × 7 ="
