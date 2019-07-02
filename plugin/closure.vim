" Version: 0.1.0
" Maintainer: Emil Nilsson <emil.nilsson@protonmail.com>
" Description: Highlights the closest closure.
" Last Changed: 2019-07-03

if exists('g:loaded_hiclosure')
	finish
endif
let g:loaded_hiclosure = 1


" Only load the plugin if it is enabled in the vimrc
let g:hi_bracket_closure = get(g:, 'hi_bracket_closure', 0)
if !g:hi_bracket_closure
	finish
endif


" Use the same highlight configuration as MatchParen per default
let g:bracket_closure_color = get(g:, 'bracket_closure_color', 'MatchParen')
execute 'highlight link BracketClosure' g:bracket_closure_color


" Load functions from the Python file
let g:plugindir = expand('<sfile>:p:h')
execute 'py3file ' . g:plugindir. '/python/closure.py'


" Highlights the closest surrounding brackets of the current cursor position.
function! HighlightBracketClosure()
" First we wipe out all matches already present.
" NOTE: This might not be playing that nicely with other plugins. But hey?
call clearmatches()
python3 << EOF
highlight_surrounding_brackets()
EOF
endfunction


" Highlight the closure automatically when the cursor is moved
autocmd CursorMoved <buffer> call HighlightBracketClosure()
