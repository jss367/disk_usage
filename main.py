import os

# Exclusions based more on common unnecessary directory patterns
EXCLUDED_DIRECTORIES = {
    "/Library/Containers/",
    "/Library/Caches/",
    "/Library/Logs/",
    "/private/var/",
    "/System/",
    "/usr/",
    "/sbin/",
    "/bin/",
    "/etc/",
    "/Applications/",
}


def get_size(path=".", max_depth=5, depth=0):
    if depth > max_depth:
        # print(f"Reached maximum scan depth at {path}")
        return 0

    total = 0
    if any(excluded in path for excluded in EXCLUDED_DIRECTORIES):
        # print(f"Excluded directory {path}")
        return total

    if not os.access(path, os.R_OK | os.X_OK):
        print(f"Skipping directory {path} due to insufficient permissions")
        return total

    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    try:
                        total += entry.stat().st_size
                    except PermissionError:
                        print(f"Skipping file {entry.path} due to insufficient permissions")
                elif entry.is_dir():
                    # Decide whether to go deeper based on the directory type
                    new_path = entry.path
                    new_max_depth = max_depth if "Documents" in new_path or "Users" in new_path else max_depth - 1
                    if os.access(new_path, os.R_OK | os.X_OK):
                        total += get_size(new_path, new_max_depth, depth + 1)
                    else:
                        print(f"Skipping directory {new_path} due to insufficient permissions")
    except Exception as e:
        print(f"Error accessing {path}: {str(e)}")
    return total


def get_human_readable_size(size, decimal_places=2):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def analyze_disk_usage(path=".", max_depth=5):
    size = get_size(path, max_depth)
    readable_size = get_human_readable_size(size)
    return f"Total disk usage for {path}: {readable_size}"


if __name__ == "__main__":
    path = input("Enter the path to analyze (default is current directory): ")
    if not path:
        path = "."
    max_depth = input("Enter the maximum directory depth to scan (default is 5): ")
    max_depth = int(max_depth) if max_depth.isdigit() else 5
    print(analyze_disk_usage(path, max_depth))
