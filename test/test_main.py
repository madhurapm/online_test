import pytest, sys
sys.path.append('.')
from config_parser import ConfigParser
import json, os

def test_read_yaml():
    parser = ConfigParser('config.yaml')
    parser.read_yaml()
    assert parser.config == {'key1': 'value1', 'key2': {'sub_key1': 'sub_value1'}}

def test_read_cfg():
    parser = ConfigParser('example.cfg')
    parser.read_cfg()
    assert parser.config == {'section1': {'key1': 'value1'}}

def test_read_conf():
    parser = ConfigParser('example.conf')
    parser.read_conf()
    assert parser.config == {'key1': 'value1'}

def test_generate_flat_dict():
    parser = ConfigParser('config.yaml')
    parser.read_yaml()
    flat_dict = parser.generate_flat_dict()
    assert flat_dict == {'key1': 'value1', 'key2.sub_key1': 'sub_value1'}

def test_write_env():
    parser = ConfigParser('config.yaml')
    parser.read_yaml()
    flat_dict = parser.generate_flat_dict()
    parser.write_env(flat_dict)
    with open('.env', 'r') as f:
        lines = f.readlines()
        assert lines == ['key1=value1\n', 'key2.sub_key1=sub_value1\n']

def test_write_json():
    parser = ConfigParser('config.yaml')
    parser.read_yaml()
    flat_dict = parser.generate_flat_dict()
    parser.write_json(flat_dict)
    with open('config.json', 'r') as f:
        assert json.load(f) == flat_dict

def test_set_os_env():
    parser = ConfigParser('example.yaml')
    parser.read_yaml()
    flat_dict = parser.generate_flat_dict()
    parser.set_os_env(flat_dict)
    assert os.environ['key1'] == 'value1'
    assert os.environ['key2.sub_key1'] == 'sub_value1'