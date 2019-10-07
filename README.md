# CardGame
Kleiner Parkins Challenge

## Setup
No requirements which aren't included in Python standard library.

## Rules
Navigate with Up/Down arrow keys.
Hitting the same card twice adds 3 lives.
Hitting the same color card twice adds 1 life.
Hitting any other card loses 1 life.
Play till you hit 0.

## Game Choice
The game is designed for simplicity. While Blackjack and Solitaire are amazing games, playing them on Terminal seems a little too far fetched. My goal was to design a game that one could play while your model trains in the background. Inspired by the Google Chrome Dinosaur game, this game is what I believe a terminal based game should realistically look like. I also noticed that games with a central character make it much easier for a human user to relate to and get involved with the game, while also making it very intuitive to understand the rules of the game.

## Game Design
In order to design a game unlike Solitaire or Blackjack, I needed rendering on the fly and without user input. Python, being my go-to language as an academic researcher, offers a nice library for such a setup:  `curses`.  Credits for a good intro to `curses` in python: [https://www.youtube.com/watch?v=BK7YvpTT4Sw](https://www.youtube.com/watch?v=BK7YvpTT4Sw)

As suggested, I spent merely a few hours first learning `curses` and then implementing a simple (pretty hard coded) game. I designed Layers of cards coming in, and for each layer, I have an x position (updated leftwards in every move), and a list of (character, symbol) list for each card in the layer, where character = 2,3,...J,Q,K,A and symbol = Hearts, Spades, ...

