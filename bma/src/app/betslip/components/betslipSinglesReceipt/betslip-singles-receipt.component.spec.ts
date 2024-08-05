import { BetslipSinglesReceiptComponent } from './betslip-singles-receipt.component';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import { of as observableOf } from 'rxjs';

describe('BetslipSinglesReceiptComponent', () => {
  let component;
  let nativeBridge;
  let userService;
  let betReceiptService;
  let filtersService;
  let localeService;
  let storageService;
  let cmsService;
  let fbService;
  let windowRef,
  gtmService,
  receipts,
  changeDetection;

  beforeEach(() => {
    receipts = [
      {
        name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{
          part: [
            {
              eventId: '1',
              event: {
                id: '1',
                categoryName: 'football',
                categoryId: '16',
                drilldownTagNames: 'test',
                typeName: 'league',
              }
            }
          ]
        }]
      },
      {
        name: 'Unnamed 2nd Favourite', stake: 3, tokenValue: 2, leg: [{
          part: [
            {
              eventId: '2',
              event: {
                id: '2',
                categoryName: 'football',
                categoryId: '16',
                drilldownTagNames: 'test',
                typeName: 'league',
              }
            }
          ]
        }]
      }
    ];
    nativeBridge = {
      multipleEventPageLoaded: jasmine.createSpy('multipleEventPageLoaded'),
      onEventDetailsStreamAvailable: jasmine.createSpy('onEventDetailsStreamAvailable'),
      onEventAlertsClick: jasmine.createSpy('onEventAlertsClick'),
      footballEventPageLoaded: jasmine.createSpy('footballEventPageLoaded'),
      hasShowFootballAlerts: jasmine.createSpy('hasShowFootballAlerts').and.returnValue(true),
      showFootballAlerts: jasmine.createSpy('showFootballAlerts'),
      hasOnEventAlertsClick: jasmine.createSpy('hasOnEventAlertsClick').and.returnValue(true),
      onActivateWinAlerts: jasmine.createSpy(),
      getMobileOperatingSystem: jasmine.createSpy().and.returnValue('android'),
      winAlertsStatus: jasmine.createSpy(),
      pushNotificationsEnabled: true,
      disableWinAlertsStatus : jasmine.createSpy()
    };

    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'), // TODO: Reverted changes from BMA-37049.
                                                                 // Will be removed after new approach implementation.
        removeEventListener: jasmine.createSpy('removeEventListener') // TODO: Reverted changes from BMA-37049.
                                                                      // Will be removed after new approach implementation.
      },
      document: {
        removeEventListener: jasmine.createSpy('removeEventListener'),
        addEventListener: jasmine.createSpy('addEventListener')
      }
    };

    userService = {
      currencySymbol: '$',
      receiptViewsCounter: 5,
      username: 'test'
    };

    betReceiptService = {
      hasStake: () => { },
      getStake: () => { },
      getReceiptOdds: () => { },
      getLinesPerStake: () => { },
      getEWTerms: () => { },
      setToggleSwitchId: () => { },
      isBogFromPriceType: () => { },
      getExcludedDrillDownTagNames: jasmine.createSpy('getExcludedDrillDownTagNames').and.returnValue('ExcludedDrillDownTagNames')
    };

    filtersService = {
      filterPlayerName: () => { },
      filterAddScore: () => { }
    };

    localeService = {
      getString: jasmine.createSpy()
    };

    storageService = {
      get: jasmine.createSpy('storageService.get').and.returnValue(undefined)
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };
    cmsService = {
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(observableOf({
        svg: 'svg',
        svgId: 'svgId'
      })),
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        CelebratingSuccess: {
          cashoutMessage: "YOU HAVE CASHED OUT: {amount}!!",
          celebrationBannerURL: "{6C768A64-74F8-46FE-A380-9DE3E51C2EBA}",
          celebrationMessage: "CONGRATS!",
          displayCelebrationBanner: true,
          duration: 48,
          winningMessage: "YOU HAVE WON: {amount}!!",
          displaySportIcon: ["openbets", "settledbets", "cashoutbets", "betreceipt", "edpmybets"]
        },
        ScoreboardsDataDisclaimer:{enabled: true, dataDisclaimer: 'Transmission delayed'}, 
        winAlerts: {displayOnBetReceipt: ['android']}
      })),
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(observableOf({
        visibleNotificationIconsFootball: {
          multiselectValue: ['android'],
          value: 'league'
        },
        displayOnBetReceipt: ['android']
      }))
    };
    changeDetection = {
      detectChanges: jasmine.createSpy('detectChanges')
    }

    component = new BetslipSinglesReceiptComponent(
      nativeBridge,
      userService,
      betReceiptService,
      filtersService,
      localeService,
      storageService,
      cmsService,
      windowRef,
      gtmService,
      changeDetection,
      fbService
    );

    component.isBogFromPriceType = jasmine.createSpy('isBogFromPriceType');
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.currencySymbol).toEqual('$');
    expect(component.filterPlayerName).toEqual(jasmine.any(Function));
    expect(component.filterAddScore).toEqual(jasmine.any(Function));
    expect(component.getEWTerms).toEqual(jasmine.any(Function));
    expect(component.getLinesPerStake).toEqual(jasmine.any(Function));
    expect(component.hasStake).toEqual(jasmine.any(Function));
    expect(component.getStake).toEqual(jasmine.any(Function));
    expect(component.getOdds).toEqual(jasmine.any(Function));
    expect(component.setToggleSwitchId).toEqual(jasmine.any(Function));
  });

  it('#ngOnInit should modify singles receipt with stakeValue and exclude extra place promo for unnamed favourites', () => {
    component.singleReceipts = [
        { name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{part: [{event: {categoryId: '21'}}]}]},
        { name: 'Unnamed 2nd Favourite', stake: 3, tokenValue: 2, leg: [{part: [{event: {categoryId: '21'}}]}]},
        { name: 'Unnamed 3rd Favourite', stake: {amount: 6}, tokenValue: 3, leg: [{part: [{event: {categoryId: '21'}}]}]}
      ];
    component.ngOnInit();

    expect(component.singleReceipts[0].stakeValue).toBe(4);
    expect(component.singleReceipts[1].stakeValue).toBe(1);
    expect(component.singleReceipts[2].stakeValue).toBe(3);
  });

  it('#ngOnInit with null values', () => {
    component.singleReceipts = [
        { name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{part: [{event: {categoryId: '21'}}]}]},
        { leg: [null]},
        { leg: [{part: [null]}]},
        { leg: [{part: [{event: undefined}]}]}
      ];
    cmsService.getItemSvg.and.returnValue(observableOf({}));
    component.ngOnInit();
    expect(component.singleReceipts[0].leg[0]).toEqual({part: [{event: {categoryId: '21'}}], svgId: 'icon-generic'});
  });
  it('ngOnInit with cms config as null', () => {
    component.singleReceipts = [
      { name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{part: [{event: {categoryId: '21'}}]}]},
      { name: 'Unnamed 2nd Favourite', stake: 3, tokenValue: 2, leg: [{part: [{event: {categoryId: '21'}}]}]},
      { name: 'Unnamed 3rd Favourite', stake: {amount: 6}, tokenValue: 3, leg: [{part: [{event: {categoryId: '21'}}]}]}
    ];
    cmsService.getSystemConfig.and.returnValue(observableOf(null));
    component.ngOnInit();
  });
  it('ngOnInit with cms config CelebratingSuccess as null', () => {
    component.singleReceipts = [
      { name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{part: [{event: {categoryId: '21'}}]}]},
      { name: 'Unnamed 2nd Favourite', stake: 3, tokenValue: 2, leg: [{part: [{event: {categoryId: '21'}}]}]},
      { name: 'Unnamed 3rd Favourite', stake: {amount: 6}, tokenValue: 3, leg: [{part: [{event: {categoryId: '21'}}]}]}
    ];
    cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: null}));
    component.ngOnInit();
  });
  it('ngOnInit with cms config displaySportIcon as undefined', () => {
    component.singleReceipts = [
      { name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{part: [{event: {categoryId: '21'}}]}]},
      { name: 'Unnamed 2nd Favourite', stake: 3, tokenValue: 2, leg: [{part: [{event: {categoryId: '21'}}]}]},
      { name: 'Unnamed 3rd Favourite', stake: {amount: 6}, tokenValue: 3, leg: [{part: [{event: {categoryId: '21'}}]}]}
    ];
    cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: {displaySportIcon: undefined}}));
    component.ngOnInit();
    expect(component.isSportIconEnabled).not.toBeTrue();
  });
  describe('#trackByIndex', () => {
    it('should call trackByIndex and track by index and betId #', () => {
      expect(component.trackByIndex(2, { betId: '23423423' } as any)).toEqual('2_23423423');
    });
  });

  describe('#showWinAlertsTooltip', () => {
    it('should call showWinAlertsTooltip when receiptViewsCounter less or equal MAX_VIEWS_COUNT', () => {
      expect(component.showWinAlertsTooltip()).toEqual(true);
      expect(storageService.get).toHaveBeenCalled();
    });
    it('should call showWinAlertsTooltip when receiptViewsCounter less or equal MAX_VIEWS_COUNT', () => {
      storageService.get = jasmine.createSpy('').and.returnValue({'receiptViewsCounter-test': 2});
      expect(component.showWinAlertsTooltip()).toEqual(false);
      expect(storageService.get).toHaveBeenCalled();
    });
  });

  describe('#toggleWinAlerts', () => {
    it('should call toggleWinAlerts method and emit winAlertsToggleChanged', () => {
      component.winAlertsToggleChanged.emit = jasmine.createSpy('winAlertsToggleChanged.emit');
      const receipt = {
        leg: [{ part: [{ eventCategoryId: '16' }] }]} as any;
      component.toggleWinAlerts(receipt, true);

      expect(component.winAlertsToggleChanged.emit).toHaveBeenCalledWith({
        receipt,
        state: true
      });
    });
  });

  describe('#buildLinesTitle', () => {
    let receipt;
    beforeEach(() => {
      receipt = {
        isFCTC: true,
        numLines: '5',
        stakePerLine: 2
      } as any;
    });
    it('forcast receipt case for 5 lines', () => {
      component.buildLinesTitle(receipt);
      expect(localeService.getString).toHaveBeenCalledWith('bs.linesPerStake', {
        lines: receipt.numLines,
        stake: receipt.stakePerLine,
        currency: '$'
      });
    });
    it('forcast receipt case for 1 line', () => {
      receipt.numLines = '1';
      component.buildLinesTitle(receipt);
      expect(localeService.getString).toHaveBeenCalledWith('bs.linePerStake', {
        lines: receipt.numLines,
        stake: receipt.stakePerLine,
        currency: '$'
      });
    });
    it('not a forcast receipt case', () => {
      receipt.isFCTC = false;
      component.buildLinesTitle(receipt);
      expect(component.buildLinesTitle(receipt)).toBeUndefined();
    });
  });

  describe('#appendDrillDownTagNames', () => {
    it('should return tagNames with , separated', () => {
      const result = component.appendDrillDownTagNames({drilldownTagNames: 'MKTFLAG_PB,', eventMarket: 'Match Result'});
      expect(result).toEqual('MKTFLAG_PB,Match Result,');
    });

    it('should return new drilldown with marketName only', () => {
      const result = component.appendDrillDownTagNames({drilldownTagNames: '', eventMarket: 'Match Result'});
      expect(result).toEqual('Match Result,');
    });
  })

  describe('setAlertsConfig', () => {
    beforeEach(() => {
      component.singleReceipts = receipts;
    });
    it('should NOT call multipleEventPageLoaded - bet not found', () => {
      component['setAlertsConfig']();
      expect(nativeBridge['multipleEventPageLoaded']).toHaveBeenCalled();
    });
    it('should hasOnEventAlertsClick - false, hasShowFootballAlerts - true', () => {
      nativeBridge.hasOnEventAlertsClick.and.returnValue(false);
      component['setAlertsConfig']();
      expect(nativeBridge['multipleEventPageLoaded']).toHaveBeenCalled();
    });
    it('should call multipleEventPageLoaded without football category name', () => {
      component.singleReceipts = [
        {
          name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{
            part: [
              {
                eventId: '1',
                event: {
                  categoryName: 'tennis',
                  categoryId: '17',
                  drilldownTagNames: 'test'
                }
              }
            ]
          }]
        }
      ];
      component['setAlertsConfig']();
      expect(nativeBridge['multipleEventPageLoaded']).not.toHaveBeenCalled();
    });

    it('should call setAlertsConfig - no allowedLeaguesList ', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf({
          visibleNotificationIcons: {
            multiselectValue: ['android'],
            value: ['test']
        },
        displayOnBetReceipt: ['android']
      }));
      component['setAlertsConfig']();
      expect(nativeBridge.multipleEventPageLoaded).not.toHaveBeenCalled();
    });
    it('should NOT do football Alerts Visible if no configuration in CMS', () => {
      spyOn<any>(component, 'setFootballAlerts').and.callThrough();
      cmsService.getFeatureConfig.and.returnValue(observableOf({
        visibleNotificationIcons: {
          multiselectValue: ['test'],
          value: 'test'
      },
      displayOnBetReceipt: ['test']
      }));
      component['setAlertsConfig']();
      expect(component['setFootballAlerts']).not.toHaveBeenCalled();
    });
    it('should NOT do football Alerts Visible if no configuration in CMS', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf({
          visibleNotificationIcons: { }
      }));
      component['setAlertsConfig']();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
    });
    it('should get visible notification icons from sport types', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf({
          visibleNotificationIcons: {
            multiselectValue: ['android'],
            value: 'league'
        }
      }));
      component['setAlertsConfig']();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
    });
  });
  describe('handleFootballAlerts', () => {
    it('handleFootballAlerts - with matching eventid', () => {
      component['singleReceipts'] = receipts.slice(0,1);
      const data = {detail: [{eventId: "1", isEnabled: true}]} as any;
      component['handleFootballAlerts'](data);
      expect(component['singleReceipts'][0].footballBellActive).toBeTrue();
    });
    it('handleFootballAlerts - without matching eventid', () => {
      component['singleReceipts'] = receipts.slice(0,1);
      const data = {detail: [{eventId: "30000", isEnabled: true}]} as any;
      component['handleFootballAlerts'](data);
      expect(component['singleReceipts'][0].footballBellActive).toBeFalsy();
    });
  });
  describe('GTM', () => {
    it('onFootballBellClick', () => {
      const part = receipts[0].leg[0].part[0];
      spyOn<any>(component, 'sendGTMMatchAlertClick').and.callThrough();
      component['onFootballBellClick'](receipts[0]);
      expect(nativeBridge['onEventAlertsClick']).toHaveBeenCalledWith(part.eventId,
        part.event.categoryName.toLocaleLowerCase(),
        part.event.categoryId,
        part.event.drilldownTagNames,
      ALERTS_GTM.BETSLIP);
      expect(nativeBridge['showFootballAlerts']).toHaveBeenCalled();
      expect(component['sendGTMMatchAlertClick']).toHaveBeenCalledWith(receipts[0]);
    });
    it('handleAlertInfoClick', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.CLICK,
        'component.PositionEvent': ALERTS_GTM.NA,
        'component.EventDetails': ALERTS_GTM.WIN_ALERT_ICON
      };
      component['handleAlertInfoClick'](receipts[0]);
      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData, receipts[0]);
    });
    it('sendGTMWinAlertToggle - enabled - false', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.TOGGLE_OFF,
        'component.PositionEvent': ALERTS_GTM.BETSLIP,
        'component.EventDetails': ALERTS_GTM.WIN_ALERT
      };
      component['sendGTMWinAlertToggle'](false, receipts[0]);
      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData, receipts[0]);
    });
  });

  describe('setFootballAlerts', () => {
    it('setFootballAlerts', () => {
      const singleReceipts = 
        {
          name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{
            part: [
              {
                eventId: '1',
                event: {
                  categoryName: 'tennis',
                  categoryId: '17',
                  drilldownTagNames: 'test',
                  typeName: 'league',
                  eventSortCode: 'test',
                  categoryCode: 'MOTOR_SPORTS'
                }
              }
            ]
          }]
        }  as any;
      component['setFootballAlerts'](singleReceipts, ['league']);
      expect(singleReceipts.footballAlertsVisible).toBeFalsy();
    });
    it('setFootballAlerts - footballAlertsVisible - true', () => {
      const singleReceipts = 
        {
          name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{
            part: [
              {
                eventId: '1',
                event: {
                  categoryName: 'football',
                  categoryId: '16',
                  drilldownTagNames: 'test',
                  typeName: 'league',
                  eventSortCode: 'test',
                  categoryCode: 'football'
                }
              }
            ]
          }]
        }  as any;
      component['setFootballAlerts'](singleReceipts, ['league']);
      expect(singleReceipts.footballAlertsVisible).toBeTrue();
    });
    it('setFootballAlerts - outright', () => {
      const singleReceipts = 
        {
          name: 'unnamed favourite', stake: 5, tokenValue: 1, leg: [{
            part: [
              {
                eventId: '1',
                event: {
                  categoryName: 'football',
                  categoryId: '16',
                  drilldownTagNames: 'test',
                  typeName: 'league',
                  eventSortCode: 'TNMT',
                  categoryCode: 'football'
                }
              }
            ]
          }]
        }  as any;
      component['setFootballAlerts'](singleReceipts, ['league']);
      expect(singleReceipts.footballAlertsVisible).toBeFalse();
    });
  });

  describe('ngOnDestroy', () => {
    it('ngOnDestroy', () => {
      component.ngOnDestroy();
      expect(component.windowRef.document.removeEventListener).toHaveBeenCalledWith('multipleEventAlertsEnabled', component.handleFootballAlerts);
    });
  });
});
