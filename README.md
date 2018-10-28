# Albert plugin for GitHub

Open GitHub repository in browser with [Albert].

![image](https://gyazo.com/22c17ac3c92c11f84c389a6ecffd4934.png)

## Installation

```
$ git clone https://github.com/tsub/albert-github.git
$ cd albert-github
$ ./install.sh
```

## Configuration

1. Create your GitHub access token in [here](https://github.com/settings/tokens).
    * Require scope is "repo".

    ![image](https://gyazo.com/debebcc36cbb85d037ca1c1db1ddb249.png)

1. Configure your GitHub access token in Albert.

    ![image](https://gyazo.com/540bbab3866fb98f1855b32084e3d98a.png)

## Trouble shooting

### I want to change the saved GitHub access token

I am not implemented the function to update the saved GitHub access token yet with Albert.

Please execute below command, then [reconfigure](#Configuration).

```
$ rm ~/.cache/albert/GitHub_access_token
```

### Repository list is not up to date

I have not implemented cache update yet.

Instead, delete the cache once.

```
$ rm ~/.cache/albert/GitHub_cache.json
```

[Albert]: https://albertlauncher.github.io
