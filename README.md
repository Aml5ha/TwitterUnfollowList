# TwitterUnfollowList
Code for generating a file of people you follow who don't follow you back

The code does not have error checking in case the login information is incorrect.

Like any selenium project, the performance of the program depends on the machine and network. The code may have to be slightly altered to account for slower machines/networks. 

The chromedriver used in this project is v 2.4 which supports Chrome v66-68. In the future a more recent version of chromedriver may be needed. 

## Overview:
The program logs into twitter and navigates to the user's profile. Then it extracts how many people you are following and then checks to see who doesn't follow you back. Every account that doesn't follow you back (meaning there is no "Follow you" tag) is printed to a file. 

## Copyright: 
I made this myself and am fine with anyone improving it or using it. I'd love to hear your thoughts on the project! 
