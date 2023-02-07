# Accidental deletions of data

https://github.com/CVEProject/cvelist/commits/master/2021/43xxx/CVE-2021-43566.json

On Nov 9, 2021 MSRC accientally deleted around 1,028 files from the cvelist git repo as well as a lot of content, it appears they forgot to use a branch?

https://github.com/CVEProject/cvelist/commit/938debeed0dc5ff4eff0a7b3a8b4f39c8881b6bd#diff-7e001bbd4c1efff3745bc4f2c5dcfa7ab2d192fef03253754eee5134003fae3f

And then a week later MITRE reverted the commit to fix it mostly:

https://github.com/CVEProject/cvelist/commit/df296d9e014bf68ef22c0583c98da3fbe42ea316#diff-7e001bbd4c1efff3745bc4f2c5dcfa7ab2d192fef03253754eee5134003fae3f
