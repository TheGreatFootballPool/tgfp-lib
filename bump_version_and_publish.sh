#!/bin/bash
# usage: [major, minor, patch] "commit message"
poetry version $1
git add .
if [ -s commit.txt ] ; then
  git commit -F commit.txt
  cat /dev/null > commit.txt
else
  git commit -m "$2"
fi
git push
NEW_VERSION=`poetry version -s`
git tag v${NEW_VERSION}
git push origin v${NEW_VERSION}
doppler run --config prd --command="poetry publish --build --username __token__ --password \$PYPI_TOKEN"
