import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog

def create_subvolume():
    subvolume_path = subvolume_entry.get()
    subprocess.run(['btrfs', 'subvolume', 'create', subvolume_path])
    messagebox.showinfo("Success", "Subvolume created!")
    refresh_subvolumes()

def create_snapshot():
    source_path = source_entry.get()
    snapshot_path = snapshot_entry.get()
    subprocess.run(['btrfs', 'subvolume', 'snapshot', source_path, snapshot_path])
    messagebox.showinfo("Success", "Snapshot created!")
    refresh_snapshots()

def delete_subvolume():
    subvolume_path = subvolume_entry.get()
    subprocess.run(['btrfs', 'subvolume', 'delete', subvolume_path])
    messagebox.showinfo("Success", "Subvolume deleted!")
    refresh_subvolumes()

def delete_snapshot():
    snapshot_path = snapshot_entry.get()
    subprocess.run(['btrfs', 'subvolume', 'delete', snapshot_path])
    messagebox.showinfo("Success", "Snapshot deleted!")
    refresh_snapshots()

def show_disk_usage():
    mount_path = mount_entry.get()
    result = subprocess.run(['btrfs', 'filesystem', 'df', mount_path], capture_output=True, text=True)
    messagebox.showinfo("Disk Usage", result.stdout)

def browse_directory(entry):
    directory_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(tk.END, directory_path)

def refresh_subvolumes():
    subvolume_listbox.delete(0, tk.END)
    mount_path = mount_entry.get()
    result = subprocess.run(['btrfs', 'subvolume', 'list', '-a', mount_path], capture_output=True, text=True)
    subvolumes = result.stdout.strip().split('\n')
    for subvolume in subvolumes:
        subvolume_listbox.insert(tk.END, subvolume)

def refresh_snapshots():
    snapshot_listbox.delete(0, tk.END)
    mount_path = mount_entry.get()
    result = subprocess.run(['btrfs', 'subvolume', 'list', '-s', mount_path], capture_output=True, text=True)
    snapshots = result.stdout.strip().split('\n')
    for snapshot in snapshots:
        snapshot_listbox.insert(tk.END, snapshot)

# Create the GUI window
window = tk.Tk()
window.title("Btrfs Manager")

# Mount Path
mount_label = tk.Label(window, text="Mount Path:")
mount_label.pack()
mount_entry = tk.Entry(window)
mount_entry.pack()

# Subvolume Management
subvolume_frame = tk.Frame(window)
subvolume_frame.pack(pady=10)
subvolume_label = tk.Label(subvolume_frame, text="Subvolume Path:")
subvolume_label.grid(row=0, column=0)
subvolume_entry = tk.Entry(subvolume_frame)
subvolume_entry.grid(row=0, column=1)
subvolume_create_button = tk.Button(subvolume_frame, text="Create Subvolume", command=create_subvolume)
subvolume_create_button.grid(row=0, column=2, padx=10)
subvolume_browse_button = tk.Button(subvolume_frame, text="Browse", command=lambda: browse_directory(subvolume_entry))
subvolume_browse_button.grid(row=0, column=3)
subvolume_listbox = tk.Listbox(subvolume_frame, width=80)
subvolume_listbox.grid(row=1, columnspan=4, pady=10)
subvolume_refresh_button = tk.Button(subvolume_frame, text="Refresh", command=refresh_subvolumes)
subvolume_refresh_button.grid(row=2, columnspan=4)

# Snapshot Management
snapshot_frame = tk.Frame(window)
snapshot_frame.pack(pady=10)
snapshot_label = tk.Label(snapshot_frame, text="Source Path:")
snapshot_label.grid(row=0, column=0)
snapshot_entry = tk.Entry(snapshot_frame)
snapshot_entry.grid(row=0, column=1)
snapshot_create_button = tk.Button(snapshot_frame, text="Create Snapshot", command=create_snapshot)
snapshot_create_button.grid(row=0, column=2, padx=10)
snapshot_browse_button = tk.Button(snapshot_frame, text="Browse", command=lambda: browse_directory(snapshot_entry))
snapshot_browse_button.grid(row=0, column=3)
snapshot_listbox = tk.Listbox(snapshot_frame, width=80)
snapshot_listbox.grid(row=1, columnspan=4, pady=10)
snapshot_refresh_button = tk.Button(snapshot_frame, text="Refresh", command=refresh_snapshots)
snapshot_refresh_button.grid(row=2, columnspan=4)

# Delete Subvolume
delete_subvolume_frame = tk.Frame(window)
delete_subvolume_frame.pack(pady=10)
delete_subvolume_label = tk.Label(delete_subvolume_frame, text="Subvolume Path:")
delete_subvolume_label.grid(row=0, column=0)
delete_subvolume_entry = tk.Entry(delete_subvolume_frame)
delete_subvolume_entry.grid(row=0, column=1)
delete_subvolume_button = tk.Button(delete_subvolume_frame, text="Delete Subvolume", command=delete_subvolume)
delete_subvolume_button.grid(row=0, column=2, padx=10)

# Delete Snapshot
delete_snapshot_frame = tk.Frame(window)
delete_snapshot_frame.pack(pady=10)
delete_snapshot_label = tk.Label(delete_snapshot_frame, text="Snapshot Path:")
delete_snapshot_label.grid(row=0, column=0)
delete_snapshot_entry = tk.Entry(delete_snapshot_frame)
delete_snapshot_entry.grid(row=0, column=1)
delete_snapshot_button = tk.Button(delete_snapshot_frame, text="Delete Snapshot", command=delete_snapshot)
delete_snapshot_button.grid(row=0, column=2, padx=10)

# Disk Usage
disk_usage_frame = tk.Frame(window)
disk_usage_frame.pack(pady=10)
disk_usage_label = tk.Label(disk_usage_frame, text="Mount Path:")
disk_usage_label.grid(row=0, column=0)
disk_usage_entry = tk.Entry(disk_usage_frame)
disk_usage_entry.grid(row=0, column=1)
disk_usage_browse_button = tk.Button(disk_usage_frame, text="Browse", command=lambda: browse_directory(disk_usage_entry))
disk_usage_browse_button.grid(row=0, column=2)
show_disk_usage_button = tk.Button(disk_usage_frame, text="Show Disk Usage", command=show_disk_usage)
show_disk_usage_button.grid(row=0, column=3)

# Run the GUI event loop
window.mainloop()
