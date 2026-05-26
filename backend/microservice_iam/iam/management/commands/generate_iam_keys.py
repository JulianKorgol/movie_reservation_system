import os

from django.core.management.base import BaseCommand, CommandError

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from microservice_iam.settings import BASE_DIR, DEBUG

keys_dir = os.path.join(BASE_DIR, "iam_keys")
public_key_copy_dir = os.path.join(BASE_DIR, "iam_public_key")
public_key_copy_path = os.path.join(public_key_copy_dir, "iam_public_key.pem")
private_key_path = os.path.join(keys_dir, "private_key.pem")
public_key_path = os.path.join(keys_dir, "public_key.pem")


class Command(BaseCommand):
    help = "Generates IAM asymetric keys for JWT signing"

    def add_arguments(self, parser):
        parser.add_argument(
            '--autodevrun',
            action='store_true',
            help="Skip raise error that keys already exist"
        )

    def handle(self, *args, **options):
        is_autodevrun = options["autodevrun"]
        if not is_autodevrun and (os.path.exists(private_key_path) or os.path.exists(public_key_path) or os.path.exists(
                public_key_copy_path)):
            raise CommandError(
                f"Keys already exist in {keys_dir}. "
                "Delete them manually if you are absolutely sure you want to rotate keys."
            )

        self.stdout.write("Start generating IAM keys")

        private_key = ec.generate_private_key(ec.SECP256R1())
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key = private_key.public_key()
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        os.makedirs(keys_dir, exist_ok=True)

        with open(private_key_path, "wb") as file:
            file.write(private_key_pem)
        os.chmod(private_key_path, 0o600)

        with open(public_key_path, "wb") as file:
            file.write(public_key_pem)
        os.chmod(public_key_path, 0o644)

        with open(public_key_copy_path, "wb") as file:
            file.write(public_key_pem)
        os.chmod(public_key_copy_path, 0o644)

        self.stdout.write("Successfully generated IAM keys")
