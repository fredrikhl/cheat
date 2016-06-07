function _cheat_autocomplete {
    local sheets="$(cheat -l | cut -d' ' -f1)"
    COMPREPLY=()
    if [ $COMP_CWORD = 1 ]; then
        COMPREPLY=(`compgen -W "$sheets" -- $2`)
    elif [ $COMP_CWORD = 2 -a "$3" = "-e" ]; then
        COMPREPLY=(`compgen -W "$sheets" -- $2`)
    fi
}

complete -F _cheat_autocomplete cheat
