import os

def get_size(path="."):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_size(entry.path)
    return total


def get_human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def analyze_disk_usage(path="."):
    size = get_size(path)
    readable_size = get_human_readable_size(size)
    return f"Total disk usage for {path}: {readable_size}"

if __name__ == "__main__":
    path = input("Enter the path to analyze (default is current directory): ")
    if not path:
        path = "."
    print(analyze_disk_usage(path))
