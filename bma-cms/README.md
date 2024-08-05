#### I. SETUP

## Prerequisites

1. Make sure what GraphicsMagic is installed.
You can check this by typing "gm" into terminal.
```
brew install graphicsmagick
```

2. Node compatible known version is v6.9.1. 
Install or change node to that version
https://nodejs.org/download/release/v6.9.1/

## Installation

get latest version from Bitbucket:
https://bitbucket.org/symphonydevelopers/bma-cms/overview

```
$ cd ./bma-cms
$ git submodule update --init --recursive
```
Install all node modules in project root directory:
```
$ npm install
```
Go to submodule and install node modules
```
$ cd bma-betstone
$ npm install
```
Go to angular folder and run bower install command:
```
$ cd public/js/lib/angular
$ bower install
```

IMPORTANT! In case you already did npm install with other node version,
you need remove node modules in root directory and bma-betstone module
```
rm -rd node_modules/
```
 


## Database

1. Install MongoDB.
Installation instruction for Mac: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/

2. Start MongoDB.

3. Fill database with data.

 - If you restore database from dump, be careful with Brands collection (Admin->Brands in CMS UI).
By using configs from other environment, you can affect Akamai folders used by other developers.

 - If you don't restore database from dump, empty "bma" database with default user will be created.

Tip: Use Robomongo or Mongobooster as MongoDB GUI.
Tip: Ping TL or Devops for database dump.
Tip: You can create dump from next database
```
mongo-cms-dev-phoenix.symphony-solutions.eu:27017
```

## Starting app

Set Akamai environment variables.

Option 1. Run Grunt build:
```
$ cd bma-cms
$ grunt serve
```
This allows to debug Node with Chrome inspector (debugging works only on Node 6.3.1)

Option 2. Run npm start
```
$ cd bma-cms
$ npm start
```

Tip: "grunt serve" task copies env.json to .env file, which is eventually used by app.

Open http://localhost:3000/keystone/ in your browser.

Authenticate with test@admin.coral.co.uk/admin


#### II. GENERAL INFORMATION

## Project structure

CMS relies on a customized fork of the KeystoneJS project, referred to as Betstone.
KeystoneJS: http://keystonejs.com/

Betstone is a Git submodule, located in bma-cms/bma-betstone folder.
Git submodules: http://git-scm.com/book/en/v2/Git-Tools-Submodules

This means there are two repositories:
https://bitbucket.org/symphonydevelopers/bma-cms
https://bitbucket.org/symphonydevelopers/bma-betstone (submodule)

Branches used by dev build:
bma-betstone - "master"
bma-cms - "develop"

If bma-betstone master branch was updated, you should do the following:
cd [path to /bma-cms]
git add bma-betstone (pointer to latest bma-betstone commit)
git commit -m 'betstone sync'
git push origin develop

## PNG/JPG images and icons

Some images are saved locally to "bma-cms/public/images/uploads".

CMS has two strategies for working with images:
 - "type: Types.AkamaiFile" - original and resized versions of image are stored only on Akamai,
 - "type: Types.LocalFilesome" -  original is stored locally, resized versions - locally and on Akamai.
Second strategy is a leftover from time, when CMS generated image sprites (later sprites were replaced by SVG).

## SVG icons

Original SVG files are stored locally.
Processed SVG files are stored as strings in database.





