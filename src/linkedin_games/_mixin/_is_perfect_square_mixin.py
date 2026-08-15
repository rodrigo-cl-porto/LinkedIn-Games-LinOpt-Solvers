from math import sqrt

class IsPerfectSquareMixin:

    @staticmethod
    def _is_perfect_square(n: int) -> bool:
        """
        Check if a number is a perfect square.
        
        Args:
            n: The number to check.

        Returns:
            `True` if `n` is a perfect square, `False` otherwise.
        """
        return sqrt(n) % 1 == 0
