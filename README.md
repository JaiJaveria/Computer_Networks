# Computer_Networks

These are the assignments that I did as part of the COL334: Computer Networks Course Semester-1, 2020-21 at IIT Delhi taught by [Prof Aaditeshwar Seth]

## Assignment 1: Internet Architecture
- This Project involved using tools like traceroute, ping, wireshark to understand how Internet Architecture is laid out and understand its intricacies.

## Assignment 2: Packet Trace Analysis
- This Project involved inspecting network traffic using tools like Wireshark and the Chrome developer tools. I had to analyze the packet traces of loading website like [CSE, IITD], [IndianExpress] and [NYTimes].

## Assignment 3: File Download
- In this, I had to write a program that could download a file from servers under different settings.
- The first setting was to just download the whole file in one go. This is done in 1.py file.
- The second setting was to download the file in parts. I downloaded 10K bytes at one time until I got the whole file. This is done in 2.py file.
- The third setting was to open multiple TCP connections to mutiple servers to download different chunks of the same file. This is done in 3.py file.
- The fourth setting was to make the download robust to disconnections. I had to make sure that in case a network failure happens, the download is resumed from where it was interrupted and not from the begining. This is done in 4.py
- I also have some files showing the results that I got. I was able to get a  ***29x***	speedup in download times with ***40*** parallel threads.


---
[Prof Aaditeshwar Seth]: https://www.cse.iitd.ac.in/~aseth/
[CSE, IITD]: https://www.cse.iitd.ac.in/
[IndianExpress]: https://indianexpress.com/
[NYTimes]: https://www.nytimes.com/