# Unity IAP

## Apple App Store

[Receipt Validation Programming Guide](https://developer.apple.com/library/content/releasenotes/General/ValidateAppStoreReceipt/Chapters/ValidateRemotely.html)

```bash
$ ./apple.py -h
usage: apple.py [-h] [-s SECRET] [-r RECEIPT]

optional arguments:
  -h, --help            show this help message and exit
  -s SECRET, --secret SECRET
                        Shared Secret
  -r RECEIPT, --receipt RECEIPT
                        Apple App Store IAP receipt
```

## Google Play Store

```bash
$ ./google.py -h
usage: google.py [-h] [-k PUBLIC_KEY] [-r RECEIPT]

optional arguments:
  -h, --help            show this help message and exit
  -k PUBLIC_KEY, --public_key PUBLIC_KEY
                        Google License Key(Public Key)
  -r RECEIPT, --receipt RECEIPT
                        Google Play IAP receipt
```

## Xiaomi App Store

```bash
$ ./xiaomi.py -h
usage: xiaomi.py [-h] [--client_id CLIENT_ID] [--client_secret CLIENT_SECRET]
                 [--public_key PUBLIC_KEY] [--verify_signature] [--verify_api]
                 [--receipt RECEIPT] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --client_id CLIENT_ID
                        UnityChannel Client ID
  --client_secret CLIENT_SECRET
                        UnityChannel Client Secret
  --public_key PUBLIC_KEY
                        UnityChannel Public Key
  --verify_signature    Verfiy signature
  --verify_api          Verfiy via server API
  --receipt RECEIPT     Xiaomi IAP receipt
  --debug               Use debug environment
```