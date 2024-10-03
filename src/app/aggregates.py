from typing import List

from django.contrib.postgres.fields import ArrayField
from django.db.models import Aggregate, FloatField


class Percentile(Aggregate):
    function = "PERCENTILE_DISC"
    name = "percentile_disc"
    template = "(%(function)s(%(fractions)s) WITHIN GROUP (ORDER BY %(order_by)s))"
    output_field = ArrayField(FloatField())

    def __init__(self, fractions: List[float], order_by: str, *args, **extra):
        if not fractions:
            raise ValueError("List of percentile fractions must not be empty!")
        if not order_by:
            raise ValueError("Order by field must be defined!")

        fractions = "ARRAY[{}]".format(",".join(map(str, fractions)))

        super().__init__(*args, **extra)

        self.extra.update(fractions=fractions, order_by=order_by)
