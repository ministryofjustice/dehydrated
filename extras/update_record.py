#!/usr/bin/env python
import click
from bootstrap_cfn.r53 import R53

@click.command()
@click.option('--hosted_zone', prompt='Enter hosted zone', help='dns hosted zone')
@click.option('--rec_type', default='TXT', help="Record type, eg: A, CNAME, TXT etc")
@click.option('--rec_name', prompt='Enter record name', help='record name')
@click.option('--rec_value', prompt='Enter record value', help='record value')
@click.option('--aws_profile', prompt='Enter profile name', help='profile name')
def update_record(hosted_zone, rec_name, rec_type, rec_value, aws_profile):
    print aws_profile
    r53_con = R53(aws_profile)
    zone_id = r53_con.get_hosted_zone_id(hosted_zone)
    print locals()

    res = r53_con.update_dns_record(zone_id,
                                    rec_name,
                                    rec_type,
                                    '"{}"'.format(rec_value))
                                    #dry_run=True)
    print res


if __name__ == '__main__':
    update_record()

