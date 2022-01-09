# Service sample

A simple setup script for creating a Windows service.
See the comments in the Config.py and ServiceHandler.py files for more
information on how to set this up.

Installing the service is done with the option --install <Name> and
uninstalling the service is done with the option --uninstall <Name>. The
value for <Name> is intended to differentiate between different invocations
of the same service code -- for example for accessing different databases or
using different configuration files.


# Installation and requirements:

In a virtual environment, install by issuing the commands:

```
pip install --upgrade cx_Freeze cx_Logging
pip install --upgrade fastapi
pip install --upgrade uvicorn
pip install --upgrade configparser
```

cx_Logging 3.0 has support for Python 3.6 up to 3.9.

# Build the executable:

```
python build.py build
```

# Run the sample

Run in a command prompt or powershell with admin priviliges.

```
D:\repositories\APIService\build\exe.win-amd64-3.8\APIWindowsService --install APIService
D:\repositories\APIService\build\exe.win-amd64-3.8\APIWindowsService --uninstall APIService
```

Bash command to delete windows service:

```
SC DELETE APIService
```