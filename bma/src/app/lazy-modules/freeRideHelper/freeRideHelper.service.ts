import { Injectable } from '@angular/core';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { CmsService } from '@core/services/cms/cms.service';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IFreeRideCampaign } from '@lazy-modules/freeRide/models/free-ride';
import { FREE_RIDE_CONSTS } from '@lazy-modules/freeRide/constants/free-ride-constants';
import { ISystemConfig } from '@core/services/cms/models';
import environment from '@environment/oxygenEnvConfig';

@Injectable({
    providedIn: 'root'
})
export class FreeRideHelperService {
    CMS_ENDPOINT: string;
    showFRBannerOnSportsPages: string[];
    activeCampaign: IFreeRideCampaign;
    module: string = FREE_RIDE_CONSTS.FREE_RIDE_MODULE;
    brand: string = environment.brand;

    constructor(
        public freeBetsService: FreeBetsService,
        public sessionStorage: SessionStorageService,
        public cmsService: CmsService,
        public pubSubService: PubSubService,
        protected http: HttpClient
    ) {
        this.CMS_ENDPOINT = environment.CMS_ENDPOINT;
        this.pubSubService.subscribe(this.module, this.pubSubService.API.SESSION_LOGIN, () => {
            this.sessionStorage.get(FREE_RIDE_CONSTS.FREERIDE_DETAILS) && this.sessionStorage.remove(FREE_RIDE_CONSTS.FREERIDE_DETAILS);
            this.sessionStorage.get(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA) && this.sessionStorage.remove(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA);
        });
        this.pubSubService.subscribe(this.module, this.pubSubService.API.SESSION_LOGOUT, () => {
            this.sessionStorage.get(FREE_RIDE_CONSTS.FREERIDE_DETAILS) && this.sessionStorage.remove(FREE_RIDE_CONSTS.FREERIDE_DETAILS);
            this.sessionStorage.get(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA) && this.sessionStorage.remove(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA);
        });
        this.freeBetsService.isFRFreeBets.subscribe((freeBetData) => {
            const freeBetDataLength =  Object.keys(freeBetData).length;
            if (freeBetDataLength && freeBetData.tokenId) {
                const freeBetResp = {
                    freeBetExpiryDate: freeBetData.freebetTokenExpiryDate,
                    freeBetTokenId: freeBetData.freebetTokenId
                };
                this.sessionStorage.set(FREE_RIDE_CONSTS.FREERIDE_DETAILS, JSON.stringify(freeBetResp));
                !this.sessionStorage.get(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA) && this.getFreeRide().subscribe((campaign: IFreeRideCampaign) => {
                    this.activeCampaign = JSON.parse(JSON.stringify(campaign));
                    this.sessionStorage.set(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA, JSON.stringify(campaign));
                });
            }
        });
        this.freeRideOnSportsPages();
    }

    /**
     * makes get data to the provided url
     * @param {string} url
     * @param {any} params
     * @returns {Observable<HttpResponse<T>>}
     */
    protected getData<T>(url: string, params: any = {}): Observable<HttpResponse<T>> {
        return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/${url}`, {
            observe: 'response',
            params: params
        });
    }

    /**
     * call to get campaign data
     * @returns {Observable<IFreeRideCampaign[]>}
     */
    public getFreeRideCampaign(): Observable<IFreeRideCampaign[]> {
        return this.getData(FREE_RIDE_CONSTS.FREE_RIDE_CAMPAIGN).pipe(
            map((campData: HttpResponse<IFreeRideCampaign[]>) => campData.body));
    }

    /**
     * returns active campaign
     * @param {IFreeRideCampaign[]} campaignList
     * @returns {IFreeRideCampaign}
     */
    public getFreeRideActiveCampaign(campaignList: IFreeRideCampaign[]): IFreeRideCampaign {
        return campaignList.find((campaign) => new Date().toDateString() === new Date(campaign.displayFrom).toDateString() && (new Date(campaign.displayFrom)).getTime() < (new Date()).getTime() && (new Date(campaign.displayTo)).getTime() > (new Date()).getTime() && campaign.isPotsCreated);
    }

    /**
     * gets FreeRide
     * @returns {Observable<IFreeRideCampaign>} 
     */
    public getFreeRide(): Observable<IFreeRideCampaign> {
        return this.getFreeRideCampaign().pipe(map((campaignResp: IFreeRideCampaign[]) => {
            return this.getFreeRideActiveCampaign(campaignResp);
        }));
    }

    /**
     * checks if campaign exist
     * @returns {boolean}
     */
    public campaignExist(): boolean {
        const activeCampaign = JSON.parse((this.sessionStorage.get(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA)));
        if (activeCampaign) {
            return new Date().toDateString() === new Date(activeCampaign.displayFrom).toDateString() && (new Date(activeCampaign.displayFrom)).getTime() < (new Date()).getTime() && (new Date(activeCampaign.displayTo)).getTime() > (new Date()).getTime();
        }
        return false;
    }

    /**
     * checks if free ride freebet exist
     * @returns {boolean}
     */
    public freeBetExist(): boolean {
        const expiryFreeBet = JSON.parse((this.sessionStorage.get(FREE_RIDE_CONSTS.FREERIDE_DETAILS)));
        if (expiryFreeBet && expiryFreeBet.freeBetExpiryDate) {
            return new Date(expiryFreeBet.freeBetExpiryDate.replace(/-/g, '/')).getTime() > (new Date()).getTime();
        }
        return false;
    }

    /**
     * checks if freeRide banner should be shown
     * @returns {boolean}
     */
    public showFreeRide(): boolean {
        !this.campaignExist() && this.sessionStorage.remove(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA);
        !this.freeBetExist() &&  this.sessionStorage.remove(FREE_RIDE_CONSTS.FREERIDE_DETAILS);
        return this.campaignExist() && this.freeBetExist();
    }

    /**
     * stores sports id's for which FR banner needs to be displayed
     */
    public freeRideOnSportsPages(): void {
        this.cmsService.getCmsInitData().subscribe((configs: ISystemConfig) => {
            const sportsConfigs = configs.sportCategories;
            this.showFRBannerOnSportsPages = sportsConfigs.reduce((total, value) => {
                    if (value.showFreeRideBanner) {
                        total.push(value.categoryId.toString());
                    }
                return total;
            }, []);
        });
    }

    /**
     * checks if freeRide banner should be shown on sports pages
     * @returns {boolean}
     */
    public showFreeRideOnSportPage(categoryId: string): boolean {
        return this.showFRBannerOnSportsPages.includes(categoryId);
    }

}
