#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd ${DIR}


NONINTERACTIVE=1 ./bin/prepare-release.sh $1

VERSION=$(uv version --short)
git commit -am "Release $VERSION"
git tag "$VERSION"
