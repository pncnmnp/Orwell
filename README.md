# Orwell

## What, Why, and How

**What would happen if we replace [2048](https://en.wikipedia.org/wiki/2048_(video_game)) with alphabets?**

Well, it won't be called 2048, for sure. But apart from that, how would we even make such a game playable?

One way is to combine same alphabets to produce higher alphabets (i.e. _A+A -> B_). But that would become a replica of 2048.

The other is to _concatenate_ the alphabets (or words). For example:- _ear_ and _th_ can be combined to produce _earth_. 
After each move (up, down, left, right), an alphabet is spawned on the board. 
This alphabet starts with the [letter frequency](https://en.wikipedia.org/wiki/Letter_frequency) identified in various texts.
Once we have formed words, we are left with two options - keep the word intact (with the hope of using it to form a larger length word) 
or _pop out_ the word from the board and redeem its points. 

If a word is popped out, the initial letter frequency is adjusted with the popped out alphabets. For instance, if a word - _earth_ 
is popped out, the probability of occurence of letters _{e,a,r,t,h}_ is reduced by an amount proportional to its current probability. 
To compensate for the overall reduced probability, we increase the rest of the alphabets by an equal amount.

Presently, I am using a [scrabble dictionary](https://github.com/zeisler/scrabble/blob/master/db/dictionary.csv) to verify whether two alphabets or words can be combined.
[Meanings](https://github.com/matthewreagan/WebstersEnglishDictionary/blob/master/dictionary.json) are being displayed after a word is popped to familiarize the player with unknown words.
Interestingly, score is directly proportional to the length of the words popped rather than the number of alphabets or words combined.

This game is based on a thought I had a few months back. It exists as a quick prototype to test my idea.

## How does the game look like?
Here is a gif of a recent game I played - 
<p align="center">
<img src="https://github.com/pncnmnp/Orwell/blob/master/screenshots/orwell.gif">
</p>

## License
The code is licensed under MIT License