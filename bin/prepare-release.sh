#!/bin/bash

if ! [ $NONINTERACTIVE ]; then
    if [ "$EDITOR" == "" ]; then
        echo '$EDITOR environement variable is not set but is required in interactive mode'
        exit -1
    fi
fi

case "$1" in
	major|minor|patch)
		: ;;
	*)
		echo "Usage: $0 <major|minor|patch>" >&2
		exit 1
esac

# Check we're on main, warn if not, exit by default but allow to continue

CURBRANCHNAME=$(git rev-parse --abbrev-ref HEAD)

if [[ "$CURBRANCHNAME" != "main" ]]; then
    echo "Current branch is $CURBRANCHNAME whereas main is expected. Exiting."
    exit 1
fi

#Check that we are up to date with origin

ref1="main"
ref2="origin/main"
git fetch origin

delta= git diff -s --exit-code $ref1 $ref2
isdif=$?
if [ "$isdif" -eq "1" ];
then
    echo "$ref1 and $ref2 are not on same hash"
    exit 1
fi


OLDVERSION=$(uv version --short)
uv version --bump $1
VERSION=$(uv version --short)

RELEASE_DATE=$(date +%Y-%m-%d)
CHANGES="CHANGES.rst"

HEADER="$VERSION ($RELEASE_DATE)"
HEADLEN=${#HEADER}

#Display the changelog  header
echo    "Changelog"          >  ${CHANGES}.new
echo -e "=========\n"        >> ${CHANGES}.new
echo    $HEADER              >> ${CHANGES}.new
perl -E "say '-' x $HEADLEN" >> ${CHANGES}.new
echo    ""                   >> ${CHANGES}.new

# Add commit messages as first message to display
git log --pretty=' * %s' --first-parent --abbrev-commit $OLDVERSION.. >> lastcommits.txt

# Nicer changelog
content=$(sed "s:Merge branch '\(.*\)' into 'main'$:\1:" < lastcommits.txt)
content=$(echo "$content" | sed 's/[fF]ix\//Fixed: /' | sed 's:-: :g')
echo "$content" | sed 's/[fF]eature[s?]\//Add: /' >> ${CHANGES}.new

rm lastcommits.txt

# Display older version changelog
tail -n +3 ${CHANGES} >> ${CHANGES}.new

mv -f ${CHANGES}.new ${CHANGES}


if ! [ $NONINTERACTIVE ]; then
  $EDITOR ${CHANGES}
fi

echo ""
echo "You can now test this version, then commit it with number $VERSION"
echo ""
