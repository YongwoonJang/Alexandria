아래 명령어를 차례로 수행하면, 잘못 Commit되었으나, git ignore로 처리못한 파일들을 처리할 수 있음.

> git rm -r --cached some-directory
> git commit -m 'Remove the now ignored directory "some-directory"'
> git push origin master
