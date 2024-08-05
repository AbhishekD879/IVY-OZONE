import { throwError, of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { AddToBetslipByOutcomeIdService } from './add-to-betslip-by-outcome-id.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';

describe('AddToBetslipByOutcomeIdService', () => {
  let service;
  let siteServerRequestHelperService;
  let cmsService;
  let dialogService;
  let overaskService;
  let gtmService;
  let pubsub;
  let windowRef;
  let betslipService;
  let storageService;
  let toteBetslipService;
  let router;
  let dynamicComponentLoader;
  let deviceService;
  let mockModuleRef;
  let location;
  let gtmTrackingService;
  let userService;
  let betslipStorageService;
  let siteServerService;
  let fanzoneStorageService;
  const mockComponent = { name: 'Lazy loaded component ref' };
  const mockOutcomesData = [{"id": "240480151", "isFanzoneMarket": true, "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
  const mockOutcomesData2 = [{"id": "240480151", "isFanzoneMarket": false, "isDisplayed": "true", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
  const mockOutcomesData3 = [{"id": "240480151", "isFanzoneMarket": true, "isDisplayed": "true", "marketId": "52637000", "name": "Fulham"}];
  const mockOutcomesData4 = [{"id": "240480151", "isFanzoneMarket": true, "marketId": "52637000", "name": "Fulham"}];
  const mockOutcomesData5 = [{"id": "240480151", "marketId": "52637000", "name": "Fulham"}];
  beforeEach(() => {
    location = {
      path: jasmine.createSpy('path').and.returnValue('betslip/add/4123')
    };
    gtmTrackingService = {
      restoreTracking: jasmine.createSpy('restoreTracking'),
      getBetOrigin: jasmine.createSpy('getBetOrigin').and.returnValue({
        location: 'origin_location',
        module: 'origin_module'
      })
    };
    siteServerRequestHelperService = {
      getEventsByOutcomes: jasmine.createSpy('getEventsByOutcomes').and.returnValue(Promise.resolve([]))
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}))
    };
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    overaskService = {
      showOveraskInProgressNotification: jasmine.createSpy('showOveraskInProgressNotification'),
      isInProcess: false
    };
    gtmService = jasmine.createSpyObj('gtmService', ['push']);
    pubsub = {
      subscribe: jasmine.createSpy('subscribe'),
      publishSync: jasmine.createSpy('publishSync'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    windowRef = {
      nativeWindow: window
    };
    betslipService = {
      count: jasmine.createSpy('count').and.returnValue(1),
      toggleSelection: jasmine.createSpy('toggleSelection').and.returnValue(observableOf({})),
      showBetslipLimitationPopup: jasmine.createSpy('bsService.showLimitationsPoopup').and.returnValue(observableOf(null)),
      mapOutcomes: jasmine.createSpy('mapOutcomes').and.returnValue(observableOf(mockOutcomesData))
    };
    storageService = jasmine.createSpyObj('storageService', ['set', 'get']);
    toteBetslipService = {
      isToteBetPresent: jasmine.createSpy('isToteBetPresent').and.returnValue(false)
    };
    router = {
      navigate: jasmine.createSpy('navigate').and.returnValue(Promise.resolve())
    };
    dynamicComponentLoader = {
      loadModule: jasmine.createSpy('loadModule').and.returnValue(Promise.resolve(mockModuleRef))
    };
    deviceService = {
      isMobile: false
    };
    mockModuleRef = {
      componentFactoryResolver: {
        resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue(mockComponent)
      }
    };
    userService = jasmine.createSpyObj(['set']);
    betslipStorageService = {
      set setEventToBetslipObservable(v) {}
    };
    siteServerService = {
      getEventsByOutcomeIds: jasmine.createSpy('getEventsByOutcomeIds').and.returnValue(Promise.resolve({}))
    };
    fanzoneStorageService = {
      get: jasmine.createSpy('get')
    };


    service = new AddToBetslipByOutcomeIdService(
      siteServerRequestHelperService,
      cmsService,
      dialogService,
      overaskService,
      gtmService,
      pubsub,
      windowRef,
      betslipService,
      storageService,
      toteBetslipService,
      router,
      dynamicComponentLoader,
      deviceService,
      location,
      gtmTrackingService,
      userService,
      betslipStorageService,
      siteServerService,
      fanzoneStorageService
    );
  });

  it('should check if sync is in progress', () => {
    service['checkForRpTipGTM'] = jasmine.createSpy('checkForRpTipGTM');
    expect(service['isAddToBetslipInProcess']()).toBeFalsy();

    service['syncProcess'].inProgress = true;

    expect(service['isAddToBetslipInProcess']()).toBeTruthy();
  });

  describe('getOutcomeHandicap', () => {
    it('should return falsy value if outcome does not have marketRawHandicapValue', () => {
      expect(service['getOutcomeHandicap']({}, {})).toBeFalsy();
      expect(service['getOutcomeHandicap']({ marketRawHandicapValue: '' }, {})).toBeFalsy();
      expect(service['getOutcomeHandicap']({ marketRawHandicapValue: null }, {})).toBeFalsy();
    });

    it('should return object without price if provided price does not have handicapValueDec', () => {
      expect(service['getOutcomeHandicap']({
        marketRawHandicapValue: 'R',
        outcomeMeaningMajorCode: 'CS'
      }, null)).toEqual({
        type: 'CS',
        raw: null
      });
      expect(service['getOutcomeHandicap']({
        marketRawHandicapValue: 'R',
        outcomeMeaningMajorCode: 'CS'
      }, {})).toEqual({
        type: 'CS',
        raw: ''
      });
    });

    it('isValidOutcome when there is no team external id', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv"})
      const response = {SSResponse: {children: mockOutcomesData4}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData4);
      service.isValidOutcome('240480151').subscribe((response) => {
        expect(response).toEqual(false);
      });
      tick();
    }));

    it('isValidOutcome', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv"})
      const response = {SSResponse: {children: mockOutcomesData}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
      service.isValidOutcome('240480151').subscribe((response) => {
        expect(response).toEqual(true);
      });
      tick();
    }));

    it('isValidOutcome on logout', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv"})
      userService.status = false;
      const response = {SSResponse: {children: mockOutcomesData}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
      service.isValidOutcome('240480151').subscribe((response) => {
        expect(response).toEqual(true);
      });
      tick();
    }));


    it('isValidOutcome when outcome id is different', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv"});
      const response = {SSResponse: {children: mockOutcomesData2}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData2);
      service.isValidOutcome('240480151').subscribe((response) => {
        expect(response).toEqual(false);
      });
      tick();
    }));

    it('isValidOutcome when outcome id is different', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv"});
      const response = {SSResponse: {children: mockOutcomesData2}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
      userService.status = false;
      service.isValidOutcome('240480151').subscribe((response) => {
        expect(service.filteredOutcomeIds).toEqual(['240480151']);
        expect(response).toEqual(true);
      });
      tick();
    }));

    it('isValidOutcome when outcome id is different', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv"});
      const response = {SSResponse: {children: mockOutcomesData}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
      service.isValidOutcome('240480154').subscribe((response) => {
        expect(response).toEqual(true);
      });
      tick();
    }));

    it('isValidOutcome when is no team external id', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv"});
      const response = {SSResponse: {children: mockOutcomesData3}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData3);
      service.isValidOutcome('240480151').subscribe((response) => {
        expect(response).toEqual(false);
      });
      tick();
    }));

    it('isValidOutcome when storage team id is false', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue(undefined);
      const response = {SSResponse: {children: mockOutcomesData3}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData3);
      service.isValidOutcome('240480151').subscribe((response) => {
        expect(response).toEqual(0);
      });
      tick();
    }));

    it('checkIfFzSelection for anonymous user', fakeAsync(() => {
      const fzStorage = {"teamId": "7yx5dqhhphyvfisohikodajhv,"};
      userService.status = false;
      const result = service['checkIfFzSelection'](mockOutcomesData[0], fzStorage);
      expect(result).toBe(true);
    }));

    it('checkIfFzSelection when user is logged in and team id doesnt match', fakeAsync(() => {
      userService.status = true;
      const fzStorage = {"teamId": "7yx5dqhhphyvfisohikodajhv12,"};
      const result = service['checkIfFzSelection'](mockOutcomesData[0], fzStorage);
      expect(result).toBe(true);
    }));

    it('checkIfFzSelection when storage is empty', fakeAsync(() => {
      userService.status = true;
      const fzStorage = {};
      const result = service['checkIfFzSelection'](mockOutcomesData[0], fzStorage);
      expect(result).toBe(0);
    }));

    it('isValidOutcome false when team id doesnt get mapped', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv,"});
        userService.status = undefined;
      const response = {SSResponse: {children: mockOutcomesData5}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData5);
      service.isValidOutcome('240480151').subscribe((response) => {
        expect(response).toEqual(false);
      });
      tick();
    }))

    it('isValidOutcome false when team id doesnt get mapped', fakeAsync(() => {
      fanzoneStorageService.get = jasmine.createSpy('').and.returnValue({
        "teamId": "7yx5dqhhphyvfisohikodajhv,"});
      const response = {SSResponse: {children: mockOutcomesData}};
      siteServerRequestHelperService.getEventsByOutcomeIds = jasmine.createSpy().and.returnValue(observableOf(response));
      betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
      service.isValidOutcome('240480151').subscribe((response) => {
        betslipService.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
        expect(response).toEqual(false);
      });
      tick();
    }));

    it('should return object with correct values', () => {
      expect(service['getOutcomeHandicap']({
        marketRawHandicapValue: 'R',
        outcomeMeaningMajorCode: 'CS'
      }, { handicapValueDec: '+5,' })).toEqual({
        type: 'CS',
        raw: '+5'
      });
    });
  });

  describe('getOutcomePrice', () => {
    const priceType = 'LP';

    it('should return empty price with priceType', () => {
      expect(service['getOutcomePrice']({ priceType })).toEqual({ priceType });
      expect(service['getOutcomePrice']({ children: [], priceType })).toEqual({ priceType });
    });

    it('should return price extended with priceType', () => {
      const price = { priceDec: '1', priceNum: '2' };

      expect(service['getOutcomePrice']({ children: [{ price }], priceType })).toEqual(jasmine.objectContaining({
        priceType,
        ...price
      }));
    });
  });

  describe('definePriceType', () => {
    it('should return "SP" price type for unnamed favourites', () => {
      const marketEntity = { priceTypeCodes: 'LP,' };
      const outcomeEntity1 = { children: [{ price: {} }], name: 'Unnamed Favourite' };
      const outcomeEntity2 = { children: [{ price: {} }], name: 'Unnamed 2ND Favourite' };

      expect(service['definePriceType'](marketEntity, outcomeEntity1)).toEqual('SP');
      expect(service['definePriceType'](marketEntity, outcomeEntity2)).toEqual('SP');
    });

    it('should return "SP" price type for market with not "LP" price type', () => {
      const marketEntity = { priceTypeCodes: 'SP,' };
      const outcomeEntity = { children: [{ price: {} }], name: 'Home' };

      expect(service['definePriceType'](marketEntity, outcomeEntity)).toEqual('SP');
    });

    it('should return "SP" price type if outcome does not have childrens', () => {
      const marketEntity = { priceTypeCodes: 'LP,' };
      const outcomeEntity = { name: 'Home' };

      expect(service['definePriceType'](marketEntity, outcomeEntity)).toEqual('SP');
    });

    it('should return "LP" price type if market has "LP" price type code, outcome has childrens' +
      ' and is not unnamed favourite', () => {
      const marketEntity = { priceTypeCodes: 'LP,' };
      const outcomeEntity = { children: [{ price: {} }], name: 'Home' };

      expect(service['definePriceType'](marketEntity, outcomeEntity)).toEqual('LP');
    });
  });

  describe('checkMaxBetsAmount', () => {
    it('should not remove bet ids if not exceeded max bets config', fakeAsync(() => {
      const ids = '1,2';

      cmsService.getSystemConfig.and.returnValue(observableOf({ Betslip: { maxBetNumber: 3 } }));
      betslipService.count.and.returnValue(1);

      service['checkMaxBetsAmount'](ids).subscribe(result => {
        expect(service.showMaxBetsErr).toBeFalsy();
        expect(result).toEqual(['1', '2']);
      });
      tick();
    }));

    it('should remove excessive new bets if it exceeds max bets config', fakeAsync(() => {
      const ids = '1,2,3,4';

      cmsService.getSystemConfig.and.returnValue(observableOf({ Betslip: { maxBetNumber: 3 } }));
      betslipService.count.and.returnValue(2);

      service['checkMaxBetsAmount'](ids).subscribe(result => {
        expect(service.showMaxBetsErr).toBeTruthy();
        expect(result).toEqual(['1']);
      });
      tick();
    }));
  });

  describe('registerSelection', () => {
    it('should publish event with betslip count', fakeAsync(() => {
      const selection = { id: '1' };
      const doNotRemove = true;
      const isSyncWithNative = false;
      const count = 5;

      betslipService.count.and.returnValue(count);
      betslipService.toggleSelection.and.returnValue(observableOf({}));

      service['registerSelection'](selection, doNotRemove, isSyncWithNative).subscribe(() => {
        expect(pubsub.publishSync).toHaveBeenCalledWith(pubsub.API.BETSLIP_COUNTER_UPDATE, 5);
        expect(pubsub.subscribe).toHaveBeenCalledWith(jasmine.any(String),
          pubsub.API.ADDTOBETSLIP_PROCESS_FINISHED, jasmine.any(Function));
      });
      tick();
    }));
  });

  describe('isLiveEvent', () => {
    it('should return true if event rawIsOffCode equals "Y"', () => {
      const response = {
        SSResponse: {
          children: [{
            event: {
              rawIsOffCode: 'Y'
            }
          }]
        }
      };

      expect(service['isLiveEvent'](response)).toBeTruthy();
    });

    it('should return true if event rawIsOffCode equals "-" and event is started', () => {
      const response = {
        SSResponse: {
          children: [{
            event: {
              rawIsOffCode: '-',
              isStarted: true
            }
          }]
        }
      };

      expect(service['isLiveEvent'](response)).toBeTruthy();
    });

    it('should return false if event rawIsOffCode equals "-" and event is not started', () => {
      const response = {
        SSResponse: {
          children: [{
            event: {
              rawIsOffCode: '-'
            }
          }]
        }
      };

      expect(service['isLiveEvent'](response)).toBeFalsy();
    });

    it('should return false if event rawIsOffCode is neither "--" or "Y"', () => {
      const response = {
        SSResponse: {
          children: [{
            event: {
              rawIsOffCode: 'N'
            }
          }]
        }
      };

      expect(service['isLiveEvent'](response)).toBeFalsy();
    });
  });

  describe('addSelectionsToBetSlip', () => {

    it('should not perform redirect in case of registerSelection fails', fakeAsync(() => {
      const goToBetSlip = false;
      const doNotRemove = true;
      const redirect = true;
      const isSyncWithNative = false;
      const selections = { id: '1' };
      const error = { msg: 'error' };

      betslipService.toggleSelection.and.returnValue(throwError(error));

      service['addSelectionsToBetSlip'](goToBetSlip, doNotRemove, redirect, isSyncWithNative, selections)
        .subscribe(() => {
        }, (result) => {
          tick();

          expect(result).toEqual(error);
          expect(router.navigate).not.toHaveBeenCalled();
          expect(userService.set).not.toHaveBeenCalled();
          expect(pubsub.publish).not.toHaveBeenCalled();
        });
    }));

    it('should perform redirect in case of registerSelection succeed with redirect param', fakeAsync(() => {
      const goToBetSlip = false;
      const doNotRemove = true;
      const redirect = true;
      const isSyncWithNative = false;
      const selections = { id: '1' };

      betslipService.toggleSelection.and.returnValue(observableOf({}));

      service['addSelectionsToBetSlip'](goToBetSlip, doNotRemove, redirect, isSyncWithNative, selections)
        .subscribe(() => {
          tick();

          expect(router.navigate).toHaveBeenCalledWith(['/']);
          expect(userService.set).toHaveBeenCalledWith({ isRedirecting: false });
          expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
        });
    }));

    it('should not open betslip if device is not mobile', fakeAsync(() => {
      const goToBetSlip = true;
      const doNotRemove = true;
      const redirect = false;
      const isSyncWithNative = false;
      const selections = { id: '1' };

      betslipService.toggleSelection.and.returnValue(observableOf({}));
      deviceService.isMobile = false;

      service['addSelectionsToBetSlip'](goToBetSlip, doNotRemove, redirect, isSyncWithNative, selections)
        .subscribe(() => {
          expect(gtmService.push).not.toHaveBeenCalled();
          expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
        });
      tick();
    }));

    it('should not open betslip if device is mobile and goToBetSlip param was false', fakeAsync(() => {
      const goToBetSlip = false;
      const doNotRemove = true;
      const redirect = false;
      const isSyncWithNative = false;
      const selections = { id: '1' };

      betslipService.toggleSelection.and.returnValue(observableOf({}));
      deviceService.isMobile = true;

      service['addSelectionsToBetSlip'](goToBetSlip, doNotRemove, redirect, isSyncWithNative, selections)
        .subscribe(() => {
          expect(gtmService.push).not.toHaveBeenCalled();
          expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
        });
      tick();
    }));

    it('should open betslip if device is mobile and goToBetSlip param was true', fakeAsync(() => {
      const goToBetSlip = true;
      const doNotRemove = true;
      const redirect = false;
      const isSyncWithNative = false;
      const selections = { id: '1' };

      betslipService.toggleSelection.and.returnValue(observableOf({}));
      deviceService.isMobile = true;

      service['addSelectionsToBetSlip'](goToBetSlip, doNotRemove, redirect, isSyncWithNative, selections)
        .subscribe(() => {
          tick(1001);
          expect(gtmService.push).toHaveBeenCalledWith('trackPageview', { virtualUrl: '/betslip-receipt' });
          expect(pubsub.publish.calls.mostRecent().args).toEqual(['show-slide-out-betslip', true]);
        });
      tick();
    }));

    it('should show max bets error popup in case if showMaxBetsErr is true', fakeAsync(() => {
      const goToBetSlip = false;
      const doNotRemove = true;
      const redirect = false;
      const isSyncWithNative = false;
      const selections = { id: '1' };
      const maxBets = 5;

      service.showMaxBetsErr = true;
      service.maxBets = maxBets;
      betslipService.toggleSelection.and.returnValue(observableOf({}));
      deviceService.isMobile = true;

      service['addSelectionsToBetSlip'](goToBetSlip, doNotRemove, redirect, isSyncWithNative, selections)
        .subscribe(() => {
          tick(1001);
          expect(dialogService.openDialog).toHaveBeenCalledWith(DialogService.API.betslip.maxStakeDialog,
            mockComponent, true, { text: maxBets });
          expect(service.showMaxBetsErr).toEqual(false);
          expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
        });
      tick();
    }));

    it('should register multiple selections', fakeAsync(() => {
      const goToBetSlip = true;
      const doNotRemove = true;
      const redirect = true;
      const isSyncWithNative = false;
      const selections = [{ id: '1' }, { id: '2' }];
      const maxBets = 5;

      service.showMaxBetsErr = true;
      service.maxBets = maxBets;
      betslipService.toggleSelection.and.returnValue(observableOf({}));
      deviceService.isMobile = true;

      service['addSelectionsToBetSlip'](goToBetSlip, doNotRemove, redirect, isSyncWithNative, selections)
        .subscribe(() => {
          tick(1001);
          expect(betslipService.toggleSelection.calls.count()).toEqual(selections.length);
          expect(router.navigate.calls.count()).toEqual(1);
          expect(dialogService.openDialog.calls.count()).toEqual(1);
          expect(gtmService.push.calls.count()).toEqual(1);
          expect(service.showMaxBetsErr).toEqual(false);
          expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
        });
      tick();
    }));
  });

  describe('getOutcomes', () => {
    it('should return empty list if no events passed', () => {
      expect(service.getOutcomes(null)).toEqual({events: {}, markets: {}, outcomes: []});
      expect(service.getOutcomes([{ event: {} }])).toEqual({events: {}, markets: {}, outcomes: []});
      expect(service.getOutcomes(undefined)).toEqual({events: {}, markets: {}, outcomes: []});
    });

    it('should return empty list if passed event does not have markets', () => {
      expect(service.getOutcomes([{
        event: {
          children: [{
            market: {}
          }]
        }
      }])).toEqual({events: {}, markets: {}, outcomes: []});
      expect(service.getOutcomes([{
        event: {
          children: [{
            market: {
              children: []
            }
          }]
        }
      }])).toEqual({events: {}, markets: {}, outcomes: []});
    });

    it('should return extended outcome', () => {
      const outcome = {
        id: '111',
        children: [{ price: {} }],
        name: 'Home'
      };
      const market = {
        children: [{ outcome }],
        priceTypeCodes: 'LP,',
        rawHandicapValue: '+5'
      };

      expect(service.getOutcomes([{
        event: {
          children: [{ market }]
        }
      }])).toEqual({events: {}, markets: {}, outcomes: [{
          ...outcome,
          marketRawHandicapValue: market.rawHandicapValue,
          priceType: 'LP'
        }]});
    });
  });

  describe('buildSelections', () => {
    it('should return null passed response does not have events', fakeAsync(() => {
      const response = {
        SSResponse: {
          children: [{}, {}]
        }
      };
      const successHandler = jasmine.createSpy('success');
      const errorHandler = jasmine.createSpy('error');

      service['buildSelections'](response).subscribe(successHandler, errorHandler);
      tick();

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith(jasmine.any(String));
    }));

    it('should return selection from only two correct events', fakeAsync(() => {
      const price = { priceDec: '1', priceNum: '2', handicapValueDec: '+5,' };
      const outcome = {
        id: '111',
        children: [{ price }],
        name: 'Home',
        priceType: 'LP',
        outcomeMeaningMajorCode: 'CS',
        marketId: '222'
      };
      const market = {
        children: [{ outcome }],
        priceTypeCodes: 'LP,',
        rawHandicapValue: '+5',
        id: '222',
        eventId: '111'
      };
      const response = {
        SSResponse: {
          children: [{
            event: {
              children: [{ market }],
              rawIsOffCode: 'Y',
              id: '111'
            }
          }, {
            event: {}
          }]
        }
      };
      const errorHandler = jasmine.createSpy('error');

      service['buildSelections'](response).subscribe((result) => {
        expect(result.length).toEqual(1);
        expect(result[0]).toEqual(jasmine.objectContaining({
          outcomes: [{
            ...outcome,
            marketRawHandicapValue: market.rawHandicapValue,
            priceType: 'LP'
          }],
          handicap: {
            type: 'CS',
            raw: '+5'
          },
          price: {
            ...price,
            priceType: outcome.priceType
          },
          eventIsLive: true
        }));
      }, errorHandler);
      tick();

      expect(errorHandler).not.toHaveBeenCalled();
    }));
  });

  describe('getEventsByOutcomeIds', () => {
    it('should retrieve events and build selection based on empty response', fakeAsync(() => {
      const ids = '1,2';
      const response = {
        SSResponse: {
          children: []
        }
      };
      const successHandler = jasmine.createSpy('success');

      siteServerRequestHelperService.getEventsByOutcomes.and.returnValue(Promise.resolve(response));

      service.getEventsByOutcomeIds(ids)
        .subscribe(successHandler, () => {
          expect(siteServerRequestHelperService.getEventsByOutcomes).toHaveBeenCalledWith({
            outcomesIds: ids,
            isValidFzSelection: false
          });
          service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({});
        });
      tick();

      expect(successHandler).not.toHaveBeenCalled();
    }));

    it('should retrieve events and build selection based on one event', fakeAsync(() => {
      const ids = '1,2';
      const price = { priceDec: '1', priceNum: '2', handicapValueDec: '+5,' };
      const outcome = {
        id: '111',
        children: [{ price }],
        name: 'Home',
        priceType: 'LP',
        outcomeMeaningMajorCode: 'CS',
        eventId: '111',
        marketId: '222'
      };
      const market = {
        children: [{ outcome }],
        priceTypeCodes: 'LP,',
        rawHandicapValue: '+5',
        id: '222',
        eventId: '111'
      };
      const response = {
        SSResponse: {
          children: [{
            event: {
              children: [{ market }],
              rawIsOffCode: 'Y',
              id: '111'
            }
          }, {
            event: {}
          }]
        }
      };

      siteServerRequestHelperService.getEventsByOutcomes.and.returnValue(Promise.resolve(response));

      service.getEventsByOutcomeIds(ids)
        .subscribe(result => {
          expect(siteServerRequestHelperService.getEventsByOutcomes).toHaveBeenCalledWith({
            outcomesIds: ids,
            isValidFzSelection: false
          });
          service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({});
          expect(result[0]).toEqual(jasmine.objectContaining({
            outcomes: [{
              ...outcome,
              marketRawHandicapValue: market.rawHandicapValue,
              priceType: 'LP'
            }],
            handicap: {
              type: 'CS',
              raw: '+5'
            },
            price: {
              ...price,
              priceType: outcome.priceType
            },
            eventIsLive: true
          }));
        });
      tick();
    }));
  });

  describe('addToBetSlip', () => {
    it('should test sorting', fakeAsync(() => {
      const ids = '111,222';
      const goToBetSlip = true;
      const doNotRemove = true;
      const redirect = true;
      const isSyncWithNative = true;
      const fromNative = false;
      const price = { priceDec: '1', priceNum: '2', handicapValueDec: '+5,' };
      const outcome = [
        {
          outcome: {
            id: '222',
            children: [{ price }],
            name: 'Home',
            priceType: 'LP',
            outcomeMeaningMajorCode: 'CS'
          }
        },
        {
          outcome: {
            id: '111',
            children: [{ price }],
            name: 'Home',
            priceType: 'LP',
            outcomeMeaningMajorCode: 'CS'
          }
        }
      ];
      const market = {
        children: [{ outcome }],
        priceTypeCodes: 'LP,',
        rawHandicapValue: '+5'
      };
      const response = {
        SSResponse: {
          children: [{
            event: {
              children: [{ market }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };
      const count = 1;

      deviceService.isMobile = true;
      cmsService.getSystemConfig.and.returnValue(observableOf({ Betslip: { maxBetNumber: 3 } }));
      siteServerRequestHelperService.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      betslipService.count.and.returnValue(count);
      betslipService.toggleSelection.and.returnValue(observableOf({}));

      service.addToBetSlip(ids, goToBetSlip, doNotRemove, redirect, isSyncWithNative, fromNative).subscribe((res) => {
        expect(res.map((selection) => {
          return selection.outcomes[0].id;
        }).join(',')).toEqual(ids);
      });
      tick(1000);
    }));

    it('should show overask in process message', () => {
      service['syncProcess'].inProgress = true;
      overaskService.isInProcess = true;

      service.addToBetSlip('1,2');

      expect(service.isAddToBetslipInProcess()).toBeFalsy();
      expect(overaskService.showOveraskInProgressNotification).toHaveBeenCalled();
    });

    it('should not check for max bets amount if sync was from native', fakeAsync(() => {
      const ids = '1,2';
      const goToBetSlip = false;
      const doNotRemove = true;
      const redirect = false;
      const isSyncWithNative = true;
      const fromNative = true;
      const response = {
        SSResponse: {
          children: []
        }
      };

      siteServerRequestHelperService.getEventsByOutcomes.and.returnValue(Promise.resolve(response));

      service.addToBetSlip(ids, goToBetSlip, doNotRemove, redirect, isSyncWithNative, fromNative).subscribe();
      tick();

      expect(cmsService.getSystemConfig).not.toHaveBeenCalled();
      expect(storageService.set).toHaveBeenCalledWith('betIds', ids);
    }));

    it('should check for unique ids', fakeAsync(() => {
      const rawIds = '1,2,1';

      service.addToBetSlip(rawIds, false, false, false, false, false).subscribe();
      tick();

      expect(storageService.set).toHaveBeenCalledWith('betIds', '1,2');
    }));

    describe('should handle error in case of cms failure', () => {
      it('by navigating to "/betslip/unavailable" and not showing max stake dialog', fakeAsync(() => {
        const ids = '1';
        service.showMaxBetsErr = false;
        cmsService.getSystemConfig.and.returnValue(throwError('Error'));

        service.addToBetSlip(ids).subscribe();
        tick();

        expect(router.navigate).toHaveBeenCalledWith(['/betslip', 'unavailable']);
        expect(siteServerRequestHelperService.getEventsByOutcomes).not.toHaveBeenCalled();
        expect(service.isAddToBetslipInProcess()).toBeFalsy();
      }));

      it('by navigating to home page and showing max stake dialog when redirect is truthy', fakeAsync(() => {
        const ids = '1';
        service.showMaxBetsErr = true;
        service['getEvents'] = { bind: jasmine.createSpy() };
        cmsService.getSystemConfig.and.returnValue(throwError('Error'));
        service['showMaxStakeDialog'] = jasmine.createSpy();

        service.addToBetSlip(ids).subscribe();
        tick();

        expect(service['getEvents'].bind).toHaveBeenCalled();
        expect(router.navigate).toHaveBeenCalledWith(['/']);
        expect(service['showMaxStakeDialog']).toHaveBeenCalled();
        expect(siteServerRequestHelperService.getEventsByOutcomes).not.toHaveBeenCalled();
        expect(service.isAddToBetslipInProcess()).toBeFalsy();
      }));

      it('by showing max stake dialog but not navigating to home page when redirect is falsy', fakeAsync(() => {
        const ids = '1';
        service.showMaxBetsErr = true;
        service['getEvents'] = { bind: jasmine.createSpy() };
        cmsService.getSystemConfig.and.returnValue(throwError('Error'));
        service['showMaxStakeDialog'] = jasmine.createSpy();

        service.addToBetSlip(ids, true, true, false).subscribe();
        tick();

        expect(service['getEvents'].bind).toHaveBeenCalled();
        expect(router.navigate).not.toHaveBeenCalled();
        expect(service['showMaxStakeDialog']).toHaveBeenCalled();
        expect(siteServerRequestHelperService.getEventsByOutcomes).not.toHaveBeenCalled();
        expect(service.isAddToBetslipInProcess()).toBeFalsy();
      }));
    });

    it('should handle error in case of betslipService.toggleSelection failure', fakeAsync(() => {
      const ids = '1';
      const goToBetSlip = true;
      const doNotRemove = true;
      const redirect = false;
      const isSyncWithNative = false;
      const fromNative = false;

      betslipService.toggleSelection.and.returnValue(throwError('error'));

      service.addToBetSlip(ids, goToBetSlip, doNotRemove, redirect, isSyncWithNative, fromNative).subscribe();
      tick();

      expect(router.navigate).toHaveBeenCalledWith(['/betslip', 'unavailable']);
      expect(gtmService.push).not.toHaveBeenCalled();
      expect(service.isAddToBetslipInProcess()).toBeFalsy();
    }));

    it('should return formed selection', fakeAsync(() => {
      const ids = '111';
      const goToBetSlip = true;
      const doNotRemove = true;
      const redirect = true;
      const isSyncWithNative = true;
      const fromNative = false;
      const price = { priceDec: '1', priceNum: '2', handicapValueDec: '+5,' };
      const outcome = {
        id: '111',
        children: [{ price }],
        name: 'Home',
        priceType: 'LP',
        outcomeMeaningMajorCode: 'CS',
        eventId: '111',
        marketId: '222'
      };
      const market = {
        children: [{ outcome }],
        priceTypeCodes: 'LP,',
        rawHandicapValue: '+5',
        eventId: '111',
        id: '222'
      };
      const response = {
        SSResponse: {
          children: [{
            event: {
              children: [{ market }],
              rawIsOffCode: 'Y',
              id: '111'
            }
          }, {
            event: {}
          }]
        }
      };
      const count = 1;
      const mockRacing = {
        location: 'Bet Receipt',
        module: 'RP Tip',
        dimension86: 0,
        dimension87: 0,
        dimension88: null
      };
      deviceService.isMobile = true;
      cmsService.getSystemConfig.and.returnValue(observableOf({ Betslip: { maxBetNumber: 3 } }));
      siteServerRequestHelperService.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      betslipService.count.and.returnValue(count);
      toteBetslipService.isToteBetPresent.and.returnValue(false);
      betslipService.toggleSelection.and.returnValue(observableOf({}));

      service.addToBetSlip(ids, goToBetSlip, doNotRemove, redirect, isSyncWithNative, fromNative, false, mockRacing).subscribe();
      tick(1001);

      expect(router.navigate).toHaveBeenCalledWith(['/']);
      expect(gtmService.push).toHaveBeenCalled();
      expect(betslipService.toggleSelection).toHaveBeenCalledWith(jasmine.objectContaining({
        outcomes: [{
          id: outcome.id,
          children: [{
            price: {
              ...price,
              priceType: outcome.priceType
            }
          }],
          name: 'Home',
          priceType: 'LP',
          outcomeMeaningMajorCode: 'CS',
          marketRawHandicapValue: '+5',
          eventId: '111',
          marketId: '222'
        }],
        handicap: {
          type: outcome.outcomeMeaningMajorCode,
          raw: market.rawHandicapValue
        },
        price: {
          ...price,
          priceType: outcome.priceType
        },
        eventIsLive: true,
        details: jasmine.objectContaining({isSPLP: false, marketPriceTypeCodes: 'LP,'}),
        GTMObject: {
          eventAction: 'add to betslip',
          tracking: {
            module: 'banner',
            location: 'betslip/add/4123'
          }
        }
      }), doNotRemove, isSyncWithNative);
      expect(pubsub.publishSync).toHaveBeenCalledWith(pubsub.API.BETSLIP_COUNTER_UPDATE, count);
    }));

    it('should set flag to prevent route reload', fakeAsync(() => {
      spyOn(service, 'addSelectionsToBetSlip');
      service.addToBetSlip('', false, false, true, false, false).subscribe();
      tick();

      expect(userService.set).toHaveBeenCalledWith({ isRedirecting: true });
    }));

    it('should NOT set flag to prevent route reload', fakeAsync(() => {
      spyOn(service, 'addSelectionsToBetSlip');
      service.addToBetSlip('', false, false, false, false, false).subscribe();
      tick();

      expect(userService.set).not.toHaveBeenCalled();
    }));

    it('should show limitations popup', () => {
      toteBetslipService.isToteBetPresent.and.returnValue(true);
      service.addToBetSlip('', false, false, false, false, false);

      expect(router.navigate).toHaveBeenCalled();
      expect(betslipService.showBetslipLimitationPopup).toHaveBeenCalled();
    });
  });

  describe('syncToBetslip', () => {
    it('should show betslip limitation popup', fakeAsync(() => {
      toteBetslipService.isToteBetPresent.and.returnValue(true);

      service.syncToBetslip({}).subscribe(result => {
        tick(1001);
        expect(result).toBeNull();
        expect(service.isAddToBetslipInProcess()).toBeFalsy();
        expect(betslipService.showBetslipLimitationPopup).toHaveBeenCalled();
      });
      tick();
    }));

    it('should show betslip limitation popup', fakeAsync(() => {
      toteBetslipService.isToteBetPresent.and.returnValue(false);
      service['syncProcess'].inProgress = true;
      overaskService.isInProcess = true;

      service.syncToBetslip({}).subscribe(result => {
        expect(result).toBeNull();
        expect(service.isAddToBetslipInProcess()).toBeFalsy();
        expect(overaskService.showOveraskInProgressNotification).toHaveBeenCalled();
      });
      tick();
    }));

    describe('should sync simple bet', () => {
      let price, outcome, eventData, betSelection, expectedPrice;

      beforeEach(() => {
        price = { priceDec: '1', priceNum: '2', handicapValueDec: '+5,' };
        outcome = {
          id: '111',
          prices: [price],
          name: 'Home',
          priceType: 'LP',
          marketRawHandicapValue: 'H',
          outcomeMeaningMajorCode: 'CS'
        };
        eventData = [
          {
            markets: [ {
              outcomes: [outcome],
              priceTypeCodes: 'LP,',
              rawHandicapValue: '+5'
            } ],
            rawIsOffCode: 'Y'
          }, {}
        ];
        betSelection = {
          outcomeId: '1',
          type: 'simple',
          userStake: '2.00',
          userEachWay: false,
          price: {
            priceType: 'LP'
          },
          isVirtual: false,
          eventId: 123,
          isOutright: false,
          isSpecial: false,
          GTMObject: {
            eventAction: 'event'
          }
        };
        expectedPrice = { priceType: 'LP' };
        toteBetslipService.isToteBetPresent.and.returnValue(false);
        service['syncProcess'].inProgress = false;
        overaskService.isInProcess = false;
        siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.resolve(eventData));
        spyOn(service as any, 'getOutcomeHandicap').and.callThrough();
        spyOn(service, 'addSelectionsToBetSlip').and.returnValue(observableOf());
        spyOn(service as any, 'normalizeScorecastOutcomes').and.callThrough();
      });

      it('when price is provided', () => {});
      it('when price is not provided', () => {
        delete betSelection.price;
        expectedPrice = { priceDec: '1', priceNum: '2', handicapValueDec: '+5,' };
      });

      afterEach(fakeAsync(() => {
        service.syncToBetslip(betSelection).subscribe();
        tick();
        expect(storageService.set).toHaveBeenCalledWith('betIds', '1');
        expect(service.getOutcomeHandicap).toHaveBeenCalled();
        expect((service as any).normalizeScorecastOutcomes).not.toHaveBeenCalled();
        expect(service.addSelectionsToBetSlip).toHaveBeenCalledWith(false, false, false, true, [{
          userStake: '2.00',
          userEachWay: false,
          outcomes: [outcome],
          handicap: { type: 'CS', raw: '+5' },
          price: expectedPrice,
          eventIsLive: true,
          isVirtual: false,
          eventId: 123,
          isOutright: false,
          isSpecial: false,
          GTMObject: { eventAction: 'event' },
          details: jasmine.objectContaining({ marketPriceTypeCodes: 'LP,' })
        }], 0);
      }));
    });

    it('should sync not simple bet', fakeAsync(() => {
      const price = { priceDec: '1', priceNum: '2', handicapValueDec: '+5,' };
      const outcome = {
        id: '111',
        prices: [price],
        name: 'Home',
        priceType: 'LP',
        marketRawHandicapValue: 'H',
        outcomeMeaningMajorCode: 'CS'
      };
      const eventData = [
        {
          markets: [ {
            outcomes: [outcome],
            priceTypeCodes: 'LP,',
            rawHandicapValue: '+5'
          } ],
          rawIsOffCode: 'N'
        }, {}
      ];
      const betSelection = {
        outcomeId: '1',
        type: 'notSimple',
        userStake: '2.00',
        userEachWay: false,
        price: {
          priceType: 'LP'
        },
        isVirtual: false,
        eventId: 123,
        isOutright: false,
        isSpecial: false,
        GTMObject: {
          eventAction: 'event'
        }
      };

      toteBetslipService.isToteBetPresent.and.returnValue(false);
      service['syncProcess'].inProgress = false;
      overaskService.isInProcess = false;
      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.resolve(eventData));
      spyOn(service, 'addSelectionsToBetSlip').and.returnValue(observableOf());
      spyOn(service as any, 'normalizeScorecastOutcomes').and.callThrough();

      service.syncToBetslip(betSelection as IBetSelection).subscribe();
      tick();
      expect(service.addSelectionsToBetSlip).toHaveBeenCalledWith(false, false, false, true, [{
        userStake: '2.00',
        userEachWay: false,
        outcomes: [outcome],
        handicap: undefined,
        type: 'NOTSIMPLE',
        price: { priceType: 'LP' },
        eventIsLive: false,
        isVirtual: false,
        eventId: 123,
        isOutright: false,
        isSpecial: false,
        GTMObject: { eventAction: 'event' }
      }], 0);
      expect((service as any).normalizeScorecastOutcomes).not.toHaveBeenCalled();
    }));

    describe('should sync scorecast bet', () => {
      let outcome1, outcome2, eventData, betSelection, sortedOutcomes;

      beforeEach(() => {
        outcome1 = { id: '2', name: 'FS' };
        outcome2 = { id: '1', name: 'CS' };
        eventData = [{ markets: [
          { outcomes: [outcome1], priceTypeCodes: 'LP,' },
          { outcomes: [outcome2], priceTypeCodes: 'LP,' }
        ] }];
        betSelection = {
          outcomeId: [1, 2],
          type: 'scorecast'
        };
        sortedOutcomes = [jasmine.objectContaining(outcome2), jasmine.objectContaining(outcome1)];
        toteBetslipService.isToteBetPresent.and.returnValue(false);
        overaskService.isInProcess = false;
        service['syncProcess'].inProgress = false;
        siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.resolve(eventData));
        spyOn(service, 'addSelectionsToBetSlip').and.returnValue(observableOf());
      });

      it('and restore original outcomes order', () => {});
      it('and attempt to restore outcomes order', () => {
        betSelection.outcomeId = 1;
      });
      it('and attempt to restore outcomes order ', () => {
        betSelection.outcomeId = [3, 1];
      });
      it('and keep existing outcomes order (fallback)', () => {
        betSelection.outcomeId = [undefined, null];
        sortedOutcomes = [jasmine.objectContaining(outcome1), jasmine.objectContaining(outcome2)];
      });
      afterEach(fakeAsync(() => {
        service.syncToBetslip(betSelection).subscribe();
        tick();
        expect(service.addSelectionsToBetSlip).toHaveBeenCalledWith(false, false, false, true,
          [jasmine.objectContaining({ outcomes: sortedOutcomes, type: 'SCORECAST' })], 0);
      }));
    });

    it('should save event',  () => {
      const setterSpy = spyOnProperty(betslipStorageService, 'setEventToBetslipObservable', 'set');

      service.getEvent = jasmine.createSpy('getEvent').and.returnValue(observableOf({}));
      service.syncToBetslip({});

      expect(service.getEvent).toHaveBeenCalled();
      expect(setterSpy).toHaveBeenCalled();
    });

    it('should return betSelection observable if type is simple', fakeAsync(() => {
      const betSelection = {
        outcomeId: '1',
        type: 'simple',
        userStake: '2.00',
        userEachWay: false,
        price: {
          priceType: 'LP'
        },
        isVirtual: false,
        GTMObject: {
          eventAction: 'event'
        }
      };
      const events = [{
        prices: [{}],
        markets: [{
          outcomes: [{}]
        }]
      }];

      service.getEvent = jasmine.createSpy('getEvent').and.returnValue(observableOf(events));
      service.getOutcomesFromQuickBetEvent = jasmine.createSpy('getOutcomesFromQuickBetEvent').and.returnValue(events);
      service.getOutcomeHandicap = jasmine.createSpy('getOutcomeHandicap').and.returnValue({});

      service.syncToBetslip(betSelection as IBetSelection).subscribe(() => {
        expect(service.getOutcomesFromQuickBetEvent).toHaveBeenCalled();
        expect(service.getOutcomeHandicap).toHaveBeenCalled();
      });

      tick();
    }));

    it('should return betSelection observable if type is notSimple', fakeAsync(() => {
      const betSelection = {
        outcomeId: '1',
        type: 'notSimple',
        userStake: '2.00',
        userEachWay: false,
        price: {
          priceType: 'LP'
        },
        isVirtual: false,
        GTMObject: {
          eventAction: 'event'
        }
      };
      const event = [
        {
          prices: [{}],
          markets: [
            {
              outcomes: [{name: 'unnamed favourite'}],
              priceTypeCodes: []
            }
          ]
        }
      ];

      service.getEvent = jasmine.createSpy('getEvent').and.returnValue(observableOf(event));
      service.getOutcomeHandicap = jasmine.createSpy('getOutcomeHandicap').and.returnValue({});

      service.syncToBetslip(betSelection as IBetSelection).subscribe(() => {
        expect(service.getOutcomeHandicap).not.toHaveBeenCalled();
      });

      tick();
    }));
  });

  describe('sortSelectionBasedOnIds', () => {
    it(`should filter undefined selections`, () => {
      const selectionsStub = [{ outcomes: [{ id: '222' }] }] as any;
      const res = service['sortSelectionBasedOnIds']('333,222', selectionsStub);
      expect(res.every(el => el)).toBeTruthy();
    });
  });

  describe('reuseSelections', () => {
    it('overask in process', () => {
      overaskService.isInProcess = true;
      service.reuseSelections([], []);
      expect(overaskService.showOveraskInProgressNotification).toHaveBeenCalledTimes(1);
    });

    it('navigate to betslip true', () => {
      overaskService.isInProcess = true;
      service.reuseSelections([], [], false, true);
      expect(overaskService.showOveraskInProgressNotification).toHaveBeenCalledTimes(1);
    });

    it('getEvents when user is logged in and selection is valid', fakeAsync(() => {
      service.isValidSelection = true;
      userService.status = true;
      service['getEvents']('1318944369,1318944368,1318944367');
      tick();
    }))

    it('getEvents when user is not logged in and selection is not valid', fakeAsync(() => {
      service.isValidSelection = false;
      userService.status = false;
      service['getEvents']('1318944369,1318944368,1318944367');
      tick();
    }))

    it('success', fakeAsync(() => {
      service['getEvents'] = jasmine.createSpy().and.returnValue(observableOf(null));
      service['buildSelectionsFromBetReceipts'] = jasmine.createSpy();
      service['gtmTrackAddToBetSlip'] = jasmine.createSpy();
      service['addSelectionsToBetSlip'] = jasmine.createSpy().and.returnValue(observableOf(null));

      service.reuseSelections([], []).subscribe();
      tick();

      expect(storageService.set).toHaveBeenCalledTimes(1);
      expect(service['getEvents']).toHaveBeenCalledTimes(1);
      expect(service['buildSelectionsFromBetReceipts']).toHaveBeenCalledTimes(1);
      expect(service['gtmTrackAddToBetSlip']).toHaveBeenCalledTimes(1);
      expect(service['addSelectionsToBetSlip']).toHaveBeenCalledTimes(1);
    }));

    it('error', fakeAsync(() => {
      service['getEvents'] = jasmine.createSpy().and.returnValue(throwError(null));

      service.reuseSelections([], []).subscribe();
      tick();

      expect(storageService.set).toHaveBeenCalledTimes(1);
      expect(service['getEvents']).toHaveBeenCalledTimes(1);
      expect(router.navigate).toHaveBeenCalledTimes(1);
    }));
    it('error', fakeAsync(() => {
      service['getEvents'] = jasmine.createSpy().and.returnValue(throwError(20));

      service.reuseSelections([], []).subscribe();
      tick();

      expect(storageService.set).toHaveBeenCalledTimes(1);
      expect(service['getEvents']).toHaveBeenCalledTimes(1);
      expect(router.navigate).not.toHaveBeenCalled();
    }));
  });

  describe('buildSelectionsFromBetReceipts', () => {
    let siteServeResponse;

    beforeEach(() => {
      siteServeResponse = {
        SSResponse: {
          children: [{
            event: {
              id: '111',
              children: [{
                market: {
                  priceTypeCodes: 'LP',
                  id: '222',
                  eventId: '111',
                  isSCAvailable: true,
                  children: [{
                    outcome: {
                      id: 1,
                      eventId: '111',
                      marketId: '222',
                      name: 'Outcome 1',
                      children: [{
                        price: {
                          priceDec: '11.00',
                          priceDen: '1',
                          priceNum: '10',
                          priceType: 'LP'
                        }
                      }]
                    }
                  }, {
                    outcome: {
                      id: 2,
                      eventId: '111',
                      marketId: '222',
                      name: 'Outcome 2',
                      children: [{
                        price: {
                          priceDec: '3.00',
                          priceDen: '1',
                          priceNum: '2',
                          priceType: 'LP'
                        }
                      }]
                    }
                  }]
                }
              }]
            }
          }]
        }
      };
    });

    it('should handle case when no events returned from SS', () => {
      spyOn(service, 'getOutcomes');
      service['buildSelectionsFromBetReceipts']({
        SSResponse: {
          children: [{}]
        }
      }, []);
      expect(service.getOutcomes).not.toHaveBeenCalled();
    });

    it('should build single and multiple selections', () => {
      const receipts = [{
          betType: 'SGL',
          isFCTC: true,
          leg: [{
            part: [{
              outcome: 1,
              event: {
                rawIsOffCode: 'Y'
              }
            }],
            eventEntity: {
              categoryId: '1',
              typeId: '1',
              id: '1',
              originalName: 'abc',
              name: 'abc',
              markets: [{
                marketName: 'qa',
                name: 'qa'
              }]
            }
          }]
        },
        {
          betType: 'SGL',
          leg: [{
            part: [{
              outcome: 1,
              event: {
                rawIsOffCode: '-',
                isStarted: true
              }
            }],
            eventEntity: {
              categoryId: '1',
              typeId: '1',
              id: '1',
              originalName: 'abc',
              name: 'abc',
              markets: [{
                marketName: 'qa',
                name: 'qa'
              }]
            }
          }]
        },
        {
          betType: 'DBL',
          leg: [{
              part: [{
                outcome: 1,
                event: {
                  rawIsOffCode: 'Y'
                }
              }],
              eventEntity: {
                categoryId: '1',
                typeId: '1',
                id: '1',
                originalName: 'abc',
                name: 'abc',
                markets: [{
                  marketName: 'qa',
                  name: 'qa'
                }]
              }
            },
            {
              part: [{
                outcome: 2,
                event: {
                  rawIsOffCode: '-',
                  isStarted: true
                }
              }],
              eventEntity: {
                categoryId: '1',
                typeId: '1',
                id: '1',
                originalName: 'abc',
                name: 'abc',
                markets: [{
                  marketName: 'qa',
                  name: 'qa'
                }]
              }
            }
          ]
        }
      ];
      siteServeResponse.SSResponse.children[0].event.children[0].market.children[0].outcome.eventId = null;
      const result = service['buildSelectionsFromBetReceipts'](siteServeResponse, receipts);

      expect(result.length).toBe(3);
      expect(result[0].price).toEqual({
        priceDec: '11.00',
        priceDen: '1',
        priceNum: '10',
        priceType: 'LP'
      });
    });

    it('should build single and multiple selections with no event entity', () => {
      const receipts = [{
          betType: 'SGL',
          isFCTC: true,
          leg: [{
            part: [{
              outcome: 1,
              event: {
                rawIsOffCode: 'Y'
              }
            }],
            eventEntity: undefined
          }]
        },
        {
          betType: 'SGL',
          leg: [{
            part: [{
              outcome: 1,
              event: {
                rawIsOffCode: '-',
                isStarted: true
              }
            }],
            eventEntity: {
              categoryId: '1',
              typeId: '1',
              id: '1',
              originalName: 'abc',
              name: 'abc',
              markets: [{
                marketName: 'qa',
                name: 'qa'
              }]
            }
          }]
        },
        {
          betType: 'DBL',
          leg: [{
              part: [{
                outcome: 1,
                event: {
                  rawIsOffCode: 'Y'
                }
              }],
              eventEntity: undefined
            },
            {
              part: [{
                outcome: 2,
                event: {
                  rawIsOffCode: '-',
                  isStarted: true
                }
              }],
              eventEntity: undefined
            }
          ]
        }
      ];
      siteServeResponse.SSResponse.children[0].event.children[0].market.children[0].outcome.eventId = null;
      const result = service['buildSelectionsFromBetReceipts'](siteServeResponse, receipts);

      expect(result.length).toBe(3);
      expect(result[0].price).toEqual({
        priceDec: '11.00',
        priceDen: '1',
        priceNum: '10',
        priceType: 'LP'
      });
    });

    it('should return 3 selections', () => {
      siteServeResponse.SSResponse.children[0].event.children[0].market.children.push({
        outcome: {
          id: 3,
          name: 'Outcome 3',
          marketId: '222',
          children: [{
            price: {
              priceDec: '3.00',
              priceDen: '1',
              priceNum: '2',
              priceType: 'LP'
            }
          }]
        }
      });

      const receipts = [{
        betType: 'DBL',
        leg: [{
          part: [{
            outcome: 1, event: { rawIsOffCode: 'Y' }
          }],
          eventEntity: {
            categoryId: '1',
            typeId: '1',
            id: '1',
            originalName: 'abc',
            name: 'abc',
            markets: [{
              marketName: 'qa',
              name: 'qa'
            }]
          }
        }, {
          part: [{
            outcome: 2, event: { rawIsOffCode: '-', isStarted: true }
          }],
          eventEntity: {
            categoryId: '1',
            typeId: '1',
            id: '1',
            originalName: 'abc',
            name: 'abc',
            markets: [{
              marketName: 'qa',
              name: 'qa'
            }]
          }
        }]
      }, {
        betType: 'TRX',
        leg: [{
          part: [{
            outcome: 1, event: { rawIsOffCode: 'Y' },
          }],
          eventEntity: {
            categoryId: '1',
            typeId: '1',
            id: '1',
            originalName: 'abc',
            name: 'abc',
            markets: [{
              marketName: 'qa',
              name: 'qa'
            }]
          }
        }, {
          part: [{
            outcome: 2, event: { rawIsOffCode: '-', isStarted: true }
          }],
          eventEntity: {
            categoryId: '1',
            typeId: '1',
            id: '1',
            originalName: 'abc',
            name: 'abc',
            markets: [{
              marketName: 'qa',
              name: 'qa'
            }]
          }
        }, {
          part: [{
            outcome: 3, event: { rawIsOffCode: '-', isStarted: false }
          }],
          eventEntity: {
            categoryId: '1',
            typeId: '1',
            id: '1',
            originalName: 'abc',
            name: 'abc',
            markets: [{
              marketName: 'qa',
              name: 'qa'
            }]
          }
        }]
      }];
      const result = service['buildSelectionsFromBetReceipts'](siteServeResponse, receipts);

      expect(result.length).toBe(3);
    });

    it('should build scorecast selection', () => {
      const receipts = [{
        betType: 'SGL',
        odds: {
          dec: '17.00',
          frac: '16/1'
        },
        leg: [{
          legSort: 'SC',
          part: [{
            outcome: 1
          }, {
            outcome: 2
          }],
          eventEntity: {
            categoryId: '1',
            typeId: '1',
            id: '1',
            originalName: 'abc',
            name: 'abc',
            markets: [{
              marketName: 'qa',
              name: 'qa'
            }]
          }
        }]
      }];
      const result = service['buildSelectionsFromBetReceipts'](siteServeResponse, receipts);

      expect(result.length).toEqual(1);
      expect(result[0].type).toEqual('SCORECAST');
      expect(result[0].price).toEqual({
        priceDec: '17.00',
        priceDen: 1,
        priceNum: 16,
        priceType: 'LP'
      });
    });
  });

  describe('gtmTrackAddToBetSlip', () => {
    const emptyGtmData = {
      eventAction: 'add to betslip',
      eventLabel: 'success',
      event: 'trackEvent',
      eventCategory: 'betslip',
      ecommerce: {
        add: {
          products: []
        }
      }
    };
    const racingPostGA = {
      location: 'Bet Receipt',
      module: 'RP Tip',
      dimension86: 0,
      dimension87: 0,
      dimension88: null
    } as any;
    it('should track add to betslip with deep link (/betslip/add/{outcomedId})', () => {
      const eventsResponse = {
        SSResponse: {
          children: [{
            event: {
              name: 'event name 1',
              id: '742345',
              categoryId: 52,
              isYourCallBet: 'false',
              typeId: '34',
              isStarted: false,
              children: [{
                market: {
                  name: 'Market name 11',
                  children: [
                    { outcome: { id: 2 } },
                    { outcome: { id: 6 } },
                  ]
                }
              }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };
      const racingMockData = {};
      service['gtmTrackAddToBetSlip'](eventsResponse, false, racingMockData);
      expect(gtmTrackingService.restoreTracking).toHaveBeenCalledWith({
        module: 'banner',
        location: 'betslip/add/4123'
      });

      const gtmData = {
        eventAction: 'add to betslip',
        eventLabel: 'success',
        event: 'trackEvent',
        eventCategory: 'betslip',
        ecommerce: {
          add: {
            products: [{
              name: 'event name 1',
              category: '52',
              variant: '34',
              brand: 'Market name 11',
              dimension60: '742345',
              dimension61: 2,
              dimension62: 0,
              dimension63: 0,
              dimension64: 'betslip/add/4123',
              dimension65: 'banner',
              dimension166: 'normal'
            }, {
              name: 'event name 1',
              category: '52',
              variant: '34',
              brand: 'Market name 11',
              dimension60: '742345',
              dimension61: 6,
              dimension62: 0,
              dimension63: 0,
              dimension64: 'betslip/add/4123',
              dimension65: 'banner',
              dimension166: 'normal'
            }]
          }
        }
      };

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });

    it('should add data to reuseBetSelections from else condition', () => {
      storageService.get.and.returnValue(undefined);
      const eventsResponse = {
        SSResponse: {
          children: [{
            event: {
              name: 'event name 1',
              id: '742345',
              categoryId: 52,
              isYourCallBet: 'false',
              typeId: '34',
              isStarted: false,
              children: [{
                market: {
                  name: 'Market name 11',
                  children: [
                    { outcome: { id: 2 } }
                  ]
                }
              }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };
      const racingMockData = {};
      const tracking = {
        2: {
          betType: "reuse",
          location: undefined,
          module: "origin_module"
        }
      };
      service['gtmTrackAddToBetSlip'](eventsResponse, true, racingMockData);
      expect(storageService.set).toHaveBeenCalledWith('reuseBetSelections', tracking);
    });

    it('should add data to reuseBetSelections from if condition', () => {
      storageService.get.and.returnValue({
        "742346": {
          location: 'origin_location',
          module: 'origin_module'
        }
      });
      const eventsResponse = {
        SSResponse: {
          children: [{
            event: {
              name: 'event name 1',
              id: '742345',
              categoryId: 52,
              isYourCallBet: 'false',
              typeId: '34',
              isStarted: false,
              children: [{
                market: {
                  name: 'Market name 11',
                  children: [
                    { outcome: { id: 2 } }
                  ]
                }
              }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };
      const racingMockData = {};
      const tracking = {
        2: {
          "location": undefined,
          "module": "origin_module",
          "betType": "reuse"
        },
        742346: {
          "location": "origin_location",
          "module": "origin_module"
        }
      };
      service['gtmTrackAddToBetSlip'](eventsResponse, true, racingMockData);
      expect(storageService.set).toHaveBeenCalledWith('reuseBetSelections', tracking);
    });
    it('should track add to betslip with deep link', () => {
      const eventsResponse = {
        SSResponse: {
          children: [{
            event: {
              name: 'event name 1',
              id: '742345',
              categoryId: 52,
              isYourCallBet: 'false',
              typeId: '34',
              isStarted: false,
              children: [{
                market: {
                  name: 'Market name 11',
                  children: [
                    { outcome: { id: 2 } },
                    { outcome: { id: 6 } },
                  ]
                }
              }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };

      service['gtmTrackAddToBetSlip'](eventsResponse, false, racingPostGA);
      expect(gtmTrackingService.restoreTracking).toHaveBeenCalledWith({
        module: 'banner',
        location: 'betslip/add/4123'
      });

      const gtmData = {
        eventAction: 'add to betslip',
        eventLabel: 'success',
        event: 'trackEvent',
        eventCategory: 'betslip',
        ecommerce: {
          add: {
            products: [{
              brand: 'Market name 11',
              category: '52',
              dimension60: '742345',
              dimension61: 2,
              dimension62: 0,
              dimension63: 0,
              dimension64: 'Bet Receipt',
              dimension65: 'RP Tip',
              dimension88: null,
              dimesnion86: 0,
              dimesnion87: 0,
              name: 'event name 1',
              quantity: undefined,
              variant: '34',
              dimension166: 'normal'
            }, {
              brand: 'Market name 11',
              category: '52',
              dimension60: '742345',
              dimension61: 6,
              dimension62: 0,
              dimension63: 0,
              dimension64: 'Bet Receipt',
              dimension65: 'RP Tip',
              dimension88: null,
              dimesnion86: 0,
              dimesnion87: 0,
              name: 'event name 1',
              quantity: undefined,
              variant: '34',
              dimension166: 'normal'
            }]
          }
        }
      };

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });

    it('should handle empty event list', () => {
      const eventsResponse = {
        SSResponse: {
          children: [{}]
        }
      };
      const mock = {};
      service['gtmTrackAddToBetSlip'](eventsResponse, false, mock);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', emptyGtmData);
    });

    it('should set products = [] when no outcomes', () => {
      const eventsResponse = {
        SSResponse: {
          children: [{
            event: {
              name: 'event name 1',
              id: '742345',
              categoryId: 52,
              isYourCallBet: 'false',
              typeId: '34',
              isStarted: false,
              children: [{
                market: {
                  name: 'Market name 11',
                }
              }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };
      const racing = {};
      service['gtmTrackAddToBetSlip'](eventsResponse, false, racing);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', emptyGtmData);
    });

    it('should set isYourCall (dimension63) and isStarted (dimension62) to equal 1', () => {
      const eventsResponse = {
        SSResponse: {
          children: [{
            event: {
              name: 'event name 1',
              id: '742345',
              categoryId: 52,
              isYourCallBet: 'true',
              typeId: '34',
              isStarted: true,
              children: [{
                market: {
                  name: 'Market name 11',
                  children: [
                    { outcome: { id: 2 } }
                  ]
                }
              }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };
      const racingMock = {};
      service['gtmTrackAddToBetSlip'](eventsResponse, false, racingMock);

      const gtmData = {
        eventAction: 'add to betslip',
        eventLabel: 'success',
        event: 'trackEvent',
        eventCategory: 'betslip',
        ecommerce: {
          add: {
            products: [{
              name: 'event name 1',
              category: '52',
              variant: '34',
              brand: 'Market name 11',
              dimension60: '742345',
              dimension61: 2,
              dimension62: 1,
              dimension63: 1,
              dimension64: 'betslip/add/4123',
              dimension65: 'banner',
              dimension166: 'normal'
            }]
          }
        }
      };

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });

    it('should track reuse selection', () => {
      const eventsResponse = {
        SSResponse: {
          children: [{
            event: {
              name: 'event name 1',
              id: '742345',
              categoryId: 52,
              isYourCallBet: 'true',
              typeId: '34',
              isStarted: true,
              children: [{
                market: {
                  name: 'Market name 11',
                  children: [
                    { outcome: { id: 2 } }
                  ]
                }
              }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };
      const racingDataMock = {};
      service['gtmTrackAddToBetSlip'](eventsResponse, true, racingDataMock, undefined, 'betslip');
      const gtmData = {
        eventAction: 'reuse selection',
        eventLabel: 'success',
        event: 'trackEvent',
        eventCategory: 'betslip',
        ecommerce: {
          add: {
            products: [{
              name: 'event name 1',
              category: '52',
              variant: '34',
              brand: 'Market name 11',
              dimension60: '742345',
              dimension61: 2,
              dimension62: 1,
              dimension63: 1,
              dimension64: 'betslip',
              dimension65: 'origin_module',
              dimension166: 'reuse'
            }]
          }
        }
      };

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });

    it('should take dynamically entered module name', () => {
      const eventsResponse = {
        SSResponse: {
          children: [{
            event: {
              name: 'event name 1',
              id: '742345',
              categoryId: 52,
              isYourCallBet: 'true',
              typeId: '34',
              isStarted: true,
              children: [{
                market: {
                  name: 'Market name 11',
                  children: [
                    { outcome: { id: 2 } }
                  ]
                }
              }],
              rawIsOffCode: 'Y'
            }
          }, {
            event: {}
          }]
        }
      };

      const trackingModule = 'Dynamic module test';

      service['gtmTrackAddToBetSlip'](eventsResponse, true, '', trackingModule, 'betslip');
      const gtmData = {
        eventAction: 'reuse selection',
        eventLabel: 'success',
        event: 'trackEvent',
        eventCategory: 'betslip',
        ecommerce: {
          add: {
            products: [{
              name: 'event name 1',
              category: '52',
              variant: '34',
              brand: 'Market name 11',
              dimension60: '742345',
              dimension61: 2,
              dimension62: 1,
              dimension63: 1,
              dimension64: 'betslip',
              dimension65: 'Dynamic module test',
              dimension166: 'reuse'
            }]
          }
        }
      };

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });

    it('should return observable of event',  fakeAsync(() => {
      const idsArray = [1, 2];

      service.getEvent(idsArray).subscribe((res) => {
        expect(res).toEqual({});
      });
      tick();

      expect(siteServerService.getEventsByOutcomeIds).toHaveBeenCalledWith({ outcomesIds: idsArray, racingFormOutcome: true });
    }));

    describe('getOutcomesFromQuickBetEvent', () => {
      it('should return empty list of outcomes',  () => {
        const event = {
          prices: [{}],
          markets: [
            {
              outcomes: [{name: 'unnamed favourite'}],
              priceTypeCodes: [],
              rawHandicapValue: '1'
            }
          ]
        };
        const expectedResult = [{ name: 'unnamed favourite', marketRawHandicapValue: '1', priceType: 'SP' }];

        expect(service.getOutcomesFromQuickBetEvent(event)).toEqual(expectedResult);
      });

      it('should return list with outcomes',  () => {
        const event = {
          markets: [
            {
              outcomes: [
                {
                  id: 1,
                  name: 'unnamed favourite'
                }
              ],
              rawHandicapValue: 1,
              priceTypeCodes: 'LP',
            }
          ]
        } as any;

        expect(service.getOutcomesFromQuickBetEvent(event).length).toEqual(1);
      });
    });
  });

  describe('handleDirectLinkOutcome', () => {
    it('handleDirectLinkOutcome', fakeAsync(() => {
      const selections = <any>[
        {
          outcomes: [
            {
              outcomeStatusCode: 'A'
            }
          ]
        }
      ];
      service.handleDirectLinkOutcome(selections);
      tick(2500);
      expect(pubsub.publishSync).not.toHaveBeenCalledWith('BS_SHOW_SUSP_OVERLAY');
    }));

    it('handleDirectLinkOutcome (suspended)', fakeAsync(() => {
      const selections = <any>[
        {
          outcomes: [
            {
              outcomeStatusCode: 'S'
            }
          ]
        }
      ];
      service.handleDirectLinkOutcome(selections);
      tick(2500);

      expect(pubsub.publishSync).toHaveBeenCalledWith('BS_SHOW_SUSP_OVERLAY');
    }));
  });

  describe('#getOutComeId', () => {
    it("if event outcome is an array", () => {
      const part = [{
          outcome: [1],
          outcomeId: 1
        }];
      const result = service['getOutComeId'](part[0]);
      expect(result).toBe(1);
    });
    it("if event outcome is not an array", () => {
      const part = [{
        outcome: 1
      }];
      const result = service['getOutComeId'](part[0]);
      expect(result).toBe(1);
    });
  });
});
