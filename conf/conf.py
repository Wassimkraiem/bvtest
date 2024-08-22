from conf.utils import get_env


ENABLE_SENTRY = get_env("ENABLE_SENTRY", default=False)
CORS_ALLOWED_ORIGINS = get_env("CORS_ALLOWED_ORIGINS", default="*")
REDIS_HOST_URL = get_env("REDIS_HOST_URL", required=True)
PROPAGATE_EXCEPTIONS = True
S3_BUCKET = get_env("S3_BUCKET", required=True)
AWS_KEY = get_env("AWS_KEY", required=True)
AWS_SECRET = get_env("AWS_SECRET", required=True)
EXPIRATION_S3_PRESIGNED_URL = 60 * 12
DYNAMODB_REGION = get_env("DYNAMODB_REGION", required=True)
AWS_DYNAMODB_ACCESS_KEY = get_env("AWS_DYNAMODB_ACCESS_KEY", required=True)
AWS_DYNAMODB_SECRET_KEY = get_env("AWS_DYNAMODB_SECRET_KEY", required=True)
FORMS_DYNAMO_TABLE_NAME = get_env("FORMS_DYNAMO_TABLE_NAME", required=True)
CAPTCHA_SECRET = get_env("CAPTCHA_SECRET", required=True)
SENTRY_DSN = get_env("SENTRY_DSN", required=False)
FLASK_ENV = get_env("FLASK_ENV", default="development")
AWS_REGION = get_env("AWS_REGION", default="us-east-1")
