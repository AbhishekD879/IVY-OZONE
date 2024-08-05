import { BannersService } from 'app/core/services/aemBanners/banners.service';
import { BRANDS_FOR_AEM } from './utils';
import { of } from 'rxjs';
import { fakeAsync, flush } from '@angular/core/testing';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { singleOfferFromLibrary } from '@core/services/aemBanners/test/data/singleOfferFromLibrary.mock';
import { VanillaApiService } from '@frontend/vanilla/core';
const { fromServer, toComponent, mergeOffersMock, formatOfferObject, response } = singleOfferFromLibrary;

describe('BannersService', () => {
  let service: BannersService;
  let vanillaApiService: Partial<VanillaApiService>;
  let siteServerRequestHelperService;
  let storageService;

  const AT_PROPERTY_VALUE = '123';
  const BETSLIP_AT_PROPERTY_VALUE = '456';

  beforeEach(() => {
    environment.AEM_CONFIG = {
      server: 'http://lc-aem.com',
      at_property: AT_PROPERTY_VALUE,
      betslip_at_property: BETSLIP_AT_PROPERTY_VALUE
    };

    vanillaApiService = {
      post: jasmine.createSpy('post').and.returnValue(of(fromServer)),
      get: jasmine.createSpy('get').and.returnValue(of([{
        type: 'segmentDefault',
        teasers: [{
          title: 'Test',
          subTitle: 'QA',
          itemId: '{1234}'
        }]
      }]))
    };
    storageService = {
      get: () => {},
      remove: () => {}
    };

    siteServerRequestHelperService = {
      getEventsByOutcomes: jasmine.createSpy('getEventsByOutcomes').and.returnValue(Promise.resolve([]))
    };
    service = new BannersService(
      vanillaApiService as VanillaApiService,
      siteServerRequestHelperService,
      storageService
    );
  });



  it('fetchOffersFromAEM else case', (done: DoneFn) => {
    spyOn<any>(service, 'getLibraryOffers').and.returnValue(of({data: [], resolved: false, message: null}));
    service.fetchOffersFromAEM({page: 'page', brand: 'coral', maxOffers: 10}).subscribe((dataForCarousel) => {
    }, (error) => {
      expect(error).toBeDefined();
      done();
    });
    expect(service['getLibraryOffers']).toHaveBeenCalled();
  });


  it('Library success but result is empty', (done: DoneFn) => {
    const teasersObj = [{'type':'priority','teasers':[]},{'type':'regulatory','teasers':[]},
    {'type':'default','teasers':[]}, {'type':'','teasers':[]}];
    spyOn<any>(service, 'getLibraryOffers').and.returnValue(of({data: teasersObj , resolved: true, message: null}));

    service.fetchOffersFromAEM({page: 'page', brand: 'coral', maxOffers: 10}).subscribe((dataForCarousel) => {
      done();
    });
  });

 

  it('Throw error on missing required params  for response.json', (done: DoneFn) => {
    try {
      service['createLibraryEndpoint'](<any>{
        sth: 'sth',
      });
    } catch (error) {
      expect(error).toBeDefined();
      done();
    }
  });

  it('Error is thrown when library fail and target fail', (done: DoneFn) => {
    spyOn<any>(service, 'getLibraryOffers').and.returnValue(of({resolved: false, data: null, message: null}));

    service.fetchOffersFromAEM({page: 'page', brand: 'coral', maxOffers: 10}).subscribe((dataForCarousel) => {}, (error => {
      expect(error).toBeDefined();
      done();
    }));
  });

  it('Requests offers from library', fakeAsync(() => {
    spyOn<any>(service, 'getLibraryOffers').and.callThrough();
    service.fetchOffersFromAEM({
      page: 'page',
      brand: 'coral',
      maxOffers: 7,
    }).subscribe((dataForCarousel) => {
      const actualOffer = dataForCarousel.offers[0];
      const expectedOffer = toComponent[0];
      expect(actualOffer.brand).toBe(expectedOffer.brand);
    });
    flush();
  }));

  describe('get odds getEventsByOutcomeIds', () => {
    const ids = '588455222';
    const offer = {
      outcomeId: ids
    };

    it('get odds should retrieve events and build selection based on one event', fakeAsync(() => {
      siteServerRequestHelperService.getEventsByOutcomes.and.returnValue(Promise.resolve(response[0]));
      service.getOdds(offer);
      expect(siteServerRequestHelperService.getEventsByOutcomes).toHaveBeenCalledWith({
        outcomesIds: ids
      });
    }));

    it('get bannerStatus when selection is empty', fakeAsync(() => {
      const offers = [];
      siteServerRequestHelperService.getEventsByOutcomes.and.returnValue(Promise.resolve(response[1]));
      service.getOdds(offer);
      expect(siteServerRequestHelperService.getEventsByOutcomes).toHaveBeenCalledWith({
        outcomesIds: ids
      });
    }));

    it('get bannerStatus when response is empty', fakeAsync(() => {
      const offers = [{
        outcomeId: ''
      }];
      const emptyResponse = {
        SSResponse: {
          children: [{
            eventStatusCode: 'A'
          }]
        }
      };
      siteServerRequestHelperService.getEventsByOutcomes.and.returnValue(Promise.resolve(emptyResponse));
      service.getOdds(offer);
      expect(siteServerRequestHelperService.getEventsByOutcomes).toHaveBeenCalledWith({
        outcomesIds: ids
      });
    }));
  });

  it('Requests offers from Target', (done: DoneFn) => {
    spyOn<any>(service, 'getLibraryOffers').and
      .returnValue(of({resolved: true, data: null, message: 'Rejection reason'}));

    service.fetchOffersFromAEM({
      page: 'page',
      brand: 'coral',
      maxOffers: 7,
      device: 'web'
    }).subscribe((dataForCarousel) => {
      done();
    });
  });

  it('Parses and formats offer from library', (done: DoneFn) => {
    spyOn<any>(service, 'getLibraryOffers').and.returnValue(of({resolved: true, data: fromServer, message: 'Resolved'}));

    service.fetchOffersFromAEM({
      page: 'page',
      brand: 'coral',
      maxOffers: 7,
      device: 'web'
    }).subscribe((dataForCarousel) => {
      const actualOffer = dataForCarousel.offers[0];
      const expectedOffer = toComponent[0];
      expect(actualOffer.brand).toBe(expectedOffer.brand);
      done();
    });
  });
  

  // Fix after stopping combining Roxanne and Mobenga
  describe('Links setting for brands', () => {
    const webUrl = 'http://weburl.com';
    const appUrl = 'http://appurl.com';
    const roxanneWebUrl = 'http://roxanneweburl.com';
    const roxanneAppUrl = 'http://appurl.com';

    beforeEach(() => {
      service['_settings'] = {};
    });

    it('Test temp link for Roxanne Web', (done: DoneFn) => {
      service['_settings'].device = 'web';
      service['_settings'].brand = BRANDS_FOR_AEM.ladbrokes;

      const offerWithLink = service.formatOffer(<any>{webUrl, appUrl, roxanneWebUrl, roxanneAppUrl});

      expect(offerWithLink.link).toEqual(roxanneWebUrl);
      done();
    });

    it('Test temp link for Roxanne App', (done: DoneFn) => {
      service['_settings'].device = 'app';
      service['_settings'].brand = BRANDS_FOR_AEM.ladbrokes;

      const offerWithLink = service.formatOffer(<any>{webUrl, appUrl, roxanneWebUrl, roxanneAppUrl});

      expect(offerWithLink.link).toEqual(roxanneAppUrl);
      done();
    });

    it('Test temp link for Roxanne App if special Roxanne field missing', (done: DoneFn) => {
      service['_settings'].device = 'app';
      service['_settings'].brand = BRANDS_FOR_AEM.ladbrokes;

      const offerWithLink = service.formatOffer(<any>{webUrl, appUrl, roxanneWebUrl });

      expect(offerWithLink.link).toEqual(appUrl);
      done();
    });

    it('Test temp link for OX Web', (done: DoneFn) => {
      service['_settings'].device = 'web';
      service['_settings'].brand = BRANDS_FOR_AEM.coral;

      const offerWithLink = service.formatOffer(<any>{webUrl, appUrl, roxanneWebUrl, roxanneAppUrl});

      expect(offerWithLink.link).toEqual(webUrl);
      done();
    });

    it('Test temp link for OX App', (done: DoneFn) => {
      service['_settings'].device = 'app';
      service['_settings'].brand = BRANDS_FOR_AEM.coral;

      const offerWithLink = service.formatOffer(<any>{webUrl, appUrl, roxanneWebUrl, roxanneAppUrl});

      expect(offerWithLink.link).toEqual(appUrl);
      done();
    });
  });

  it('formatOfferResponse', ()=> {
    service['_settings'] = { maxOffers: 6, brand: 'coral' };
    const index= 0;
    const formattedResponse = service.formatOfferResponse(formatOfferObject[0],index);
    expect(formattedResponse.outcomeId).toEqual(formatOfferObject[0].liveOddsBannerSelectionID);
  });

  it('formatOfferResponse else conditions', ()=> {
    service['_settings'] = { maxOffers: 6, brand: 'coral' };
    const index= 0;
    const formattedResponse = service.formatOfferResponse(formatOfferObject[1],index);
    expect(formattedResponse.foregroundAltText).toEqual('');
  });

  it('formatOfferResponse no tc and banner link condition', ()=> {
    service['_settings'] = { maxOffers: 6, brand: 'coral' };
    const index= 0;
    const formattedResponse = service.formatOfferResponse(formatOfferObject[2],index);
    expect(formattedResponse.tcTarget).toEqual('');
  });

  it('formatOfferResponse no banner link condition', ()=> {
    service['_settings'] = { maxOffers: 6, brand: 'coral' };
    const index= 0;
    const formattedResponse = service.formatOfferResponse(formatOfferObject[3],index);
    expect(formattedResponse.title).toEqual('');
  });

 describe('#mergeOffers', () => {
    const offers = <any>{
        library: [{'title': '7 Places 3'},{'title': '7 Places 4'},{'title': '7 Places 5'}],
        pinned: [{'title': '7 Places 1'},{'title': '7 Places 2'}],
        rg: [{'title': '7 Places 6'}],
        target: []
      },
      equal = <any>mergeOffersMock;

   it('should show all the 6 offers', () => {
     const itOffers = _.clone(offers),
       itEqual = _.clone(equal);
     service['_settings'] = { maxOffers: 6, brand: 'coral' };
     const mergofferslist = service.mergeOffers(itOffers);
     expect(mergofferslist).toEqual(itEqual);
   });

   it('when no offers as library is empty', () => {
     const itoffers = <any>{
       library: undefined,
       pinned: undefined,
       rg: [{ 'title': '7 Places 6' }],
       target: undefined
     };
     const itOffers = _.clone(itoffers);
     service['_settings'] = { maxOffers: 6, brand: 'coral' };
     const mergeofferslist = service.mergeOffers(itOffers);
     expect(mergeofferslist).toEqual([]);
   });

    it('should show 5 offers - without rg', () => {
      const itOffers = _.clone(offers),
        itEqual = _.clone(equal).slice(0, -1);

      delete itOffers.rg;

      service['_settings'] = { maxOffers: 6, brand: 'coral' };
      expect(service.mergeOffers(itOffers)).toEqual(itEqual);
    });

    it('should show 2 offers - without rg', () => {
      const itOffers = _.clone(offers);
      service['_settings'] = { maxOffers: 2 };
      service.mergeOffers(itOffers);

      delete itOffers.rg;

      service['_settings'] = { maxOffers: 2, brand: 'coral' };
      expect(service.mergeOffers(itOffers)).toEqual(<any>[mergeOffersMock[0],mergeOffersMock[1]]);
    });

    it('should show 1 offer - without rg', () => {
      const itOffers = _.clone(offers);

      service['_settings'] = { maxOffers: 1,brand: 'coral' };
      expect(service.mergeOffers(itOffers)).toEqual(<any>[mergeOffersMock[0]]);
    });

    it('should show 1 plain offer - without rg when pinned are missing', () => {
      const itOffers = _.clone(offers);
      delete itOffers.pinned;
      service['_settings'] = { maxOffers: 1 ,brand: 'coral' };
      const finalOffers = service.mergeOffers(itOffers);
      expect(finalOffers[0].title).toEqual(mergeOffersMock[2].title);
    });

  });
  describe('fetchOffersFromAEM check for teaser data', ()=> {
    it('storage not available', (done: DoneFn) => {
      const getSpy = spyOn(storageService, 'get').and.returnValue([]);
      const teasersObj = [{'type':'priority','teasers':[]},{'type':'regulatory','teasers':[]},
      {'type':'default','teasers':[]}, {'type':'','teasers':[]}];
      spyOn<any>(service, 'getLibraryOffers').and.returnValue(of({data: teasersObj , resolved: true, message: null}));
      service.fetchOffersFromAEM({page: 'page', brand: 'coral', maxOffers: 10}).subscribe((dataForCarousel) => {
        done();
      });
    });
    it('storage available and page matches', (done: DoneFn) => {
      const getSpy = spyOn(storageService, 'get').and.returnValue({ data: [], resolved: true, message: 'page'});
      spyOn<any>(service, 'getLibraryOffers').and.callThrough();
      service.fetchOffersFromAEM({page: 'page', brand: 'coral', maxOffers: 7}).subscribe((dataForCarousel) => {
        done();
      });
    });
    it('storage available and page donot matches', (done: DoneFn) => {
      const getSpy = spyOn(storageService, 'get').and.returnValue({ data: [], resolved: true, message: 'football'});
      const teasersObj = [{'type':'priority','teasers':[]},{'type':'regulatory','teasers':[]},
      {'type':'default','teasers':[]}, {'type':'','teasers':[]}];
      spyOn<any>(service, 'getLibraryOffers').and.returnValue(of({data: teasersObj , resolved: true, message: null}));
  
      service.fetchOffersFromAEM({page: 'page', brand: 'coral', maxOffers: 10}).subscribe((dataForCarousel) => {
        done();
      });
    }); 
    it('storage available and no page', (done: DoneFn) => {
      const getSpy = spyOn(storageService, 'get').and.returnValue({ data: [], resolved: true });
      const teasersObj = [{'type':'priority','teasers':[]},{'type':'regulatory','teasers':[]},
      {'type':'default','teasers':[]}, {'type':'','teasers':[]}];
      spyOn<any>(service, 'getLibraryOffers').and.returnValue(of({data: teasersObj , resolved: true, message: null}));
  
      service.fetchOffersFromAEM({page: 'page', brand: 'coral', maxOffers: 10}).subscribe((dataForCarousel) => {
        done();
      });
    });    
  });
});
