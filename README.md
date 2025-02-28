# Serial Capture to PCAP

This repository contains scripts to convert serial streams into PCAP files for subsequent interpretation with Wireshark.

The scripts work in conjunction with `text2pcap`, part of the Wireshark suite, to represent each read or write operation on the serial device as a UDP packet. For example:

    python3 spmcsv2text.py < examples/spm.csv \
    | text2pcap -D -t iso -u 1234,1234 - - \
    | tshark -V -O data -r -

To save to a file, use:

    ... | text2pcap -D -t iso -u 1234,1234 -F pcap - output.pcap

See [rgov/wireshark-udp-reassembly](https://github.com/rgov/wireshark-udp-reassembly) for an example of how to write a Wireshark dissector to reassemble data units that are split across separate UDP packets.

`spmcsv2text.py` processes captures made by the Windows app [Serial Port Monitor](https://www.serial-port-monitor.org/) by Electonic Team, Inc. The script does not understand the proprietary .spm file format; export the capture to a CSV file by right clicking and selecting "Export to...".

`strace2text.py` processes captures from the `strace` utility on Linux. The recommended `strace` arguments are shown below. It is important to pass `--fd=n` to the script to select the file descriptor for the serial device.

    strace -e read,write -s 65535 -tt -xx -o strace.log -- cmd
    python3 strace2text.py --fd=3 < strace.log \
    | text2pcap -D -t iso -u 1234,1234 - - \
    | tshark -V -O data -r -
