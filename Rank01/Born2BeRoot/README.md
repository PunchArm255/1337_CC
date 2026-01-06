*This project has been created as part of the 42 curriculum by mnassiri.*

# Born2BeRoot

## Description
`Born2BeRoot` is a System Administration project that introduces the fundamentals of virtualization and server configuration. The goal is to create a secure, minimal server environment using Debian, strictly adhering to a set of security policies. Rocky is also an option, but I'm not autistic.

Unlike previous programming projects, this involves setting up a specific file system structure using **LVM** (Logical Volume Manager), configuring a firewall (**UFW**), implementing strong **password policies**, managing **sudo** privileges, and securing **SSH** access. The project also includes a custom **Bash script** to monitor server health and broadcast statistics to all connected terminals.

## Instructions

The project is submitted as a `signature.txt` file, which contains the SHA1 checksum of the virtual machine disk (`.vdi` or `.qcow2`).

* **Obtaining the signature:**
    ```bash
    shasum Born2BeRoot.vdi
    ```

### Usage

1.  **Start the VM** in VirtualBox (our Hypervisor).
2.  **Connect to the VM via SSH:**
    ```bash
    # Since I used a Bridged Adapter, you will connect using the host IP

    ssh mnassiri@hostIP -p 4242
    ```
3.  **Check the Monitoring Script:**
    The script broadcasts system info on server startup, then every 10 minutes after that:
    ```bash
    vim monitoring.sh
    ```

## Resources
These are the resources I used to get this project done:

### Documentation & Guides:
- **Born2BeRoot Guide by mzanana:** https://github.com/mzanana/Born2BeRoot/blob/main/README.md
- **Gitbook Guide by Laendrun:** https://42-cursus.gitbook.io/guide/1-rank-01/born2beroot

### Youtube Videos:
- **"Born2BeRoot part 1 : Installation and partitioning"** by MyCodeUrCode.
- **"Born2BeRoot part 2 : Installation and partitioning"** by MyCodeUrCode.

### AI Usage:
- **Google Gemini:** Used it for a mockup defense to simulate evaluation questions, debug the `monitoring.sh` script logic, and break down some complex concepts.

## Project Details & Choices

### Operating System Choice: Debian
For this project, **Debian** was chosen over Rocky.

* **Why Debian?**
    Debian is known for its extreme stability. It uses the `APT` package manager and `.deb` packages, which are widely documented and beginner-friendly.
* **Pros:** Highly stable, large community support, easy upgrades.
* **Cons:** Software packages can be older because stability is prioritized over new features.

### Comparisons

#### Debian vs. Rocky
* **Debian:** Community-driven project, focuses on stability for general servers and desktops.
* **Rocky:** A rebuild of RHEL (Red Hat Enterprise Linux). Focuses on more complex enterprise environments.

#### AppArmor vs. SELinux
* **AppArmor (Used in Debian):** It restricts programs based on file paths. It is generally considered easier to configure and learn for beginners.
* **SELinux (Used in Rocky):** It restricts programs based on labels/inodes. It is extremely complex and powerful but has a steeper learning curve and is harder to debug.

#### UFW vs. Firewalld
* **UFW (Used in Debian):** "Uncomplicated Firewall". It is an interface that's designed to be easy to use with simple commands like `ufw allow 4242`.
* **Firewalld (Used in Rocky):** A dynamic firewall manager with support for network/firewall "zones" (e.g., public, home, work). It is more complex but offers greater flexibility for changing network environments.

#### VirtualBox vs. UTM
* **VirtualBox:** A Type-2 Hypervisor for x86-64 architecture. It's been around for a while and is well known at this point. Used it because our iMacs are all x64.
* **UTM:** A virtualization tool for Macs (specifically those running Apple Silicon) that uses QEMU, also a Type-2 Hypervisor. While powerful for running other architectures on ARM, VirtualBox is still preferred in this case because all our computers are x64.