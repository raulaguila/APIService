# API Rest as a windows service

Sample of API rest as a windows service in python with cx_Freeze.
In this development, i used python v3.8.5

# Installation and requirements:

In a virtual environment, install the packages by issuing the command:

```
pip install --upgrade -r requirements.txt
```

cx_Logging 3.0 has support for Python 3.6 up to 3.9.

# Build the executable:

```
python build.py build
```

# Run the service

Run in a command prompt or powershell with admin priviliges.

To install: (need admin priviliges)

```
build\exe.win-amd64-3.8\APIWindowsService --install APIService
```

To access the API, access in your browse this address: http://127.0.0.1:5050/docs

To uninstall: (need admin priviliges)

```
build\exe.win-amd64-3.8\APIWindowsService --uninstall APIService
```

Bash command to stop a windows service with status "stopping": (need admin priviliges)

```
sc queryex [service name]
taskkill /F /PID [PID of service]
```

Bash command to delete windows service: (need admin priviliges)

```
sc delete [service name]
```