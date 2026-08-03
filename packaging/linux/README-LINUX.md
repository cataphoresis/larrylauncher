# LarryLauncher for Linux

This archive contains the Linux LarryLauncher and a bundled LarryBootstrap runtime.

## Requirements

- Debian 13, amd64
- an ordinary user with working `sudo` access
- internet access for installation operations

## Verify and start

```bash
sha256sum --check LarryLauncher-Linux-v0.2.0.tar.gz.sha256
tar -xzf LarryLauncher-Linux-v0.2.0.tar.gz
cd LarryLauncher-Linux-v0.2.0
./larry-launcher --action audit
```

Run `./larry-launcher` for the interactive menu. The interactive install action asks for confirmation; explicit `--action install` begins immediately.
