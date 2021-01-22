import typing

import ROOT

import o2qaplots.plot as plot
from o2qaplots.plot_base import PlottingTask, macro, ROOTObj
from o2qaplots.file_utils import discover_root_objects


class Plot(PlottingTask):
    plot_type = "define_your_type"
    save_output = False

    def process(self):
        histograms = discover_root_objects(
            ROOT.TFile(self.file), lambda x: self.plot_type in x
        )
        print(histograms)

        return {ROOTObj(x): ROOTObj(x).get(self.file) for x in histograms}


class Plot1D(Plot):
    parser_description = "Plots all the 1d histograms."
    parser_command = "plot1d"
    plot_type = "TH1"


class Plot2D(Plot):
    parser_description = "Plots all the 2d histograms."
    parser_command = "plot2d"
    plotting_function = plot.plot_2d
    plot_type = "TH2"


if __name__ == "__main__":
    macro(Plot)
