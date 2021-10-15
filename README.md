# Arbitrage-Alerts
This Program sends alerts when there is an arbitrage opportunity according to the limits user set, from the markets user chose.


What is Arbitrage?
Arbitrage is basically taking advantage of the difference in prices. I am definitely not an economist or something like that, but in my view it is like taking the apple from the market where it is low priced and selling the apple where it is high priced. (For more information: https://en.wikipedia.org/wiki/Arbitrage)

So what my program does is you set the markets you want to compare and then you set price limits. Program compares USDT/TRY prices and when the difference of them exceeds the limit you set, the program plays a sound saying difference is between the prices you decided. 

If anyone uses this information correctly, then they have a good chance of earning money from these opportunities. But certainly I am not recommending anything.
NOT INVESTMENT ADVICE


How this program runs. 
* It uses selenium and chromium to scrape price data from websites. 
* also shows user the price data with a clean an fine tkinter application. (with a few bugs, for example, the OS you are using may say the program is not responding, but it is setting the webdriver to scrape data) 

The program can be really functionalized with async programming or multithreading, so i am publishing the program when it is unfinished. I am open to advices. Thanks for your interest.

Before using the program, make sure your chrome browser's version matches the version of chromium webdriver which is in the 'driver' folder.

mail: kerem.kirici36@gmail.com
ig: keremmkirici_
twitter: keremmkirici
