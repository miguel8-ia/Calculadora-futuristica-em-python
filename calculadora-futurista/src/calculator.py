"""Lógica matemática da calculadora (sem nenhuma dependência de interface)."""

from __future__ import annotations

from decimal import Context, Decimal, InvalidOperation, Overflow, ROUND_HALF_UP

MAX_DIGITS = 15
MAX_VALUE = Decimal(10) ** MAX_DIGITS
_ROUNDING = Context(prec=MAX_DIGITS, rounding=ROUND_HALF_UP)

# Símbolo interno -> símbolo exibido na tela
SYMBOLS = {"+": "+", "-": "−", "*": "×", "/": "÷"}


class CalculatorError(Exception):
    """Erro de cálculo com mensagem pronta para ser exibida ao usuário."""


class Calculator:
    """Calculadora de operações básicas, avaliada da esquerda para a direita.

    Usa ``Decimal`` para evitar erros como 0.1 + 0.2 = 0.30000000000000004
    e nunca usa ``eval()``.
    """

    def __init__(self) -> None:
        self.clear()

    # ------------------------------------------------------------ estado
    @property
    def display(self) -> str:
        """Texto principal da tela (número atual ou mensagem de erro)."""
        return self._error or self._current

    @property
    def expression(self) -> str:
        """Texto secundário da tela (operação em andamento)."""
        return self._expression

    @property
    def has_error(self) -> bool:
        return self._error is not None

    # ------------------------------------------------- operações básicas
    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        return a + b

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        return a - b

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        return a * b

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise CalculatorError("Divisão por zero")
        return a / b

    # ------------------------------------------------------------ entrada
    def input_digit(self, digit: str) -> None:
        """Acrescenta um dígito (0-9) ao número atual."""
        if len(digit) != 1 or digit not in "0123456789":
            raise ValueError(f"Dígito inválido: {digit!r}")
        self._begin_number_if_needed()
        if self._digit_count() >= MAX_DIGITS:
            return
        if self._current in ("0", "-0"):
            self._current = self._current[:-1] + digit
        else:
            self._current += digit

    def input_decimal(self) -> None:
        """Acrescenta o separador decimal, se ainda não existir."""
        self._begin_number_if_needed()
        if "." not in self._current:
            self._current += "."

    def set_operator(self, operator: str) -> None:
        """Define a operação (+, -, *, /). Encadeia cálculos pendentes."""
        if operator not in SYMBOLS:
            raise ValueError(f"Operador inválido: {operator!r}")
        if self._error:
            return
        try:
            if self._operator is not None and not self._start_new:
                result = self._apply(self._accumulator, self._operator,
                                     Decimal(self._current))
                self._current = self._format(result)
                self._accumulator = Decimal(self._current)
            elif self._operator is None:
                self._accumulator = Decimal(self._current)
        except CalculatorError as exc:
            self._fail(str(exc))
            return
        self._operator = operator
        self._expression = (f"{self._format(self._accumulator)} "
                            f"{SYMBOLS[operator]}")
        self._start_new = True

    def calculate(self) -> None:
        """Executa a operação pendente (tecla '=')."""
        if self._error or self._operator is None:
            return
        right = Decimal(self._current)
        try:
            result = self._apply(self._accumulator, self._operator, right)
            shown = self._format(result)
        except CalculatorError as exc:
            self._fail(str(exc))
            return
        self._expression = (f"{self._format(self._accumulator)} "
                            f"{SYMBOLS[self._operator]} "
                            f"{self._format(right)} =")
        self._current = shown
        self._accumulator = None
        self._operator = None
        self._start_new = True

    def percent(self) -> None:
        """Converte o número atual em porcentagem.

        Em ``200 + 10 %`` o resultado é 20 (10% de 200).
        Em ``50 × 10 %`` o resultado é 0.1 (apenas divide por 100).
        """
        if self._error:
            return
        value = Decimal(self._current)
        if self._operator in ("+", "-") and self._accumulator is not None:
            value = self._accumulator * value / 100
        else:
            value = value / 100
        try:
            self._current = self._format(value)
        except CalculatorError as exc:
            self._fail(str(exc))
            return
        self._start_new = self._operator is None

    def toggle_sign(self) -> None:
        """Alterna entre positivo e negativo."""
        if self._error or self._current == "0":
            return
        if self._current.startswith("-"):
            self._current = self._current[1:]
        else:
            self._current = "-" + self._current

    def clear(self) -> None:
        """Volta ao estado inicial (tecla 'C')."""
        self._current = "0"
        self._accumulator: Decimal | None = None
        self._operator: str | None = None
        self._expression = ""
        self._error: str | None = None
        self._start_new = False

    def backspace(self) -> None:
        """Apaga o último caractere digitado."""
        if self._error:
            self.clear()
            return
        if self._start_new:
            return
        self._current = self._current[:-1]
        if self._current in ("", "-"):
            self._current = "0"

    # ------------------------------------------------------------ internos
    def _begin_number_if_needed(self) -> None:
        if self._error:
            self.clear()
        if self._start_new:
            if self._operator is None:
                self._expression = ""
            self._current = "0"
            self._start_new = False

    def _digit_count(self) -> int:
        return len(self._current.replace("-", "").replace(".", ""))

    def _fail(self, message: str) -> None:
        self._error = message
        self._current = "0"
        self._accumulator = None
        self._operator = None
        self._expression = ""
        self._start_new = True

    def _apply(self, left: Decimal, operator: str, right: Decimal) -> Decimal:
        operations = {"+": self.add, "-": self.subtract,
                      "*": self.multiply, "/": self.divide}
        try:
            return operations[operator](left, right)
        except (InvalidOperation, Overflow) as exc:
            raise CalculatorError("Operação inválida") from exc

    @staticmethod
    def _format(value: Decimal) -> str:
        """Arredonda para 15 dígitos significativos e remove zeros inúteis."""
        rounded = _ROUNDING.create_decimal(value)
        if abs(rounded) >= MAX_VALUE:
            raise CalculatorError("Resultado muito grande")
        if rounded == 0:
            return "0"
        return format(rounded.normalize(), "f")
