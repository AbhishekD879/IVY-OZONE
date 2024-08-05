import { of, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { IBetHistoryBet, IBetHistoryLeg } from '@app/betHistory/models/bet-history.model';
import { EditMyAccaService } from './edit-my-acca.service';

describe('EditMyAccaService', () => {
  let service: EditMyAccaService;
  let cmsService;
  let pubSubService;
  let betHistoryMainService;
  let bppService;
  let clientUserAgentService;
  let deviceService;
  let infoDialogService;
  let localeService;
  let windowRefService;
  let siteServerService;
  let domToolsService;
  let awsService;
  let gtm;
  let openCancelDialogCb;
  let timeSyncService;
  let storageService;

  beforeEach(() => {
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriber, method, cb ) => {
        if (method === 'EMA_OPEN_CANCEL_DIALOG') {
          openCancelDialogCb = cb;
        }
      }),
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
    };
    betHistoryMainService = {
      getBetStatus: jasmine.createSpy('getBetStatus').and.returnValue('open')
    };
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of({
        bet: [{
          subjectToCashout: {
            newBetStake: '10'
          },
          betPotentialWin: '20',
          payout: [{
            potential: '10'
          }]
        }]
      }))
    };
    clientUserAgentService = {
      getId: jasmine.createSpy('clientUserAgentService')
    };
    deviceService = {};
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog').and.callFake((a, b, c, d, onClose, arr) => {
        onClose && onClose();
        arr && arr[0].handler();
      }),
      closePopUp: jasmine.createSpy('closePopUp')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('str')
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue( [{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}])
    };
    windowRefService = {
      nativeWindow: {
        scrollTo: jasmine.createSpy()
      },
      document: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    siteServerService = {
      getEventsByOutcomeIds: jasmine.createSpy().and.returnValue(Promise.resolve([{
        markets: [{ outcomes: [{ id: 123, prices: [{}] }] }]
      }]))
    };
    domToolsService = {
      getPageScrollTop: jasmine.createSpy('getPageScrollTop'),
      scrollPageTop: jasmine.createSpy('scrollPageTop')
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    timeSyncService = {
      ip: '192.168.3.1'
    };

    service = new EditMyAccaService(
      pubSubService,
      bppService,
      clientUserAgentService,
      deviceService,
      cmsService,
      betHistoryMainService,
      infoDialogService,
      localeService,
      windowRefService,
      siteServerService,
      domToolsService,
      awsService,
      gtm,
      timeSyncService,
      storageService
    );

    service['emaConfig'] = {} as any;

    service.bet = null;
  });

  describe('removeLeg', () => {
    let bet;

    beforeEach(() => {
      bet = {
        emaPriceError: true,
        betId:3,
        leg: [{
          removing: true,
          eventEntity: {
            typeId: '9981'
          }
        }, {
          removing: false,
          eventEntity: {
            name: 'test name',
            categoryId: '82',
            typeId: '9981',
            id: '1231231231',
            isStarted: true,
            markets: [
              {
                name: 'market name',
                outcomes: [
                  {
                    id: '847271'
                  }
                ]
              }
            ]
          },
          part: [{ eventId: '11' }]
        }, {
          removing: false,
          status: 'won'
        }, {
          removing: false,
          status: 'open'
        }]
      } as any;
    });

    it('removeLeg', () => {
      service['createLegs'] = jasmine.createSpy();
      service['makeValidateBetRequest'] = jasmine.createSpy();
      service['trackRemoveLeg'] = jasmine.createSpy('trackRemoveLeg').and.callThrough();
      service.bet = {} as any;
      service.removeLeg(bet, bet.leg[1]);
      expect(service['trackRemoveLeg']).toHaveBeenCalledWith(bet, bet.leg[1]);
      expect(bet.emaPriceError).toBeFalsy();
      expect(service['createLegs']).toHaveBeenCalledWith([bet.leg[3]]);
      expect(service['makeValidateBetRequest']).toHaveBeenCalledWith(bet, [bet.leg[1]]);
    });

    it('removeLeg (notify unsaved ema in widget)', () => {
      service['createLegs'] = jasmine.createSpy();
      service['makeValidateBetRequest'] = jasmine.createSpy();
      service['trackRemoveLeg'] = jasmine.createSpy('trackRemoveLeg').and.callThrough();
      windowRefService.document.querySelector.and.returnValue({});
      service.bet = {} as any;
      service.removeLeg(bet, bet.leg[1]);

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_UNSAVED_IN_WIDGET, true);
    });

    it('removeLeg (notify unsaved ema on EDP)', () => {
      service['createLegs'] = jasmine.createSpy();
      service['makeValidateBetRequest'] = jasmine.createSpy();
      service['trackRemoveLeg'] = jasmine.createSpy('trackRemoveLeg').and.callThrough();
      windowRefService.document.querySelector.and.callFake(selector => selector !== '.my-bets-content edit-my-acca-confirm');
      service.bet = {} as any;
      service.removeLeg(bet, bet.leg[1]);

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_UNSAVED_ON_EDP, true);
    });
  });

  describe('undoRemoveLeg', () => {
    beforeEach(() => {
      service['createLegs'] = jasmine.createSpy('createLegs');
      service['setStakeAndPayout'] = jasmine.createSpy('setStakeAndPayout');
      service['makeValidateBetRequest'] = jasmine.createSpy('makeValidateBetRequest');
      service['bet'] = {} as any;
    });

    let bet;

    beforeEach(() => {
      bet = {
        emaPriceError: true,
        betId:3,
        leg: [{
          removing: true,
          eventEntity: {
            typeId: '9981'
          }
        }, {
          removing: false,
          eventEntity: {
            name: 'test name',
            categoryId: '82',
            typeId: '9981',
            id: '1231231231',
            isStarted: true,
            markets: [
              {
                name: 'market name',
                outcomes: [
                  {
                    id: '847271'
                  }
                ]
              }
            ]
          },
          part: [{ eventId: '11' }]
        }, {
          removing: false,
          status: 'won'
        }, {
          removing: false,
          status: 'open'
        }]
      } as any;
    });
    it('set initial state', () => {
      service.initialStake = '10';
      (service['createLegs'] as any).and.returnValue([]);
      service.undoRemoveLegs({leg: [] } as any, [{} as any]);

      expect(service['createLegs']).toHaveBeenCalledTimes(1);
      expect(service['setStakeAndPayout']).toHaveBeenCalledTimes(1);
      expect(service['makeValidateBetRequest']).not.toHaveBeenCalled();
    });

    it('validate bet', () => {
      (service['createLegs'] as any).and.returnValue([{}]);
      const newleg: any = { part: [{ eventId: 11}] };
      const newbet = {
        emaPriceError: true,
        betId: 3,
        leg: [{ removing: false }, { removing: true }, newleg]
      } as any;
      service.removeLeg(bet, bet.leg[1]);
      service.undoRemoveLegs(newbet, [newleg]);

      expect(bet.emaPriceError).toBeFalsy();
      expect(service['createLegs']).toHaveBeenCalledTimes(2);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
      expect(service['makeValidateBetRequest']).toHaveBeenCalledTimes(2);
    });

    it('edit my acca should call setSignpostMethod', () => {
      (service['createLegs'] as any).and.returnValue([{}]);
      const newleg: any = { part: [{ eventId: 11}] };
      const newbet = {
        emaPriceError: true,
        betId: 3,
        leg: [{ removing: false }, { removing: true }, newleg]
      } as any;
      service.removeLeg(bet, bet.leg[1]);
      service.undoRemoveLegs(newbet, [newleg]);
      service.setSignPostData(bet, newbet.betId)

      expect(bet.emaPriceError).toBeFalsy();
      expect(service['createLegs']).toHaveBeenCalledTimes(2);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
      expect(service['makeValidateBetRequest']).toHaveBeenCalledTimes(2);
    });

    it('edit my acca should call setSignpostMethod with removedBetLegs', () => {
      (service['createLegs'] as any).and.returnValue([{}]);
      const newleg: any = { part: [{ eventId: 11}] };
      const newbet = {
        emaPriceError: true,
        betId: 3,
        leg: [{ removing: true }, { removing: true }, newleg]
      } as any;
      service.removedBetLegs = [
        {
          betId: 3,
          eventIds: [11]
        }
       ] as any;
      service.setSignPostData(bet, newbet.betId);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
    });

    it('remove leg should call storeRemovedLegs', () => {
      (service['createLegs'] as any).and.returnValue([{}]);

      const newleg: any = { part: [{ eventId: 11}] };
      const newbet = {
        emaPriceError: true,
        betId: 2,
        leg: newleg
      } as any;
      service.removedBetLegs = [
        {
          betId: 3,
          eventIds: [11]
        }
       ] as any;
      service.storeRemovedLegs(newbet.betId, newbet.leg);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
    });

    it('remove leg should call storeRemovedLegs with bet Id exists', () => {
      (service['createLegs'] as any).and.returnValue([{}]);
      const newleg: any = { part: [{ eventId: 11}] };
      const newbet = {
        emaPriceError: true,
        betId: 3,
        leg: newleg
      } as any;
      service.removedBetLegs = [
        {
          betId: 3,
          eventIds: [11]
        }
       ] as any;
      service.storeRemovedLegs(newbet.betId, newbet.leg);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
    });
  });

  describe('canRemoveLegs', () => {
    it('canRemoveLegs (pending)', () => {
      expect(service.canRemoveLegs({ validateBetStatus: 'pending' } as any)).toBeFalsy();
    });

    it('canRemoveLegs (ok)', () => {
      service.hasSuspendedLegs = () => true;
      expect(service.canRemoveLegs({ validateBetStatus: 'ok' } as any)).toBeFalsy();
    });

    it('canRemoveLegs (ok, removing)', () => {
      service.hasSuspendedLegs = () => false;
      expect(service.canRemoveLegs(
        { validateBetStatus: 'ok', leg: [{ removing: true }, { status: 'open' }, { status: 'open' }] } as any)
      ).toBeTruthy();
    });

    it('canRemoveLegs (ok, removedLeg)', () => {
      service.hasSuspendedLegs = () => false;
      expect(service.canRemoveLegs(
        { validateBetStatus: 'ok', leg: [{ removedLeg: true }, { status: 'open' }, { status: 'open' }] } as any)
      ).toBeTruthy();
    });
  });

  describe('canUndoRemoveLegs', () => {
    it('canUndoRemoveLegs (pending)', () => {
      expect(service.canUndoRemoveLegs({ validateBetStatus: 'pending' } as any)).toBeFalsy();
    });

    it('canUndoRemoveLegs (ok, has suspended legs)', () => {
      service.hasSuspendedLegs = () => true;
      expect(service.canUndoRemoveLegs({ validateBetStatus: 'ok' } as any)).toBeFalsy();
    });

    it('canUndoRemoveLegs (ok)', () => {
      service.hasSuspendedLegs = () => false;
      service.emaInProcess = false;
      expect(service.canUndoRemoveLegs({ validateBetStatus: 'ok' } as any)).toBeTruthy();
    });

    it('canUndoRemoveLegs (in progress)', () => {
      service.hasSuspendedLegs = () => false;
      service.emaInProcess = true;
      expect(service.canUndoRemoveLegs({ validateBetStatus: 'ok' } as any)).toBeFalsy();
    });
  });


  it('EMAEnabled', () => {
    service['emaConfig'].enabled = false;
    expect(service.EMAEnabled).toBe(false);

    service['emaConfig'].enabled = true;
    expect(service.EMAEnabled).toBe(true);
  });

  it('isEmaInProcess', () => {
    service['emaInProcess'] = false;
    expect(service.isEmaInProcess).toBe(false);

    service['emaInProcess'] = true;
    expect(service.isEmaInProcess).toBe(true);
  });

  it('editMyAcca', fakeAsync(() => {

    service.removedBetLegs = {
      bet: [{
        betId: 3,
        eventIds: 11
      }]
    } as any;
    service.bet = {
      betId: 3,
      leg: [{
        sportsLeg: {
          price: {
            priceTypeRef: {
              id: 'LP'
            }
          },
          legPart: [{
            outcomeRef: {
              id: '11'
            }
          }],
          winPlaceRef: {
            id: 'WIN'
          }
        },
      }],
      event:  ['11','2'],
      outcomes:{ 11: { lp_den: '10', lp_num: '20' } }
    } as any;
    storageService.get.and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
    service['waitAndMakeReadBet'] = jasmine.createSpy().and.returnValue(of({
      bet: [{ payout: [{}] }]
    }));
    service['showEditSuccessMessage'] = jasmine.createSpy();
    service['trackConfirmEditMyAcca'] = jasmine.createSpy('trackConfirmEditMyAcca').and.callThrough();

    
    service.editMyAcca(service.bet as any).subscribe();
    expect(awsService.addAction).toHaveBeenCalledWith('EditMyAccaService=>placeBet=>Start', jasmine.any(Object));

    tick();

    expect(service['trackConfirmEditMyAcca']).toHaveBeenCalledWith(service.bet as any, true);  
    expect(bppService.send).toHaveBeenCalledTimes(1);
    expect(service['showEditSuccessMessage']).toHaveBeenCalledTimes(1);
    expect(service['waitAndMakeReadBet']).toHaveBeenCalledTimes(1);
    expect(awsService.addAction).toHaveBeenCalledWith('EditMyAccaService=>placeBet=>Success', jasmine.any(Object));
  }));

  it('editMyAcca (error)', fakeAsync(() => {
    service.bet = {
      leg: []
    } as any;
    service['placeBetErrorHandler'] = jasmine.createSpy();
    service['showEditSuccessMessage'] = jasmine.createSpy();
    service['waitAndMakeReadBet'] = jasmine.createSpy();

    (service['waitAndMakeReadBet'] as any).and.returnValue(of({ betError: [{}] }));
    service['trackConfirmEditMyAcca'] = jasmine.createSpy('trackConfirmEditMyAcca').and.callThrough();

    service.editMyAcca({ leg: [] } as any).subscribe();
    tick();

    (service['waitAndMakeReadBet'] as any).and.returnValue(throwError({}));
    service.editMyAcca({ leg: [] } as any).subscribe(null, () => {
    });
    tick();

    expect(service['trackConfirmEditMyAcca']).toHaveBeenCalledWith({ leg: [], emaPriceError: false } as any, false);
    expect(service['trackConfirmEditMyAcca']).toHaveBeenCalledTimes(2);
    expect(bppService.send).toHaveBeenCalledTimes(2);
    expect(service['placeBetErrorHandler']).toHaveBeenCalledTimes(2);
    expect(service['waitAndMakeReadBet']).toHaveBeenCalledTimes(2);
    expect(awsService.addAction).toHaveBeenCalledWith('EditMyAccaService=>placeBet=>Error', jasmine.any(Object));
  }));

  describe('isBetOpen', () => {
    it('should check if isBetOpen (status open)', () => {
      expect(service.isBetOpen(<any>{})).toEqual(true);
    });

    it('should check if isBetOpen (status suspended)', () => {
      betHistoryMainService.getBetStatus.and.returnValue('suspended');
      expect(service.isBetOpen(<any>{})).toEqual(false);
    });
  });

  describe('hasSuspendedLegs', () => {
    it('should check if bet hasSuspendedLegs (open)', () => {
      const bet: any = { leg: [{ status: 'open' }] };
      expect(service.hasSuspendedLegs(bet)).toEqual(false);
    });

    it('should check if bet hasSuspendedLegs (suspened)', () => {
      const bet: any = { leg: [{ status: 'suspended' }] };
      expect(service.hasSuspendedLegs(bet)).toEqual(true);
    });

    it('should check if bet hasSuspendedLegs (suspended and removed)', () => {
      const bet: any = { leg: [{ status: 'suspended', removedLeg: true }] };
      expect(service.hasSuspendedLegs(bet)).toEqual(false);
    });
  });

  describe('hasOpenLegs', () => {
    it('should check if bet hasOpenLegs (suspended legs)', () => {
      const bet = { leg: [{ status: 'suspended' }] };
      expect(service['hasOpenLegs'](<any>bet)).toEqual(false);
    });

    it('should check if bet hasOpenLegs (open legs)', () => {
      const bet = { leg: [{ status: 'open', part: [{ priceNum: '10' }] }, { status: 'open', part: [{ priceNum: '5' }] }] };
      expect(service['hasOpenLegs'](<any>bet)).toEqual(true);
    });

    it('should check if bet hasOpenLegs (no sp selections)', () => {
      const bet = { leg: [{ status: 'open', part: [{ priceNum: null }] }, { status: 'open', part: [{ priceNum: null }] }] };
      expect(service['hasOpenLegs'](<any>bet)).toEqual(false);
    });

    it('should check if bet hasOpenLegs (no sp selections)', () => {
      const bet = { leg: [{ status: 'open', part: [{ priceNum: '10' }] }, { status: 'open', part: [{ priceNum: '10' }] }] };
      expect(service['hasOpenLegs'](<any>bet)).toEqual(true);
    });
  });

  describe('canEditBet', () => {
    it('should check if canEditBet (acca, EMA Enabled)', () => {
      service['emaConfig'].enabled = true;
      const bet: any = {
        leg: [{ status: 'open', part: [{ priceNum: '10' }] }, { status: 'open', part: [{ priceNum: '5' }] }],
        numLines: '1',
        numLegs: '4'
      };
      expect(service.canEditBet(bet)).toEqual(true);
    });

    it('should check if canEditBet (EMA not Enabled)', () => {
      const bet: any = {
        leg: [{ status: 'open', part: [{ priceNum: '10' }] }, { status: 'open', part: [{ priceNum: '5' }] }],
        numLines: '1',
        numLegs: '4'
      };
      expect(service.canEditBet(bet)).toEqual(false);
    });

    it('should check if canEditBet (not acca)', () => {
      service['emaConfig'].enabled = true;
      const bet: any = {
        leg: [{ status: 'open', part: [{}] }, { status: 'open', part: [{}] }],
        numLines: '1',
        numLegs: '1'
      };
      expect(service.canEditBet(bet)).toEqual(false);
    });

    it('should check if canEditBet (has suspended legs)', () => {
      service['emaConfig'].enabled = true;
      const bet: any = {
        leg: [{ status: 'open', part: [{ priceNum: '10' }] }, { status: 'suspended', part: [{ priceNum: '10' }] }],
        numLines: '1',
        numLegs: '4'
      };
      expect(service.canEditBet(bet)).toEqual(true);
    });
  });

  describe('isLegResulted', () => {
    it('should check if isLegResulted (open)', () => {
      const leg = { status: 'open' } as IBetHistoryLeg;
      expect(service.isLegResulted(leg)).toEqual(false);
    });

    it('should check if isLegResulted (won)', () => {
      const leg = { status: 'won' } as IBetHistoryLeg;
      expect(service.isLegResulted(leg)).toEqual(true);
    });
  });

  describe('hasLegsWithLostStatus', () => {
    it('should check if hasLegsWithLostStatus (no lost legs)', () => {
      const bet = { leg: [{ status: 'open' }] } as IBetHistoryBet;
      expect(service.hasLegsWithLostStatus(bet)).toEqual(false);
    });

    it('should check if hasLegsWithLostStatus (lost legs)', () => {
      const bet = { leg: [{ status: 'open' }, { status: 'lost' }] } as IBetHistoryBet;
      expect(service.hasLegsWithLostStatus(bet)).toEqual(true);
    });

    it('should check if hasLegsWithLostStatus (removed lost legs)', () => {
      const bet = { leg: [{ status: 'open' }, { status: 'lost', removedLeg: true }] } as IBetHistoryBet;
      expect(service.hasLegsWithLostStatus(bet)).toEqual(false);
    });
  });

  it('showEditCancelMessage', () => {
    service['toggleBetEdit'] = jasmine.createSpy();

    service.showEditCancelMessage();

    expect(infoDialogService.openInfoDialog).toHaveBeenCalledWith(
      'str', 'str', undefined, undefined, jasmine.any(Function), [{
        caption: 'Cancel edit',
        cssClass: 'btn-style4',
        handler: jasmine.any(Function)
      }, {
        caption: 'Continue editing'
      }]
    );
    expect(service['toggleBetEdit']).toHaveBeenCalled();
    expect(infoDialogService.closePopUp).toHaveBeenCalled();
    expect(domToolsService.getPageScrollTop).toHaveBeenCalledTimes(1);
    expect(domToolsService.scrollPageTop).toHaveBeenCalledTimes(1);
  });

  it('showEditCancelMessage (EMA_OPEN_CANCEL_DIALOG)', () => {
    service.unsavedAcca = <any>{
      isAccaEdit: true, leg: []
    };
    spyOn<any>(service, 'showEditCancelMessage');
    openCancelDialogCb();
    expect(domToolsService.getPageScrollTop).toHaveBeenCalledTimes(1);
  });

  it('showEditSuccessMessage', () => {
    service['toggleBetEdit'] = jasmine.createSpy();
    infoDialogService.openInfoDialog = jasmine.createSpy('openInfoDialog')
      .and
      .callFake((a, b, c, d, callback, arr) => {
        callback && callback();
      });
    service['showEditSuccessMessage']({} as any, 1, '');

    expect(service.emaInProcess).toBeFalsy();
    expect(service['toggleBetEdit']).toHaveBeenCalled();
    expect(pubSubService.publishSync).toHaveBeenCalledWith('EDIT_MY_ACCA');
    expect(service.savedAccas[1]).toBe('success');
    expect(windowRefService.nativeWindow.scrollTo).toHaveBeenCalled();
    expect(service.isAccaEdit).toBeTruthy();
  });

  it('#clearAccas', () => {
    service.isAccaEdit = true;
    service.clearAccas();
    expect(service.isAccaEdit).toBeFalsy();

    service.isAccaEdit = false;
    service.savedAccas = {'1' : 'success'};
    service.clearAccas();
    expect(service.savedAccas).toEqual({});
    expect(service.unsavedAcca).toBeUndefined();
  });

  describe('toggleBetEdit', () => {
    beforeEach(() => {
      service['setStakeAndPayout'] = jasmine.createSpy();
      service['createValidateRequest'] = jasmine.createSpy();
      service['trackStartEditMyAcca'] = jasmine.createSpy('trackStartEditMyAcca');
    });
    it('case: (true true)', () => {
      const bet = { isAccaEdit: true, stake: '10', leg: [] } as any;
      service['initialStake'] = '10';

      service.toggleBetEdit(bet);
      expect(service['trackStartEditMyAcca']).not.toHaveBeenCalled();
      expect(bet.isAccaEdit).toEqual(false);
      expect(service['setStakeAndPayout']).toHaveBeenCalledWith(bet as any, '10', undefined);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_UNSAVED_IN_WIDGET, false);
    });

    it('case: (false false)', () => {
      const bet = {
        isAccaEdit: false,
        leg: []
      } as any;
      service.initialStake = null;
      service.toggleBetEdit(<any>bet, 'cashout');
      expect(service['trackStartEditMyAcca']).toHaveBeenCalledWith(bet as any, 'cashout');
      expect(bet.isAccaEdit).toEqual(true);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
    });

    it('case: (false true)', () => {
      const bet = {
        isAccaEdit: false,
        leg: []
      } as any;
      service['initialStake'] = '10';
      service.toggleBetEdit(<any>bet);
      expect(bet.isAccaEdit).toEqual(true);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
    });

    it('case: (true false)', () => {
      service['setPrices'] = jasmine.createSpy();
      const bet = { isAccaEdit: true, leg: [{ part: [{ price: [{ num: 1, den: 2 }] }] }, { part: [{ price: [null] }] }] };
      service.initialStake = null;
      service.toggleBetEdit(<any>bet);
      expect(bet.isAccaEdit).toEqual(false);
      expect(service['setPrices']).toHaveBeenCalled();
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
    });

    it('case: (this.bet null)', () => {
      const bet: IBetHistoryBet = {
        leg: []
      } as any;
      service.bet = null;
      service['createValidateRequest'] = jasmine.createSpy();
      service.toggleBetEdit(bet);
      expect(service['createValidateRequest']).toHaveBeenCalled();
    });

    it('case: (this.bet {})', () => {
      const bet: IBetHistoryBet = {
        leg: []
      } as any;
      service.bet = {} as any;
      service['createValidateRequest'] = jasmine.createSpy();
      service.toggleBetEdit(bet);
      expect(service['createValidateRequest']).toHaveBeenCalled();
    });
  });

  it('cancelActiveEdit', () => {
    service['toggleBetEdit'] = jasmine.createSpy();

    service['activeBet'] = {} as any;
    service.cancelActiveEdit({} as any);

    service['activeBet'] = null;
    service.cancelActiveEdit({} as any);

    expect(service.toggleBetEdit).toHaveBeenCalledTimes(1);
  });

  describe('isAccaBet', () => {
    it('should check if isAccaBet (not acca)', () => {
      const bet: any = { numLines: '1', numLegs: '1' };
      expect(service.isAccaBet(bet)).toEqual(false);
    });

    it('should check if isAccaBet (acca)', () => {
      const bet: any = { numLines: '1', numLegs: '4' };
      expect(service.isAccaBet(bet)).toEqual(true);
    });
  });

  describe('makeValidateBetRequest', () => {
    it('makeValidateBetRequest(success)', fakeAsync(() => {
      service['setLegRefs'] = jasmine.createSpy();
      service['setBetType'] = jasmine.createSpy();
      service['validateBetSuccessHandler'] = jasmine.createSpy();
      service['validateBetErrorHandler'] = jasmine.createSpy();
      service['bet'] = { leg: [] } as any;

      service['makeValidateBetRequest']({} as any, {} as any);

      bppService.send.and.returnValue(of({ betError: [] }));
      service['makeValidateBetRequest']({} as any, {} as any);

      tick();

      expect(service['setLegRefs']).toHaveBeenCalledTimes(2);
      expect(service['setBetType']).toHaveBeenCalledTimes(2);
      expect(service['validateBetSuccessHandler']).toHaveBeenCalledTimes(1);
      expect(service['validateBetErrorHandler']).toHaveBeenCalledTimes(1);

      expect(awsService.addAction).toHaveBeenCalledWith('EditMyAccaService=>validateBet=>Start', jasmine.any(Object));
      expect(awsService.addAction).toHaveBeenCalledWith('EditMyAccaService=>validateBet=>Success', jasmine.any(Object));
    }));

    it('makeValidateBetRequest(success) with considerPriceError - true', fakeAsync(() => {
      service['setLegRefs'] = jasmine.createSpy();
      service['setBetType'] = jasmine.createSpy();
      service['bet'] = { id: 348, emaPriceError: false, leg: [ { id: 1, legNo: '1'} ] } as any;

      bppService.send.and.returnValue(of({} ) );
      service['makeValidateBetRequest'](service['bet'] as any, service['bet'].leg as any, true, true);

      // @ts-ignore
      expect(service['bet'].emaPriceError).toBeTruthy();
    }));

    it('makeValidateBetRequest(success) with considerPriceError - undefined', fakeAsync(() => {
      service['setLegRefs'] = jasmine.createSpy();
      service['setBetType'] = jasmine.createSpy();
      service['bet'] = { id: 348, emaPriceError: false, leg: [ { id: 1, legNo: '1'} ] } as any;

      bppService.send.and.returnValue(of({} ) );
      service['makeValidateBetRequest'](service['bet'] as any, service['bet'].leg as any, true, undefined);

      // @ts-ignore
      expect(service['bet'].emaPriceError).toBeUndefined();
    }));

    it('makeValidateBetRequest(error)', fakeAsync(() => {
      service['validateBetErrorHandler'] = jasmine.createSpy();
      service['bet'] = { leg: [], bet: [{ legRef: {}, betTypeRef: { id: 1 } }] } as any;

      bppService.send.and.returnValue(throwError(new HttpErrorResponse({})));
      service['makeValidateBetRequest']({} as any, {} as any);

      tick();
      expect(service['validateBetErrorHandler']).toHaveBeenCalledTimes(1);
      expect(awsService.addAction).toHaveBeenCalledWith('EditMyAccaService=>validateBet=>Error', jasmine.any(Object));
    }));
  });

  it('setStakeAndPayout', () => {
    const bet = {} as any;
    service['bet'] = { bet: [{}] } as any;
    service['setStakeAndPayout'](bet, '10', '20');

    expect(bet.stake).toEqual('10');
    expect(bet.potentialPayout).toEqual('20');
  });

  it('setStakeAndPayout (no payout)', () => {
    const bet = { potentialPayout: '30' } as any;
    service['bet'] = { bet: [{}] } as any;
    service['setStakeAndPayout'](bet, '10');

    expect(bet.potentialPayout).toEqual('30');
  });

  it('createValidateRequest', () => {
    const result = service['createValidateRequest']({
      stake: '1', type: 'LP', currency: '$', leg: {}
    } as any);
    expect(clientUserAgentService.getId).toHaveBeenCalled();
    expect(result).toEqual({
      betslip: jasmine.any(Object),
      bet: jasmine.any(Array),
      leg: jasmine.any(Object)
    } as any);
  });

  it('setLegRefs', () => {
    service.bet = {
      bet: [{
        legRef: null
      }],
      leg: [{
        documentId: '2'
      }, {
        documentId: '3'
      }]
    } as any;

    service['setLegRefs']();
    expect(service.bet.bet[0].legRef).toEqual([{ documentId: '2' }, { documentId: '3' }]);
  });

  it('setBetType', () => {
    service.bet = {
      bet: [{
        betTypeRef: {}
      }]
    } as any;

    service['setBetType'](1);
    expect(service.bet.bet[0].betTypeRef.id).toEqual('SGL');
    service['setBetType'](2);
    expect(service.bet.bet[0].betTypeRef.id).toEqual('DBL');
    service['setBetType'](3);
    expect(service.bet.bet[0].betTypeRef.id).toEqual('TBL');
    service['setBetType'](5);
    expect(service.bet.bet[0].betTypeRef.id).toEqual('ACC5');
    service['setBetType'](15);
    expect(service.bet.bet[0].betTypeRef.id).toEqual('AC15');
  });

  it('createLegs lp', () => {
    const res = service['createLegs']([{
      legNo: '1',
      part: [{
        priceNum: '10',
        priceDen: '20',
        priceType: 'L',
        outcome: '12345'
      }],
      legSort: {}
    }] as any[]);

    expect(res).toEqual([{
      documentId: '1',
      sportsLeg: {
        price: {
          priceTypeRef: {
            id: 'LP'
          }
        },
        legPart: [{
          outcomeRef: {
            id: '12345'
          }
        }],
        winPlaceRef: {
          id: 'WIN'
        }
      }
    }] as any);
  });

  it('createLegs sp', () => {
    const res = service['createLegs']([{
      legNo: '1',
      part: [{
        priceType: 'S',
        outcome: '12345'
      }],
      legSort: {}
    }] as any[]) as any[];

    expect(res[0].sportsLeg.price.priceTypeRef.id).toEqual('SP' as any);
  });

  it('createLegs', () => {
    const legs: any[] = [{
      legNo: '1',
      part: [
        { priceNum: 3, priceDen: 4, priceType: 'L', outcome: '11' }
      ],
      legSort: {}
    }, {
      legNo: '2',
      part: [
        { priceNum: null, priceDen: null, priceType: 'S', outcome: [{ id: '22' }] }
      ],
      legSort: {}
    }];

    const result: any[] = service['createLegs'](legs);

    expect(result).toEqual([{
      documentId: '1',
      sportsLeg: {
        price: { priceTypeRef: { id: 'LP' } },
        legPart: [{
          outcomeRef: { id: '11' }
        }],
        winPlaceRef: { id: 'WIN' }
      }
    }, {
      documentId: '2',
      sportsLeg: {
        price: { priceTypeRef: { id: 'SP' } },
        legPart: [{
          outcomeRef: { id: '22' }
        }],
        winPlaceRef: { id: 'WIN' }
      }
    }]);
  });

  it('createLegPart', () => {
    expect(service['createLegPart']('123' as any, '5', '--')).toEqual({
      outcomeRef: {
        id: '123'
      }
    });
  });

  it('createLegPart handicap', () => {
    expect(service['createLegPart']([{ id: '123' }] as any, '5', 'MH')).toEqual({
      outcomeRef: {
        id: '123'
      },
      range: {
        high: '5',
        low: '5',
        rangeTypeRef: {
          id: 'MATCH_HANDICAP'
        }
      }
    } as any);
  });

  it('validateBetSuccessHandler', () => {
    const legs = [{ removing: true }] as any;
    service['setStakeAndPayout'] = jasmine.createSpy();
    service['bet'] = { bet: [{}] } as any;

    service['validateBetSuccessHandler']({} as any, {} as any, {} as any);
    service['validateBetSuccessHandler']({
      bet: [{ subjectToCashout: {} }]
    } as any, {
      isAccaEdit: true
    } as any, legs as any);

    expect(service['setStakeAndPayout']).toHaveBeenCalledTimes(1);
    expect(legs[0].removing).toEqual(false);
  });

  it('validateBetSuccessHandler (false => true )', () => {
    const legs = [{ removing: true }] as any;
    service['setStakeAndPayout'] = jasmine.createSpy();
    service['bet'] = { bet: [{}] } as any;
    service['validateBetSuccessHandler']({
      bet: [{ subjectToCashout: {} }]
    } as any, {
      isAccaEdit: true
    } as any, legs, true);

    expect(legs[0].removing).toEqual(true);
  });

  it('validateBetErrorHandler', () => {
    let bet = {id: 1} as any;
    service['validateBetErrorHandler']([] as any, bet as any);
    expect(bet.validateBetStatus).toEqual(undefined);

    bet = { ...bet, isAccaEdit: true };
    service['validateBetErrorHandler']([] as any, bet as any);
    expect(bet.validateBetStatus).toEqual('fail');

    bet = { ...bet, isAccaEdit: true };
    service['validateBetErrorHandler']([{}] as any, bet as any);
    expect(bet.validateBetStatus).toEqual('fail');

    bet = { ...bet, isAccaEdit: true };
    service['validateBetErrorHandler']([{ subErrorCode: 'PRICE_CHANGED' }] as any, bet as any);
    expect(bet.validateBetStatus).toEqual('ok');
    expect(service.savedAccas[1]).toBe('error');
    expect(service.emaInProcess).toBeFalsy();

    bet = { betId: '5', isAccaEdit: true };
    service['validateBetErrorHandler']([{ subErrorCode: 'PRICE_CHANGED' }] as any, bet as any);
    expect(bet.validateBetStatus).toEqual('ok');
    expect(service.savedAccas['5']).toBe('error');
    expect(service.emaInProcess).toBeFalsy();
  });

  it('placeBetErrorHandler (no error)', () => {
    service['placeBetErrorHandler']([{}] as any, {betId: 1} as any);

   expect(service.savedAccas[1]).toBe('error');
   expect(service.emaInProcess).toBeFalsy();
  });

  it('placeBetErrorHandler (error not pricechange)', () => {
    service['isPriceError'] = jasmine.createSpy().and.returnValue(false);
    service['placeBetErrorHandler']([] as any, {betId: 1} as any);
    expect(service.savedAccas[1]).toBe('error');
    expect(service.emaInProcess).toBeFalsy();
  });

  it('placeBetErrorHandler (error pricechange)', fakeAsync(() => {
    const bet = { emaPriceError: false, outcomes: {}, leg: [ { id: 1 }] } as any;
    service['getBetWithPrices'] = jasmine.createSpy();
    service['makeValidateBetRequest'] = jasmine.createSpy();
    service['placeBetErrorHandler']([{ subErrorCode: 'PRICE_CHANGED', price: [] }] as any, bet);
    tick();

    expect(siteServerService.getEventsByOutcomeIds).toHaveBeenCalled();
    expect(service['getBetWithPrices']).toHaveBeenCalled();
    expect(service['makeValidateBetRequest']).toHaveBeenCalledWith(bet, bet.leg, true, true);
  }));

  it('placeBetErrorHandler (error pricechange with outcomeMap)', fakeAsync(() => {
    service['getBetWithPrices'] = jasmine.createSpy();
    service['makeValidateBetRequest'] = jasmine.createSpy();
    service['setPrices'] = jasmine.createSpy();
    service['placeBetErrorHandler']([{
      subErrorCode: 'PRICE_CHANGED',
      outcomeRef: { id: '345' },
      price: [{ priceNum: '10', priceDen: '1' }]
    }] as any, { outcomes: { 123: {} } } as any);
    tick();
    expect(service['setPrices']).toHaveBeenCalled();
  }));

  describe('isPriceError', () => {
    it('no error (no code)', () => {
      expect(service['isPriceError'](null)).toBeFalsy();
    });

    it('no error (no code)', () => {
      expect(service['isPriceError']({})).toBeFalsy();
    });

    it('no error (PRICE_CHANGED)', () => {
      expect(service['isPriceError']([{ subErrorCode: 'PRICE_CHANGED' }])).toBeTruthy();
    });

    it('no error (CASHOUT_VALUE_CHANGE)', () => {
      expect(service['isPriceError']([{ subErrorCode: 'CASHOUT_VALUE_CHANGE' }])).toBeTruthy();
    });

    it('no error (CASHOUT_VALUE_CHANGE)', () => {
      expect(service['isPriceError']({ failureDescription: 'CASHOUT_VALUE_CHANGE' })).toBeTruthy();
    });
  });

  it('getBetWithPrices', () => {
    service.bet = {
      leg: [{
        sportsLeg: {
          price: {},
          legPart: [{
            outcomeRef: {
              id: '123'
            }
          }]
        }
      }]
    } as any;

    service.getBetWithPrices({ outcomes: { 123: { lp_den: '10', lp_num: '20' } } } as any);
    expect(service.bet.leg[0].sportsLeg.price).toEqual({ num: '20', den: '10' } as any);
  });

  describe('waitAndMakeReadBet', () => {
    it('no bet', () => {
      service['waitAndMakeReadBet']({
        bet: null
      } as any);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('bet confirmed', () => {
      service['waitAndMakeReadBet']({
        bet: [{ isConfirmed: 'Y' }]
      } as any);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('bet is not confirmed', fakeAsync(() => {
      service['waitAndMakeReadBet']({
        bet: [{ isConfirmed: 'N', confirmationExpectedAt: '-1' }]
      } as any).subscribe(() => {
        expect(pubSubService.publish).toHaveBeenCalledTimes(1);
        expect(bppService.send).toHaveBeenCalledTimes(1);
      });
      tick();
    }));
  });

  describe('betLiveUpdateHandler', () => {
    it('emaInProcess', () => {
      service['getRemovedResultedLegs'] = jasmine.createSpy();
      service['emaInProcess'] = true;
      service['activeBet'] = { leg: [] } as any;

      service['betLiveUpdateHandler']({} as any);
      expect(service['getRemovedResultedLegs']).not.toHaveBeenCalled();
    });

    it('no active bet', () => {
      service['setStakeAndPayout'] = jasmine.createSpy();
      service['activeBet'] = null;

      service['betLiveUpdateHandler']({ id: '123', updatePayload: { num: 1, den: 2 } } as any);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
    });

    it('no initial stake', () => {
      service['setStakeAndPayout'] = jasmine.createSpy();
      service['activeBet'] = { leg: [] } as any;
      service['initialStake'] = null;
      service['hasSuspendedLegs'] = () => true;

      service['betLiveUpdateHandler']({ id: '123', updatePayload: { num: 1, den: 2 } } as any);
      expect(service['setStakeAndPayout']).not.toHaveBeenCalled();
    });

    it('priceUpdateIndex >=0', () => {
      service['setStakeAndPayout'] = jasmine.createSpy();
      service['updatePrices'] = jasmine.createSpy();
      service['initialStake'] = '1.00';
      service['activeBet'] = {
        leg: [{ removing: true }, {}],
        outcome: ['123', '234']
      } as any;
      service['hasSuspendedLegs'] = () => false;
      service['betLiveUpdateHandler']({ id: '234', updatePayload: { num: 1, den: 2 } } as any);

      expect(service['updatePrices']).toHaveBeenCalledWith(1, { num: 1, den: 2 });
    });

    it('priceUpdateIndex >=0 and removing false', () => {
      service['setStakeAndPayout'] = jasmine.createSpy();
      service['updatePrices'] = jasmine.createSpy();
      service['initialStake'] = '1.00';
      service['activeBet'] = {
        leg: [{ removing: false }, {}],
        outcome: ['123', '234']
      } as any;
      service['hasSuspendedLegs'] = () => false;
      service['betLiveUpdateHandler']({ id: '234', updatePayload: { num: 1, den: 2 } } as any);

      expect(service['updatePrices']).not.toHaveBeenCalled();
    });

    it('undo remove resulted legs', () => {
      service['undoRemoveLegs'] = jasmine.createSpy('undoRemoveLegs');
      service['activeBet'] = { leg: [{ removing: true }, {}] } as any;
      service['hasSuspendedLegs'] = () => false;
      service['getRemovedResultedLegs'] = () => [{}, {}] as any;
      service['betLiveUpdateHandler']({ id: '123', updatePayload: { num: 1, den: 2 } } as any);
      expect(service['undoRemoveLegs']).toHaveBeenCalledTimes(1);
    });

    it('undo remove resulted legs and removing false', () => {
      service['undoRemoveLegs'] = jasmine.createSpy('undoRemoveLegs');
      service['activeBet'] = { leg: [{ removing: false }, {}] } as any;
      service['hasSuspendedLegs'] = () => false;
      service['getRemovedResultedLegs'] = () => [{}, {}] as any;
      service['betLiveUpdateHandler']({ id: '123', updatePayload: { num: 1, den: 2 } } as any);
      expect(service['undoRemoveLegs']).not.toHaveBeenCalled();
    });

    it('no suspended or resulted legs', () => {
      service['undoRemoveLegs'] = jasmine.createSpy('undoRemoveLegs');
      service['activeBet'] = { leg: [{ removing: true }, {}] } as any;
      service['hasSuspendedLegs'] = () => false;
      service['betLiveUpdateHandler']({ id: '123', updatePayload: { num: 1, den: 2 } } as any);
      expect(service['undoRemoveLegs']).not.toHaveBeenCalledTimes(1);
    });
  });

  it('getRemovedResultedLegs', () => {
    const bet = {
      leg: [{
        status: 'won',
        removing: true
      }, {
        status: 'void',
        removing: true
      }, {
        status: 'void'
      }, {
        status: 'won'
      }]
    } as any;
    expect(service['getRemovedResultedLegs'](bet).length).toEqual(2);
  });

  it('updatePrices', () => {
    service.bet = { leg: [] } as any;
    service['setPrices'] = jasmine.createSpy();
    service['createLegs'] = jasmine.createSpy();
    service['makeValidateBetRequest'] = jasmine.createSpy();

    service['activeBet'] = {
      leg: [{
        removing: true,
        part: [{}]
      }, {
        part: [{}],
        status: 'lost'
      }, {
        part: [{}]
      }]
    } as any;

    service['updatePrices'](0, { lp_num: '10', lp_den: '5' } as any);

    expect(service['setPrices']).toHaveBeenCalledWith(0, '10', '5');
    expect(service['createLegs']).toHaveBeenCalledWith([{
      part: [{}]
    }] as any);
    expect(service['makeValidateBetRequest']).toHaveBeenCalledWith(jasmine.any(Object), jasmine.any(Object), true);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.UPDATE_EMA_ODDS);
  });

  it('setPrices', () => {
    service['activeBet'] = {
      leg: [{ part: [{}] }]
    } as any;

    service['setPrices'](0, '10', '5');
    expect(service['activeBet'].leg[0].part[0]).toEqual({ priceNum: 10, priceDen: 5 } as any);
  });

  it('#canChangeRoute returns true#1', () => {
    const result = service.canChangeRoute();

    expect(result).toBeTruthy();
  });

  it('#canChangeRoute returns true#2', () => {
    service.unsavedAcca = {
      isAccaEdit: false,
      leg: []
    } as any;

    const result = service.canChangeRoute();

    expect(result).toBeTruthy();
  });

  it('#canChangeRoute returns true#3', () => {
    service.unsavedAcca = {
      isAccaEdit: false,
      leg: [
        { removing: false }
      ]
    } as any;

    const result = service.canChangeRoute();

    expect(result).toBeTruthy();
  });

  it('#canChangeRoute returns false', () => {
    service.unsavedAcca = {
      isAccaEdit: true,
      leg: [
        { removing: true }
      ]
    } as any;

    const result = service.canChangeRoute();

    expect(result).toBeFalsy();
  });

  it('#trackStartEditMyAcca should push start edit event to gtm', () => {
    service['gtmLocation'] = undefined;
    spyOn<any>(service, 'getGtmInfo').and.callThrough();
    const bet: IBetHistoryBet = {
      betType: 'bet-type',
      leg: [
        {
          eventEntity: {
            typeId: 311
          }
        }
      ]
    } as any;
    const gtmData = {
      eventCategory: 'edit acca',
      eventAction: 'start',
      eventLabel: 'success',
      betType: 'bet-type',
      betInPlay: 'No',
      customerBuilt: 0,
      location: 'cashout'
    };

    service['trackStartEditMyAcca'](bet, 'cashout');
    expect(service['gtmLocation']).toEqual('cashout');
    expect(service['getGtmInfo']).toHaveBeenCalledWith(bet);
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', gtmData);
  });

  describe('#trackRemoveLeg', () => {
    it('should push gtm event on remove leg', () => {
      spyOn<any>(service, 'getGtmInfo').and.callThrough();
      const leg: IBetHistoryLeg = {
        eventEntity: {
          name: 'test name',
          categoryId: '82',
          typeId: '9981',
          id: '1231231231',
          isStarted: true,
          markets: [
            {
              name: 'market name',
              outcomes: [
                {
                  id: '847271'
                }
              ]
            }
          ]
        }
      } as any;
      const bet: IBetHistoryBet = {
        betType: 'bet-type',
        leg: [
          leg
        ]
      } as any;
      const gtmData = {
        eventAction: 'remove',
        eventLabel: 'success',
        eventName: 'test name',
        categoryID: '82',
        typeID: '9981',
        eventMarket: 'market name',
        selectionID: '847271',
        eventID: '1231231231',
        eventCategory: 'edit acca',
        betType: 'bet-type',
        location: 'unknown',
        betInPlay: 'Yes',
        customerBuilt: 0
      };

      service['trackRemoveLeg'](bet, leg);
      expect(service['getGtmInfo']).toHaveBeenCalledWith(bet);
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });

    it('should push gtm event on remove leg (originalName, eventIsLive)', () => {
      spyOn<any>(service, 'getGtmInfo').and.callThrough();
      const leg: IBetHistoryLeg = {
        eventEntity: {
          name: 'test name',
          originalName: 'original name',
          categoryId: '82',
          typeId: '9981',
          id: '1231231231',
          isStarted: false,
          eventIsLive: true,
          markets: [
            {
              name: 'market name',
              outcomes: [
                {
                  id: '847271'
                }
              ]
            }
          ]
        }
      } as any;
      const bet: IBetHistoryBet = {
        betType: 'bet-type',
        leg: [
          leg
        ]
      } as any;
      const gtmData = {
        eventAction: 'remove',
        eventLabel: 'success',
        eventName: 'original name',
        categoryID: '82',
        typeID: '9981',
        eventMarket: 'market name',
        selectionID: '847271',
        eventID: '1231231231',
        eventCategory: 'edit acca',
        betType: 'bet-type',
        location: 'unknown',
        betInPlay: 'Yes',
        customerBuilt: 0
      };

      service['trackRemoveLeg'](bet, leg);
      expect(service['getGtmInfo']).toHaveBeenCalledWith(bet);
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });
  });

  it('#trackConfirmEditMyAcca should track confirm success event', () => {
    spyOn<any>(service, 'getGtmInfo').and.callThrough();
    const bet: IBetHistoryBet = {
      betType: 'bet-type',
      leg: [
        {
          eventEntity: {
            typeId: '9981',
            isStarted: true,
          },
          removing: true
        },
        {
          removing: false,
          eventEntity: {
            typeId: '99841',
            isStarted: true,
          },
        }, {
          eventEntity: {
            typeId: '99821',
            isStarted: true,
          },
          removing: false,
          removedLeg: true
        }
      ]
    } as any;
    const gtmData = {
      eventCategory: 'edit acca',
      eventAction: 'confirm',
      eventLabel: 'success',
      betType: 'bet-type',
      betInPlay: 'Yes',
      customerBuilt: 0,
      location: 'unknown',
      emaStartLegs: 2,
      emaEndLegs: 1
    };

    service['trackConfirmEditMyAcca'](bet, true);
    expect(service['getGtmInfo']).toHaveBeenCalledWith(bet);
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', gtmData);
  });

  describe('#getBetLiveStatus', () => {
    it('should check bet leg live status and return Yes', () => {
      const bet: IBetHistoryBet = {
        leg: [
          { eventEntity: { isStarted: true, eventIsLive: false } },
          { eventEntity: { isStarted: false, eventIsLive: true } }
        ]
      } as any;
      expect(service['getBetLiveStatus'](bet)).toBe('Yes');
    });

    it('should check bet leg live status and return No', () => {
      const bet: IBetHistoryBet = {
        leg: [
          { eventEntity: { isStarted: false, eventIsLive: false } },
          { eventEntity: { isStarted: false, eventIsLive: false } }
        ]
      } as any;
      expect(service['getBetLiveStatus'](bet)).toBe('No');
    });

    it('should check bet leg live status and return Both; ignore leg without event', () => {
      const bet: IBetHistoryBet = {
        leg: [
          {},
          { eventEntity: { isStarted: true, eventIsLive: false } },
          { eventEntity: { isStarted: false, eventIsLive: false } }
        ]
      } as any;
      expect(service['getBetLiveStatus'](bet)).toBe('Both');
    });
  });

  describe('#isBuildYourBet', () => {
    it('should check type id and set isBuildYourBet and return 0 (case: no leg)', () => {
      const bet: IBetHistoryBet = {} as any;
      expect(service['isBuildYourBet'](bet)).toBe(0);
    });

    it('should check type id and set isBuildYourBet and return 0 (case: no leg with event)', () => {
      const bet: IBetHistoryBet = {
        leg: [{}]
      } as any;
      expect(service['isBuildYourBet'](bet)).toBe(0);
    });

    it('should check type id and set isBuildYourBet and return 0 (case: no env.BYB_CONFIG)', () => {
      const bet: IBetHistoryBet = {
        leg: [{}, {
          eventEntity: {
            typeId: 1
          }
        }]
      } as any;
      expect(service['isBuildYourBet'](bet)).toBe(0);
    });

    it('should check type id and set isBuildYourBet and return 1 (case: different type ID)', () => {
      Object.defineProperty(service, 'env', {
        value: {
          BYB_CONFIG: { HR_YC_EVENT_TYPE_ID: 3 }
        }
      });
      const bet: IBetHistoryBet = {
        leg: [{
          eventEntity: {
            typeId: 1
          }
        }]
      } as any;
      expect(service['isBuildYourBet'](bet)).toBe(0);
    });

    it('should check type id and set isBuildYourBet and return 1 (case: all success)', () => {
      Object.defineProperty(service, 'env', {
        value: {
          BYB_CONFIG: { HR_YC_EVENT_TYPE_ID: 1 }
        }
      });
      const bet: IBetHistoryBet = {
        leg: [{
          eventEntity: {
            typeId: 1
          }
        }]
      } as any;
      expect(service['isBuildYourBet'](bet)).toBe(1);
    });
  });

  describe('#getGtmInfo ', () => {
    it('should return general GTM info', () => {
      spyOn<any>(service, 'getBetLiveStatus').and.callThrough();
      spyOn<any>(service, 'isBuildYourBet').and.callThrough();
      service['gtmLocation'] = 'cashout';
      const bet: IBetHistoryBet = {
        betType: 'bet-type',
        leg: [
          { eventEntity: { isStarted: true, eventIsLive: false } },
          { eventEntity: { isStarted: false, eventIsLive: true } }
        ]
      } as any;

      expect(service['getGtmInfo'](bet)).toEqual({
        eventCategory: 'edit acca',
        betType: 'bet-type',
        location: 'cashout',
        betInPlay: 'Yes',
        customerBuilt: 0,
      } as any);
      expect(service['getBetLiveStatus']).toHaveBeenCalledWith(bet);
      expect(service['isBuildYourBet']).toHaveBeenCalledWith(bet);
    });

    it('should set location to unknown', () => {
      service['gtmLocation'] = undefined;
      const bet: IBetHistoryBet = {
        betType: 'bet-type',
        leg: [
          { eventEntity: { isStarted: true, eventIsLive: false } },
          { eventEntity: { isStarted: false, eventIsLive: true } }
        ]
      } as any;

      expect(service['getGtmInfo'](bet)).toEqual({
        eventCategory: 'edit acca',
        betType: 'bet-type',
        location: 'unknown',
        betInPlay: 'Yes',
        customerBuilt: 0,
      } as any);
    });
  });

  describe('removeSavedAcca', () => {
    it('should remove saved Acca if it is saved', () => {
      service.savedAccas = { '1' : 'success' };
      service.removeSavedAcca('1');
      expect(service.savedAccas['1']).toBeUndefined();
    });
    it('shouldn`t remove items from saved accas if bet id don`t match', () => {
      service.savedAccas = { '1' : 'success' };
      service.removeSavedAcca('2');
      expect(service.savedAccas['1']).toBeDefined();
    });
  });

});
