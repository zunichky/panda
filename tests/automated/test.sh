#!/bin/bash -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd)"
pytest $(ls $DIR/$1*.py)
