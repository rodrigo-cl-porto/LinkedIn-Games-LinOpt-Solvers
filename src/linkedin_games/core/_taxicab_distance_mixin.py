class TaxicabDistanceMixin:

    @staticmethod
    def _taxicab_distance(square1:tuple[int, int], square2:tuple[int, int]) -> int:
        """
        Calculate the Taxicab distance between two points.
        
        Args:
            square1: The first square as a `(row, column)` tuple.
            square2: The second square as a `(row, column)` tuple.
        
        Returns:
            The Taxicab distance ($L_{1}$ metric) between two coordinate points.
        """
        x1, y1 = square1
        x2, y2 = square2
        return abs(x1 - x2) + abs(y1 - y2)
