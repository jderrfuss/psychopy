from pathlib import Path
from psychopy.experiment.components.keyboard import KeyboardComponent
from psychopy.hardware.keyboard import Keyboard, KeyboardDevice
from psychopy.tests import utils
from psychopy.tests.test_experiment.test_components import BaseComponentTests
from psychopy import session


class BaseKeyboardComponentTests(BaseComponentTests):
    comp = KeyboardComponent
    libraryClass = Keyboard

    def makeSession(self):
        # make a Session
        self.session = session.Session(
            root=Path(utils.TESTS_DATA_PATH) / "test_components",
        )
        # setup default window
        self.session.setupWindowFromParams({})

    def testKeyboardClear(self):
        """
        Test that KeyPress responses are cleared at the start of each Routine
        """
        # add keyboard clear experiment
        self.session.addExperiment("testClearKeyboard/testClearKeyboard.psyexp", "keyboardClear")
        # run keyboard clear experiment
        self.session.runExperiment("keyboardClear")
        # make sure `getter` Routine didn't finish on first frame
        entry = self.session.runs[-1].entries[-1]
        assert (entry['getter.stopped'] - entry['getter.started']) > 0.5


class TestIohubKeyboardComponent(BaseKeyboardComponentTests):
    def setup_class(self):
        # setup session
        self.makeSession(self)
        # set backend to ioHub
        KeyboardDevice._backend = "iohub"


class TestPtbKeyboardComponent(BaseKeyboardComponentTests):
    def setup_class(self):
        # setup session
        self.makeSession(self)
        # set backend to ioHub
        KeyboardDevice._backend = "ptb"
