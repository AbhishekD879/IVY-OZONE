import { first } from 'rxjs/operators';
import { Observable, Subscriber } from 'rxjs';
import {
  AT_JS_LOADING_TIMEOUT,
  IOfferGroupsFromServer,
  ISiteCoreTeaserFromServer
} from '@core/models/aem-banners-section.model';

export const dynamicBannersPageMap = {
  home: 'homepage',
  sports_homepage: 'sports-homepage',
  horseracing: 'horse-racing',
  americanfootball: 'american-football',
  aussierules: 'australian-rules',
  beachsoccer: 'beach-soccer',
  beachvolleyball: 'beach-volleyball',
  gaelicfootball: 'gaelic-football',
  icehockey: 'ice-hockey',
  modernpentathlon: 'modern-pentathlon',
  motorbikes: 'motor-bikes',
  speedway: 'motor-speedway',
  motorsports: 'motor-sports',
  tote: 'intl-tote',
  rugbyleague: 'rugby-league',
  rugbyunion: 'rugby-union',
  synchronisedswimming: 'synchronized-swimming',
  tabletennis: 'table-tennis',
  tvspecials: 'tv-specials',
  waterpolo: 'water-polo',
  ufcmma: 'ufc',
  greyhound: 'greyhounds',
  winter_sports: 'winter-sports',
  sportmultiples: 'sport-multiples',
  retail: 'homepage',
  showDownHome: 'showdown-home',
  virtuals: 'virtuals'
};

export const BRANDS_FOR_AEM = {
  coral: 'coral',
  ladbrokes: 'ladbrokes'
};

export const DEFAULT_OPTIONS = {
  device: 'web',
  maxOffers: 7,
  atJsLoadingTimeout: AT_JS_LOADING_TIMEOUT
};

export const DEFAULT_BRAND_FOR_AEM = 'coral';

export default class Utils {
  static resolveBrandOrDefault(key: string = 'coral') {
    const brand = BRANDS_FOR_AEM[key.toLowerCase()];
    if (brand) {
      return BRANDS_FOR_AEM[key.toLowerCase()];
    } else {
      return DEFAULT_BRAND_FOR_AEM;
    }
  }

  static assign(dest,  ...sources) {
    const obj = sources.reduce((r, o) => {
      Object.keys(o).forEach(k => (r[k] = o[k]));
      return r;
    }, dest);
    return obj;
  }

  static isEmpty(val) {
    return val === undefined || val === null || val === '';
  }

  static dedupe(multi) {
    const seen = {};

    return multi.map(offersGroup => {
      return offersGroup.filter(offer => {
        const offerId = offer.Id;
        if (Utils.isEmpty(offerId)) {
          return true;
        }
        if (seen.hasOwnProperty(offerId)) {
          return false;
        } else {
          seen[offerId] = true;
          return true;
        }
      });
    });
  }

  static doPoll(fn, ...params): Observable<any>  {
    const timeout = params.length > 1 && params[0] !== undefined ? params[0] : 1000;
    const interval = params.length > 2 && params[1] !== undefined ? params[1] : 100;
    const endTime = Number(new Date()) + Number(timeout);

    return new Observable((src: Subscriber<any>) => {
      Utils.tryResolve(fn, endTime, interval, result => {
        if (result) {
          src.next({resolved: true, result: result});
        } else {
          src.next({resolved: false});
        }
      });
    }).pipe(first());
  }

  static tryResolve(fn, endTime, interval, callback) {
    const result = fn();

    if (result === true || Number(new Date()) >= endTime) {
      return callback(result);
    } else {
      setTimeout(() => { Utils.tryResolve(fn, endTime, interval, callback); }, interval);
    }
  }

  static flatMap(a, fn) {
    return (<any>[].concat)(...a.map(fn));
  }

  /**
   * Retrieves list of target banners from Sitecore and filters based on id
   * @param offers - IOfferGroupsFromServer
   * @returns {IOfferGroupsFromServer}
   */
  static formatSitecore(offers: IOfferGroupsFromServer): IOfferGroupsFromServer {
    const formattedOffers = [] as IOfferGroupsFromServer;
    formattedOffers.target = offers.target;
    offers.library.forEach((libOffer: ISiteCoreTeaserFromServer) => {
      switch (libOffer.type) {
        case 'priority': formattedOffers.pinned = libOffer.teasers;
          break;
        case 'default': formattedOffers.library = libOffer.teasers;
          break;
        case 'regulatory': formattedOffers.rg = libOffer.teasers;
          break;
        default:
          break;
      }
    });
    return formattedOffers;
  }
}
