# LinUwUx Runtime for openSUSE/Fedora

Standalone Linux runtime for Wine & Proton.

<p align="center">
  <a href="#installation">Installation</a>
  ·
  <a href="#usage">Usage</a>
  ·
  <a href="#architecture">Architecture</a>
  ·
  <a href="#build">Build</a>
  ·
  <a href="#tests">Tests</a>
  ·
  <a href="#faq">FAQ</a>
</p>

---

## About

**LinUwUx Runtime** is a standalone runtime rework of the functionality provided by `LinUwUx.patch`.

Instead of applying LinUwUx modifications directly to Wine and Proton, this project provides the required behavior through a preloadable Linux shared library.

The goal is to decouple the LinUwUx runtime behavior from a particular Wine or Proton source tree and make it possible to use and develop the implementation independently.

> [!IMPORTANT]
> This project is experimental and under active development.

## Installation

LinUwUx Runtime is distributed as an RPM package across distinct repositories for **openSUSE** and **Fedora**.

### openSUSE

Add the OBS repository and install via `zypper`:

```sh
sudo zypper addrepo https://download.opensuse.org/repositories/home:ascendxpss/openSUSE_Tumbleweed/home:ascendxpss.repo

sudo zypper refresh

sudo zypper install shaduwulf-linuwux-runtime
```

### Fedora

Enable the COPR repository and install via `dnf`:

```sh
sudo dnf copr enable ascendxps/AscendXP

sudo dnf install shaduwulf-linuwux-runtime
```

The Fedora package is available from the [AscendXP COPR repository](https://copr.fedorainfracloud.org/coprs/ascendxps/AscendXP/).

The package installs the runtime library to:

```text
/usr/lib64/liblinuwux_runtime.so
```

After installation, configure your Wine, Proton, Steam, Heroic, or Lutris launch environment to preload the library.

For example:

```sh
LD_PRELOAD=/usr/lib64/liblinuwux_runtime.so COMMAND [ARG...]
```

If an existing `LD_PRELOAD` value needs to be preserved:

```sh
LD_PRELOAD="/usr/lib64/liblinuwux_runtime.so${LD_PRELOAD:+:$LD_PRELOAD}" \
COMMAND [ARG...]
```

## Usage

### Steam

Select Proton-CachyOS or Proton-GE as the game's compatibility tool.

Open **Properties → General → Launch Options** and add:

```text
LD_PRELOAD=/usr/lib64/liblinuwux_runtime.so %command%
```

### Faugus Launcher

Select Proton-CachyOS or Proton-GE as the game's runner.

1. Right-click the game.
2. Select **Edit**.
3. Find **Game Arguments**.
4. Add:

```text
LD_PRELOAD=/usr/lib64/liblinuwux_runtime.so
```

For runtime logging:

```text
LINUWUX_DEBUG=1 LD_PRELOAD=/usr/lib64/liblinuwux_runtime.so
```

### Heroic Games Launcher

Select Proton-GE or another compatible community Proton build.

1. Open the game's **Settings**.
2. Select **Advanced**.
3. Find **Environment Variables**.
4. Add:

```text
Name:  LD_PRELOAD
Value: /usr/lib64/liblinuwux_runtime.so
```

For runtime logging, add:

```text
Name:  LINUWUX_DEBUG
Value: 1
```

Do not put `LD_PRELOAD=...` in **Game Arguments**. Heroic provides a dedicated environment-variable configuration.

### Lutris

Open the game's configuration and go to:

**System options → Environment variables**

Add:

```text
Key:   LD_PRELOAD
Value: /usr/lib64/liblinuwux_runtime.so
```

For runtime logging:

```text
Key:   LINUWUX_DEBUG
Value: 1
```

### Command line

The runtime can be injected manually:

```sh
LD_PRELOAD="/usr/lib64/liblinuwux_runtime.so${LD_PRELOAD:+:$LD_PRELOAD}" \
COMMAND [ARG...]
```

### Debugging

Enable runtime logging with:

```sh
LINUWUX_DEBUG=1 \
LD_PRELOAD="/usr/lib64/liblinuwux_runtime.so${LD_PRELOAD:+:$LD_PRELOAD}" \
COMMAND [ARG...]
```

## FAQ

### How does the Hypervisor (HV) bypass work? What are the requirements?

**LinUwUx Runtime is a required part of the setup, but it is not the complete solution.**

This repository develops and distributes the standalone LinUwUx runtime required by the setup. The HV bypass itself, its configuration, additional requirements, and the overall setup are outside the scope of this project.

For information about the complete setup, requirements, compatibility, or troubleshooting, refer to the dedicated discussion and documentation for the wider LinUwUx project.

### Which Proton versions are supported?

The runtime primarily targets community Proton builds.

The main supported and tested environments are:

* Proton-CachyOS
* Proton-GE

Compatibility with other Wine or Proton builds may vary.

Valve's official Proton builds are currently outside the supported target and should not be assumed to work with the runtime.

### Does it require a custom Proton build?

No.

One of the main purposes of the runtime architecture is to provide LinUwUx behavior without requiring the LinUwUx modifications to be compiled directly into Wine or Proton.

A compatible Wine or Proton environment is still required to run Windows software.

### Does it patch or replace Wine or Proton?

No.

The runtime is loaded into the Linux-side process environment through `LD_PRELOAD`.

It does not replace Wine or Proton binaries and does not require a patched Wine or Proton source tree.

### Is this the same as LinUwUx.patch?

No, although it implements the same LinUwUx protocol and is a rework of the behavior introduced by `LinUwUx.patch`.

The original patch implements LinUwUx through modifications to Wine and Proton. LinUwUx Runtime instead restructures the relevant behavior into a standalone shared library.

### Why use a standalone runtime?

Keeping LinUwUx behavior outside Wine and Proton reduces its coupling to a particular Wine or Proton source tree.

The implementation is divided into focused components with separate responsibilities, including:

* CPUID interception and protocol handling
* syscall redirection
* Syscall User Dispatch integration
* KUSER_SHARED_DATA handling
* faketime handling
* Wine prefix registry handling
* signal handling
* `prctl` interposition
* time-function interposition

### Which architectures are supported?

Currently, x86-64 Linux is supported.

Some runtime mechanisms are architecture-specific, including the `prctl` interposer entry point, CPUID handling, and CPU-context manipulation.

### Is it production-ready?

Not yet.

The project is experimental and under active development.

The core LinUwUx mechanisms are implemented and have focused tests, but broader testing across games, Proton versions, and runtime environments is still required.

## Current implementation

The runtime currently implements core mechanisms required by the LinUwUx protocol, including:

* CPUID interception and LinUwUx command handling
* CPU vendor spoofing
* `TargetSysHandler` registration
* syscall redirection
* Syscall User Dispatch integration
* LinUwUx syscall trampoline ABI handling
* XMM4 syscall-number forwarding
* XMM5 one-shot syscall bypass handling
* KUSER_SHARED_DATA setup and patching
* faketime handling and shared faketime state
* Wine prefix `HwProfileGuid` handling
* Proton-related environment setup
* signal-handler interposition
* `prctl` interposition
* `clock_gettime` and `gettimeofday` interposition

The current implementation targets x86-64 Linux.

## Architecture

The runtime is built as:

```text
liblinuwux_runtime.so
```

It is loaded into the target process through `LD_PRELOAD`.

The implementation is split into focused runtime modules:

```text
src/
├── runtime.c       runtime initialization and common infrastructure
├── signals.c       signal interposition and dispatch
├── cpuid.c         CPUID faulting, spoofing, and LinUwUx command handling
├── syscall.c       syscall redirection and trampoline ABI handling
├── sud.c           Syscall User Dispatch state and selector handling
├── prctl.c         prctl interposition and SUD integration
├── prctl_entry.S   x86-64 prctl interposition entry point
├── kuser.c         KUSER_SHARED_DATA setup and patching
├── time.c          faketime state and time-function interposition
└── registry.c      Wine-prefix hardware-profile registry handling
```

The shared library is built with hidden ELF visibility by default. Only interfaces that must interpose host functions are exported.

The currently exported interposers are:

```text
clock_gettime
gettimeofday
prctl
sigaction
```

## Build

Build the runtime with:

```sh
make
```

Clean the build with:

```sh
make clean
```

The resulting shared library is created in the repository root:

```text
liblinuwux_runtime.so
```

## Tests

Focused runtime tests are currently provided for:

* faketime CPUID behavior
* repeated faketime state updates
* syscall trampoline resume semantics
* XMM4 syscall-number forwarding
* XMM5 one-shot bypass semantics

Some test binaries must be executed from a filesystem that permits execution.

## Credits

The original LinUwUx work and `LinUwUx.patch` were created by **LinUwUx**.

Special thanks to **LinUwUx** for the original work and for giving this standalone rework the green light.

For provenance and licensing details, see `NOTICE.md`.

## License

LinUwUx Runtime is distributed under the GNU Lesser General Public License version 2.1 or later.

See `LICENSE` for the complete license text.
