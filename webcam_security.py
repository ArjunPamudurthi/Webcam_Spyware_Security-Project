import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import webbrowser
import base64

# Try to import PIL with proper error handling for PyInstaller
PIL_AVAILABLE = False
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError as e:
    print(f"PIL/Pillow not available: {e}")
    print("Camera logo will not be displayed, but the application will continue to work.")

from tkinter import Tk, PhotoImage
import io
import tempfile
import sys
import os
import time
import winreg
import ctypes
from ctypes import wintypes

import random
import string

# Try to import cv2 with proper error handling for PyInstaller
CV2_AVAILABLE = False
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError as e:
    print(f"OpenCV not available: {e}")
    print("Video recording features will not be available, but the application will continue to work.")

import glob

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Relaunch the script with admin rights
    import sys
    import os
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, '"' + os.path.abspath(__file__) + '"', None, 1)
    sys.exit()

# --- PASSWORD DEFINITION ---
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    # Remove problematic characters for password entry if needed
    characters = characters.replace('"', '').replace("'", '').replace('\\', '')
    return ''.join(random.choice(characters) for _ in range(length))

password = generate_password()




import smtplib
from email.message import EmailMessage
import threading


def send_password_email(password):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "arjunpamudurthi@gmail.com"
    SMTP_PASSWORD = "eclf hwzl bqee ipnq"

    sender_email = SMTP_USERNAME
    recipient_email = "arjunpamudurthi@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = "Your Generated Webcam Security Password"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(f"Hello Arjun Pamudurthi,\n\nYour generated webcam security password is:\n\n{password}\n\nPlease keep it secure.\n\nRegards,\nWebcam Security System")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print("Password email sent successfully.")
    except Exception as e:
        error_message = (
            f"Failed to send the password email due to an error: {e}\n\n"
            "Please check the following:\n"
            "1. Your internet connection is active.\n"
            "2. The SMTP settings in the script are correctly configured.\n"
            "3. The email address and password are correct.\n"
            "4. If you're using Gmail with 2FA, you may need an 'App Password'."
        )
        print(error_message)
        # Show a more informative error messagebox to the user
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Email Configuration Error", error_message)
        root.destroy()

def send_intrusion_alert_email(event_time, event_type="Suspicious Login Attempt"):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "arjunpamudurthi@gmail.com"
    SMTP_PASSWORD = "eclf hwzl bqee ipnq"

    sender_email = SMTP_USERNAME
    recipient_email = "arjunpamudurthi@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = f"Intrusion Alert: {event_type}"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(f"Alert! Suspicious activity detected on your Webcam Security System.\n\nEvent: {event_type}\nTime: {event_time}\n\nPlease check your system immediately.\n\nRegards,\nWebcam Security System")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print("Intrusion alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send intrusion alert email: {e}")

def send_intrusion_alert_email_async(event_time, event_type="Suspicious Login Attempt"):
    threading.Thread(target=send_intrusion_alert_email, args=(event_time, event_type), daemon=True).start()

log_file = "camera_log.txt"

# --- FUNCTION DEFINITIONS ---

def show_info():
    # Show project info without camera image
    html_content = '''
    <html>
    <head><title>Project Information</title></head>
    <body style="font-family:Arial;">
        <h2>Project Information</h2>
        <div style="margin-bottom:16px;">
            <p>This project was developed by Arjun Pamudurthi as a part of Cyber Security Internship. The motive of this project is to provide secure control over webcam access and help prevent unauthorized usage, enhancing user privacy and security.</p>
        </div>
        <table border="1" cellpadding="8" style="border-collapse:collapse;">
            <tr><th>Project Details</th><th>Value</th></tr>
            <tr><th>Project Name</th><td>WebCam Spyware Security</td></tr>
            <tr><th>Project Description</th><td>Security tool for webcam monitoring and control</td></tr>
            <tr><th>Start Date</th><td>06-07-2025</td></tr>
            <tr><th>End Date</th><td>2025-07-10</td></tr>
            <tr><th>Status</th><td>Completed</td></tr>
        </table>
        <h3>Developer Details</h3>
        <table border="1" cellpadding="8" style="border-collapse:collapse;">
            <tr>
                <th>Name</th>
                <th>Employee ID</th>
                <th>Email</th>
            </tr>
<tr><td>ST#IS#7623</td><td>Arjun Pamudurthi</td><td>arjunpamudurthi@gmail.com</td></tr>
        </table>
        <h3>Company Details</h3>
        <table border="1" cellpadding="8" style="border-collapse:collapse;">
            <tr><th>Company Name</th><td>Supraja Technologies</td></tr>
            <tr><th>Contact</th><td>contact@suprajatechnologies.com</td></tr>
        </table>
    </body>
    </html>
    '''
    import tempfile, webbrowser
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html_content)
        temp_html_path = f.name
    webbrowser.open(temp_html_path)

def view_logs():
    def on_ok():
        if password_entry.get() == password:
            password_window.destroy()
            try:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        log_content = f.read()
                    if log_content.strip():
                        log_win = tk.Toplevel(root)
                        log_win.title("Camera Logs")
                        log_win.geometry("400x300")
                        tk.Label(log_win, text="Camera Access Logs", font=("Arial", 12, "bold"), bg="black", fg="white").pack(pady=5)
                        log_text = tk.Text(log_win, wrap="word", bg="black", fg="lime", font=("Consolas", 10))
                        log_text.insert("1.0", log_content)
                        log_text.config(state="disabled")
                        log_text.pack(expand=True, fill="both", padx=10, pady=10)
                    else:
                        messagebox.showinfo("Log Empty", "Log file is empty.")
                else:
                    messagebox.showwarning("Log Missing", f"Log file not found at: {os.path.abspath(log_file)}")
            except Exception as e:
                messagebox.showerror("Log Error", f"Could not read log file: {e}")
        else:
            error_label.config(text="Incorrect password. Try again.")
            password_entry.delete(0, tk.END)
            record_intruder_video()
            send_intrusion_alert_email_async(time.strftime('%Y-%m-%d %H:%M:%S'), "Incorrect Password for View Logs")

    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x150")
    tk.Label(password_window, text="Enter Password:").pack(pady=10)
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack(pady=5)
    tk.Button(password_window, text="OK", command=on_ok).pack(pady=5)
    error_label = tk.Label(password_window, text="", fg="red")
    error_label.pack()

def check_status():
    # Check webcam status by trying to open it
    if not CV2_AVAILABLE:
        messagebox.showerror("Camera Status", "OpenCV not available - cannot check camera status")
        return
        
    try:
        cam = cv2.VideoCapture(0)
        if cam is not None and cam.isOpened():
            cam.release()
            messagebox.showinfo("Camera Status", "Webcam is ENABLED.")
        else:
            messagebox.showinfo("Camera Status", "Webcam is DISABLED.")
    except Exception as e:
        messagebox.showerror("Camera Status", f"Error checking webcam: {e}")

def change_password():
    def on_ok():
        new_pass = password_entry.get()
        if new_pass:
            global password
            password = new_pass
            with open(log_file, "a") as log:
                log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Password changed to: {new_pass}\n")
            messagebox.showinfo("Change Password", "Password changed successfully.")
            pw_window.destroy()
        else:
            error_label.config(text="Password cannot be empty.")

    def on_wrong_password():
        record_intruder_video()
        send_intrusion_alert_email_async(time.strftime('%Y-%m-%d %H:%M:%S'), "Incorrect Password for Change Password")

    pw_window = tk.Toplevel(root)
    pw_window.title("Change Password")
    pw_window.geometry("300x150")
    tk.Label(pw_window, text="Enter New Password:").pack(pady=10)
    password_entry = tk.Entry(pw_window, show="*")
    password_entry.pack(pady=5)
    tk.Button(pw_window, text="OK", command=on_ok).pack(pady=5)
    error_label = tk.Label(pw_window, text="", fg="red")
    error_label.pack()

def run_bat_with_password(bat_file, success_message, status_message=None):
    def on_ok():
        if password_entry.get() == password:
            subprocess.run([bat_file], text=True)
            password_window.destroy()
            success_label.config(text=success_message)
            if status_message is not None:
                status_label.config(text=status_message)
        else:
            error_label.config(text="Incorrect password. Try again.")
            password_entry.delete(0, tk.END)
            record_intruder_video()
            send_intrusion_alert_email_async(time.strftime('%Y-%m-%d %H:%M:%S'), f"Incorrect Password for {bat_file}")

    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x200")

    tk.Label(password_window, text="Enter Password:").pack()
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()

    tk.Button(password_window, text="OK", command=on_ok).pack()
    error_label = tk.Label(password_window, text="", fg="red")
    error_label.pack()

def disable_camera():
    run_bat_with_password("disable_cam.bat", "Camera Disabled Successfully", status_message="Camera was disabled")
    with open(log_file, "a") as log:
        log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Camera Disabled\n")

def enable_camera():
    run_bat_with_password("enable_cam.bat", "Camera Enabled Successfully", status_message="Camera was enabled")
    with open(log_file, "a") as log:
        log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Camera Enabled\n")

# --- SQL CONSOLE FOR DATABASE ---

def open_sql_console():
    def on_ok():
        if password_entry.get() == password:
            password_window.destroy()
            # Open SQL Console
            sql_win = tk.Toplevel(root)
            sql_win.title("SQLite Console")
            sql_win.geometry("600x400")
            tk.Label(sql_win, text="Enter SQL Query:", font=("Arial", 11, "bold")).pack(pady=5)
            query_entry = scrolledtext.ScrolledText(sql_win, height=5, width=70, font=("Consolas", 10))
            query_entry.pack(padx=10, pady=5)
            result_text = scrolledtext.ScrolledText(sql_win, height=15, width=70, font=("Consolas", 10))
            result_text.pack(padx=10, pady=5)
            result_text.config(state="disabled")

            def run_query():
                sql = query_entry.get("1.0", tk.END).strip()
                if not sql:
                    return
                try:
                    conn = sqlite3.connect('users.db')
                    c = conn.cursor()
                    c.execute(sql)
                    if sql.lower().startswith("select"):
                        rows = c.fetchall()
                        columns = [desc[0] for desc in c.description] if c.description else []
                        output = ''
                        if columns:
                            output += '\t'.join(columns) + '\n' + '-'*60 + '\n'
                        for row in rows:
                            output += '\t'.join(str(x) for x in row) + '\n'
                        if not rows:
                            output += '[No rows returned]'
                    else:
                        conn.commit()
                        output = '[Query executed successfully]'
                    conn.close()
                except Exception as e:
                    output = f'[Error] {e}'
                result_text.config(state="normal")
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, output)
                result_text.config(state="disabled")

            tk.Button(sql_win, text="Run Query", command=run_query, bg="red", fg="white", font=("Arial", 11, "bold")).pack(pady=5)
        else:
            error_label.config(text="Incorrect password. Try again.")
            password_entry.delete(0, tk.END)
            record_intruder_video()
            send_intrusion_alert_email_async(time.strftime('%Y-%m-%d %H:%M:%S'), "Incorrect Password for SQL Console")

    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x150")
    tk.Label(password_window, text="Enter Password:").pack(pady=10)
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack(pady=5)
    tk.Button(password_window, text="OK", command=on_ok).pack(pady=5)
    error_label = tk.Label(password_window, text="", fg="red")
    error_label.pack()

# --- GUI SETUP ---


root = tk.Tk()
root.title("Web Cam Security")
# Increase window size for more space
root.geometry("500x650")
root.configure(bg="black")

# Success Label
success_label = tk.Label(root, text="", fg="lime", bg="black", font=("Arial", 10))
success_label.pack()

import threading

def send_password_email_async(password):
    threading.Thread(target=send_password_email, args=(password,), daemon=True).start()

def show_password_messagebox():
    messagebox.showinfo("Generated Password", f"Your generated password is:\n\n{password}")

# Show generated password in a popup after main window appears
root.after(100, show_password_messagebox)

# Send generated password via email automatically in background thread
send_password_email_async(password)

# Variable to track email sent status
email_sent_status = tk.StringVar(root)
email_sent_status.set("Email not sent successfully")

# Project Info Button
tk.Button(root, text="Project Info", bg="red", fg="white", command=show_info, font=("Arial", 12, "bold")).pack(pady=10)

# Title Label
tk.Label(root, text="WebCam Spyware Security", fg="white", bg="black", font=("Arial", 16)).pack(pady=10)

# Show camera logo below heading using file path
try:
    if PIL_AVAILABLE:
        pil_img = Image.open(r"E:\camera logo.png")
        # Resize once and cache
        pil_img.thumbnail((64, 64), Image.LANCZOS)
        camera_img = ImageTk.PhotoImage(pil_img)
        logo_label = tk.Label(root, image=camera_img, bg="black")
        logo_label.image = camera_img  # Keep reference to avoid garbage collection
        logo_label.pack(pady=10)
    else:
        tk.Label(root, text="🎥 WEBCAM SECURITY 🎥", bg="black", fg="white", font=("Arial", 14)).pack(pady=10)
except Exception as e:
    tk.Label(root, text="[Camera Image Not Found]", bg="black", fg="red").pack()

# Action Buttons Row

row = tk.Frame(root, bg="black")
tk.Button(row, text="View Logs", bg="red", fg="white", width=15, command=view_logs).pack(side="left", padx=10)
tk.Button(row, text="Check Status", bg="red", fg="white", width=15, command=check_status).pack(side="left", padx=10)
row.pack(pady=10)


# Change Password
tk.Button(root, text="Change Password", bg="red", fg="white", width=34, command=change_password).pack(pady=10)

# Open SQL Console Button
tk.Button(root, text="Open SQL Console", bg="red", fg="white", width=34, command=open_sql_console).pack(pady=5)

# Disable / Enable Block


control_frame = tk.Frame(root, bg="gray")
# Camera status label (white box) inside control_frame
status_label = tk.Label(control_frame, text="", fg="black", bg="white", font=("Arial", 12), width=34, height=4, relief="groove")
status_label.pack(pady=10)


# --- Enable/Disable Button Functions ---
def button1_clicked():
    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x200")

    password_label = tk.Label(password_window, text="Enter Password:")
    password_label.pack()

    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()

    error_label = tk.Label(password_window, text="", font=("Arial", 12), bg="#f2f2f2", fg="#ff0000")
    error_label.pack()

    def ok_button():
        if password_entry.get() == password:
            import subprocess
            # Run registry commands directly to disable camera (for UWP apps)
            subprocess.Popen([
                'reg', 'delete', r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam', '/v', 'Value', '/f'
            ], shell=True)
            subprocess.Popen([
                'reg', 'add', r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam', '/v', 'Value', '/t', 'REG_DWORD', '/d', '0', '/f'
            ], shell=True)
            # --- Hardware-level disable using PowerShell ---
            # This disables all imaging devices (webcams) via Device Manager
            ps_script = (
                'Get-PnpDevice -Class Camera | Where-Object { $_.Status -eq "OK" } | ForEach-Object { Disable-PnpDevice -InstanceId $_.InstanceId -Confirm:$false }'
            )
            subprocess.Popen([
                'powershell', '-Command', ps_script
            ], shell=True)
            password_window.destroy()
            success_label.config(text="Camera Disabled Successfully")
            status_label.config(text="Camera was disabled")
            with open(log_file, "a") as log:
                log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Camera Disabled\n")
        else:
            error_label.config(text="Incorrect password. Please try again.")
            password_entry.delete(0, tk.END)
            record_intruder_video()
            send_intrusion_alert_email_async(time.strftime('%Y-%m-%d %H:%M:%S'), "Incorrect Password for Disable Camera")

    ok_btn = tk.Button(password_window, text="OK", command=ok_button)
    ok_btn.pack()

def button2_clicked():
    # --- Fix indentation so OK button is always created ---
    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x200")

    password_label = tk.Label(password_window, text="Enter Password:")
    password_label.pack()

    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()

    error_label = tk.Label(password_window, text="", font=("Arial", 12), bg="#f2f2f2", fg="#ff0000")
    error_label.pack()

    def ok_button():
        if password_entry.get() == password:
            import subprocess
            # Run registry command directly to enable camera (for UWP apps)
            subprocess.Popen([
                'reg', 'delete', r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam', '/v', 'Value', '/f'
            ], shell=True)
            # --- Hardware-level enable using PowerShell ---
            # This enables all imaging devices (webcams) via Device Manager
            ps_script = (
                'Get-PnpDevice -Class Camera | Where-Object { $_.Status -eq "Disabled" } | ForEach-Object { Enable-PnpDevice -InstanceId $_.InstanceId -Confirm:$false }'
            )
            proc = subprocess.Popen([
                'powershell', '-Command', ps_script
            ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            if proc.returncode == 0 and b"Access is denied" not in stderr and b"Generic failure" not in stderr:
                # Try to rescan devices to force Windows to refresh hardware state
                subprocess.Popen(['powershell', '-Command', 'Get-PnpDevice -Class Camera | ForEach-Object { $_ | Enable-PnpDevice -Confirm:$false }'], shell=True)
                messagebox.showinfo("Enable Camera", "Camera enabled. If it does not work, please reboot or enable manually in Device Manager.")
            else:
                messagebox.showerror("Enable Camera Failed", "Camera could not be enabled automatically due to access denied. Please run the application as administrator or enable the camera manually in Device Manager.")
            password_window.destroy()
            success_label.config(text="Camera Enabled Successfully")
            status_label.config(text="Camera was enabled")
            with open(log_file, "a") as log:
                log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Camera Enabled\n")
        else:
            error_label.config(text="Incorrect password. Please try again.")
            password_entry.delete(0, tk.END)
            record_intruder_video()
            send_intrusion_alert_email_async(time.strftime('%Y-%m-%d %H:%M:%S'), "Incorrect Password for Enable Camera")

    ok_btn = tk.Button(password_window, text="OK", command=ok_button)
    ok_btn.pack()
# --- INTRUDER VIDEO RECORDING ---
def record_intruder_video(duration=10, output_file="intruder.avi"):
    if not CV2_AVAILABLE:
        print("[Intruder] OpenCV not available - cannot record video")
        return
        
    try:
        # Ensure directory exists
        video_dir = os.path.join(os.getcwd(), 'intruder_videos')
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        output_file = os.path.join(video_dir, f'intruder_{timestamp}.avi')
        
        # Try DirectShow first (Windows), then MSMF, then default
        backends_to_try = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
        cap = None
        
        for backend in backends_to_try:
            try:
                cap = cv2.VideoCapture(0, backend)
                if cap.isOpened():
                    print(f"[Intruder] Using backend: {backend}")
                    break
                else:
                    cap.release()
                    cap = None
            except Exception as e:
                print(f"[Intruder] Backend {backend} failed: {e}")
                if cap:
                    cap.release()
                    cap = None
        
        if cap is None or not cap.isOpened():
            print("[Intruder] Could not open webcam for recording.")
            try:
                from tkinter import messagebox
                messagebox.showwarning("Intruder Video", "Camera is disabled or unavailable, so intruder video could not be recorded.")
            except Exception:
                pass
            return
        
        # Set camera properties to very low resolution for maximum speed
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        cap.set(cv2.CAP_PROP_FPS, 3)
        
        # Wait for camera to stabilize
        time.sleep(0.5)
        
        # Get actual frame size from camera
        ret, test_frame = cap.read()
        if not ret:
            print("[Intruder] Could not read test frame from camera")
            cap.release()
            return
            
        frame_height, frame_width = test_frame.shape[:2]
        print(f"[Intruder] Camera resolution: {frame_width}x{frame_height}")
        
        # Use MJPG codec for fastest compression and smallest files
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        final_output_file = os.path.splitext(output_file)[0] + '.avi'
        
        # Very low frame rate (3 FPS) for ultra-fast loading
        out = cv2.VideoWriter(final_output_file, fourcc, 3.0, (160, 120))
        
        if not out.isOpened():
            print("[Intruder] Could not initialize video writer")
            cap.release()
            return
        
        print(f"[Intruder] Starting {duration} second recording...")
        start_time = time.time()
        frame_count = 0
        
        # Write the test frame first (resize to target size)
        test_frame_resized = cv2.resize(test_frame, (160, 120))
        out.write(test_frame_resized)
        frame_count += 1
        
        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret:
                print(f"[Intruder] Failed to read frame at {time.time() - start_time:.1f}s")
                break
            
            # Resize to very small resolution for ultra-fast processing
            frame = cv2.resize(frame, (160, 120))
            out.write(frame)
            frame_count += 1
            
            # Longer delay for ultra-low frame rate (~3 FPS)
            time.sleep(0.3)  # 300ms delay for 3-4 FPS
        
        cap.release()
        out.release()
        
        actual_duration = time.time() - start_time
        print(f"[Intruder] Video recorded: {frame_count} frames in {actual_duration:.1f}s to {final_output_file}")
        
        # Log the video file and time
        with open('intruder_video_log.txt', 'a') as vlog:
            vlog.write(f"{final_output_file}\t{timestamp}\t{frame_count} frames\t{actual_duration:.1f}s\n")
            
    except Exception as e:
        print(f"[Intruder] Error recording video: {e}")
        try:
            if 'cap' in locals() and cap:
                cap.release()
            if 'out' in locals() and out:
                out.release()
        except:
            pass
# --- VIEW INTRUDER VIDEO FUNCTION ---
def view_intruder_video():
    video_dir = os.path.join(os.getcwd(), 'intruder_videos')
    if not os.path.exists(video_dir):
        messagebox.showinfo("No Intruder Video", "No intruder video has been recorded yet.")
        return
    
    # Look for all video file types (include MJPG .avi files)
    video_patterns = ['intruder_*.avi', 'intruder_*.mp4', 'intruder_*.mov']
    video_files = []
    for pattern in video_patterns:
        video_files.extend(glob.glob(os.path.join(video_dir, pattern)))
    
    video_files = sorted(video_files)
    if not video_files:
        messagebox.showinfo("No Intruder Video", "No intruder video has been recorded yet.")
        return
    latest_video = video_files[-1]
    # Get timestamp from filename (remove extension dynamically)
    try:
        filename = os.path.basename(latest_video)
        timestamp = filename[9:].rsplit('.', 1)[0].replace('_', ' ')
    except Exception:
        timestamp = "Unknown"
    # Show info and play video
    info = f"Latest Intruder Video Recorded At:\n{timestamp}\n\nFile: {os.path.basename(latest_video)}"
    if messagebox.askyesno("View Intruder Video", info + "\n\nDo you want to play this video?"):
        try:
            # Open with default video player
            os.startfile(latest_video)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open video: {e}")


# --- DATABASE CONNECTION AND USER TABLE ---
def init_user_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, user, email FROM users')
    users = c.fetchall()
    conn.close()
    return users

def add_user(user, password, email, details=None):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (user, password, email, details) VALUES (?, ?, ?, ?)', (user, password, email, details))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore if user already exists
    conn.close()

# Remove old users.db if it exists to avoid schema mismatch (with retry on PermissionError)
def safe_remove_db(db_path, retries=5, delay=0.5):
    for _ in range(retries):
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
            break
        except PermissionError:
            time.sleep(delay)
    else:
        print(f"Warning: Could not remove {db_path} after {retries} retries. Please close any programs using it.")


# Remove old users.db if it exists to avoid schema mismatch (with retry on PermissionError)
safe_remove_db('users.db')
# Initialize the user database on startup
init_user_db()
# Add only Arjun user
add_user('arjun', 'arjunpass', 'arjunpamudurthi@gmail.com', 'Project developer')


# Add Enable/Disable Camera buttons and View Intruder Video button to the output page (after function definitions)
tk.Button(control_frame, text="Disable Camera", bg="red", fg="white", font=("Arial", 12), width=20, command=button1_clicked).pack(pady=10)
tk.Button(control_frame, text="Enable Camera", bg="red", fg="white", font=("Arial", 12), width=20, command=button2_clicked).pack(pady=10)
tk.Button(control_frame, text="View Intruder Video", bg="red", fg="white", font=("Arial", 12), width=20, command=view_intruder_video).pack(pady=10)

control_frame.pack(pady=30)

# Start the GUI main loop
root.mainloop()
