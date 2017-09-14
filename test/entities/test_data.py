__author__ = 'tinglev@kth.se'

from everest_util.entities.application import Application
from everest_util.entities.cluster import Cluster
from everest_util.entities.service import Service
from everest_util.entities.image import Image
from everest_util.systems.registry import Registry
import root_path

def get_test_application():
    root_dir = root_path.get_root_path()
    registry = Registry('', '', '')
    app = Application(registry, root_dir)
    app._application_name = 'kth-azure-app'
    app._cluster = Cluster(root_dir)
    app._cluster._name = 'stage'
    app._file_content_md5 = 'paeio08v4927v4972bv924v'
    service = Service(registry)
    service._name = 'web'
    service._image = Image()
    service._image._name = 'kth-azure-app'
    service._image._registry = 'kthregistryv2.sys.kth.se'
    service._image._static_version = '${{WEB_VERSION}}'
    service._image._is_semver = True
    service._image._semver_version = '^2.1.0'
    service._labels.add_label('se.kth.label.bool', 'True')
    service._labels.add_label('se.kth.label.int', '123')
    service._deploy_labels.add_label('se.kth.deploy.label', 'This is a string')
    service._env_list.add_env('ENV_KEY1', 'ENV_VALUE1')
    app._services.append(service)
    service = Service(registry)
    service._name = 'redis'
    service._image = Image()
    service._image._name = 'redis'
    service._image._static_version = '1.6.3'
    app._services.append(service)
    return app
