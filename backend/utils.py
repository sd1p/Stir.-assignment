import zipfile
from bson import ObjectId

proxies = [
    {
        "address": "198.23.239.134",
        "port": 6540,
    },
    {
        "address": "207.244.217.165",
        "port": 6712,
    },
    {
        "address": "107.172.163.27",
        "port": 6543,
    },
    {
        "address": "64.137.42.112",
        "port": 5157,
    },
    {
        "address": "173.211.0.148",
        "port": 6641,
    },
    {
        "address": "161.123.152.115",
        "port": 6360,
    },
    {
        "address": "167.160.180.203",
        "port": 6754,
    },
    {
        "address": "154.36.110.199",
        "port": 6853,
    },
    {
        "address": "173.0.9.70",
        "port": 5653,
    },
    {
        "address": "173.0.9.209",
        "port": 5792,
    },
]


def convert_objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: convert_objectid_to_str(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    return obj


def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """
    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt("{proxy_port}")
            }},
            bypassList: ["localhost"]
        }}
    }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{proxy_username}",
                password: "{proxy_password}"
            }}
        }};
    }}

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """

    with zipfile.ZipFile("proxy_auth_extension.zip", "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
