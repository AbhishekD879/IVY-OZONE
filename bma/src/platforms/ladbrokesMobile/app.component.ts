import { OnInit, OnDestroy, Component, ApplicationRef, NgZone } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { NavigationEnd, Router, Event, NavigationStart } from '@angular/router';
import decorateTick from './../app-decorator';
import { Subscription } from 'rxjs';
//import { CasinoPlatformLoaderService } from '@casinocore/loader';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@coreModule/services/cms/models';

@Component({
  selector: 'root-app',
  templateUrl: './app.component.html'
})
export class RootComponent implements OnInit, OnDestroy {
  isHomePage: boolean = true;
  isProduction = environment.production;
  protected routeChangeListener: Subscription;

  constructor(
    private applicationRef: ApplicationRef,
    private ngZone: NgZone,
    private pubSubService: PubSubService,
    private router: Router,
    //private casinoPlatformLoaderService: CasinoPlatformLoaderService,
    private cmsService: CmsService
  ) {
    decorateTick(this.applicationRef, this.ngZone, this.pubSubService, this.router);
  }

  ngOnInit(): void {
    this.checkHomeUrl();
    this.routeChangeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationStart || event instanceof NavigationEnd) {
        this.checkHomeUrl();
      }
    });
  }

  checkHomeUrl() {
    const currentURL: string = this.router.url.split('?')[0];
    this.isHomePage = (currentURL === '/' || currentURL.indexOf('/home') > -1) ? true : false;
  }

  ngAfterViewInit(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      const gamingEnabled = config.GamingEnabled || {};
      const { enabledGamingOverlay } = gamingEnabled;
        if (enabledGamingOverlay) {
        //  this.casinoPlatformLoaderService.loadCasinoPlatformModule(process.env.NODE_ENV, { disableCasinoLocalStorage: true });
        }
    });
  }

  ngOnDestroy(): void {
    this.routeChangeListener && this.routeChangeListener.unsubscribe();
  }
}
