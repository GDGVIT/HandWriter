### Fedora
To manage HandWriter with Fedora's (or CentOS') package manager -
```bash
sudo rpm -v --import https://fbs.sh/SaurusXI/HandWriter/public-key.gpg
sudo dnf config-manager --add-repo https://fbs.sh/SaurusXI/HandWriter/rpm/HandWriter.repo
sudo dnf install handwriter
```
(On CentOS, replace 'dnf' by 'yum' and 'dnf config-manager' by 'yum-config-manager'.)
If HandWriter is already installed, you can force an immediate update via:
```bash
sudo dnf upgrade handwriter --refresh
```
This is for Fedora. For CentOS, use:
```bash
sudo yum clean all && sudo yum upgrade handwriter
```
Finally, you can also install without automatic updates by downloading:
https://fbs.sh/SaurusXI/HandWriter/HandWriter.rpm

### Arch  
To manage HandWriter with pacman -
```bash
curl -O https://fbs.sh/SaurusXI/HandWriter/public-key.gpg && sudo pacman-key --add public-key.gpg && sudo pacman-key --lsign-key 29D5FDA07C763B56745B9E598AC59FA1ADE43023 && rm public-key.gpg
echo -e '\n[HandWriter]\nServer = https://fbs.sh/SaurusXI/HandWriter/arch' | sudo tee -a /etc/pacman.conf
sudo pacman -Syu handwriter
```
If HandWriter is already installed, you can force an immediate update via:
```bash
sudo pacman -Syu --needed handwriter
```
Finally, you can also install without automatic updates by downloading:
https://fbs.sh/SaurusXI/HandWriter/HandWriter.pkg.tar.xz

### Debian and its derivatives (Ubuntu etc.)
To manage HandWriter with your package manager -
```bash
sudo apt-get install apt-transport-https
wget -qO - https://fbs.sh/SaurusXI/HandWriter/public-key.gpg | sudo apt-key add -
echo 'deb [arch=amd64] https://fbs.sh/SaurusXI/HandWriter/deb stable main' | sudo tee /etc/apt/sources.list.d/handwriter.list
sudo apt-get update
sudo apt-get install handwriter
```
If HandWriter is already installed, you can force an immediate update via:
```bash
sudo apt-get update -o Dir::Etc::sourcelist="/etc/apt/sources.list.d/handwriter.list" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"
sudo apt-get install --only-upgrade handwriter
```
Finally, you can also install without automatic updates by downloading:
    https://fbs.sh/SaurusXI/HandWriter/HandWriter.deb
