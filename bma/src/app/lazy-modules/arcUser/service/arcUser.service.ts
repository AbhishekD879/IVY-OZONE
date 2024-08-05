import { Injectable } from '@angular/core';
import { ClaimsService, UserService } from '@frontend/vanilla/core';
import { CmsService } from '@app/core/services/cms/cms.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { IArcUserData, IsportsActions } from '../model/arcUser-model';
import { APP_LOADED_SUBCRIBER, ARC_CROSSSELL, ARC_QUICKBET, ARC_USER_CONSTANTS } from '../constants/arcUser-constants';
import { ISystemConfig } from '@app/core/services/cms/models/system-config';
@Injectable({
  providedIn: 'root'
})

export class ArcUserService {
  arcPrimaryReason: string;
  arcRiskBandLevel: string;
  sportAction: boolean;
  quickbet: boolean = false;
  crossSellRemoval: boolean = false;
  arcUserConstants: string[] = ARC_USER_CONSTANTS;
  constructor(
    private pubSubService: PubSubService,
    private claimsService: ClaimsService,
    private userService: UserService,
    private cmsService: CmsService
  ) {
    this.pubSubService.subscribe(APP_LOADED_SUBCRIBER, [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.APP_IS_LOADED, this.pubSubService.API.RELOAD_COMPONENTS], () => {
      this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
        if(config?.ArcConfig && config.ArcConfig.enableArc) {
          this.initialData();
        }
      });
    });
  }
  /**
   * Get CMS data for the Arc User
   * @returns void
   */
     fetchArcCms(): void {
      this.cmsService.formArcData(this.arcPrimaryReason, this.arcRiskBandLevel).subscribe((arcConfig: IArcUserData) => {
        if (arcConfig && arcConfig.enabled) {
          this.crossSellRemoval = arcConfig.sportsActions.find((sportsItem:IsportsActions) => sportsItem.action === this.arcUserConstants[0])?.enabled || false;
          this.pubSubService.publish(ARC_CROSSSELL, this.crossSellRemoval);
          this.quickbet = arcConfig.sportsActions.find((sportsItem:IsportsActions) => sportsItem.action === this.arcUserConstants[1])?.enabled || false;
          if(this.quickbet){
            this.pubSubService.publish(ARC_QUICKBET,this.pubSubService.API.QUICKBET_PANEL_CLOSE);
          }
        }
     });
  }

  /**
   * @returns void
   */
  private initialData(): void {
    this.arcPrimaryReason = this.claimsService.get(this.arcUserConstants[2]);
    this.arcRiskBandLevel = this.claimsService.get(this.arcUserConstants[3]);
    if (this.arcPrimaryReason && this.arcRiskBandLevel && this.userService.isAuthenticated) {
      this.fetchArcCms();
    }
  }

}
