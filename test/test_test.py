import logging
import pytest
import sys
import os
from logging import DEBUG, INFO, ERROR, getLogger

logger = getLogger('test')


class Msg(object):

    def __init__(self):
        self.moon = 'moon'

    def moon_(self):
        try:
            r = 1 / 0
        except:
            print('moooon')
            sys.exit(200)

    def log_debug(self):
        logger.debug('debug', extra={'add_iti onal data': 'debug msg'})

    def log_info(self):
        logger.info('info', extra={'add_iti o nal data': 'info msg'})

    def log_err(self):
        logger.error('error', extra={'add_iti o nal data': 'error msg'})

    def exit(self):
        sys.exit(1)

    def exit_202(self):
        sys.exit(202)


class TestMsg(object):

    @classmethod
    def setup_class(cls):
        print('start')
        cls.m = Msg()

    @classmethod
    def teardown_class(cls):
        print('end')

    def test_moon_exit(self):
        with pytest.raises(SystemExit):
            self.m.moon_()

    def test_moon_print(self, capfd):
        with pytest.raises(SystemExit):
            self.m.moon_()
            out, err = capfd.readouterr()
            assert out == 'aaa\nbbb\n'
            assert err is ''

    def test_moon_log_error(self, caplog):
        caplog.set_level(DEBUG)

        self.m.log_debug()
        assert [('test', DEBUG, 'debug')] == caplog.record_tuples
        # assert caplog.records[0].extra == 'info'

    def test_exit_system_exit(self):
        """ Test SystemExit """
        with pytest.raises(SystemExit) as e:
            self.m.exit()
        # e.value で SystemExit を参照できる
        assert e.value.code == 1

    def test_exit_system_exit_202(self):
        """ Test SystemExit """
        with pytest.raises(SystemExit) as e:
            self.m.exit_202()
        # e.value で SystemExit を参照できる
        assert e.value.code == 202
