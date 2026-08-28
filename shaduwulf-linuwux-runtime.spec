Name:           shaduwulf-linuwux-runtime
Version:        0.1.1
Release:        0
Summary:        Standalone Linux preload runtime library for Wine and Proton
License:        LGPL-2.1-or-later
Group:          System/Libraries
URL:            https://github.com/xshaduwulfx/shaduwulf-linuwux-runtime
Source0:        https://github.com/xshaduwulfx/shaduwulf-linuwux-runtime/releases/latest/download/liblinuwux_runtime.so

ExclusiveArch:  x86_64

%description
A preloadable runtime library (liblinuwux_runtime.so) providing CPUID spoofing,
syscall redirection, and time interposition for Wine and Proton environments.

%prep

%build

%install
install -d -m 0755 %{buildroot}%{_libdir}
install -m 0755 %{SOURCE0} %{buildroot}%{_libdir}/liblinuwux_runtime.so

%post
if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
    if [ -d "$USER_HOME" ]; then
        mkdir -p "$USER_HOME/.local/lib"
        cp --reflink=auto -f %{_libdir}/liblinuwux_runtime.so "$USER_HOME/.local/lib/liblinuwux_runtime.so"
        chown -h "$SUDO_USER:" "$USER_HOME/.local/lib/liblinuwux_runtime.so"
        chown -R "$SUDO_USER:$USER_GROUP" "$USER_HOME/.local/lib"
        chmod 0755 "$USER_HOME/.local/lib"
        chmod 0755 "$USER_HOME/.local/lib/liblinuwux_runtime.so"
    fi
fi

%postun
if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
    TARGET_LINK="$USER_HOME/.local/lib/liblinuwux_runtime.so"
    if [ -f "$TARGET_LINK" ] || [ -L "$TARGET_LINK" ]; then
        rm -f "$TARGET_LINK"
    fi
    rmdir --ignore-fail-on-non-empty "$USER_HOME/.local/lib" 2>/dev/null || true
fi

%files
%{_libdir}/liblinuwux_runtime.so
