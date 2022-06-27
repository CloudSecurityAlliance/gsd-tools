# Build Support
Files here support the build to collect context before quasar boots

## Build Version

We collect details from the underlying .git folder of the parent project to identify the current sha.
This is addressed by reading either the detached head file for a sha or if that is a ref to another
branch we read the HEAD sha of that branch instead.

Under normal circumstances we will read from `ref/main` in production and your feature branch in development.
