from django.apps import apps
from django.conf import settings


def get_class_from_app_label(label):
    '''
    Given the label of a pod, get the Pod class associated with it.
    '''
    appconfig = apps.get_app_config(label)
    return appconfig.pod_class


def load_pod(index, config):
    '''
    Given the index of the pod, and the config dictionary for the pod, this
    returns the instance of that pod.
    '''
    config = config.copy()
    app_label = config.pop('app_label')
    config['index'] = index
    return get_class_from_app_label(app_label)(config)


pods = tuple(
    load_pod(i, c) for i, c in enumerate(settings.PODS)
)
