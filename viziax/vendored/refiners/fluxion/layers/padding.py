from torch import nn

from viziax.vendored.refiners.fluxion.layers.module import Module


class ReflectionPad2d(nn.ReflectionPad2d, Module):
    def __init__(self, padding: int) -> None:
        super().__init__(padding=padding)
