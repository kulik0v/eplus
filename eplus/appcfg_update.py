# -*- encoding: UTF-8 -*-
import os
import sys
import argparse
import yaml

SFX = '.deploy.yaml'


def simulate_legacy_update():
    parser = argparse.ArgumentParser(
        description='Deploy',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('yaml_file', metavar='YAML', help='app.yaml file')
    # parser.add_argument('-v', '--verbose', action='count', help='increase output verbosity')
    parser.add_argument('-p', '--promote', action='store_true', help='do migrate traffic.')
    # parser.add_argument('-a', '--ask', action='store_true', help='dont be quiet.')

    args, extra_args = parser.parse_known_args()

    # print('a', args)
    # print('f', args.yaml_file)
    # print('u', extra_args)

    with open(args.yaml_file, 'r') as fh:
        # except yaml.YAMLError as exc:
        #     print(exc)
        yaml_data = yaml.safe_load(fh)

    application = yaml_data.pop('application', None)
    version = yaml_data.pop('version', None)

    if 'module' in yaml_data:
        yaml_data['service'] = yaml_data.pop('module')

    dst_yaml = args.yaml_file + SFX

    if not os.stat(dst_yaml):
        raise Exception('Temporary yaml ({}) already exist'.format(dst_yaml))

    with open(dst_yaml, 'w') as fh:
        yaml.safe_dump(yaml_data, fh)


    new_args = ['gcloud', 'app', 'deploy']
    if not args.promote:
        new_args.append('--no-promote')

    # if not args.ask:
    #     new_args.append('--quiet')

    if application:
        new_args.append('--project={}'.format(application))

    if version:
        new_args.append('--version={}'.format(version))

    new_args.append(dst_yaml)
    new_args.extend(extra_args)
    # print new_args

    sys.argv = new_args
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from gcloud import main
    main()

    os.unlink(dst_yaml)

