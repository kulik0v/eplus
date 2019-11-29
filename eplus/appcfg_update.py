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
    parser.add_argument('-ep', '--promote', action='store_true', help='Migrate traffic.')
    parser.add_argument('-ek', '--keepyaml', action='store_true', help='Keep modified yaml.')

    parser.add_argument('--version', action='store', help='The version of the app.')
    parser.add_argument('--project', action='store', help='The Google Cloud Platform project name to use for this invocation.')

    options, extra_args = parser.parse_known_args()

    source_yaml = options.yaml_file

    with open(source_yaml, 'r') as fh:
        yaml_data = yaml.safe_load(fh)

    update_options(options, yaml_data)

    target_yaml = get_unniq_target_yaml(source_yaml)

    with open(target_yaml, 'w+') as fh:
        yaml.safe_dump(yaml_data, fh)

    args = create_args_list(options, target_yaml, extra_args)

    print('RUNNING: ' + ' '.join(args))
    run_main(args)

    if not options.keepyaml:
        os.unlink(target_yaml)


def update_options(options, yaml_data):
    """
    :param options: argparse.Namespace
    :param yaml_data: object
    """

    application = yaml_data.pop('application', None)
    if not options.project and application:
        options.project = application

    version = yaml_data.pop('version', None)
    if not options.version and version:
        options.version = version

    if 'module' in yaml_data:
        yaml_data['service'] = yaml_data.pop('module')


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


def create_args_list(options, target_yaml, extra_args):
    """
    :param options: argparse.Namespace
    :param target_yaml: object
    :param extra_args: list
    :return: list
    """

    new_args = ['gcloud', 'app', 'deploy']
    if not options.promote:
        new_args.append('--no-promote')

    if options.project:
        new_args.append('--project={}'.format(options.project))

    if options.version:
        new_args.append('--version={}'.format(options.version))

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
