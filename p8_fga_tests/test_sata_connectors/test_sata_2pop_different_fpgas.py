"""
retina example that just feeds data from a retina to live output via an
intermediate population
"""
import spynnaker8 as p
from p8_integration_tests.base_test_case import BaseTestCase


def do_run():
    # Setup
    p.setup(timestep=1.0)

    # FPGA Retina

    p.Population(2000, p.external_devices.ArbitraryFPGADevice(
        n_neurons=2000, fpga_link_id=12, fpga_id=1, label="bacon1"),
                 label='External sata thing 1')

    p.Population(2000, p.external_devices.ArbitraryFPGADevice(
        n_neurons=2000, fpga_link_id=12, fpga_id=2, label="bacon2"),
                 label='External sata thing 2')

    p.run(1000)
    p.end()


class Sata2PopDifferentFPGAsTest(BaseTestCase):

    def test_sata_2pop_different_fpgas(self):
        do_run()


if __name__ == "__main__":
    do_run()
