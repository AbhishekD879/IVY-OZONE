import { HttpClientModule } from '@angular/common/http';
import {
  Injector,
  NgModule,
  NgModuleFactory,
  NO_ERRORS_SCHEMA,
  CUSTOM_ELEMENTS_SCHEMA,
  Compiler
} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { STORE_PREFIX, runOnAppInit } from '@frontend/vanilla/core';
import { BmaModule } from '@bmaModule/bma.module';
import { CoreModule } from '@coreModule/core.module';
import { DesktopModule } from '@desktopModule/desktop.module';
import { SharedModule } from '@sharedModule/shared.module';
import { VanillaInitModule } from '@vanillaInitModule/vanilla-init.module';
import { AppRoutingModule } from '@coralDesktop/app-routing.module';
import { RootComponent } from '@coralDesktop/app.component';
import { LocaleService } from '@coreModule/services/locale/locale.service';
import * as sbDesktopLangData from '@localeModule/translations/en-US/sbdesktop.lang';
import { HostAppBootstrapper } from '@app/host-app/host-app-bootstrapper.service';
import { CoralSportsClientConfigModule } from '@app/client-config/client-config.module';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
@NgModule({
  imports: [
    AppRoutingModule,
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    CoreModule,
    VanillaInitModule,
    SharedModule.forRoot(),
    BmaModule,
    DesktopModule,
    CoralSportsClientConfigModule.forRoot()
  ],
  declarations: [
    RootComponent
  ],
  providers: [
    { provide: STORE_PREFIX, useValue: 'coralsports.' },
    runOnAppInit(HostAppBootstrapper)
  ],
  bootstrap: [
  ],
  schemas: [NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule {
  constructor(
    private injector: Injector,
    private localeService: LocaleService,
    private compiler: Compiler,
    private routingState: RoutingState
  ) {
    this.routingState.loadRouting();
    const paths = {
      '@lazy-modules/locale/translation.module': import('@lazy-modules/locale/translation.module')
                                                  .then(module => module.TranslationModule),
      '@lazy-modules/performanceMark/performanceMark.module': import('@lazy-modules/performanceMark/performanceMark.module')
                                                                .then(module => module.PerformanceMarkModule),
      '@lazy-modules/awsFirehose/awsFirehose.module': import('@lazy-modules/awsFirehose/awsFirehose.module')
      .then(module => module.AWSFirehoseModule),
      '@lazy-modules/arcUser/arcUser.module': import('@lazy-modules/arcUser/arcUser.module')
        .then(module => module.ArcUserModule),
      '@lazy-modules/serviceClosure/service-closure.module': import('@lazy-modules/serviceClosure/service-closure.module')
      .then(module => module.ServiceClosureModule),
      '@lazy-modules/betpackPage/betpack-cms.module': import('@lazy-modules/betpackPage/betpack-cms.module')
      .then(module => module.BetpackCmsModule),
      '@lazy-modules/flagSource/flag-source.module': import('@lazy-modules/flagSource/flag-source.module')
      .then(module => module.FlagSourceModule)
    };

    for (const path in paths) {
      if (path) {
        paths[path].then((loadedModule: any) => {
          return this.loadModuleFactory(loadedModule);
        }).then((moduleFactory: NgModuleFactory<any>) => moduleFactory.create(this.injector));
      }
    }

    this.localeService.setLangData(sbDesktopLangData);
  }

  loadModuleFactory(loadedModule: any): NgModuleFactory<any> {
    if (loadedModule instanceof NgModuleFactory) {
      return loadedModule;
    } else {
      return this.compiler.compileModuleAsync(loadedModule) as any;
    }
  }
}
