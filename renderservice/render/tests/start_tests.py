"""Starts tests for the Render Service, daemon and webservice."""
import unittest

#
# Resource Generation Tests
#

from render.tests.resources.test_arrows import ArrowsResourceTest  # noqa: F401
from render.tests.resources.test_barcode_checksum_poster import BarcodeChecksumPosterResourceTest  # noqa: F401
from render.tests.resources.test_binary_cards_small import BinaryCardsSmallResourceTest  # noqa: F401
from render.tests.resources.test_binary_cards import BinaryCardsResourceTest  # noqa: F401
from render.tests.resources.test_binary_to_alphabet import BinaryToAlphabetResourceTest  # noqa: F401
from render.tests.resources.test_binary_windows import BinaryWindowsResourceTest  # noqa: F401
from render.tests.resources.test_grid import GridResourceTest  # noqa: F401
from render.tests.resources.test_job_badges import JobBadgesResourceTest  # noqa: F401
from render.tests.resources.test_left_right_cards import LeftRightCardsResourceTest  # noqa: F401
from render.tests.resources.test_modulo_clock import ModuloClockResourceTest  # noqa: F401
from render.tests.resources.test_parity_cards import ParityCardsResourceTest  # noqa: F401
from render.tests.resources.test_piano_keys import PianoKeysResourceTest  # noqa: F401
from render.tests.resources.test_searching_cards import SearchingCardsResourceTest  # noqa: F401
from render.tests.resources.test_sorting_network import SortingNetworkResourceTest  # noqa: F401
from render.tests.resources.test_sorting_network_cards import SortingNetworkCardsResourceTest  # noqa: F401
from render.tests.resources.test_train_stations import TrainStationsResourceTest  # noqa: F401
from render.tests.resources.test_treasure_hunt import TreasureHuntResourceTest  # noqa: F401

#
# General Tests
#

from render.tests.daemon.test_daemon_utils import DaemonUtilsTest  # noqa: F401
from render.tests.daemon.test_file_manager import FileManagerTest  # noqa: F401
from render.tests.daemon.test_resource_generator import ResourceGeneratorTest  # noqa: F401
from render.tests.daemon.test_queue_handler import QueueHandlerTest  # noqa: F401

from render.tests.webserver.test_webserver_app import WebserverAppTest  # noqa: F401

#
# Webservice Tests
#

if __name__ == "__main__":
    unittest.main()
