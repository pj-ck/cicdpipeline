import os
import time
import jwt
import requests

# Constants
VERSION = "1.0.3"  # Must match manifest.json
XPI_FILE_PATH = os.path.expanduser("~/Desktop/my-ext.xpi")
ADDON_SLUG = "new-add"  # Replace with your actual addon slug

AMO_API_URL = "https://addons.mozilla.org/api/v5/addons"
UPLOAD_URL = f"{AMO_API_URL}/upload/"
VERSION_URL = f"{AMO_API_URL}/addon/{ADDON_SLUG}/versions/"  # ✅ Fixed the endpoint

# JWT credentials
JWT_ISSUER = os.getenv("AMO_JWT_ISSUER")
JWT_SECRET = os.getenv("AMO_JWT_SECRET")

if not JWT_ISSUER or not JWT_SECRET:
    raise EnvironmentError("Set AMO_JWT_ISSUER and AMO_JWT_SECRET as environment variables.")

# Generate JWT token
issued_at = int(time.time())
payload = {
    "iss": JWT_ISSUER,
    "jti": os.urandom(16).hex(),
    "iat": issued_at,
    "exp": issued_at + 60
}
jwt_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
if isinstance(jwt_token, bytes):
    jwt_token = jwt_token.decode("utf-8")

print(f"🔐 JWT Token Prefix: {jwt_token[:25]}...")
print(f"UPLOAD_URL: {UPLOAD_URL}")

# Upload the .xpi file
try:
    with open(XPI_FILE_PATH, "rb") as xpi_file:
        upload_response = requests.post(
            UPLOAD_URL,
            headers={"Authorization": f"JWT {jwt_token}"},
            files={"upload": ("my-ext.xpi", xpi_file, "application/x-xpinstall")},
            data={"channel": "listed"}  # Change to "unlisted" if needed
        )

    upload_response.raise_for_status()

    uuid = upload_response.json().get("uuid")
    print(f"✅ Upload successful. UUID: {uuid}")

    # Create a new version
    print(f"🚀 Creating version {VERSION}...")

    version_payload = {
        "upload": uuid,
        "version": VERSION,
        "channel": "listed"
    }

    version_response = requests.post(
        VERSION_URL,
        headers={
            "Authorization": f"JWT {jwt_token}",
            "Content-Type": "application/json"
        },
        json=version_payload
    )

    if version_response.status_code in (201, 202):
        print(f"✅ Version {VERSION} created successfully!")
    else:
        print("❌ Failed to create version.")
        print("Status Code:", version_response.status_code)
        print("Response:", version_response.text)

except requests.exceptions.RequestException as e:
    print(f"❌ An error occurred: {e}")
    if 'upload_response' in locals():
        print("Status Code:", upload_response.status_code)
        print("Response:", upload_response.text)






        