import { Component, Input, OnInit } from "@angular/core";
import { SignpostingCMSConfig, SelectThresholdTypes } from "app/lazy-modules/signposting/models/freebet-signposting.model";
import { SignpostingCmsService } from 'app/lazy-modules/signposting/services/signposting.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { UserService } from '@core/services/user/user.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
    selector: 'freebet-signposting',
    templateUrl: './freebet-signposting.component.html',
    styleUrls: ['./freebet-signposting.component.scss']
})

export class FreebetSignpostingComponent implements OnInit {

    @Input() public betInfo: any;
    @Input() public signpostingTitle: string = 'eachway';
    @Input() public eventLocation: string = 'betslip';
    public isSignpostingEnabled: boolean = false;
    public signpostingCMSConfig: SignpostingCMSConfig;
    public signpostingMessage: string;
    public selectThresholdTypeEnum: any = SelectThresholdTypes;
    public brand: string = environment.brand;

    /**
     * Constructor
     * @param signpostingCmsService: SignpostingCmsService
     */
    constructor(
        private signpostingCmsService: SignpostingCmsService,
        private gtmService: GtmService,
        private userService: UserService) {
    }

    /**
     * ngOnInit
     */
    ngOnInit(): void {
        if (this.signpostingCmsService.freeBetSignpostingArray) {
            const res: SignpostingCMSConfig[] = this.signpostingCmsService.freeBetSignpostingArray;
            this.onLoadSignpostingCheck(res);
        }
    }

    /**
     * Validates and displays signposting
     * @param res: SignpostingCMSConfig[]
     */
    private onLoadSignpostingCheck(res: SignpostingCMSConfig[]): void {

        this.signpostingCMSConfig = res.find(item => item.title.toLowerCase() === this.signpostingTitle.toLowerCase());

        if (this.signpostingCMSConfig && this.signpostingCMSConfig.isActive && this.signpostingCMSConfig.price
            && this.betInfo && this.betInfo.price && this.betInfo.price.priceNum && this.betInfo.price.priceDen) {
            let oddsDec: number;
            if (this.userService.oddsFormat === 'dec' && this.betInfo.price.priceDec) {
                oddsDec = +this.betInfo.price.priceDec;
            } else {
                oddsDec = +this.betInfo.price.priceNum / +this.betInfo.price.priceDen;
                oddsDec = oddsDec + 1;
            }

            if (this.signpostingCMSConfig.price.priceType === this.selectThresholdTypeEnum.Decimal && this.signpostingCMSConfig.price.priceDec) {
                if (oddsDec <= +this.signpostingCMSConfig.price.priceDec) {
                    this.isSignpostingEnabled = true;
                }
            } else if (this.signpostingCMSConfig.price.priceType === this.selectThresholdTypeEnum.Fractional
                && this.signpostingCMSConfig.price.priceNum && this.signpostingCMSConfig.price.priceDen) {
                const thresholdDec: number = +this.signpostingCMSConfig.price.priceNum / +this.signpostingCMSConfig.price.priceDen;
                if (oddsDec <= thresholdDec) {
                    this.isSignpostingEnabled = true;
                }
            }

            if (this.isSignpostingEnabled) {
                this.signpostingMessage = this.signpostingCMSConfig.signPost;
                this.onLoadGATrackingCheck();
            }
        }
    }

    /**
     * Validates the location event and initiates GA tracking 
    */
    private onLoadGATrackingCheck(): void {
        if (this.eventLocation === 'betslip' && !this.signpostingCmsService.gtmLoadingStatus.betslip) {
            this.setFreeBetGtmData();
            this.signpostingCmsService.gtmLoadingStatus.betslip = true;
        } else if (this.eventLocation === 'quickbet' && !this.signpostingCmsService.gtmLoadingStatus.quickbet) {
            this.setFreeBetGtmData();
            this.signpostingCmsService.gtmLoadingStatus.quickbet = true;
        }
    }

    /**
    * set GA tracking object
    */
    private setFreeBetGtmData(): void {
        const gtmData = {
            'event': 'contentView',
            'component.CategoryEvent': 'promotions',
            'component.LabelEvent': 'each way free bet',
            'component.ActionEvent': 'load',
            'component.PositionEvent': 'not applicable',
            'component.LocationEvent': this.eventLocation === 'quickbet' ? 'quick bet' : 'betslip',
            'component.EventDetails': 'each way free bet info msg',
            'component.URLClicked': 'not applicable',
            'sportID': this.eventLocation === 'quickbet' ? this.betInfo.categoryId : this.betInfo.sportId
        };

        // undefined sportID
        if (!gtmData.sportID) {
            gtmData.sportID = 'not applicable';
        }

        this.gtmService.push(gtmData.event, gtmData);
    }
}