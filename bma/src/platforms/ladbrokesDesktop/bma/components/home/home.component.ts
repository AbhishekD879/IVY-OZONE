import { Component, ChangeDetectorRef, OnInit, OnDestroy } from '@angular/core';

import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { CmsService } from '@coreModule/services/cms/cms.service';

import * as _ from 'underscore';
import { HomeComponent } from '@bma/components/home/home.component';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { IDesktopHomePageOrder } from '@app/core/services/cms/models/system-config';
import { UserService } from '@app/core/services/user/user.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';


@Component({
  selector: 'home',
  templateUrl: 'home.component.html'
})

export class DesktopHomeComponent extends HomeComponent implements OnInit, OnDestroy {
  isGermanUser: boolean;
  isFanzoneEnabled = true;

  moduleOrder: Array<[string,number]> = new Array<[string,number]>();
  constructor(
    protected cd: ChangeDetectorRef,
    protected cmsService: CmsService,
    protected dynamicComponentLoader: DynamicLoaderService,
    protected germanSupportService: GermanSupportService,
    protected pubSubService: PubSubService,
    protected freeRideHelperService: FreeRideHelperService,
    protected user: UserService,
    protected bonusSuppressionService: BonusSuppressionService
  ) {
    super(cmsService, dynamicComponentLoader, pubSubService);

  }

  ngOnInit() {
    super.ngOnInit();
    this.isGermanUser = this.germanSupportService.isGermanUser();
    this.pubSubService.subscribe('HomeComponent',
      [
        this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN,
        this.pubSubService.API.SESSION_LOGOUT
      ], () => {
        this.isGermanUser = this.germanSupportService.isGermanUser();
        this.pubSubService.subscribe('HomeComponent', this.pubSubService.API.FANZONE_DATA, (fanzone) => {
          this.isFanzoneEnabled = false;
          this.cd.detectChanges()
          this.isFanzoneEnabled = true;
        });
      }
    );
    const homePageModules: IDesktopHomePageOrder = {inPlay: 0, nextRace: 0, yourCall: 0, featured: 0};
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      const modules = (config && config.DesktopHomePageOrder) ? Object.assign(homePageModules, config.DesktopHomePageOrder) : homePageModules;
      this.moduleOrder = Object.entries(modules).sort((a: Array<any>, b: Array<any>) => b[1]-a[1]);
    });
  }

  ngOnDestroy() {
    this.pubSubService.unsubscribe('HomeComponent');
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
