#!/bin/bash
dkr_id=${DKR_ID:-1}
sudo /etc/init.d/dbus start
#echo -e "$VNC_PASSWD\n$VNC_PASSWD\ny\n$VNC_VIEW_PASSWD\n$VNC_VIEW_PASSWD" |vnc4passwd
echo -e "$VNC_PASSWD\n$VNC_PASSWD\ny\n$VNC_VIEW_PASSWD\n$VNC_VIEW_PASSWD" |tigervncpasswd
tigervncserver :${dkr_id}
xrandr --newmode "480x853"   33.00  480 504 552 624  853 856 866 886 -hsync +vsync
xrandr --addmode VNC-0  "480x853"
xrandr --newmode "856x480"   31.75  856 880 960 1064  480 483 493 500 -hsync +vsync
xrandr --addmode VNC-0 "856x480"
xrandr --newmode "768x1024"   65.25  768 816 896 1024  1024 1027 1037 1063 -hsync +vsync
xrandr --addmode VNC-0 "768x1024"
xrandr --newmode "1024x768"   63.50  1024 1072 1176 1328  768 771 775 798 -hsync +vsync
xrandr --addmode VNC-0 "1024x768"
xrandr --newmode "720x1280"   77.50  720 776 848 976  1280 1283 1293 1327 -hsync +vsync
xrandr --addmode VNC-0 "720x1280"
xrandr --newmode "1280x720"   74.50  1280 1344 1472 1664  720 723 728 748 -hsync +vsync
xrandr --addmode VNC-0 "1280x720"
xrandr --newmode "544x1110"   49.50  544 576 632 720  1110 1113 1123 1151 -hsync +vsync
xrandr --addmode VNC-0 "544x1110"
xrandr --newmode "1110x544"   47.00  1112 1152 1256 1400  540 543 553 562 -hsync +vsync
xrandr --addmode VNC-0 "1110x544"
xrandr -s "544x1110"
