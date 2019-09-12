# -*- encoding: UTF-8 -*-
import os
import sys
import argparse
import yaml
from random import randint


def simulate_legacy_update():
    parser = argparse.ArgumentParser(
        description='Deploy',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('yaml_file', metavar='YAML', help='app.yaml file')
    parser.add_argument('-p', '--promote', action='store_true', help='migrate traffic.')
    options, extra_args = parser.parse_known_args()

    with open(options.yaml_file, 'r') as fh:
        yaml_data = yaml.safe_load(fh)

    application = yaml_data.pop('application', None)
    version = yaml_data.pop('version', None)

    if 'module' in yaml_data:
        yaml_data['service'] = yaml_data.pop('module')

    target_yaml = get_unniq_target_yaml(options.yaml_file)

    with open(target_yaml, 'w+') as fh:
        yaml.safe_dump(yaml_data, fh)

    args = create_args_list(options, target_yaml, application, version, extra_args)
    run_main(args)

    os.unlink(target_yaml)


def get_target_yaml(source_yaml):
    """
    :param source_yaml: str
    :return: str
    """

    return '{base}.deploy{r}.yaml'.format(
        base=source_yaml,
        r=randint(1000, 9999)
    )


def get_unniq_target_yaml(source_yaml):
    """
    :param source_yaml: str
    :return: str
    """

    target_yaml = None
    while not target_yaml:
        target_yaml = get_target_yaml(source_yaml)

        if os.path.isfile(target_yaml):
            target_yaml = None

    return target_yaml


def create_args_list(options, target_yaml, application, version, extra_args):
    """
    :type options: object
    :param target_yaml: object
    :param application: str
    :param version: str
    :param extra_args: list
    :return: list
    """

    new_args = ['gcloud', 'app', 'deploy']
    if not options.promote:
        new_args.append('--no-promote')

    if application:
        new_args.append('--project={}'.format(application))

    if version:
        new_args.append('--version={}'.format(version))

    new_args.append(target_yaml)
    new_args.extend(extra_args)

    return new_args


class ExitException(Exception):
    pass


def _un_exit(*args):
    raise ExitException(*args)


def run_main(args):
    """
    :param args: list
    """

    sys.argv = args
    sys.exit = _un_exit

    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from gcloud import main

    try:
        main()
    except ExitException:
        pass
