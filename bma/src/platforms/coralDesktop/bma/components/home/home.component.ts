import { Component } from '@angular/core';

import { CmsService } from '@core/services/cms/cms.service';

import * as _ from 'underscore';
import { HomeComponent } from '@bma/components/home/home.component';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { IDesktopHomePageOrder } from '@app/core/services/cms/models/system-config';
@Component({
  selector: 'home',
  templateUrl: 'home.component.html'
})

export class DesktopHomeComponent extends HomeComponent {
  moduleOrder: Array<[string,number]> = new Array<[string,number]>();
  constructor(
    protected cmsService: CmsService,
    protected dynamicComponentLoader: DynamicLoaderService,
    protected pubSubService: PubSubService
  ) {
    super(cmsService, dynamicComponentLoader,pubSubService);
  }

  ngOnInit() {
    super.ngOnInit();
    const homePageModules: IDesktopHomePageOrder = {inPlay: 0, nextRace: 0, yourCall: 0, featured: 0};
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      const modules = (config && config.DesktopHomePageOrder) ? Object.assign(homePageModules, config.DesktopHomePageOrder) : homePageModules;
      this.moduleOrder = Object.entries(modules).sort((a: Array<any>, b: Array<any>) => b[1]-a[1]);
    });
  }

  /**
   * Says whether to show ribbon module or not
   * @return {boolean}
   */
  showRibbon(): boolean {
    const id: string = 'tab-build-your-bet';
    const ribbon = _.findWhere(this.ribbon, { id });

    return ribbon ? ribbon.visible && (ribbon.showTabOn === 'both' || ribbon.showTabOn === 'desktop') : false;
  }
}
