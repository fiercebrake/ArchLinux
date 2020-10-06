#!/bin/python

import os
import sys
import stat
import shutil
import tarfile
import fileinput
import subprocess as sp
import http.client as httplib
from subprocess import check_output


if sys.argv[2] == '':
    print('an argument is missing')
    sys.exit()
else:
    dvc = sys.argv[1]
    step = sys.argv[2]
    wd = '/khora/downloads/archlinux/'

if dvc == 'lt':
    dvc_name = 'aster.tekne.sv'
    ird0 = 'intel-ucode'
if dvc == 'pc':
    dvc_name = 'yugen.tekne.sv'
    ird0 = 'amd-ucode'


def conn_chck(url="www.google.com", timeout=3):
    conn = httplib.HTTPConnection(url, timeout=timeout)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
        sys.exit()


def mdr():
    dirs = ['/khora/od/Documents/', '/khora/od/Pictures/', '/khora/od/Music/',
            '/khora/games/steamapps/', '/khora/vms/',
            '/home/fierce_brake/.vim/autoload/',
            '/home/fierce_brake/.vim/bundle/',
            '/home/fierce_brake/.config/autostart/',
            '/home/fierce_brake/.config/onedrive/',
            '/home/fierce_brake/.local/share/Steam/',
            '/home/fierce_brake/.themes/', '/home/fierce_brake/.ssh/',
            '/home/fierce_brake/bin/', '/etc/X11/xorg.conf.d/',
            '/etc/pacman.d/hooks/', '/boot/loader/entries/',
            '/var/log/onedrive/']
    for dir in dirs:
        if not os.path.exists('dir'):
            os.makedirs(dir)

    os.symlink('/khora/od/', '/home/fierce_brake/OneDrive')
    os.symlink('/khora/od/Music', '/home/fierce_brake/Music')
    os.symlink('/khora/games', '/home/fierce_brake/Games')
    os.symlink('/khora/downloads', '/home/fierce_brake/Downloads')
    os.symlink('/khora/games/steamapps/',
               '/home/fierce_brake/.local/share/Steam/steamapps')
    content = ['[Trigger] \n', 'Operation=Install \n', 'Operation=Upgrade \n',
               'Operation=Remove \n', 'Type=Package \n',
               'Target=nvidia-dkms \n', 'Target=linux-zen \n', '\n',
               '[Action] \n', 'Description=Nvidia \n', 'Depends=mkinitcpio \n',
               'When=PostTransaction \n', 'NeedsTargets \n', 'Exec=/bin/sh -c '
               '"while read -r trg; do case $trg in linux-zen) exit 0; esac; '
               'done; /usr/bin/mkinitcpio -P"']
    with open('/etc/pacman.d/hooks/nvidia.hook', 'a') as nv0:
        nv0.writelines(content)

    with fileinput.FileInput('/etc/mkinitcpio.conf', inplace=True,
                             backup='.bak') as mk0:
        for line in mk0:
            print(line.replace('MODULES=()', 'MODULES=(nvidia nvidia_modeset '
                               'nvidia_drm)'), end='')

    with open('/etc/profile', 'r') as pf0:
        contents = pf0.readlines()
        contents.insert(21, "append_path '/home/fierce_brake/bin'")
        contents.insert(22, '\n')
    with open('/etc/profile', 'w') as pf1:
        pf1.writelines(contents)

    shutil.chown(os.path.join('/var/log/onedrive'), 'fierce_brake', 'users')
    os.chmod(os.path.join('/var/log/onedrive'), 0o775)

    shutil.chown('/home/fierce_brake/', 'fierce_brake', 'users')
    os.chmod('/home/fierce_brake/', 0o775)
    for fn, sflds, fnames in os.walk('/home/fierce_brake/'):
        for sf in sflds:
            shutil.chown(os.path.join(fn, sf), 'fierce_brake', 'users')
            os.chmod(os.path.join(fn, sf), 0o775)
            for fname in fnames:
                shutil.chown(os.path.join(fn, fname), 'fierce_brake', 'users')
                os.chmod(os.path.join(fn, fname), 0o664)
    shutil.chown('/khora/', 'fierce_brake', 'users')
    os.chmod('/khora/', 0o775)
    for fn, sflds, fnames in os.walk('/khora/'):
        for sf in sflds:
            shutil.chown(os.path.join(fn, sf), 'fierce_brake', 'users')
            os.chmod(os.path.join(fn, sf), 0o775)
            for fname in fnames:
                shutil.chown(os.path.join(fn, fname), 'fierce_brake', 'users')
                os.chmod(os.path.join(fn, fname), 0o664)
                if '.sh' or '.py' in fname:
                    os.chmod(os.path.join(fn, fname), stat.S_IRWXU)


def packages():
    # main applications
    sp.run(['pacman', '-Sy', '--needed', 'strawberry', 'firefox',
            'icedtea-web', 'flashplugin', 'obs-studio', 'filezilla',
           # Video
            'nvidia-dkms', 'nvidia-utils', 'lib32-nvidia-utils', 'mesa',
            'nvidia-settings', 'vulkan-icd-loader', 'lib32-mesa',
            'vulkan-intel', 'lib32-vulkan-intel', 'lib32-virtualgl',
            'vulkan-icd-loader', 'lib32-vulkan-icd-loader', 'xf86-video-intel',
            # Gaming
            'steam', 'lutris', 'wine-staging', 'lib32-gnutls', 'lib32-libldap',
            'lib32-libgpg-error', 'lib32-sqlite', 'lib32-libpulse', 'giflib',
            'lib32-giflib', 'libpng', 'lib32-libpng', 'libldap', 'wqy-zenhei',
            'lib32-libldap', 'gnutls', 'lib32-gnutls', 'mpg123',
            'lib32-mpg123', 'openal', 'lib32-openal', 'v4l-utils',
            'lib32-v4l-utils', 'libpulse', 'lib32-libpulse', 'libgpg-error',
            'lib32-libgpg-error', 'alsa-plugins', 'lib32-sdl2',
            'lib32-alsa-plugins', 'alsa-lib', 'lib32-alsa-lib',
            'libjpeg-turbo', 'lib32-libjpeg-turbo', 'sqlite', 'lib32-sqlite',
            'libxcomposite', 'lib32-libxcomposite', 'libxinerama',
            'lib32-libgcrypt', 'libgcrypt', 'lib32-libxinerama', 'ncurses',
            'lib32-ncurses', 'opencl-icd-loader', 'lib32-opencl-icd-loader',
            'libxslt', 'lib32-libxslt', 'libva', 'lib32-libva', 'gtk3',
            'lib32-gtk3', 'gst-plugins-base-libs', 'lib32-libxml2',
            'lib32-gst-plugins-base-libs', 'lib32-dbus',
            'lib32-libcurl-compat', 'nss-mdns', 'lib32-nss', 'lib32-gamemode',
            'gamemode',
            # virtualization
            'virt-manager', 'virt-viewer', 'libvirt', 'qemu', 'ebtables',
            'openbsd-netcat', 'dnsmasq', 'bridge-utils',
            # Utilities'
            'ntfs-3g', 'exfat-utils', 'unrar', 'unzip', 'tar', 'p7zip',
            'reflector', 'git', 'bash-completion', 'curl', 'mariadb', 'w3m',
            'time', 'traceroute', 'dnsutils', 'hdparm', 'man', 'fwupd',
            'openssh', 'openssl', 'acpid', 'crda', 'util-linux', 'hidapi',
            'rclone', 'dmidecode', 'ovmf', 'wget', 'whois', 'ttf-dejavu',
            'ttf-liberation', 'profile-sync-daemon', 'bluez', 'bluez-utils',
            'networkmanager', 'networkmanager-openvpn', 'irqbalance',
            'pkgfile',
            # Desktop Environment
            'xfce4', 'xfce4-goodies', 'libcanberra', 'gvfs', 'arandr',
            'pulseaudio', 'pulseaudio-bluetooth', 'thunar-archive-plugin',
            'pavucontrol', 'lightdm', 'lightdm-gtk-greeter',
            'lightdm-gtk-greeter-settings', 'file-roller',
            'nm-connection-editor', 'network-manager-applet',
            'transmission-gtk', 'blueman', 'pasystray'])

    if dvc == 'pc':
        shutil.move(wd + 'xorg.conf',
                    '/etc/X11/xorg.conf.d/20-nvidia.conf')
        with open('/etc/modprobe.d/blacklist.conf', 'w') as bl0:
            bl0.write('install snd_hda_codec_hdmi /bin/true')

    with fileinput.FileInput('/etc/pulse/daemon.conf',
                             inplace=True, backup='.bak') as pa0:
        for line in pa0:
            print(line.replace('; high-priority = yes',
                               'high-priority = yes'), end='')
    with fileinput.FileInput('/etc/pulse/daemon.conf',
                             inplace=True, backup='.bak') as pa1:
        for line in pa1:
            print(line.replace('; nice-level = -11', 'nice-level = -11'),
                  end='')
    with fileinput.FileInput('/etc/pulse/daemon.conf', inplace=True,
                             backup='.bak') as pa2:
        for line in pa2:
            print(line.replace('; realtime-scheduling = yes',
                               'realtime-scheduling = yes'), end='')
    with fileinput.FileInput('/etc/pulse/daemon.conf',
                             inplace=True, backup='.bak') as pa3:
        for line in pa3:
            print(line.replace('; realtime-priority = 5',
                               'realtime-priority = 5'), end='')
    with fileinput.FileInput('/etc/pulse/daemon.conf', inplace=True,
                             backup='.bak') as pa4:
        for line in pa4:
            print(line.replace('; resample-method = speex-float-1',
                               'resample-method = speex-float-10'), end='')
    with open('/etc/pulse/default.pa', 'r') as pa5:
        contents = pa5.readlines()
        contents.insert(34, 'load-module module-switch-on-connect \n')
        contents.insert(35, '\n')
    with open('/etc/pulse/default.pa', 'w') as pa6:
        pa6.writelines(contents)
    with fileinput.FileInput('/etc/pulse/default.pa', inplace=True,
                             backup='.bak') as pa7:
        for line in pa7:
            print(line.replace('load-module module-bluetooth-policy',
                               'load-module module-bluetooth-policy '
                               'auto_switch=2'), end='')

    with fileinput.FileInput('/etc/mkinitcpio.conf', inplace=True,
                             backup='.bak') as mk0:
        for line in mk0:
            print(line.replace('MODULES=()', 'MODULES=(nvidia nvidia_modeset '
                               'nvidia_drm)'), end='')

    sp.run(['timedatectl', 'set-ntp', 'true'])
    sp.run(['fc-cache', '-f'])
    os.rmdir('/var/lib/libvirt/images')
    os.symlink('/khora/vms', '/var/lib/libvirt/images',
               target_is_directory=True)

    with open('/etc/security/limits.conf', 'r') as lm0:
        contents = lm0.readlines()
        contents.insert(49, 'fierce_brake hard nofile 524288 \n')
    with open('/etc/security/limits.conf', 'w') as lm1:
        lm1.writelines(contents)

    with open('/etc/systemd/system.conf', 'r') as sc0:
        contents = sc0.readlines()
        contents.insert(55, 'DefaultLimitNOFILE=524288 \n')
    with open('/etc/systemd/system.conf', 'w') as sc1:
        sc1.writelines(contents)

    with open('/etc/libvirt/qemu.conf', 'w') as qemu:
        qemu.write('nvram = [ "/usr/share/ovmf/x64/OVMF_CODE.fd:/usr/share/'
                   'ovmf/x64/OVMF_VARS.fd" ]')

    with fileinput.FileInput('/etc/bluetooth/main.conf',
                             inplace=True, backup='.bak') as bt0:
        for line in bt0:
            print(line.replace('#AutoEnable=false',
                               'AutoEnable=false'), end='')
    with fileinput.FileInput('/etc/bluetooth/main.conf',
                             inplace=True, backup='.bak') as bt1:
        for line in bt1:
            print(line.replace('#FastConnectable = false',
                               'FastConnectable = false'), end='')
    with fileinput.FileInput('/etc/bluetooth/main.conf',
                             inplace=True, backup='.bak') as bt2:
        for line in bt2:
            print(line.replace('#Name = BlueZ', '#Name = ' + dvc_name), end='')

    if dvc == "lt":
        sp.run(['pacman', '-Sy', '--needed', 'bumblebee', 'primus',
                'lib32-primus'])
        with open('/etc/bumblebee/bumblebee.conf', 'r') as bc0:
            contents = bc0.readlines()
            contents.insert(40, 'VGL_READBACK=pbo optirun glxgears \n')
        with open('/etc/bumblebee/bumblebee.conf', 'w') as bc1:
            bc1.writelines(contents)
        with fileinput.FileInput('/etc/bumblebee/bumblebee.conf',
                                 inplace=True, backup='.bak') as bc2:
            for line in bc2:
                print(line.replace('VGLTransport=proxy',
                                   'VGLTransport=rgb'), end='')
        with fileinput.FileInput('/etc/bumblebee/bumblebee.conf',
                                 inplace=True, backup='.bak') as bc3:
            for line in bc3:
                print(line.replace('Bridge=auto', 'Bridge=primus'), end='')
        with fileinput.FileInput('/etc/bumblebee/bumblebee.conf',
                                 inplace=True, backup='.bak') as bc4:
            for line in bc4:
                print(line.replace('#   BusID "PCI:01:00:0"',
                                   '    BusID "PCI:01:00:0"'), end='')
        sp.run(['gpasswd', '-a', 'fierce_brake', 'bumblebee'])
        sp.run(['systemctl', 'enable', 'bumblebeed'])


def s0():
    conn_chck()
    sp.run(['timedatectl', 'set-ntp', 'true'])

    with fileinput.FileInput('/etc/pacman.conf',
                             inplace=True, backup='.bak') as pm0:
        for line in pm0:
            print(line.replace('#[multilib]', '[multilib]'), end='')
    with open('/etc/pacman.conf', 'r') as pm1:
        contents = pm1.readlines()
        contents[92] = 'Include = /etc/pacman.d/mirrorlist'
        contents.insert(93, '\n')
    with open('/etc/pacman.conf', 'w') as pm2:
        pm2.writelines(contents)

    sp.run(['pacman', '-Sy', 'reflector'])
    sp.run(['reflector', '--verbose', '--country', 'United States', '-l',
            '10', '--sort', 'rate', '--save', '/etc/pacman.d/mirrorlist'])
    sp.run(['pacstrap', '/mnt/', 'base', 'base-devel', 'linux-zen',
            'linux-zen-docs', 'linux-zen-headers', 'linux-firmware', 'python',
            'vim', 'sudo', 'efibootmgr', 'e2fsprogs', 'dosfstools',
            'f2fs-tools', ird0])

    with open('/mnt/etc/hosts', 'w') as hs0:
        hs0.write('127.0.0.1 localhost \n')
    with open('/mnt/etc/hosts', 'a') as hs1:
        hs1.write('127.0.0.1 ' + dvc_name + ' \n')
    with open('/mnt/etc/hostname', 'w') as hstn:
        hstn.write(dvc_name)

    with fileinput.FileInput('/mnt/etc/sudoers',
                             inplace=True, backup='.bak') as sd0:
        for line in sd0:
            print(line.replace('# %wheel ALL=(ALL) ALL',
                               '%wheel ALL=(ALL) ALL'), end='')
    with open('/mnt/etc/sudoers', 'r') as sd1:
        contents = sd1.readlines()
        contents.insert(79, 'fierce_brake ALL=(ALL) ALL')
        contents.insert(80, '\n')
    with open('/mnt/etc/sudoers', 'w') as sd2:
        sd2.writelines(contents)
    with open('/mnt/etc/sudoers', 'r') as sd3:
        contents = sd3.readlines()
        contents.insert(97, 'fierce_brake ALL=(ALL) NOPASSWD: '
                        '/usr/bin/psd-overlay-helper')
        contents.insert(98, '\n')
    with open('/mnt/etc/sudoers', 'w') as sd4:
        sd4.writelines(contents)

    with fileinput.FileInput('/mnt/etc/locale.gen',
                             inplace=True, backup='.bak') as lclg:
        for line in lclg:
            print(line.replace('#en_US.UTF-8 UTF-8',
                               'en_US.UTF-8 UTF-8'), end='')

    sp.run(['locale-gen'])
    with open('/mnt/etc/locale.conf', 'w') as vimrc:
        vimrc.write('LANG=en_US.UTF-8')

    shutil.copyfile('/etc/pacman.conf', '/mnt/etc/pacman.conf')
    shutil.copyfile('/etc/pacman.d/mirrorlist', '/mnt/etc/pacman.d/mirrorlist')
    gfst = check_output(['genfstab', '-U', '-p',
                         '/mnt'], universal_newlines=True)
    with open('/mnt/etc/fstab', 'w') as fst0:
        fst0.write(str(gfst))
    sp.run(['vim', '/mnt/etc/fstab'])
    os.symlink('/usr/bin/vim', '/mnt/usr/bin/vi')
    sp.run(['arch-chroot', '/mnt'])


def s1():
    conn_chck()
    os.link('/usr/share/zoneinfo/America/El_Salvador', '/etc/localtime')
    sp.run(['hwclock', '--systohc'])
    sp.run(['localectl', 'set-locale', 'LANG=en_US.UTF-8'])
    sp.run(['locale-gen'])

    sp.run(['passwd'])
    sp.run(['useradd', '-mg', 'users', '-G', 'wheel,storage,power,lp,rfkill',
            '-s', '/bin/bash', 'fierce_brake'])
    sp.run(['passwd', 'fierce_brake'])
    sp.run(['pacman', '-Sy'])

    mdr()

    packages()

    sp.run(['usermod', '-a', '-G', 'libvirt', 'fierce_brake'])
    sp.run(['systemctl', 'set-default', 'graphical.target'])
    sp.run(['systemctl', 'enable', 'bluetooth.service', 'fstrim.service',
            'libvirtd.service', 'NetworkManager.service',
            'irqbalance.service', 'lightdm.service'])
    sp.run(['su', '-', 'fierce_brake'])


def aur():
    conn_chck()
    sp.run(['wget', 'https://tpo.pe/pathogen.vim'],
           cwd='/home/fierce_brake/.vim/autoload/')
    sp.run(['git', 'clone', '--recurse-submodules',
            'https://github.com/python-mode/python-mode.git'],
           cwd='/home/fierce_brake/.vim/bundle/')
    if dvc == 'pc':
        shutil.move(wd + 'nvidia-settings-rc',
                    '/home/fierce_brake/.nvidia-settings-rc')
        shutil.chown('/home/fierce_brake/.nvidia-settings-rc',
                     'fierce_brake', 'users')
        os.chmod('/home/fierce_brake/.nvidia-settings-rc', 0o440)
    content = ['execute pathogen#infect() \n',
               'execute pathogen#helptags() \n', 'syntax on \n',
               'filetype plugin indent on \n',
               'set showmode nonumber nohlsearch \n',
               'set ai ts=4 expandtab \n', 'nmap <C-N> :set invnumber<CR> \n',
               'set number \n', 'set background=light \n',
               'let g:solarized_termcolors=256 \n',
               'let g:solarized_termtrans=0 \n',
               'let g:solarized_degrade=0 \n', 'let g:solarized_bold=1 \n',
               'let g:solarized_underline=1 \n', 'let g:solarized_italic=1 \n',
               'let g:solarized_contrast="normal" \n',
               'let g:solarized_visibility="normal" \n',
               'colorscheme solarized']
    with open('/home/fierce_brake/.vimrc', 'a') as vimrc:
        vimrc.writelines(content)
    content = ['skip_dir = "BackUps|MobileApps|Pictures/Personal|'
               'Pictures/Professional|Pictures/Samsung Gallery|Music" \n',
               'log_dir = "/var/log/onedrive/" \n',
               'disable_notifications = "false" \n',
               'enable_logging = "true" \n', 'user_agent = "Mozilla/5.0 (X11; '
               'Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"']
    with open('/home/fierce_brake/.config/onedrive/config', 'a') as odconfig:
        odconfig.writelines(content)
    sp.run(['git', 'clone', 'https://aur.archlinux.org/pikaur.git',
            '/tmp/pikaur'])
    sp.run(['makepkg', '-fsirc'], cwd='/tmp/pikaur/')
    sp.run(['pikaur', '-Syu'])

    with fileinput.FileInput('/home/fierce_brake/.config/pikaur.conf',
                             inplace=True, backup='.bak') as pk0:
        for line in pk0:
            print(line.replace('noedit = no', 'noedit = yes'), end='')
    with fileinput.FileInput('/home/fierce_brake/.config/pikaur.conf',
                             inplace=True, backup='.bak') as pk1:
        for line in pk1:
            print(line.replace('donteditbydefault = no',
                               'donteditbydefault = yes'), end='')
    with fileinput.FileInput('/home/fierce_brake/.config/pikaur.conf',
                             inplace=True, backup='.bak') as pk2:
        for line in pk2:
            print(line.replace('nodiff = no', 'nodiff = yes'), end='')

    sp.run(['pikaur', '-Sy', '--needed', 'ttf-ms-fonts', 'libldac',
            'python-notify2', 'steam-fonts', 'vim-colors-solarized-git',
            'aic94xx-firmware', 'zoom', 'onedrive-abraunegg', 'google-chrome',
            'xpadneo-dkms-git', 'wd719x-firmware', 'teamviewer',
            'xfce4-volumed-pulse', 'sound-theme-smooth',
            'pulseaudio-modules-bt', 'ttf-google-fonts-git'])
    sp.run(['pikaur', '-Sy', '--needed', 'polychromatic', 'openrazer-meta'])
    sp.run(['systemctl', '--user', 'enable', 'teamviewerd.service',
            'gamemoded.service'])
    sp.run(['sudo', 'gpasswd', '-a', 'fierce_brake', 'plugdev'])
    my_tar = tarfile.open(wd + '98942-minimal-grey2.tar.gz')
    my_tar.extractall('/home/fierce_brake/.themes')
    my_tar.close()

    sp.run(['sudo', 'efibootmgr', '--disk', '/dev/nvme0n1', '--part', '1',
            '--create', '--label', 'Arch Linux', '--loader',
            '/vmlinuz-linux-zen', '--unicode', 'root=LABEL=ROOT rw initrd=\\' +
            ird0 + '.img initrd=\\initramfs-linux-zen.img quiet '
            'mitigations=off nvidia-drm.modeset=1', '--verbose'])


def od():
    sp.run(['onedrive', '--synchronize', '--resync', '--download-only',
            '--verbose'])
    sp.run(['systemctl', '--user', 'enable', 'onedrive'])
    sp.run(['systemctl', '--user', 'start', 'onedrive'])
    os.symlink('/khora/od/Documents/', '/home/fierce_brake/Documents')
    os.symlink('/khora/od/Pictures/', '/home/fierce_brake/Pictures')
    for fn, sflds, fnames in os.walk('/khora/od/Documents/'):
        for sf in sflds:
            for fname in fnames:
                if '.sh' in fname:
                    os.chmod(os.path.join(fn, fname), stat.S_IRWXU)
                if '.py' in fname:
                    os.chmod(os.path.join(fn, fname), stat.S_IRWXU)
    with open('/home/fierce_brake/.bash_profile', 'a') as bsh:
        bsh.write('export PATH="${PATH}:/home/fierce_brake/bin"')
    os.symlink('/khora/od/Documents/sc/asd.py', '/home/fierce_brake/bin/asd')
    shutil.copyfile('/khora/od/Documents/sc/keys/id_rsa',
                    '/home/fierce_brake/.ssh/id_rsa')
    shutil.copyfile('/khora/od/Documents/sc/keys/id_rsa.pub',
                    '/home/fierce_brake/.ssh/id_rsa.pub')
    os.chmod('/khora/od/Documents/sc/keys/id_rsa', 0o400)
    os.chmod('/khora/od/Documents/sc/keys/id_rsa.pub', 0o400)
    os.symlink('/khora/od/Pictures/Avatars/fierce-yugen.jpg',
               '/home/fierce_brake/.face.icon')
    os.symlink('/khora/od/Pictures/Avatars/fierce-yugen.jpg',
               '/home/fierce_brake/.face')
    os.remove('/home/fierce_brake/.bashrc')
    os.symlink('/home/fierce_brake/Documents/sc/bashrc.txt',
               '/home/fierce_brake/.bashrc')

    with fileinput.FileInput('/home/fierce_brake/.config/xfce4/xfconf/xfce-'
                             'perchannel-xml/xfce4-keyboard-shortcuts.xml',
                             inplace=True, backup='.bak') as kb0:
        for line in kb0:
            print(line.replace('<property name="XF86WWW" type="string" '
                               'value="exo-open --launch WebBrowser"/>',
                               '<property name="&lt;Super&gt;b" type="string" '
                               'value="exo-open --launch WebBrowser"/>'),
                  end='')
    with fileinput.FileInput('/home/fierce_brake/.config/xfce4/xfconf/xfce-'
                             'perchannel-xml/xfce4-keyboard-shortcuts.xml',
                             inplace=True, backup='.bak') as kb1:
        for line in kb1:
            print(line.replace('<property name="&lt;Primary&gt;&lt;Alt&gt;t" '
                               'type="string" value="exo-open --launch '
                               'TerminalEmulator"/>', '<property '
                               'name="&lt;Super&gt;t" type="string" '
                               'value="exo-open '
                               '--launch TerminalEmulator"/>'), end='')
    with fileinput.FileInput('/home/fierce_brake/.config/xfce4/xfconf/xfce-'
                             'perchannel-xml/xfce4-keyboard-shortcuts.xml',
                             inplace=True, backup='.bak') as kb2:
        for line in kb2:
            print(line.replace('<property name="XF86Mail" type="string" '
                               'value="exo-open --launch MailReader"/>',
                               '<property name="&lt;Super&gt;e" type="string" '
                               'value="exo-open '
                               '--launch FileManager"/>'), end='')

    content = ['#!/bin/bash \n', 'nvidia-settings -l \n',
               'rclone --vfs-cache-mode writes mount OneDrive:/Music '
               '/khora/od/Music & \n']
    with open('/home/fierce_brake/.xprofile', 'a') as xp0:
        xp0.writelines(content)

    sp.run(['rclone', 'config'])


if step == 's0':
    s0()
if step == 's1':
    s1()
if step == 'aur':
    aur()
if step == 'od':
    od()
