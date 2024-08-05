import { Component, OnInit } from '@angular/core';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IFeaturedModule } from '@featured/components/featured-tab/featured-module.model';
import { Observable } from 'rxjs';
import { LAZY_LOAD_ROUTE_PATHS } from '@bma/constants/lazyload-route-paths.constant';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'home',
  templateUrl: 'home.component.html'
})

export class HomeComponent extends AbstractOutletComponent implements OnInit {
  femData: any;
  ribbon: IFeaturedModule[];
  isEnhancedMultiplesEnabled: boolean = false;
  bannerHome: string;
  private readonly title = 'HomeModuleComponent';
  brand: string = environment.brand;

  constructor(
    private cms: CmsService,
    protected dynamicComponentLoader: DynamicLoaderService,
    protected pubSubService: PubSubService
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    this.bannerHome = LAZY_LOAD_ROUTE_PATHS.home;
    this.moduleRibbonData();
    this.pubSubService.subscribe(this.title, [this.pubSubService.API.SEGMENTED_INIT_FE_REFRESH], () => {
      this.moduleRibbonData();
    });
  }

  moduleRibbonData() {
    this.cms.getRibbonModule().subscribe((initialData: { getRibbonModule: IFeaturedModule[]; getMMOutcomesByEventType: any; }) => {
      // to avoid this the bottle neck and having 500 error b/c of e.g.
      // banners have not been loaded.
      this.femData = initialData.getMMOutcomesByEventType;
      this.ribbon = initialData.getRibbonModule;

      this.hideSpinner();
    }, () => {
      this.showError();
    });
    this.getIsEnhancedMultiplesEnabled().subscribe((isEnhancedMultiplesEnabled: boolean) => {
      this.isEnhancedMultiplesEnabled = isEnhancedMultiplesEnabled;
    });
  }

  private getIsEnhancedMultiplesEnabled(): Observable<boolean> {
    return this.cms.getToggleStatus('EnhancedMultiples');
  }
}
