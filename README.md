# Closure Highlighting
*Highlighting the closest surrounding brackets of the cursor.*

## Features

This plugin will highlight the first closure of square/curly brackets or 
parenthesis that it finds.

## Installation

Using [Pathogen](https://github.com/tpope/vim-pathogen)
you simply place this plugin in `~/.vim/bundle`,
e.g. via cloning this repository.

The plugin is only loaded if `hi_bracket_closure` is set to `1`.
In other words, to use this plugin place the following line in your vimrc:

`let hi_bracket_closure = 1`

## Configuration

The highlight colour can be controlled via highlight group *BracketClosure*.
