__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
import warnings
warnings.filterwarnings("ignore")

class Deletefigures:

    def cleanup(self):
        files = ['integration/benchmarkprojectsupportsize.pdf', 'integration/benchmarkcellswapratio.pdf', 'integration/benchmarktimesssize.pdf',
                 'integration/benchmarkselectsupportsize.pdf', 'integration/benchmarkgroup.pdf', 'integration/benchmarkjoin.pdf',
                 'integration/benchmarkproject.pdf','integration/benchmarkselect.pdf', 'integration_ssb/barchartssbtime.pdf',
                 'integration_ssb/ssbq11.pdf', 'integration_ssb/ssbstatichistoryawareprice.pdf', 'integration_ssb/ssbstatichistorytime.pdf',
                 'integration_tpch/barcharttpchtimetest.pdf']
        for file in files:
            try:
                os.remove(file)
            except OSError:
                pass


if __name__ == "__main__":
    c = Deletefigures()
    c.cleanup()

