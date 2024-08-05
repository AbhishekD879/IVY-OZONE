import { Component, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { ModuleRibbonComponent } from '@app/shared/components/moduleRibbon/module-ribbon.component';
import { ModuleRibbonService } from '@app/core/services/moduleRibbon/module-ribbon.service';
import { SessionService } from '@authModule/services/session/session.service';
import { Location } from '@angular/common';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { CmsService } from '@core/services/cms/cms.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { SegmentEventManagerService } from '@app/lazy-modules/segmentEventManager/service/segment-event-manager.service';

  @Component({
    selector: 'module-ribbon',
    templateUrl: 'module-ribbon.component.html'
  })

  export class LadbrokesModuleRibbonComponent extends ModuleRibbonComponent implements OnInit {
    private moduleName = 'ModuleRibbon';
    constructor(
      protected location: Location,
      protected ribbonService: ModuleRibbonService,
      protected user: UserService,
      protected pubSubService: PubSubService,
      protected router: Router,
      protected sessionService: SessionService,
      protected cmsService: CmsService,
      private germanSupportService: GermanSupportService,
      device: DeviceService,
      sessionStorageService: SessionStorageService,
      bonusSuppressionService: BonusSuppressionService,   
    private segmentEventManagerService: SegmentEventManagerService
    ) {
      super(location, ribbonService, user, pubSubService, router, sessionService, cmsService,device,sessionStorageService, bonusSuppressionService);
    }

    ngOnInit(): void {
      super.ngOnInit();

      if (!this.user.status) {
        this.filterNextRaces();
      }

      this.pubSubService.subscribe(this.moduleName, [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN], () => {
          this.user.bppToken && this.segmentEventManagerService.getOtfSegmentUserStatus();
          this.filterModulesBasedOnRgyellow();
      });
    }

    protected addPrivateMarketTab(): void {
      if (this.user && this.user.status && !this.isOnPrivateMarketTab() && !this.privateMarketTabCreated) {
        this.privateMarketTabCreated = true;
        this.ribbonService.getPrivateMarketTab(_.clone(this.ribbon)).subscribe(result => {
          this.moduleList = [...result];
          if (!this.isRedirectNeeded()) {
            this.filterNextRaces();
          }
          this.setLocation();
        }, () => this.privateMarketTabCreated = false);
      }
    }

    private isRedirectNeeded() {
      return this.canRedirectToHomePage() || this.canRedirectToPrivateMarketsTab();
    }

    /**
     * Hide Next Races Tab on ribbon for German Users
     */
    private filterNextRaces(): void {
      this.moduleList = this.germanSupportService.toggleItemsList(this.moduleList, 'filterNextRaces');
      this.filterModulesBasedOnRgyellow();
    }
  }
