# Freerice_Bot
<h3>
This is a bot that constantly plays the freerice.com Multiplication Table category (must start preset on the category).
</h3>

Uses pyautogui and BeautifulSoup to look through the HTML of the page to see the value of each button and the question. This bot manually saves 
the page (as a Webpage, complete), scans through the html downloaded, and clicks using pyautogui based on which result is which. After clicking on a button, the bot waits
for the green of the button (if it waits for over 10 seconds, it continues)
