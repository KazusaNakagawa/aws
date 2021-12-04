import logging
import pytest
import sys
import os
from logging import DEBUG, INFO, ERROR, getLogger

logger = getLogger('test')


class Msg(object):

    def __init__(self):
        self.moon = 'moon'

    def division(self, num):
        try:
            return 1 / num
        except ZeroDivisionError:
            print('moooon')
            logger.error('error', extra={'add_iti onal data': 'error msg'})
            sys.exit(200)

    def log_debug(self):
        logger.debug('debug', extra={'add_iti onal data': 'debug msg'})

    def log_info(self):
        logger.info('info', extra={'add_iti o nal data': 'info msg'})

    def log_err(self):
        logger.error('error', extra={'add_iti o nal data': 'error msg'})
        sys.exit(1)

    def exit(self):
        sys.exit(1)

    def exit_202(self):
        sys.exit(202)

    def exit_203(self):
        sys.exit(203)


class TestMsg(object):

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
        assert [('test', ERROR, 'error')] == caplog.record_tuples
        assert e.value.code == 200

    def test_log_debug(self, caplog):
        caplog.set_level(DEBUG)

        self.m.log_debug()
        assert [('test', DEBUG, 'debug')] == caplog.record_tuples

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
