# Jewelify Project

This repository contains the source code for the Jewelify project. This project is an e-commerce application for jewelry. The main feature of this project is (would) be to virtually try any choosen jewelry on the user, using the camera.

## Table of contents

${toc}

## Installation

Note: This installation process is for development only, **NOT** for production

#### Prerequisites

1. Docker
2. Docker compose

#### Steps

1. Clone this repo using:

    ```sh
    git clone https://github.com/arushgupta2007/jewelify_project.git
    ```

2. Create a sample docker-compose.yml file at the root of this project:

    ```yaml
    # use version 3
    version: '3'

    # define all services (something like containers)
    services:
        # Database
        database:
            image: mariadb:10.6.3-focal # we will be using Mariadb
            restart: always # restart the database in case the process ends
            environment:
                MYSQL_ROOT_PASSWORD: db_pass # set db password TODO: Change to more secure password
            volumes:
                # TODO: Change the below line
                # For e.g: ~/Desktop/Jewelify_project/mariadb:/var/lib/mysql
                - <insert your volume path here>:/var/lib/mysql

        # Define worker (part of vendure architecture)
        worker:
            # define where & how the docker conatiner should be built
            build:
                context: ./backend
                dockerfile: Dockerfile
            # Set defualt command for worker (you may have to put the command all in one line)
            command:
                [
                    './wait-for-it.sh',
                    'database:3306',
                    '--',
                    'yarn',
                    'run:worker',
                ]

            # define environment variables
            environment:
                DATABASE_HOST: database
                DATABASE_PORT: 3306
            # Set dependency (This is not needed becuase worker is defined after database, but this is kept for clarity)
            depends_on:
                - database

        # define server (part of vendure architecture)
        server:
            # define where and how the docker container should be built
            build:
                context: ./backend
                dockerfile: Dockerfile
            # expose ports
            ports:
                - 3000:3000
            # set default command (you may have to put the command all in one line)
            command:
                [
                    './wait-for-it.sh',
                    'database:3306',
                    '--',
                    'yarn',
                    'run:server',
                ]
            # set environment variables
            environment:
                DATABASE_HOST: database
                DATABASE_PORT: 3306
            # set dependency (This is not needed becuase server is defined after worker and database, but this is kept for clarity)
            depends_on:
                - database
                - worker
        # define storefront (The main UI the end user sees)
        storefront:
            # define where and how the docker conatiner should be built
            build:
                context: ./frontend
                dockerfile: Dockerfile
            # set network_mode to host
            # TODO: Find a way to avoid this, by editing the server API location in the frontend code
            # Ideally we would like to only expose port 4201
            network_mode: host
    ```

3. Run the conatiners! In the root directory, run:
    ```sh
    docker-compose up --build
    ```
    You whould see some logs like:
    ```
    database_1    | 2021-08-04 05:32:11+00:00 [Note] [Entrypoint]: Entrypoint script for MariaDB Server 1:10.6.3+maria~focal started.
    database_1    | 2021-08-04 05:32:12+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
    database_1    | 2021-08-04 05:32:12+00:00 [Note] [Entrypoint]: Entrypoint script for MariaDB Server 1:10.6.3+maria~focal started.
    worker_1      | wait-for-it.sh: waiting 15 seconds for database:3306
    database_1    | 2021-08-04  5:32:12 0 [Note] mysqld (mysqld 10.6.3-MariaDB-1:10.6.3+maria~focal) starting as process 1 ...
    storefront_1  | yarn run v1.22.5
    storefront_1  | $ ng serve --port 4201
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Number of pools: 1
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Using crc32 + pclmulqdq instructions
    database_1    | 2021-08-04  5:32:12 0 [Note] mysqld: O_TMPFILE is not supported on /tmp (disabling future attempts)
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Using Linux native AIO
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Initializing buffer pool, total size = 134217728, chunk size = 134217728
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Completed initialization of buffer pool
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: 128 rollback segments are active.
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Creating shared tablespace for temporary tables
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Setting file './ibtmp1' size to 12 MB. Physically writing the file full; Please wait ...
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: File './ibtmp1' size is now 12 MB.
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: 10.6.3 started; log sequence number 7169328; transaction id 56533
    database_1    | 2021-08-04  5:32:12 0 [Note] Plugin 'FEEDBACK' is disabled.
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Loading buffer pool(s) from /var/lib/mysql/ib_buffer_pool
    database_1    | 2021-08-04  5:32:12 0 [Warning] You need to use --log-bin to make --expire-logs-days or --binlog-expire-logs-seconds work.
    database_1    | 2021-08-04  5:32:12 0 [Note] Server socket created on IP: '0.0.0.0'.
    database_1    | 2021-08-04  5:32:12 0 [Note] Server socket created on IP: '::'.
    database_1    | 2021-08-04  5:32:12 0 [Warning] 'proxies_priv' entry '@% root@7c0ceb273f28' ignored in --skip-name-resolve mode.
    database_1    | 2021-08-04  5:32:12 0 [Note] mysqld: ready for connections.
    database_1    | Version: '10.6.3-MariaDB-1:10.6.3+maria~focal'  socket: '/run/mysqld/mysqld.sock'  port: 3306  mariadb.org binary distribution
    database_1    | 2021-08-04  5:32:12 0 [Note] InnoDB: Buffer pool(s) load completed at 210804  5:32:12
    server_1      | wait-for-it.sh: waiting 15 seconds for database:3306
    database_1    | 2021-08-04  5:32:13 3 [Warning] Aborted connection 3 to db: 'unconnected' user: 'unauthenticated' host: '172.19.0.4' (This connection closed normally without authentication)
    server_1      | wait-for-it.sh: database:3306 is available after 0 seconds
    database_1    | 2021-08-04  5:32:13 4 [Warning] Aborted connection 4 to db: 'unconnected' user: 'unauthenticated' host: '172.19.0.3' (This connection closed normally without authentication)
    worker_1      | wait-for-it.sh: database:3306 is available after 1 seconds
    server_1      | yarn run v1.22.5
    server_1      | $ ts-node ./src/index.ts
    worker_1      | yarn run v1.22.5
    worker_1      | $ ts-node ./src/index-worker.ts
    storefront_1  | - Generating browser application bundles...
    worker_1      | info 8/4/21, 5:32 AM - [Vendure Worker] Bootstrapping Vendure Worker (pid: 43)...
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Bootstrapping Vendure Server (pid: 41)...
    server_1      | info 8/4/21, 5:32 AM - [AssetServerPlugin] Creating asset server middleware
    server_1      | info 8/4/21, 5:32 AM - [EmailPlugin] Creating dev mailbox middleware
    server_1      | info 8/4/21, 5:32 AM - [AdminUiPlugin] Creating admin ui middleware (prod mode)
    server_1      | info 8/4/21, 5:32 AM - [RoutesResolver] HealthController {/health}:
    server_1      | info 8/4/21, 5:32 AM - [RouterExplorer] Mapped {/health, GET} route
    worker_1      | info 8/4/21, 5:32 AM - [JobQueue] Starting queue: apply-collection-filters
    worker_1      | info 8/4/21, 5:32 AM - [JobQueue] Starting queue: send-email
    worker_1      | info 8/4/21, 5:32 AM - [JobQueue] Starting queue: update-search-index
    server_1      | info 8/4/21, 5:32 AM - [NestApplication] Nest application successfully started
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] ================================================
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Vendure server (v1.1.3) now running on port 3000
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] ------------------------------------------------
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Shop API:     http://localhost:3000/shop-api
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Admin API:    http://localhost:3000/admin-api
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Asset server: http://localhost:3000/assets
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Dev mailbox:  http://localhost:3000/mailbox
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Admin UI:     http://localhost:3000/admin
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] ================================================
    storefront_1  | WARNING: The `make-container-max-widths` mixin has been deprecated as of v4.5.2. It will be removed entirely in v5.
    storefront_1  |     node_modules/bootstrap/scss/mixins/_deprecate.scss 8:5                          deprecate()
    storefront_1  |     node_modules/bootstrap/scss/mixins/_grid.scss 27:3                              make-container-max-widths()
    storefront_1  |     src/app/core/components/collections-menu/collections-menu.component.scss 16:13  @content
    storefront_1  |     node_modules/bootstrap/scss/mixins/_breakpoints.scss 62:7                       media-breakpoint-up()
    storefront_1  |     src/app/core/components/collections-menu/collections-menu.component.scss 13:5   root stylesheet
    storefront_1  |
    server_1      | warn 8/4/21, 5:33 AM - [Vendure Server] FORBIDDEN: error.forbidden
    server_1      | warn 8/4/21, 5:33 AM - [Vendure Server] FORBIDDEN: error.forbidden
    server_1      | warn 8/4/21, 5:33 AM - [Vendure Server] FORBIDDEN: error.forbidden
    storefront_1  | ✔ Browser application bundle generation complete.
    storefront_1  |
    storefront_1  | Initial Chunk Files                    | Names         |      Size
    storefront_1  | vendor.js                              | vendor        |   5.64 MB
    storefront_1  | main.js                                | main          |   1.55 MB
    storefront_1  | polyfills-es5.js                       | polyfills-es5 | 920.33 kB
    storefront_1  | polyfills.js                           | polyfills     | 467.89 kB
    storefront_1  | styles.css                             | styles        | 165.45 kB
    storefront_1  | runtime.js                             | runtime       |  12.23 kB
    storefront_1  |
    storefront_1  | | Initial Total |   8.72 MB
    storefront_1  |
    storefront_1  | Lazy Chunk Files                       | Names         |      Size
    storefront_1  | src_app_checkout_checkout_module_ts.js | -             | 405.97 kB
    storefront_1  | src_app_account_account_module_ts.js   | -             | 169.71 kB
    storefront_1  | common.js                              | common        |   1.83 kB
    storefront_1  |
    storefront_1  | Build at: 2021-08-04T05:33:15.503Z - Hash: f1082c49e274ff29e764 - Time: 56363ms
    storefront_1  |
    storefront_1  | ** Angular Live Development Server is listening on localhost:4201, open your browser on http://localhost:4201/ **
    storefront_1  |
    storefront_1  |
    storefront_1  | ✔ Compiled successfully.
    storefront_1  | - Generating browser application bundles...
    storefront_1  | ✔ Browser application bundle generation complete.
    storefront_1  |
    storefront_1  | 9 unchanged chunks
    storefront_1  |
    storefront_1  | Build at: 2021-08-04T05:33:18.254Z - Hash: 3d09564af23646535bcd - Time: 1912ms
    storefront_1  |
    storefront_1  | ✔ Compiled successfully.
    ```
4. Navigate to `http://localhost:3000/admin`. The username and password both are `superadmin`. Once you login, you should see the admin UI provided by vendure. But, there won't be any products or facets, or tax info, or anything. This is becuase out database is empty.
5. Fill the database.
    1. First make sure your `docker-compose up --build` command is still running.
    2. We need to get the docker container ID of the database. In GNU/Linux the command is:
        ```sh
        docker ps | grep mariadb | awk {print $1}
        ```
        This command gets all the running conatiners, then finds the one running the mariadb image, the prints out the first column (The ID)
    3. Use the `dump.sql` file to populate the database with data. In GNU/Linux, the comand is:
        ```sh
        docker exec -i $(docker ps | grep mariadb | awk {print $1}) sh -c 'exec mysql -uroot -pdb_pass' < dump.sql
        ```
        Make sure You run this command from the root of the project. If not, the specify the corect path of dump.sql. \
        Note: This command will only work if your shell is bash or zsh, or any shell which supports putting output of a command as a parameter to another command using the $() operator. \
        This command uses the dump.sql to populate the database.
    4. The Database is now populated!
6. Refresh the connection to `http://localhost:3000/admin`. You should now see dummy products, facets, collections, etc.
7. Check out `http://localhost:4201/`. This is the main UI, the end user will see. \
   Note: There seems to be quite a few bugs that need to be fixed in this UI.
8. Done! Enjoy

## Usage

Simply run `docker-compose up --build`. The logs themselves will show where to go! For e.g:

```
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] ================================================
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Vendure server (v1.1.3) now running on port 3000
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] ------------------------------------------------
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Shop API:     http://localhost:3000/shop-api
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Admin API:    http://localhost:3000/admin-api
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Asset server: http://localhost:3000/assets
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Dev mailbox:  http://localhost:3000/mailbox
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] Admin UI:     http://localhost:3000/admin
    server_1      | info 8/4/21, 5:32 AM - [Vendure Server] ================================================
```

and a bit later:

```
    storefront_1  | ** Angular Live Development Server is listening on localhost:4201, open your browser on http://localhost:4201/ **
```

That's it!

## How does this work?

#### Database

The Database is created using the docker-compose. Look at the first service in the `docker-compose.yml` file.

```yaml
# Database
database:
    image: mariadb:10.6.3-focal # we will be using Mariadb
    restart: always # restart the database in case the process ends
    environment:
        MYSQL_ROOT_PASSWORD: db_pass # set db password TODO: Change to more secure password
    volumes:
        # TODO: Change the below line
        # For e.g: ~/Desktop/Jewelify_project/mariadb:/var/lib/mysql
        - <insert your volume path here>:/var/lib/mysql
```

The database we will be using is [MariaDB](https://mariadb.org/). The docker image for MariaDB is hosted [here](https://hub.docker.com/_/mariadb). \
The environment variable `MYSQL_ROOT_PASSWORD` is resposible to set the root user's password (for the database). Using the volume, data is stored on the host machine, so even if you kill the docker conatiner, the data is not lost. The next time you start the docker container, you start of where you left! \
The reason MariaDB is used, is MySQL does not play nicely with docker. Also, MariaDB aims to compatible with MySQL, so you would not have any issues if you are familiar with MySQL.

#### Woker and server

The worker's and server's conatiners are both built from `frontend/Dockerfile`. Take a look at this file:

```yaml
FROM node:14

WORKDIR /usr/src/Jewelify_project

COPY package.json ./
COPY yarn.lock ./
RUN yarn
COPY ./ ./
RUN chmod +x /usr/src/Jewelify_project/wait-for-it.sh
```

It uses the node 14 base image (as that is the node version the vendure server and vendure storefront are compatible with).
Then it sets the working dir.
Then it copies the `package.json` and `yarn.lock` file, to install all dependencies. Then it copies over all other files. Then, it changes the persions of the `wait-for-it.sh` script to executable. This script was got from [this example repo](https://github.com/vendure-ecommerce/vendure-docker-compose)
Lastly, the default command is set using the docker compose.

#### Storefront

The Storefront's conatiners are built from `backend/Dockerfile`. Let's have a look:

```yaml
FROM node:14

WORKDIR /usr/src/Jewelify_project_frontend/

COPY ./package.json ./
COPY ./yarn.lock ./

RUN yarn

COPY ./ ./

CMD yarn start
```

It uses the node 14 base image (as that is the node version the vendure server and vendure storefront are compatible with)
Then, it sets the working directory.
Then, it copies the `package.json` and `yarn.lock` files, to the container to install ll dependencies.
Then, it copies over all other files.
Then, it sets the default command to `yarn start`

In the `docker-compose.yml`:

```yaml
# define storefront (The main UI the end user sees)
storefront:
    # define where and how the docker conatiner should be built
    build:
        context: ./frontend
        dockerfile: Dockerfile
    # set network_mode to host
    # TODO: Find a way to avoid this, by editing the server API location in the frontend code
    # Ideally we would like to only expose port 4201
    network_mode: host
```

The "sub-project" directory is specified along with the Dockerfile.
Currently, the storefront access the API to the server at `http://localhost:3000/`, but there is no API running at that port **inside that container**. As a workaround, `network_mode` is set to host. Now, there is an API running at `http://localhost:3000/` because the docker conatiner for the server as exposed the port 3000 to the host (in the `docker-compose.yml`).

#### Try On Integration

This is currently non functional. It is planned to open a HTTP API so the Storefront can access. This is the backend for the Try On feature.

## Deploy

How are we going to deploy this application? The vendure server is running at port 3000, the storefront is running at port 4201, the Try On backed would be running at another port (maybe 31415). How should we bundle all of this? \
After building the storefront for production (`yarn build`), it can be deployed with the server at port 3000. But, what about the Try On backend. Nginx to the rescue! Using nginx we can route the necessary API calls to the Try On backend, while other API calls to the vendure server. In this way, we can deploy the entire application in the same domain!
