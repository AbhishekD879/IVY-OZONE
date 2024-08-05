import { Injectable } from '@angular/core';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';


@Injectable({
    providedIn: 'root'
})
export class MaxPayOutErrorService {
    maxPayOutSubscription: any;
    maxPayOutTooltip: string;
    toolTipArgs: { [key: string]: string };
    link: string;
    click: string;
    maxPayFlag: boolean = false;
    private readonly MAX_PAYOUT_TOOLTIP = 'MaxPayToolTip';

    constructor(private cmsService: CmsService) {
        this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
            if (config && config.maxPayOut) {
                this.maxPayFlag = config.maxPayOut.maxPayoutFlag;
            }
        });
        this.setMaxPayOutTooltip();
    }
    /**
  * Get MaxPayout tooltip Values
  * @returns void
  */
    private setMaxPayOutTooltip(): void {
        this.maxPayOutSubscription = this.cmsService.getFeatureConfig(this.MAX_PAYOUT_TOOLTIP).subscribe(
            (config: ISystemConfig) => {
                if (config && config.enabled) {
                    this.maxPayOutTooltip = config.title;
                    this.link = config.link;
                    this.click = config.click;
                    this.maxPayOutTooltip = this.maxPayOutTooltip.length > 50 ?
                        `${this.maxPayOutTooltip.substring(0, 50)}...` : this.maxPayOutTooltip;
                    this.toolTipArgs = {
                        maxpayout: this.maxPayOutTooltip,
                        link: this.link,
                        click: this.click
                    };
                }
            });
    }
}
