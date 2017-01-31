# Dehydrated shell script - cli manual steps for Lets Encrypt cert creation

## Prep virtualenv (optional, only needed if python script below is used)

Per title, this step is optional. Create a virtualenv with a method of your choice, eg mkvirtualenv or directly through virtualenv.

Install the requirements. Mainly `bootstrap-cfn` (most deploy versions will work already), as well as `click` python packages.

```
pip install -r requirements.txt
```
Alternatively, if a deploy virtualenv is available, pip installing just `click` might be enough.


##Start Lets Encrypt cert issuing process


Start the process and follow instructions on screen. It will eventually pause and instruct you on the next step, which can be performed manually or via the `update_record.py` script below.

```
./dehydrated --config extras/config -c -a rsa -t dns-01 -k extras/hook.sh -d staging.test.dsd.io -o final
```

This command would place the final certs under the directory "final", adjust as needed.

##Update record to complete challenge

```
./update_record.py --hosted_zone test.dsd.io --rec_type TXT \
--rec_name _acme-challenge.staging.test.dsd.io \
--rec_value 6EkRh6upH5-eYG9rruJoHrb3VmogKH0tIMu30wqwfd4 \
--aws_profile temp01
```
This step will take some time, usually up to 60 seconds. Use the command (optionally via specifying a nameserver like google's to avoid local caching) to validate the value is set to what you specified above:

```
$ host -t TXT _acme-challenge.staging.test.dsd.io
```
or using 8.8.8.8 as a DNS server:
```
$ host -t TXT _acme-challenge.staging.test.dsd.io 8.8.8.8
```


## Cleanup of DNS record
No script given, since this is just MVP to get started. See hook script for info and python script for more details on how to implement.


## Post creation steps
Obtain certs from `final` directory and plug them into infra/code as needed. The accounts directory is only needed if the cert would need to be revoked. As the certificate life is fairly short, saving the account shouldn't be needed too often.


## Update record python script
This has been tested mainly with TXT records.. as this is what the challenges are.

```
$ ./update_record.py --help
Usage: update_record.py [OPTIONS]

Options:
  --hosted_zone TEXT  dns hosted zone
  --rec_type TEXT     Record type, eg: A, CNAME, TXT etc
  --rec_name TEXT     record name
  --rec_value TEXT    record value
  --aws_profile TEXT  profile name
  --help              Show this message and exit.
```
