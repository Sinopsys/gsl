#!/usr/bin/env bash

curr_date=$(date +%d_%m_%Y)

git add .
git commit -m "Update algorithms: $curr_date."
git push


# EOF
