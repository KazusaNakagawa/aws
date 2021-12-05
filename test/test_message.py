import pytest
import sys

from logging import DEBUG, INFO, ERROR, getLogger

# Logger generation
logger = getLogger(__name__)


class Msg(object):
    """ Sample Code """

    def __init__(self):
        pass

    def division(self, num):
        """ divide

        params
        ------
          num(int): Number to put in denominator

        return
        ------
          Return the result of division

        """
        try:
            return 1 / num
        except ZeroDivisionError:
            print('moooon')
            logger.error('error', extra={'add initial data': 'error msg'})
            sys.exit(200)

    def log_debug(self):
        logger.debug('debug', extra={'add initial data': 'debug msg'})

    def log_info(self):
        logger.info('info', extra={'add initial data': 'info msg'})

    def log_err(self):
        logger.error('error', extra={'add initial data': 'error msg'})
        sys.exit(1)

    def exit(self):
        sys.exit(1)

    def exit_202(self):
        sys.exit(202)

    def exit_203(self):
        sys.exit(203)


class TestMsg(object):
    """ Test Code.
      Essentially, create a separate file as a test file.
    """

    @classmethod
    def setup_class(cls):
        print('\n*** start ***\n')
        cls.m = Msg()

    @classmethod
    def teardown_class(cls):
        print('\n\n*** end ***')

    def test_moon_exit(self):
        with pytest.raises(SystemExit):
            self.m.division(0)

    def test_moon_print(self, caplog, capfd):
        caplog.set_level(ERROR)

        with pytest.raises(SystemExit) as e:
            self.m.division(0)
        out, err = capfd.readouterr()

        assert out == 'moooon\n'
        assert err is ''
        assert [('test.test_message', ERROR, 'error')] == caplog.record_tuples
        assert e.value.code == 200

    def test_log_debug(self, caplog):
        caplog.set_level(DEBUG)

        self.m.log_debug()
        assert [('test.test_message', DEBUG, 'debug')] == caplog.record_tuples

    def test_log_err_sys_exit(self):
        with pytest.raises(SystemExit) as e:
            self.m.log_err()
        assert e.value.code == 1

    def test_exit_system_exit(self):
        """ Test SystemExit """
        with pytest.raises(SystemExit) as e:
            self.m.exit()
        assert e.value.code == 1

    def test_exit_system_exit_202(self):
        """ Test SystemExit """
        with pytest.raises(SystemExit) as e:
            self.m.exit_202()

        assert e.type == SystemExit
        assert e.value.code == 202

    def test_exit_pytest_fix(self):
        with pytest.raises(SystemExit) as e:
            self.m.exit_203()

        assert e.type == SystemExit
        assert e.value.code == 203
