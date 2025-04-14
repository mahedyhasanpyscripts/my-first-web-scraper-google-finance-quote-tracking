import time
import win32gui
import win32process
import psutil
from collections import defaultdict
import matplotlib.pyplot as plt  


APPS = {
    "VS Code": ["code.exe"],
    "Google Chrome": ["chrome.exe"],
    "Microsoft Edge": ["msedge.exe"]
}

app_times = defaultdict(float)
app_tabs = defaultdict(set)

SMART_KEYWORDS = [
    "localhost", "127.0.0.1", ".test", ":8000", ":3000", ":5173",  
    "github", "gitlab", "stackoverflow", "postman", "swagger",    
    "vscode", "vs code", "sublime", "terminal",                    
    "api", "json", "js", "php", "react", "vue", "node", "express", 
    "code", "editor", "docker", "env", "sql", "db", "debug",       
]

def get_active_window_title_and_process():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        process_name = proc.name().lower()
        window_title = win32gui.GetWindowText(hwnd)
        return process_name, window_title
    except Exception as e:
        print(f"[ERROR] {e}")
        return "unknown.exe", ""

def find_app_name(proc_name):
    for app, keywords in APPS.items():
        if any(keyword == proc_name for keyword in keywords):
            return app
    return proc_name.capitalize()

def is_programming_related(app_name, window_title):
    full_text = f"{app_name} {window_title}".lower()
    return any(keyword in full_text for keyword in SMART_KEYWORDS)

def show_pie_chart(programming_percent, non_programming_percent):
    labels = ['Programming 🧠', 'Non-Programming 💤']
    sizes = [programming_percent, non_programming_percent]
    colors = ['#4CAF50', '#F44336']
    explode = (0.1, 0)  # explode programming slice

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("🕒 Time Distribution")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def run_tracker(duration=40):  # Track for 40 seconds
    print(f"Tracking activity for {duration} seconds...")
    interval = 1
    total_time = 0
    last_check = time.time()

    while total_time < duration:
        proc_name, window_title = get_active_window_title_and_process()
        app_name = find_app_name(proc_name)

        tab_key = app_name
        if app_name in ["Google Chrome", "Microsoft Edge"] and window_title:
            tab_key = f"{app_name} ({window_title})"
            app_tabs[app_name].add(window_title)

        current_time = time.time()
        elapsed = current_time - last_check
        app_times[tab_key] += elapsed

        total_time += elapsed
        last_check = current_time
        time.sleep(interval)

    print("\n🎯 Grouped Active Time Breakdown:\n")
    grouped = defaultdict(float)
    for app_tab, seconds in app_times.items():
        app_name = app_tab.split(" (")[0]
        grouped[app_name] += seconds

    for app, total in sorted(grouped.items(), key=lambda x: x[1], reverse=True):
        percent = (total / total_time) * 100
        print(f"✨ {app}: {percent:.2f}% ({total:.2f} seconds)")
        if app_tabs[app]:
            print("   - Tabs:")
            for tab in sorted(app_tabs[app]):
                print(f"     • {tab}")
        print()

    # Programming-related summary
    programming_time = 0
    for app_tab, seconds in app_times.items():
        app_name = app_tab.split(" (")[0]
        window_title = app_tab.split(" (")[1][:-1] if " (" in app_tab else ""
        if is_programming_related(app_name, window_title):
            programming_time += seconds

    non_programming_time = total_time - programming_time
    programming_percent = (programming_time / total_time) * 100
    non_programming_percent = 100 - programming_percent

    print("✔ Programming-Related Activity: {:.2f}%".format(programming_percent))
    print("💤 Non-Programming / Other Activity: {:.2f}%".format(non_programming_percent))

    # 🧁 Show pie chart
    show_pie_chart(programming_percent, non_programming_percent)

if __name__ == "__main__":
    run_tracker()
