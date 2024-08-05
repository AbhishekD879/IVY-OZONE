import { FreeBetsService } from '@ladbrokesMobile/core/services/freeBets/free-bets.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { from as observableFrom } from 'rxjs';

describe('LadbrokesFreeBetsService', () => {
  let service: FreeBetsService;
  let siteServer;
  let extensionsStorage;
  let user;
  let pubsub;
  let storage;
  let session;
  let time;
  let bpp;
  let nativeBridge;
  let dialog;
  let routingHelper;
  let filters;
  let sportsConfigHelperService;
  let locale;
  let device;
  let initState;

  beforeEach(() => {
    siteServer = {
      getData: jasmine.createSpy('getData'),
      getCategories: jasmine.createSpy('getCategories')
    };
    extensionsStorage = {};
    user = {
      status: true,
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(false)
    };
    pubsub = {
      subscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      API: pubSubApi,
    };
    sportsConfigHelperService = {
      getSportPathByCategoryId: jasmine.createSpy('getSportPathByCategoryId')
    };
    initState = JSON.stringify([{
      freebetTokenId: '12',
      freebetTokenExpiryDate: '2050-12-11 22:00:00',
      freebetOfferName: 'testOffer',
      freebetTokenValue: 300,
      tokenPossibleBet: {
        betId: '12',
        betLevel: 'EVENT'
      }
    }]);
    storage = {
      get: jasmine.createSpy().and.returnValue(initState),
      set: jasmine.createSpy(),
      remove: jasmine.createSpy(),
      getCookie: jasmine.createSpy().and.returnValue(true)
    };
    session = {
      whenProxySession: jasmine.createSpy().and.returnValue(
        new Promise<void>(function (resolve) {
          resolve();
        }))
    };
    time = {
      compareDate: jasmine.createSpy(),
      formatByPattern: jasmine.createSpy().and.returnValue('2019/01/20 10:33')
    };
    bpp = {
      send: jasmine.createSpy().and.returnValue(observableFrom([{
        response: {
          model: {
            freebetToken: [{
              freebetTokenExpiryDate: '2050-12-11 22:00:00',
              freebetTokenId: '12',
              tokenPossibleBet: {
                betId: null,
                betLevel: 'EVENT'
              }
            }]
          }
        }
      }]))
    };
    nativeBridge = {
      onFreeBetUpdated: jasmine.createSpy()
    };
    dialog = {};
    routingHelper = {};
    filters = {
      currencyPosition: jasmine.createSpy().and.returnValue('$300')
    };
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('test')
    };
    device = {
      isDesktop: false
    };

    spyOn(console, 'info');

    service = new FreeBetsService(
      siteServer,
      extensionsStorage,
      user,
      pubsub,
      storage,
      session,
      time,
      bpp,
      nativeBridge,
      dialog,
      routingHelper,
      filters,
      locale,
      device,
      sportsConfigHelperService
    );
  });

  it('FreeBetsService should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('enhanceFreeBetItem', () => {
    it('@enhanceFreeBetItem with less then 7', () => {

      const date = '2050-12-11T22:00:00.000Z';
      const freeBetItem = ({ freebetTokenExpiryDate: date, expires: null, usedBy: null }) as any;
      time.compareDate.and.returnValue(1);
      service['enhanceFreeBetItem'](freeBetItem);
      expect(time.formatByPattern).toHaveBeenCalledWith(jasmine.any(Object), 'yyyy-MM-dd HH:mm:ss');
      expect(freeBetItem.expires).not.toBeNull();
    });
    it('@enhanceFreeBetItem with more then 7', () => {

      const date = '2050-12-11T22:00:00.000Z';
      const freeBetItem = ({ freebetTokenExpiryDate: date, expires: null, usedBy: null }) as any;
      time.compareDate.and.returnValue(8);
      service['enhanceFreeBetItem'](freeBetItem);

      expect(time.formatByPattern).toHaveBeenCalledWith(jasmine.any(Object), 'dd/MM/yyyy');
      expect(freeBetItem.usedBy).not.toBeNull();

    });

    afterEach(() => {
      service = null;
    });
  });
});
