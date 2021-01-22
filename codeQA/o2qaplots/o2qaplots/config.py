import json
import typing


class AxisConfig:
    """Configures an histogram axis representation.

    Attributes:
        view_range: the axes range that will be visible in the plot
        log: whether the axis should be shown in a log scale.

    Args:
        view_range: the axes range that will be visible in the plot
        log: whether the axis should be shown in a log scale.
    """

    def __init__(self, view_range: typing.List[float] = None, log: bool = False):
        self.view_range = view_range
        self.log = log

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} view_range={self.view_range} log={self.log}>"
        )


class PlotConfig:
    """Configures an individual plot.

    Attributes:
        x_axis: AxisConfig with the configuration for the x axis
        y_axis: AxisConfig with the configuration for the y axis

    Args:
        x_axis: an AxisConfig with for the axis, or a dict to be passed to the constructor of AxisConfig
        y_axis:  an AxisConfig with for the axis, or a dict to be passed to the constructor of AxisConfig

    """

    def __init__(
        self,
        x_axis: typing.Union[AxisConfig, dict] = AxisConfig(),
        y_axis: typing.Union[AxisConfig, dict] = AxisConfig(),
    ):
        if not isinstance(x_axis, AxisConfig):
            x_axis = AxisConfig(**x_axis)

        if not isinstance(y_axis, AxisConfig):
            y_axis = AxisConfig(**y_axis)

        self.x_axis = x_axis
        self.y_axis = y_axis

    def __repr__(self):
        return f"<{self.__class__.__name__} x_axis={repr(self.x_axis)} y_axis={repr(self.y_axis)}>"


class JsonConfig(dict):
    """ "Class used to read and store the JSON configuration files.
    It reads the configuration from the JSON file and it stores it in as a dictionary. The values of the dictionary
    are automatically converted into an PlotConfig.
    In case the configuration is not set for a particular object, this configuration will return a PlotConfig with its
    default value.

    """

    def __init__(self, json_file_name=None):
        if json_file_name is not None:
            with open(json_file_name) as json_file:
                values = json.load(json_file)
                super().__init__({k: PlotConfig(**v) for k, v in values.items()})
        else:
            super(JsonConfig, self).__init__()

    def get(self, key):
        """Get the configuration from a particular object

        Args:
            key: key (name) of the object

        Returns
            If the key is valid, returns the PlotConfig which corresponds to this key. Otherwise a PlotConfig with its
            default values is returned.
        """
        if super(JsonConfig, self).get(key) is not None:
            return super(JsonConfig, self).get(key)

        return PlotConfig()
