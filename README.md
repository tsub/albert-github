# Albert extension for GitHub

Open GitHub repository in browser with [Albert].

![image](https://gyazo.com/fff7125ea22e33c863f6fd535d7f2b8b.png)

## Installation

1. Clone repository and execute install script

    ```
    $ git clone https://github.com/tsub/albert-github.git
    $ cd albert-github
    $ ./install.sh
    ```

1. Enable GitHub extension in Albert

    ![image](https://gyazo.com/f52dfc08974751837263647782dadee4.png)

## Configuration

1. Create your GitHub access token in [here](https://github.com/settings/tokens)
    * Require scope is "repo"

    ![image](https://gyazo.com/debebcc36cbb85d037ca1c1db1ddb249.png)

1. Configure your GitHub access token in Albert

    ![image](https://gyazo.com/540bbab3866fb98f1855b32084e3d98a.png)

## Usage

:warning: The first time is very slow because there is no cache.

1. Please type `gh ` in Albert

    ![image](https://gyazo.com/fff7125ea22e33c863f6fd535d7f2b8b.png)

1. Incremental search is also possible

    ![image](https://gyazo.com/22c17ac3c92c11f84c389a6ecffd4934.png)

## Trouble shooting

### I want to change the saved GitHub access token

1. Delete your saved GitHub access token

    ![image](https://gyazo.com/81064b6a07399bb1cbd7395c8615b4ff.png)

1. Then [reconfigure](#Configuration)

### Repository list is not up to date

1. Delete cached repositories

    ![image](https://gyazo.com/bd0b9de6be8c11b3f62b117d9114b9e7.png)

1. Then [refetch repositories](#Usage) after deleted

[Albert]: https://albertlauncher.github.io
