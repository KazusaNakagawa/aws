## About
Control aws with boto3 and chalice.

## environment

- Python 3.8.8

## Usage

1.Create and start containers
```bash
$ docker-compose up -d
```
2.Enter the container with bash
```bash
$ docker-compose exec web bash 
```

3.Set aws configure
```bash
$ aws configure

# >> Fill in the fields that will be asked
AWS Access Key ID [None]: <IAM Access Key ID>
AWS Secret Access Key [None]: <IAM Secret Access Key>
Default region name [None]: <region name>
Default output format [None]: json
```

4.Access jupyter lab
 - http://localhost:8888/
 
5.mariadb container in

```bash
$ docker-compose exec mariadb bash
```

## Reference
- [aws Regions and Zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)