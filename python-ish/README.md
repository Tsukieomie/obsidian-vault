# 🐍 Python Setup for iSH

Complete Python development environment for iSH (iOS Linux Shell).

## 📋 What's Included

- **Setup Script**: Automated Python installation for iSH
- **Example Scripts**: Ready-to-run Python examples
- **Launcher**: Interactive menu for running scripts
- **Package Manager**: Pre-configured requirements.txt

## 🚀 Quick Start

### 1. Install Python on iSH

First, make sure you have iSH installed on your iOS device, then run:

```bash
cd python-ish
./setup-ish.sh
```

This will:
- Install Python 3 and pip
- Install development tools
- Install useful Python packages
- Set up your environment

### 2. Run the Launcher

```bash
./run.py
```

Or:

```bash
python3 run.py
```

This opens an interactive menu where you can:
- Run example scripts
- Execute custom Python code
- Open Python REPL
- View Python info

## 📚 Example Scripts

### 1. Hello World (`hello.py`)
Simple introduction to Python on iSH
```bash
python3 examples/hello.py
```

### 2. File Operations (`file_operations.py`)
Learn to read, write, and manipulate files
```bash
python3 examples/file_operations.py
```

### 3. Web Fetching (`web_fetch.py`)
Make HTTP requests and download files
```bash
python3 examples/web_fetch.py
```

### 4. Data Analysis (`data_analysis.py`)
Basic data manipulation and analysis
```bash
python3 examples/data_analysis.py
```

## 🔧 Manual Installation

If the automated setup doesn't work, install manually:

```bash
# Update package index
apk update

# Install Python
apk add python3 py3-pip

# Install build tools
apk add python3-dev build-base

# Install packages
pip3 install -r requirements.txt
```

## 📦 Installed Packages

The `requirements.txt` includes:

- **requests** - HTTP library
- **numpy** - Numerical computing
- **pandas** - Data analysis
- **matplotlib** - Plotting
- **beautifulsoup4** - Web scraping
- **click** - CLI tools
- **rich** - Rich terminal output
- **Pillow** - Image processing
- **openpyxl** - Excel files

## 💻 Running Python Code

### Method 1: Run Scripts Directly
```bash
python3 script.py
```

### Method 2: Use the Launcher
```bash
./run.py
```
Then select a script from the menu

### Method 3: Python REPL
```bash
python3
```

### Method 4: Run One-Liners
```bash
python3 -c "print('Hello from iSH!')"
```

## 📝 Creating Your Own Scripts

1. Create a new Python file:
```bash
nano my_script.py
```

2. Add the shebang line at the top:
```python
#!/usr/bin/env python3
```

3. Make it executable:
```bash
chmod +x my_script.py
```

4. Run it:
```bash
./my_script.py
```

## 🛠️ Troubleshooting

### Python command not found
Try using `python3` instead of `python`:
```bash
python3 script.py
```

### Permission denied
Make the script executable:
```bash
chmod +x script.py
```

### Package installation fails
Update pip first:
```bash
pip3 install --upgrade pip
```

### Not enough space
iSH has limited storage. Remove unnecessary packages:
```bash
apk del <package-name>
```

## 📱 iSH-Specific Notes

- **Storage**: iSH has limited storage (~2GB). Be mindful of package sizes.
- **Performance**: iSH emulates x86 on ARM, so some operations are slower.
- **Packages**: Not all Python packages work on Alpine Linux. Stick to pure Python packages when possible.
- **Persistence**: Data persists between iSH sessions, but the app can be terminated by iOS.

## 🌟 Tips for iSH

1. **Save often**: iOS can kill iSH at any time
2. **Use lightweight packages**: Avoid heavy dependencies
3. **Test incrementally**: Run code frequently to catch errors early
4. **Use virtual environments**: Keep projects isolated
5. **Backup important code**: Sync to cloud storage

## 🔗 Useful Commands

```bash
# Check Python version
python3 --version

# List installed packages
pip3 list

# Install a new package
pip3 install package-name

# Upgrade a package
pip3 install --upgrade package-name

# Uninstall a package
pip3 uninstall package-name

# Search for packages
pip3 search package-name

# Show package info
pip3 show package-name
```

## 📖 Learning Resources

- [Python Official Docs](https://docs.python.org/3/)
- [iSH GitHub](https://github.com/ish-app/ish)
- [Python Package Index](https://pypi.org/)

## 🎯 Next Steps

1. Explore the example scripts
2. Modify them to learn
3. Create your own scripts
4. Install additional packages as needed
5. Build your own projects!

## ⚠️ Known Limitations

- No GUI support (use CLI/TUI libraries instead)
- Limited multiprocessing support
- Some C-extension packages may not compile
- Network operations may be slower than native

## 🤝 Contributing

Feel free to add more examples or improve existing ones!

## 📄 License

Free to use and modify for your projects.

---

Happy coding on iSH! 🎉
