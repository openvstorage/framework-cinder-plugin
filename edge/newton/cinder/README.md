# CINDER

## Description

The custom CINDER driver provides the ability to manage volumes through Open Stack.

**IMPORTANT:** These files must be patched on machines where `cinder-volume` is installed. Preferably under their own directories.

## Driver

The CINDER driver can be found under `volume/drivers` and should be installed under its respective directory.
After installing the driver, you should restart `cinder-volume`.
