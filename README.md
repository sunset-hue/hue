# hue
Just a random package manager that may or may not work idk 

Features it's (probably) gonna have in it's first version (ty cameron.simpson, discord!)

query PyPI's index
resolve your package and its constraints
resolve the dependencies of the package, and their constraints (this is just a recursive call to the same solver, perhaps, for each dep - and then recursively their deps)
find the latest version which can be resolved for everything
fetch it and install it
the install is basicly an unzip if you fetch a wheel (.whl) or a build if you fetch a source dist (sdist)
the build involves fetching the sdist, consulting its metadata for a build tool , fetch the build tool if not present, use it to build the package, then install