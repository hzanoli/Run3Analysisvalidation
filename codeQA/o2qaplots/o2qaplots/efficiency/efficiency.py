import typing

import ROOT

from o2qaplots.plot_base import (
    Configurable,
    InputConfigurable,
    PlottingTask,
    ROOTObj,
    TaskInput,
    macro,
)


def calculate_efficiency(
    reconstructed: ROOT.TH3D,
    generated: ROOT.TH3D,
    eta_cut: float = None,
    pt_range: typing.List[float] = None,
):
    """Calculated the efficiency as function of the feature in axis.

    Args:
        reconstructed: histogram with the reconstructed information.
        generated: histogram with the generated information.
        eta_cut: applies the selection |n| < eta_cut to the efficiency
        pt_range: selects only particles with pt_range[0] < pt < pt_range[1]

    Returns:
        efficiency: a TGraph with the efficiencies
    """

    epsilon = 0.0001

    if eta_cut is not None:
        generated.GetYaxis().SetRangeUser(-1.0 * eta_cut + epsilon, eta_cut - epsilon)
        reconstructed.GetYaxis().SetRangeUser(
            -1.0 * eta_cut + epsilon, eta_cut - epsilon
        )

    if pt_range is not None:
        if len(pt_range) != 2:
            raise ValueError(
                "You should pass exactly two values to the transverse momentum"
                "range (pt_range)."
            )

        generated.GetXaxis().SetRangeUser(pt_range[0] + epsilon, pt_range[1] - epsilon)
        reconstructed.GetXaxis().SetRangeUser(
            pt_range[0] + epsilon, pt_range[1] - epsilon
        )

    generated_1d = generated.Project3D("x")
    reconstructed_1d = reconstructed.Project3D("x")

    # efficiency = ROOT.TEfficiency(reconstructed_1d, generated_1d)
    efficiency = reconstructed_1d.Clone("Efficiency")
    efficiency.Divide(generated_1d)

    return efficiency


class Efficiency(PlottingTask):
    parser_description = "Calculates the efficiency for the physical primary particles."
    parser_command = "eff"

    eta = Configurable("--eta", "-e", default=1.4, type=float, help="Selection in eta.")

    pt_range = Configurable(
        "--pt_range",
        "-pt",
        default=(0.0, 10.0),
        nargs=2,
        action="append",
        type=float,
        help="Cut in pt_range[0] < pt <= pt_range[1].",
    )

    particle = InputConfigurable(
        "-p",
        "--particle",
        help="particle to be processed",
        type=str,
        choices=["electron", "pion", "kaon", "muon", "proton"],
        default="pion",
    )

    generated = TaskInput("qa-tracking-efficiency/generatedKinematics")
    reconstructed = TaskInput("qa-tracking-efficiency/reconstructedKinematics")

    efficiency = ROOTObj("qa-tracking-efficiency/primaryTrackEfficiency")

    def process(self):
        efficiency = calculate_efficiency(
            self.reconstructed, self.generated, self.eta, self.pt_range
        )

        return {self.efficiency: efficiency}


if __name__ == "__main__":
    macro(Efficiency)
