# Oxygen
This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 6.2.2

## Getting Started:

Welcome to the prepository of the BMA/Invictus/OXYGEN application. This project based on `Angular6`.

- Project documentation lives here [https://confluence.egalacoral.com](https://confluence.egalacoral.com)
- Tasks and bugs lives here [Jira](https://jira.egalacoral.com)

## Dependencies:

Tools needed to run this app:
* `node 11.15.0`, `npm`, `Apache`

#### Apache:
Please follow this [instruction](https://bitbucket.org/symphonydevelopers/bma/wiki/Setup%20instructions) to install and configure Apache on your platform.

#### Running without Apache:
If you don't want to use Apache for local development - you can skip steps **3** and **6** and read step **9** instead in this [instruction](https://bitbucket.org/symphonydevelopers/bma/wiki/Setup%20instructions).

## Installing

After installing and configuring all dependencies. Clone this repository and install all project develop dependency.

- `clone this repo`
- `cd bma`
- `npm install`
- as bma project is inside `vanilla coralsports project`, after install remove folders node_modules/@angular , node_modules/@vanilla  

## Running the App with Development server

**Important!** If you don't use Apache for local development then you need to run next commands with superuser permission. `$ sudo npm run ...`

**Coral**:

Run `npm run start serveCoralMobile --env.environment={environment}` for a dev server. Navigate to `https://bm-tst1.coral.co.uk/`.

Run `npm run start serveCoralDesktop --env.environment={environment}` for a dev server. Navigate to `https://bm-tst1.coral.co.uk/`.

**Ladbrokes**:
         
Run `npm run start serveLadbrokesMobile --env.environment={environment}` for a dev server. Navigate to `https://bm-tst1.ladbrokes.com/`.

Run `npm run start serveLadbrokesDesktop --env.environment={environment}` for a dev server. Navigate to `https://bm-tst1.ladbrokes.com/`.


## Running Unit Tests

Run `npm run start testWatch` to start tests and serve unit tests webserver. Navigate to `http://0.0.0.0:9876/`  

## Running Lint

Run `npm run start lint` to run tslint check.


## Build Application

Build Application possible with webpack from `vanilla coralsports` folder.

## Generate environment profiles

Run `generateBrandProfiles` to generate all profiles for all platforms and brands.

Note: you should run any build script at least once before, to create ./build/Web/ClientDist folder in your root.
When script done you'll find coralMobile, coralDesktop, ladbrokesMobile, ladbrokesDesktop folders in ClientDist with all profiles generated.

## Budgets

Run `budgets` script to check budle size of each bundle in ClientDist folder.

Before running this script you need to make any build (e.g npm run buildLadbrokesDesktop - so then you'll have ./build/Web/ClientDist/ladbrokesDesktop/ build folder)

If budgets passed you'll see `Budgets passed.` message, otherwise you will see each file difference.

## Unit Tests Known Issues
As our `testWatch` task is running within `CoralMobile` profile, the only change for file replacement should be under `projects/coralMobile/architect.ts`. 
Of course, if it appears that tests are going to be run within other profiles, we should do the following:

- Add code snippet given below to the relevant profile in `projects/${brand}/architect.ts` under `test` field for `coralsports` project:

`'fileReplacements': [{'replace': 'src/environments/oxygenEnvConfig.ts', 'with': 'src/environments/environment.mock.ts' }],`

- Run respective build task for a brand to update `angular.json` in the root folder of the project for `coralsports`

Also, if tests are failing because of the `environment` variable, you should do the following:

1. Import `environment` variable like this: `import * as env from '@environment/oxygenEnvConfig';`
2. In **_global_** `describe` for the spec or in `beforeEach` declare and initialise `environment` variable: `const environment = env as any`;

