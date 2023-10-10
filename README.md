# cripto-p1
If you don't want to keep any of your local changes and simply want to update your local repository to match the remote repository without preserving any local modifications, you can use the following command:

git fetch origin
git reset --hard origin/main

This will fetch the latest changes from the remote repository (without merging them) and then reset your local branch (main) to match the remote branch (origin/main) without preserving any local changes. Be cautious when using this approach because it will discard all local changes and reset your branch to the state of the remote branch.