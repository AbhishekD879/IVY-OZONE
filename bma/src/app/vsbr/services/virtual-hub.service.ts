import { Subject, Observable } from 'rxjs';
import { map, timeout } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import {
    IOffer, IOfferReport,
    IParams, ISiteCoreTeaserFromServer
} from '@core/models/aem-banners-section.model';

import { VanillaApiService } from '@frontend/vanilla/core';
import { SITECORE_API_CALL, OFFER_KEYS } from '@core/services/aemBanners/enums/banners.service.enums';
import { IVirtualSports, IVirtualSportsHomePage, IVirtualSportNavigationInfo } from '@app/core/services/cms/models/virtual-sports.model';
import {
    IBannerResponseData
} from '@core/services/aemBanners/banner.service.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { IVirtualHomePageSystemConfig } from "@app/core/services/cms/models/system-config";

@Injectable({
    providedIn: 'root'
})
export class VirtualHubService {

    private _settings: IParams;
    private sitecoreVRRootFolder: string = 'VirtualHubSports';
    public siteCoreOffers: IOffer[];
    public cmsData = new Subject<any>();
    public entryPointSiteCoreOffers: IOfferReport;
    public onClickNavigationDetails: IVirtualSportNavigationInfo = {
        id: null,
        sportInfo: null
    };
    
    /**
     * Constructor
     * @param vanillaApiService : VanillaApiService
    */
    constructor(private vanillaApiService: VanillaApiService, private gtmService: GtmService, private storageService:StorageService) {
    }

    /**
     * Fetches banner virtual images from sitecore
     */
    bannerInit() {
        this.getLibraryOffers('virtuals').subscribe((value: IBannerResponseData) => {
            this.storageService.set('teasersOrgData', { data: value, resolved: true, message: 'virtuals'});
        });
    }


    /**
     * Fetches virtual hub images from sitecore
     * @param optionsPar : Params for service call
     * @param cmsVirtualSportsData : VirtualSportsData object
     * @returns 
     */
    public fetchVirtualImagesFromSiteCore(optionsPar: IParams, cmsVirtualSportsData: IVirtualSports[], virtualHubSystemConfig: IVirtualHomePageSystemConfig) {
        this._settings = optionsPar;
        return this.getSiteCoreData(cmsVirtualSportsData, virtualHubSystemConfig);
    }

    /**
     * Merge CMS and sitecore data
     * @param siteCoreOffers : virtual hub sitecore offer object
     * @param cmsVirtualConfig : CMS data object
     * @returns virtual hub homepage configuration
    */
    private mergeCmsAndSitecoreData(siteCoreOffers: IOffer[], cmsVirtualConfig: IVirtualSports[]): IVirtualSportsHomePage[] {
        const virtualHomepageConfig: IVirtualSportsHomePage[] = cmsVirtualConfig as any;
        virtualHomepageConfig.forEach(sportConfig => {
            let imageFound;
            if (this._settings.channel === 'mobile') {
                imageFound = siteCoreOffers.find(offer => offer.Id === sportConfig.mobileImageId);
            } else {
                imageFound = siteCoreOffers.find(offer => offer.Id === sportConfig.desktopImageId);
            }

            if (imageFound) {
                sportConfig.imgURL = imageFound.imgUrl;
                sportConfig.altText = imageFound.altText;
            }
        })

        return virtualHomepageConfig;
    }

    /**
     * Group offers Data into a single object
     * @param libraryInspection - object that represents results of request to sitecore
    */
    private groupAndFormatOffers(offersData: any): IOffer[] {
        let formattedTrimmedList: IOffer[] = [];
        if (offersData.length) {
            formattedTrimmedList = offersData.map((offer, idx) => this.formatOfferResponse(offer, idx));
        }
        return formattedTrimmedList;
    }


    /**
     * Get format Siteserve response
     * @param offer - object that represents Offers
     * @returns - IOffer Object
    */
    private formatOfferResponse(offer: ISiteCoreTeaserFromServer, index: number) {
        const offerObj: IOffer = {};
        offerObj.index = index;
        offerObj.Id = this.getObjectKeyValue(offer, OFFER_KEYS.itemId);
        offerObj.title = this.getObjectKeyValue(offer, OFFER_KEYS.title);
        offerObj.introductorytext = this.getObjectKeyValue(offer, OFFER_KEYS.introductoryText);
        offerObj.itemName = this.getObjectKeyValue(offer, OFFER_KEYS.itemName);
        offerObj.brand = this._settings?.brand;
        offerObj.imgUrl = this.getObjectKeyValue(offer.backgroundImage, OFFER_KEYS.src);
        offerObj.altText = this.getObjectKeyValue(offer.backgroundImage, OFFER_KEYS.alt);
        offerObj.link = offer && offer.bannerLink && offer.bannerLink.url || '';
        if (offer && offer.bannerLink && offer.bannerLink.attributes) {
            offerObj.target = this.getObjectKeyValue(offer.bannerLink.attributes, OFFER_KEYS.target);
        }
        return offerObj;
    }

    /**
     * Verify if Obj is undefined and
     * get values from object else return empty
     * @param obj - object
     * @returns - String
    */
    private getObjectKeyValue(obj: {}, key: string): string {
        return obj && obj[key] || '';
    }

    /**
     * Get Offers from Sitecore using Vanilla api
     * @param offer - object that represents Offers
     * @returns - String
    */
    private getSiteCoreData(cmsVirtualSportsData: IVirtualSports[], virtualHubSystemConfig: IVirtualHomePageSystemConfig) {
        const subPath = [];
        const configMap = {
            topSports: 'TopSports',
            otherSports: 'OtherSports',
            featureZone: 'FeatureZone',
        };

        for (const key in configMap) {
            if (virtualHubSystemConfig && virtualHubSystemConfig[key]) {
                subPath.push(configMap[key]);
            }
        }
       
        const apioptions = {
            'prefix': `${SITECORE_API_CALL.PREFIX}`
        };
        const requestParams = {
            'path': `${this.sitecoreVRRootFolder}`,
            'subPaths': subPath,
            'prefetchDepth': 1
        };
        let topOtherSportsImageConfig: IVirtualSportsHomePage[];
        const combinedTopOtherSportsSitecoreData: any = [];
        return this.vanillaApiService.post(`${SITECORE_API_CALL.PATH}`, requestParams, apioptions)
            .pipe(
                timeout(SITECORE_API_CALL.TIMEOUT),
                map((sitecoreInfo: any) => {
                    let featureZoneOffers: IOffer[];
                    sitecoreInfo.map((data, index) => {
                        if (data.type == configMap.topSports || data.type == configMap.otherSports) {
                            combinedTopOtherSportsSitecoreData.push(...sitecoreInfo[index].teasers);
                        }
                        else {
                            featureZoneOffers = this.groupAndFormatOffers(sitecoreInfo[index].teasers);
                        }
                    })

                    if(combinedTopOtherSportsSitecoreData.length > 0){
                        const siteCoreOffers: IOffer[] = this.groupAndFormatOffers(combinedTopOtherSportsSitecoreData);
                        this.siteCoreOffers = siteCoreOffers;
                        topOtherSportsImageConfig = this.mergeCmsAndSitecoreData(siteCoreOffers, cmsVirtualSportsData);
                    }
                    
                    const [topSportsConfig, otherSportsConfig] = this.partition(topOtherSportsImageConfig, 'topSports');
                    if (topSportsConfig && topSportsConfig.length > 0) {
                        topSportsConfig.sort((firstImage: IVirtualSportsHomePage, secondImage: IVirtualSportsHomePage) => Number(firstImage.topSportsIndex) - Number(secondImage.topSportsIndex));
                    }
                    if (otherSportsConfig.length > 0) {
                        otherSportsConfig.sort((a, b) => (a.title > b.title) ? 1 : ((b.title > a.title) ? -1 : 0));
                    }
                    return { topSports: topSportsConfig, otherSports: otherSportsConfig, featureZoneOffers: featureZoneOffers };
                })
            );
    }

    /**
     * Create two arrays based on filter element
    */
    private partition(arr: IVirtualSportsHomePage[], filterString: string) {
        const otherSports = [];

        const topSports = arr.filter((sportInfo) => {
            if (sportInfo[filterString]) return sportInfo;
            otherSports.push(sportInfo);
        });

        return [topSports, otherSports];
    }

    /**
     * Setter for CMS config
     * @param config : CMS config object
    */
    public setOrUpdateCmsConfig(config) {
        this.cmsData.next(config);
    }

    /**
     * Getter for CMS config
    */
    public getCmsData() {
        return this.cmsData.asObservable();
    }

    /**
     * Get Offers from Sitecore using Vanilla api
     * @param offer - object that represents Offers
     * @returns - String
     */
    private getLibraryOffers(page: string): Observable<IBannerResponseData> {
        let requestParams;
        if(page === 'virtuals'){
            requestParams = {
                "path": `mainbanners/${page}`, "subPaths": ["priority", "regulatory", "default"], "prefetchDepth": "2"
            };
        }
        else{
            requestParams = {
                'path': page ? `${this.sitecoreVRRootFolder}/${page}` : `${this.sitecoreVRRootFolder}`
            };
        }
        const apioptions = {
            'prefix': `${SITECORE_API_CALL.PREFIX}`
        };
        return this.vanillaApiService.post(`${SITECORE_API_CALL.PATH}`, requestParams, apioptions)
            .pipe(
                timeout(SITECORE_API_CALL.TIMEOUT),
                map(response => {
                    return response;
                })
            );
    }

    /**
     * Gets images for virtualhub homepage from sitecore
     * @param page : sitecore folder name
     * @returns : sitecore Offers
     */
    public getSiteCoreImages(page: string): Observable<IOfferReport> {
        const libraryRequest: Observable<IBannerResponseData> = this.getLibraryOffers(page);
        return libraryRequest.pipe(map((libraryInspection: any) => {
            let offers: IOffer[] = [];
            if (libraryInspection && libraryInspection[0]?.teasers) {
                offers = this.groupAndFormatOffers(libraryInspection[0].teasers);
            }
            return ({ offers });
        }));
    }

    /**
     * triggers GAtracking for top sports and other sports
     * @param url : navigation url
     */
    public triggerGTATracking(url: string) {
        if (this.onClickNavigationDetails.id === 'other sports') {
            this.trackOtherSportsClickGTMEvent(this.onClickNavigationDetails.sportInfo, url);
        } else if (this.onClickNavigationDetails.id === 'top sports') {
            this.trackTopSportsClickGTMEvent(this.onClickNavigationDetails.sportInfo, url);
        }
    }

    /**
   * GA tracker for othersports click event
   * @param imageInfo : IVirtualSportsHomePage
   */
    private trackOtherSportsClickGTMEvent(imageInfo: IVirtualSportsHomePage, url: string): void {
        const gtmData = {
            event: 'Event.Tracking',
            'component.CategoryEvent': 'virtuals sports',
            'component.LabelEvent': 'other sports',
            'component.ActionEvent': 'click',
            'component.PositionEvent': 'not applicable',
            'component.LocationEvent': 'other sports',
            'component.EventDetails': imageInfo.title,
            'component.URLclicked': url
        };
        this.gtmService.push(gtmData.event, gtmData);
        this.onClickNavigationDetails.id = null;
    }

    /**
      * GTM tracking for top sports
      * @param imageInfo : virtualHomePage Info
      */
    private trackTopSportsClickGTMEvent(imageInfo: IVirtualSportsHomePage, url: string): void {
        const gtmData = {
            event: 'Event.Tracking',
            'component.CategoryEvent': 'virtuals sports',
            'component.LabelEvent': 'top sports',
            'component.ActionEvent': 'click',
            'component.PositionEvent': imageInfo.topSportsIndex,
            'component.LocationEvent': 'not applicable',
            'component.EventDetails': imageInfo.title,
            'component.URLclicked': url,
        };
        this.gtmService.push(gtmData.event, gtmData);
        this.onClickNavigationDetails.id = null;
    }
}
