import { enableProdMode, importProvidersFrom, NgZone } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app.module';
import environment from '@environment/oxygenEnvConfig';
import { bootloader, AppComponent, provideVanillaCore, runOnAppInit } from '@frontend/vanilla/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideLoaders } from '@frontend/loaders';
import { FlagSourceService } from '@app/core/services/flagSource/flag-source.service';

declare let PACKAGEVERSIONS: any;
window['VERSIONS'] = PACKAGEVERSIONS;

if (environment.production) {
  enableProdMode();
}

const storedCMSInit = localStorage.getItem('OX.cmsInit');
const cmsInitUrl = `${ environment.CMS_ENDPOINT }/${ environment.brand }/initial-data/${ environment.CURRENT_PLATFORM }`,
  cmsInitPromise = (storedCMSInit) ? Promise.resolve(JSON.parse(storedCMSInit)) : fetch(cmsInitUrl).then(data => data.json());

const cmsConfigProvider = {
  provide: 'CMS_CONFIG',
  useValue: cmsInitPromise
};

bootloader().then(() => { 
  platformBrowserDynamic([cmsConfigProvider]);
  bootstrapApplication(AppComponent, {
    providers: [provideVanillaCore(), provideLoaders(), runOnAppInit(FlagSourceService), importProvidersFrom(AppModule),
      {
        provide: NgZone,
        useValue: new NgZone({ shouldCoalesceEventChangeDetection: environment.ISEVENTCOALESCING })
      }],
  }).catch((err) => console.error(err));
});
