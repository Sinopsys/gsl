#!/usr/bin/env bash

if cd $1;
then
    cd ..
    name1=$(echo $1 | rev | cut -d/ -f1 | rev)
    name2=$(echo $2 | rev | cut -d/ -f1 | rev)
    if [[ $name1 == $name2 ]]
    then
        rm -rf $name1
        git clone $2
        cd $name2
        rm -rf .git*
    fi
fi


# EOF
