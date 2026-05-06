"""Utility Class For Health Metrics Conversion"""

from pint import UnitRegistry

ureg = UnitRegistry()


class MetricsConversion:
    def __init__(self, unit, **kwargs):
        metric_name, value = next(iter(kwargs.items()))
        self.metric_name = metric_name
        self.quantity = value * ureg(unit)

    def convert_to(self, new_unit):
        """Convert metric unit

        Args:
            new_unit (str): unit to convert to
        """
        self.quantity = self.quantity.to(new_unit)

    def convert_blood_glucose(self):
        """_summary_

        Args:
            value (int): blood glucose value
            from_unit (str): current unit
            to_unit (str): unit to convert to

        Returns:
            _type_: _description_
        """
        to_unit = "mg/dL" or "milligram / deciliter"
        from_unit = self.quantity.units
        value = self.quantity.magnitude
        if from_unit == "mmol/L" or from_unit == "millimole / liter":
            value *= 18.016
        if from_unit == "mg/dL" or from_unit == "milligram / deciliter":
            value /= 18.016
            to_unit = "mmol/L" or to_unit == "millimole / liter"
        return f"{self.metric_name}: {round(value, 3)} {to_unit}"

    def metric(self):
        """Metric

        Returns:
            int | float | str: Scalar measurements
        """
        unit = self.quantity.units
        if (
            "blood_glucose" in self.metric_name
            or "blood_glucose_level" in self.metric_name
        ):
            metrics = self.convert_blood_glucose()
            return metrics
        rounded_val = round(
            (
                self.quantity.magnitude
                if hasattr(self.quantity, "magnitude")
                else self.quantity
            ),
            3,
        )
        return f"{self.metric_name} : {rounded_val} {unit}"

    @classmethod
    def calculate_bmi(cls, weight_val, weight_unit, height_val, height_unit):
        w = weight_val * ureg(weight_unit)
        h = height_val * ureg(height_unit)

        bmi_quantity = w / (h**2)

        return f"bmi: {round(bmi_quantity.to('kg/m**2').magnitude, 3)}"


# my_unit = MetricsConversion(height=20, unit="in")
# print(my_unit.metric())
# my_unit.convert_to("cm")
# print(my_unit.metric())

"""my_bmi = MetricsConversion(unit="kg/m**2", bmi=60)
print(my_bmi.metric())
print(
    MetricsConversion.calculate_bmi(
        weight_val=180, weight_unit="lb", height_val=6, height_unit="ft"
    )
)

my_bg = MetricsConversion(unit="mg/dL", blood_glucose=70)
print(my_bg.metric())
print(MetricsConversion.convert_blood_glucose(my_bg))"""
