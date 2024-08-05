import { Observable, of } from 'rxjs';
import { map, timeout } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import Utils, { BRANDS_FOR_AEM } from './utils';
import {
  IOffer,
  IOfferFromServer,
  IOfferReport,
  IOfferGroupsFromServer,
  IParams, ISiteCoreTeaserFromServer
} from '@core/models/aem-banners-section.model';

import {
  IBannerResponseData
} from '@core/services/aemBanners/banner.service.model';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { ISSResponse } from '@core/models/ss-response.model';
import { VanillaApiService } from '@frontend/vanilla/core';
import { BANNER_SERVICE_ERROR_MESSAGE, SITECORE_API_CALL, OFFER_KEYS } from '@core/services/aemBanners/enums/banners.service.enums';
import { StorageService } from '@app/core/services/storage/storage.service';

@Injectable({ providedIn: 'root' })
export class BannersService {
  updatedOffers: IOffer[];
  priceNum: number;
  priceDen: number;
  private _settings;


  constructor(
    private vanillaApiService: VanillaApiService,
    private siteServerRequestHelperService: SiteServerRequestHelperService,
    private storageService: StorageService
  ) {
  }

  /**
   * Gets offers to display in carousel - according to settings
   * @param optionsPar - IParams
   * @returns {Observable<IOfferReport>}
   */
  public fetchOffersFromAEM(optionsPar: IParams): Observable<IOfferReport> {
    this._settings = optionsPar;
    const teasersData: IOffer[] = this.storageService.get('teasersData');
    const teasersOrgData: IBannerResponseData = this.storageService.get('teasersOrgData');
    if (teasersData && teasersData.length > 0 && this._settings.page === 'homepage') {
      this.storageService.remove('teasersData');
      return of({ providers: '', offers: teasersData });
    } else if(teasersOrgData && this._settings.page === teasersOrgData.message) {
        const offers: IOffer[] = this.groupAndMergeAndFormatOffers(teasersOrgData);
        this.storageService.remove('teasersOrgData');
        return of({ providers: '', offers: offers });
    } else {
      const libraryRequest: Observable<IBannerResponseData> = this.getLibraryOffers(this._settings.page);

    // Wait for responses
    return libraryRequest.pipe(map((libraryInspection: any) => {
        if (libraryInspection.resolved) {
          const offers: IOffer[] = this.groupAndMergeAndFormatOffers(libraryInspection);
          return ({ offers });
        } else {
          throw (new Error(BANNER_SERVICE_ERROR_MESSAGE.PF));
        }
      }));
    }
  }

  /**
   *
   * @param targetInspection - object that represents results of request to Adobe Target server
   * @param libraryInspection - object that represents results of request to AEM server
   */
  public groupAndMergeAndFormatOffers(libraryInspection: IBannerResponseData): IOffer[] {
    const offerGroups: IOfferGroupsFromServer = {target: [], library: []};

    if (libraryInspection.resolved) {
      const _libraryInspection_value = libraryInspection.data ? libraryInspection.data : [];
      offerGroups.library = _libraryInspection_value;
    }

    const formattedLibOffer = Utils.formatSitecore(offerGroups);
    this.setPersonalisedForGroups(formattedLibOffer);
    return this.mergeOffers(formattedLibOffer);
  }

  public setPersonalisedForGroups({ library = [], pinned = {}, rg = null }): void {
    library.forEach(offer => this.setPersonalised(offer, false));
    this.setPersonalised(pinned, false);
    this.setPersonalised(rg, false);
  }

  /**
   * Merge Offers by functional order priority, target, default, regulatory and trim based on CMS Config
   * @param offerGroups - IOfferGroupsFromServer
   * @returns - IOffer[] - Array
   */
  public mergeOffers(offerGroups: IOfferGroupsFromServer): IOffer[] {
    // separate by parts
    const target = offerGroups.target === undefined ? [] : offerGroups.target;
    const library = offerGroups.library === undefined ? [] : offerGroups.library;
    const pinned = offerGroups.pinned === undefined ? [] : offerGroups.pinned;
    const rg = offerGroups.rg;
    // deduplicate
    const _dedupe = Utils.dedupe([pinned, target, library]);
    const [ddStartList, ddTarget, ddLibrary] = _dedupe;
    // middle of carousel => plain + target
    const baseList = ddTarget.concat(ddLibrary);
    const atLeastOneNonRgPresent = Object.keys(baseList).length && Object.keys(ddStartList).length;
    const showRg = atLeastOneNonRgPresent && (this._settings.maxOffers !== 1) && (Object.keys(ddStartList).length);
    const positionedItemsCount = ddStartList.length + (showRg ? 1 : 0);
    const upperLimit = (this._settings.maxOffers - positionedItemsCount > 0) ? (this._settings.maxOffers - positionedItemsCount) : (0);
    // trim plain + target
    const trimmedBaseList = baseList.slice(0, upperLimit);

    // construct carousel banners list => plain + target + pinned
    let orderedList: any = [].concat(ddStartList, trimmedBaseList);
    if (showRg && rg && rg.length) {
      orderedList = orderedList.concat(rg[0]);
    }

    // reassure that exact number of banners that comes from settings is shown
    if (this._settings.maxOffers < orderedList.length) {
      orderedList = orderedList.slice(0, this._settings.maxOffers);
      if (showRg && (orderedList.length > 1 && rg && rg.length)) {
        orderedList[orderedList.length - 1] = rg[0];
      }
    }

    //   return finalOffers
    const formattedTrimmedList = orderedList.map((offer, index) => this.formatOfferResponse(offer,index));
    return formattedTrimmedList;
  }


  /**
   * Get Live Odds from Siteserve
   * @param offer - object that represents Offers
   * @returns - IOffer Object
   */
  public getOdds(offer: IOffer): IOffer {
    const status = 'A';
    if(offer.outcomeId) {
          this.getEvents(offer.outcomeId).
            then(
              (response: { SSResponse: ISSResponse }) => {
                if(response.SSResponse.children[0].event) {
                  const oddsValue = response.SSResponse.children[0].event.children[0].market.children[0].outcome.children[0].price;
                  const eventStatus: string = response.SSResponse.children[0].event.eventStatusCode;
                  const marketStatus: string = response.SSResponse.children[0].event.children[0].market.marketStatusCode;
                  const outcomeStatus: string = response.SSResponse.children[0].event.children[0].market.children[0].
                  outcome.outcomeStatusCode;
                  if(eventStatus === status && marketStatus === status && outcomeStatus === status ) {
                    offer.currentOdds = `${oddsValue.priceNum}/${oddsValue.priceDen}`;
                    offer.bannerStatus = true;
                  } else {
                    offer.bannerStatus = false;
                  }
                } else {
                  offer.bannerStatus = false;
                }
              }
            );
      }
      return offer;
  }

  /**
   * Get format Siteserve response
   * @param offer - object that represents Offers
   * @returns - IOffer Object
   */
  public formatOfferResponse(offer: ISiteCoreTeaserFromServer, index: number) {
    const offerObj: IOffer = {};
    offerObj.index = index;
    offerObj.Id = this.getObjectKeyValue(offer, OFFER_KEYS.itemId);
    offerObj.title = this.getObjectKeyValue(offer, OFFER_KEYS.title);
    offerObj.introductorytext = this.getObjectKeyValue(offer, OFFER_KEYS.introductoryText);
    offerObj.subtitle = this.getObjectKeyValue(offer, OFFER_KEYS.subTitle);
    offerObj.itemName = this.getObjectKeyValue(offer, OFFER_KEYS.itemName);
    offerObj.bannerStatus = true;
    offerObj.tcText = this.getObjectKeyValue(offer, OFFER_KEYS.keyTermsAndConditions);
    offerObj.brand = this._settings.brand;
    offerObj.tcLink = offer.termsAndConditionsLink ? offer.termsAndConditionsLink.url : (offer.bannerLink? offer.bannerLink.url : '');
    offerObj.tcTarget = offer.termsAndConditionsLink && offer.termsAndConditionsLink.attributes ?
      offer.termsAndConditionsLink.attributes.target : '';
    offerObj.imgUrl = this.getObjectKeyValue(offer.backgroundImage, OFFER_KEYS.src);
    offerObj.altText = this.getObjectKeyValue(offer.backgroundImage, OFFER_KEYS.alt);
    offerObj.link = offer && offer.bannerLink && offer.bannerLink.url || '';
    if(offer && offer.bannerLink && offer.bannerLink.attributes) {
      offerObj.target = this.getObjectKeyValue(offer.bannerLink.attributes,OFFER_KEYS.target);
    }
    if(offer && offer.foregroundImage) {
      offerObj.foregroundimage = this.getObjectKeyValue(offer.foregroundImage,OFFER_KEYS.src);
      offerObj.foregroundAltText = this.getObjectKeyValue(offer.foregroundImage,OFFER_KEYS.alt);
    }
    if(offer && offer.liveOddsBannerSelectionID) {
      offerObj.bannerStatus = false;
      offerObj.outcomeId = offer.liveOddsBannerSelectionID ;
      offerObj.previousOdds = this.getObjectKeyValue(offer, OFFER_KEYS.previousOddsValue);
    }
    return offerObj;
  }

  /**
   * Verify if Obj is undefined and
   * get values from object else return empty
   * @param obj - object
   * @returns - String
   */
  public getObjectKeyValue(obj: {}, key: string): string {
    return obj && obj[key] || '';
  }

  /**
   * Data Transformation - Sitecore Response to IOffer
   * @param offer - object that represents Offers
   * @returns - IOffer Object
   */
  public formatOffer(offer: IOfferFromServer): IOffer {
    const isWebDevice = this._settings.device === 'web';
    const brand = this._settings.brand;
    let link;
    if (BRANDS_FOR_AEM.ladbrokes === brand) {
      link = isWebDevice ? offer.roxanneWebUrl : offer.roxanneAppUrl;
    }
    if (!link) {
      link = isWebDevice ? offer.webUrl : offer.appUrl;
    }
    return {
      brand: this._settings.brand,
      Id: offer.id,
      imgUrl: offer.imgUrl,
      altText: offer.offerTitle,
      title: offer.offerTitle,
      link: link,
      target: isWebDevice ? offer.webTarget : offer.appTarget,
      tcText: offer.webTandC,
      tcLink: isWebDevice ? offer.webTandCLink : offer.mobTandCLink,
      personalised: offer.personalised
    };
  }


  /**
   * Get Offers from Sitecore using Vanilla api
   * @param offer - object that represents Offers
   * @returns - String
   */
  public getLibraryOffers(page: string): Observable<IBannerResponseData> {
    const subPath = ['priority', 'regulatory', 'default'];
    const response: IBannerResponseData = { data: null, resolved: true, message: null };
    const requestParams = {
      'path': `${SITECORE_API_CALL.FOLDER}/${page}`,
      'subPaths': subPath,
      'prefetchDepth': `${SITECORE_API_CALL.PREFETCHDEPTH}`
    };
    const apioptions = {
      'prefix': `${SITECORE_API_CALL.PREFIX}`
    };
    return this.vanillaApiService.post(`${SITECORE_API_CALL.PATH}`, requestParams, apioptions)
      .pipe(
        timeout(SITECORE_API_CALL.TIMEOUT),
        map(value => {
          response.data = value;
          return response;
        })
      );
  }

  /**
   * Get Odds from SS
   * @param ids - Selection ID
   * @returns - Promise
   */
  public getEvents(ids: string | string[]): Promise<{ SSResponse: ISSResponse }> {
    return this.siteServerRequestHelperService.getEventsByOutcomes({
      outcomesIds: ids
    });
  }

  /**
   * Set Personalized for target offers
   * @param offer - object that represents Offers
   * @param personalised - boolean status
   * @returns - String
   */
  private setPersonalised(offer: IOffer, personalised: boolean): void {
    if (offer) {
      offer.personalised = personalised;
    }
  }

}
