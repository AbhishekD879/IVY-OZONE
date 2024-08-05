import { FiveASidePitchComponent } from './five-a-side-pitch.component';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { SafeHtml } from '@angular/platform-browser';
describe('#FiveASidePitchComponent', () => {
  let component;
  let fiveASideService;
  let router;
  let routingHelperService;
  let infoDialogService;
  let localeService;
  let user;
  let pubSubService;
  let bet;
  let gtmService;
  let deviceService;
  let freeBetsService;
  let storageService;
  let activatedRoute;
  let fiveASideContestSelectionService;

  beforeEach(() => {
    fiveASideService = {
      getFormations: jasmine.createSpy('getFormations').and.returnValue(of([{
        id: '1',
        actualFormation: '1-1-1-1',
        position1: 'position1',
        stat1: {id: 1, title: 'title1'},
        position2: 'position2',
        stat2: {id: 1, title: 'title2'},
        position3: 'position3',
        stat3: {id: 1, title: 'title3'},
        position4: 'position4',
        stat4: {id: 1, title: 'title4'},
        position5: 'position5',
        stat5: {id: 1, title: 'title5'},
      }])),
      getFormation: jasmine.createSpy('getFormation').and.returnValue({
        id: '1',
        actualFormation: '1-1-1-1',
        position1: 'position1',
        stat1: {id: 1, title: 'title1'},
        position2: 'position2',
        stat2: {id: 1, title: 'title2'},
        position3: 'position3',
        stat3: {id: 1, title: 'title3'},
        position4: 'position4',
        stat4: {id: 1, title: 'title4'},
        position5: 'position5',
        stat5: {id: 1, title: 'title5'},
      }),
      buildPitchPlayers: jasmine.createSpy('buildPitchPlayers').and.returnValue([
        { index: 0, player: '5'}, { index: 1, player: '23'}, { index: 2, player: '7'}
      ]),
      getPlayerList: jasmine.createSpy('getPlayerList').and.returnValue(of({
        allPlayers: [],
        home: [],
        away: []
      })),
      setPlayerDetails: jasmine.createSpy('setPlayerDetails'),
      preapereOPTAInfo: jasmine.createSpy('preapereOPTAInfo'),
      sortPlayers: jasmine.createSpy('sortPlayers').and.returnValue([]),
      showView: jasmine.createSpy(),
      hideView: jasmine.createSpy(),
      activeView: false,
      isEditMode: false,
      getJourneyStaticBlocks: jasmine.createSpy('getJourneyStaticBlocks').and.returnValue(of({
        block: {
          title: 'title',
          htmlMarkup: jasmine.any(Object) as SafeHtml
        }
      })),
      playerListScrollPosition: jasmine.createSpy(),
      imagesExistOnHomeAway : []
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('event/12345')
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog').and.callFake((a, b, c, d, callback, arr) => {
        arr[1].handler();
      }),
      closePopUp: jasmine.createSpy('closePopUp')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('string')
    };
    user = {
      status: 'logged'
    };
    pubSubService = {
      publish: jasmine.createSpy('publish')
    };
    bet = {
      clear: jasmine.createSpy('clear'),
      initialize: jasmine.createSpy('initialize'),
      isRoleDisabled: jasmine.createSpy('isRoleDisabled'),
      roleEmpty: jasmine.createSpy('roleEmpty'),
      clearRole: jasmine.createSpy('clearRole'),
      addRole: jasmine.createSpy('addRole'),
      addToBetslip: jasmine.createSpy('addToBetslip'),
      getRole: jasmine.createSpy('getRole'),
      errorMessage: 'errorMessage',
      formattedPrice: '10/1',
      isValid: true,
      playersObject: {
        '1_2': { id: 12, statValue: '23'}
      },
      disabledRolesMarked: true
    };
    gtmService = {
      push: jasmine.createSpy('push'),
    };
    deviceService = {
      isDesktop: false,
      isTablet: false
    } as any;
    freeBetsService = {
      getFreeBetsData: jasmine.createSpy('getFreeBetsData').and.returnValue([{tokenPossibleBet: {betLevel: 'ANY'}}]),
      isFreeBetVisible: jasmine.createSpy('isFreeBetVisible').and.returnValue(true)
    };
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    activatedRoute = {
      snapshot: {
        paramMap: {
          get: (name: string) => {
            if (name === 'formation') {
              return '0-1-2-2';
            } else {
              return '5';
            }
          }
        },
        children: []
      },
      params: of({
        sport: 'football',
        id: '12345'
      })
    };

    fiveASideContestSelectionService = {
      defaultSelection: jasmine.createSpy('defaultSelection')
    };

    component = new FiveASidePitchComponent(
      fiveASideService,
      router,
      routingHelperService,
      infoDialogService,
      localeService,
      user,
      pubSubService,
      bet,
      gtmService,
      deviceService,
      freeBetsService,
      storageService,
      activatedRoute,
      fiveASideContestSelectionService
    );
    component.eventEntity = {
      id: 12345
    } as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.errorMessage).toEqual('errorMessage');
    expect(component.formattedPrice).toEqual('10/1');
    expect(component.isValid).toEqual(true);
    expect(component.activeView).toEqual(true);
    expect(component.playersObject).toEqual({
      '1_2': { id: 12, statValue: '23'}
    });
    expect(component.disabledRolesMarked).toEqual(true);
    expect(component.yourcallBetslipShown).toBeFalsy();
  });

  describe('#teamsImgExistOnHomeAway', () => {
    it('should return true if images exist on both teams', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: true},
      'teamtwo': {filename: 'img2', fiveASideToggle: true}};
      expect(component.teamsImgExistOnHomeAway).toBeTruthy();
    });
    it('should return false if images exist on both teams', () => {
      fiveASideService.imagesExistOnHomeAway = {};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: true},
      'teamtwo': {filename: 'img2', fiveASideToggle: false}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: false},
      'teamtwo': {filename: 'img2', fiveASideToggle: true}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: false},
      'teamtwo': {filename: 'img2', fiveASideToggle: false}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: '', fiveASideToggle: true},
      'teamtwo': {filename: 'img2', fiveASideToggle: true}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: true},
      'teamtwo': {filename: '', fiveASideToggle: true}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
  });

  describe('#ngOnInit', () => {
    it('should call ngOnInit method', () => {
      const pitch = {'formation':'0-1-2-2','players':['5','23','7']} as any;
      spyOn(component, 'getPitchDetails').and.returnValue(pitch);
      fiveASideService.getFormation.and.returnValue(null);
      component.ngOnInit();
      expect(component.formations).toEqual(
        [{
          id: '1',
          actualFormation: '1-1-1-1',
          position1: 'position1',
          stat1: {id: 1, title: 'title1'},
          position2: 'position2',
          stat2: {id: 1, title: 'title2'},
          position3: 'position3',
          stat3: {id: 1, title: 'title3'},
          position4: 'position4',
          stat4: {id: 1, title: 'title4'},
          position5: 'position5',
          stat5: {id: 1, title: 'title5'},
        }]
      );
    });

    it('should set isTabletOrDesktop to false if origin is mobile', () => {
      component.ngOnInit();
      expect(component.isTabletOrDesktop).toBeFalsy();
    });

    it('should set isTabletOrDesktop to true if origin is Desktop', () => {
      deviceService.isDesktop = true;
      deviceService.isTablet = false;
      component.ngOnInit();
      expect(component.isTabletOrDesktop).toBeTruthy();
    });

    it('should set isTabletOrDesktop to true if origin is Tablet', () => {
      deviceService.isDesktop = false;
      deviceService.isTablet = true;
      component.ngOnInit();
      expect(component.isTabletOrDesktop).toBeTruthy();
    });

    it('should call ngOnInit method when no formations', () => {
      fiveASideService.getFormations.and.returnValue(of([]));
      component.ngOnInit();

      expect(component.formations).toEqual([]);
      expect(component.matrixFormation).toEqual([]);
    });

    it('should start journey with Free bets', fakeAsync(() => {
      storageService.get.and.returnValue(null);

      component.ngOnInit();
      tick();

      expect(component.showJourney).toBeTruthy();
      expect(component.isJourneySeen).toBeFalsy();
      expect(component.availableFiveASideFreeBets).toBeTruthy();

      freeBetsService.isFreeBetVisible.and.returnValue(false);
      component.ngOnInit();
      tick();

      expect(component.showJourney).toBeTruthy();
      expect(component.isJourneySeen).toBeFalsy();
      expect(component.availableFiveASideFreeBets).toBeTruthy();
    }));

    it('should start journey without Free bets', fakeAsync(() => {
      freeBetsService.getFreeBetsData.and.returnValue([]);
      freeBetsService.isFreeBetVisible.and.returnValue(false);
      storageService.get.and.returnValue(null);

      component.ngOnInit();
      tick();

      expect(component.slides).toEqual(jasmine.any(Object));
      expect(component.showJourney).toBeTruthy();
      expect(component.isJourneySeen).toBeFalsy();
      expect(component.availableFiveASideFreeBets).toBeFalsy();
    }));

    it('should not start journey', fakeAsync(() => {
      freeBetsService.getFreeBetsData.and.returnValue([]);
      freeBetsService.isFreeBetVisible.and.returnValue(false);

      storageService.get.and.returnValue(true);

      component.ngOnInit();
      tick();

      expect(component.isJourneySeen).toBeTruthy();
      expect(component.availableFiveASideFreeBets).toEqual(false);
    }));
  });

  describe('#changeFormation', () => {
    let formation;

    beforeEach(() => {
      formation = [{
        actualFormation: '1-1-1-1',
        position1: 'position1',
        stat1: {id: 1, title: 'title1'},
        position2: 'position2',
        stat2: {id: 1, title: 'title2'},
        position3: 'position3',
        stat3: {id: 1, title: 'title3'},
        position4: 'position4',
        stat4: {id: 1, title: 'title4'},
        position5: 'position5',
        stat5: {id: 1, title: 'title5'},
      }];
    });

    it('should have selectedFormation', () => {
      component.changeFormation(formation[0]);

      expect(component.selectedFormation).toEqual(formation[0]);
    });

    it('should check matrixFormation with formation 1', () => {
      component.changeFormation(formation[0]);

      expect(component.matrixFormation[0]).toEqual({
        rowIndex: 0,
        collIndex: 1,
        position: 'position1',
        stat: 'title1',
        statId: 1,
        roleId: 'position1'
      });
    });

    it('should check matrixFormation with formation 2', () => {
      formation[0].actualFormation = '2-1-1-1';
      component.changeFormation(formation[0]);

      expect(component.matrixFormation[1]).toEqual({
        rowIndex: 0,
        collIndex: 7,
        position: 'position2',
        stat: 'title2',
        statId: 1,
        roleId: 'position2'
      });
      expect(fiveASideService.setPlayerDetails).not.toHaveBeenCalled();
    });

    it('should check matrixFormation with formation 3', () => {
      formation[0].actualFormation = '3-1-1-0';
      component.changeFormation(formation[0]);

      expect(component.matrixFormation[2]).toEqual({
        rowIndex: 0,
        collIndex: 2,
        position: 'position3',
        stat: 'title3',
        statId: 1,
        roleId: 'position3'
      });
    });

    it('should not have matrixFormation', () => {
      formation[0].actualFormation = '0-0-0-0';
      component.changeFormation(formation[0]);

      expect(component.matrixFormation.length).toEqual(0);
    });

    it('should have 5 positions in matrixFormation', () => {
      formation[0].actualFormation = '1-1-1-2';
      component.changeFormation(formation[0]);

      expect(component.matrixFormation.length).toEqual(5);
    });

    it('should go to default break', () => {
      formation[0].actualFormation = '1-5-1-2';
      component.changeFormation(formation[0]);

      expect(component.matrixFormation.length).toEqual(4);
    });

    it('#should track change formation when pitch view open first time', () => {
      component.selectedFormation = undefined;
      formation[0].actualFormation = '1-5-1-2';
      component.changeFormation(formation[0]);
      component.selectedFormation.title = 'Traditional';
      component.trackFormationChanges(component.selectedFormation);
      fiveASideService.actualFormation = component.selectedFormation;

      expect(fiveASideService.actualFormation).toBeDefined();
      expect(component.matrixFormation.length).toEqual(4);
      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          eventCategory: '5-A-Side',
          eventAction: 'Formation',
          eventLabel: 'Traditional'
        }
      );
    });

    it('#should track change formation that same type and another data', () => {
      component.selectedFormation = {};
      formation[0].actualFormation = '1-5-1-2';
      formation[0].id = '11111';
      component.changeFormation(formation[0]);
      component.selectedFormation.title = 'Traditional';
      component.selectedFormation.id = '11111';
      component.trackFormationChanges(component.selectedFormation);
      fiveASideService.actualFormation = component.selectedFormation;

      expect(fiveASideService.actualFormation).toBeDefined();
      expect(component.matrixFormation.length).toEqual(4);
      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          eventCategory: '5-A-Side',
          eventAction: 'Formation',
          eventLabel: 'Traditional'
        }
      );
    });

    it('#should track change formation', () => {
      component.selectedFormation = undefined;
      formation[0].actualFormation = 'Traditional';
      formation[0].id = '11111';
      component.changeFormation(formation[0]);
      component.selectedFormation.title = 'Traditional';
      component.selectedFormation.id = '11133311';
      component.trackFormationChanges(component.selectedFormation);
      fiveASideService.actualFormation = component.selectedFormation;

      expect(fiveASideService.actualFormation).toBeDefined();
      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          eventCategory: '5-A-Side',
          eventAction: 'Formation',
          eventLabel: 'Traditional'
        }
      );
    });

    it('#should not track change formation', () => {
      formation[0].actualFormation = '1-5-1-2';
      component.selectedFormation = formation[0];
      component.changeFormation(formation[0], false);

      expect(gtmService.push).not.toHaveBeenCalled();
    });
  });

  describe('#trackByFn', () => {
    it('should return 5 in trackByFn', () => {
      expect(component.trackByFn(5, {id: 5})).toBe('5_5');
    });
  });

  describe('#addPlayer', () => {
    it('should add player', () => {
      const item = {
        rowIndex: 1,
        collIndex: 2,
        position: 'string',
        stat: 'string',
        statId: 1,
        roleId: 'string'
      };
      fiveASideService.optaStatisticsAvailable = true;
      component.addPlayer(item);
      expect(component.currentMatrixFormation).toEqual(item);
      expect(fiveASideService.showView).toHaveBeenCalledWith({ view: 'player-list', item });
      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          eventCategory: '5-A-Side',
          eventAction: 'Choose Player',
          eventLabel: 'string'
        }
      );
    });

    it('should not add player if Role Disabled', () => {
      const item = {
        rowIndex: 1,
        collIndex: 2,
        position: 'string',
        stat: 'string',
        statId: 1,
        roleId: 'string'
      };
      fiveASideService.optaStatisticsAvailable = true;
      bet.isRoleDisabled = jasmine.createSpy('bet.isRoleDisabled').and.returnValue(true);
      component.addPlayer(item);

      expect(component.currentMatrixFormation).toEqual(undefined);
      expect(fiveASideService.showView).not.toHaveBeenCalled();
    });

    it('should Edit player', () => {
      bet.playersObject = {
        position1: {
          player: {
            name: 'Player 1'
          }
        }
      } as any;
      const item = {
        rowIndex: 1,
        collIndex: 2,
        position: 'string',
        stat: 'string',
        statId: 1,
        roleId: 'position1'
      };
      fiveASideService.optaStatisticsAvailable = true;
      const player = component.playersObject[item.roleId].player;
      component.addPlayer(item);
      expect(fiveASideService.showView).toHaveBeenCalledWith({ view: 'player-page', player, item }, true);
      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          eventCategory: '5-A-Side',
          eventAction: 'Edit Player',
          eventLabel: 'string'
        }
      );
    });

    it('Should prepare prepare OPTA info, if unavailable', () => {
      const item = {
        rowIndex: 1,
        collIndex: 2,
        position: 'string',
        stat: 'string',
        statId: 1,
        roleId: 'string'
      };
      fiveASideService.optaStatisticsAvailable = false;
      component.addPlayer(item);

      expect(fiveASideService.preapereOPTAInfo).toHaveBeenCalled();
      expect(fiveASideService.setPlayerDetails).toHaveBeenCalled();
    });
  });

  describe('#hidePitch', () => {
    it('should hide pitch when on BetReceipt', () => {
      component.isBetReceipt = true;

      component.hidePitch();

      expect(component.showPitch).toEqual(false);
      expect(router.navigate).toHaveBeenCalledWith(['/event/12345/5-a-side']);
    });

    it('should hide pitch when no matrixFormation', () => {
      expect(component.showPitch).toEqual(true);

      component.hidePitch();

      expect(component.showPitch).toEqual(false);
      expect(router.navigate).toHaveBeenCalledWith(['/event/12345/5-a-side']);
    });

    it('should hide pitch when some roles are already chosen', () => {
      component.matrixFormation = [{}] as any;
      component.hidePitch();
      bet.roleEmpty = jasmine.createSpy('roleEmpty').and.returnValue(false);

      expect(infoDialogService.openInfoDialog).toHaveBeenCalledWith('string', 'string', null, 'informationDialog', null,
        [
          { caption: 'string', cssClass: 'btn-style4', handler: jasmine.any(Function) },
          { caption: 'string', cssClass: '', handler: jasmine.any(Function) }
        ]);
      expect(localeService.getString).toHaveBeenCalledTimes(4);
      expect(infoDialogService.closePopUp).toHaveBeenCalled();
    });

    it('should hide pitch when when all roles are empty', () => {
      expect(component.showPitch).toEqual(true);

      component.matrixFormation = [{}] as any;
      bet.roleEmpty = jasmine.createSpy('roleEmpty').and.returnValue(true);
      component.hidePitch();

      expect(component.showPitch).toEqual(false);
      expect(router.navigate).toHaveBeenCalledWith(['/event/12345/5-a-side']);
    });
  });

  describe('#ngOnDestroy', () => {
    it('should call ngOnDestroy when no subcribers', () => {
      component.ngOnDestroy();

      expect(component['formationDataSubscription']).toBeUndefined();
      expect(component['playersSubscription']).toBeUndefined();
    });

    it('should unsubscribe formationDataSubscription', () => {
      component['formationDataSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['formationDataSubscription'].unsubscribe).toHaveBeenCalled();
      expect(bet.clear).toHaveBeenCalled();
    });

    it('should unsubscribe playersSubscription', () => {
      component['playersSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['playersSubscription'].unsubscribe).toHaveBeenCalled();
      expect(bet.clear).toHaveBeenCalled();
    });
  });

  describe('ctaButtonClick', () => {
    it('should not add to bet slip if bet is not valid', () => {
      bet.isValid = false;
      component.ctaButtonClick();
      expect(bet.addToBetslip).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should open log in dialog if user logged out', () => {
      bet.isValid = true;
      user.status = undefined;
      component.ctaButtonClick();
      expect(bet.addToBetslip).not.toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('OPEN_LOGIN_DIALOG', { moduleName: 'header' });
    });

    it('should add to betslip if bet is valid and user logged in', () => {
      component.eventEntity = {
        name: 'Team1 vs Team2',
        sportId: '16',
        typeId: '111',
        liveStreamAvailable: true,
        eventIsLive: false,
        id: '222'
      } as any;
      bet.isValid = true;
      user.status = 'logged';
      component.isTabletOrDesktop = true;
      component.ctaButtonClick();
      expect(component.yourcallBetslipShown).toBeTruthy();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('OPEN_LOGIN_DIALOG', { moduleName: 'header' });
    });

    it('should track adding to betslip if bet is valid and user logged in', () => {
      bet.isValid = true;
      user.status = 'logged';
      component.selectedFormation = {
        title: 'Trasitional',
        id: '1',
      } as any;
      component.eventEntity = {
        name: 'Team1 vs Team2',
        sportId: '16',
        typeId: '111',
        liveStreamAvailable: true,
        eventIsLive: false,
        id: '222'
      } as any;
      component.isTabletOrDesktop = false;
      component.ctaButtonClick();
      expect(component.yourcallBetslipShown).toBeFalsy();
      expect(bet.addToBetslip).toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('OPEN_LOGIN_DIALOG', { moduleName: 'header' });
      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          event: 'trackEvent',
          eventCategory: 'quickbet',
          eventAction: 'add to quickbet',
          eventLabel: 'success',
          ecommerce: {
            add: {
              products: [{
                name: 'Team1 vs Team2',
                category: '16',
                variant: '111',
                brand: '5-A-Side',
                metric1: 0,
                dimension60: '222',
                dimension62: 0,
                dimension63: 1,
                dimension64: 'EDP',
                dimension65: '5-A-Side',
                dimension86: 0,
                dimension87: 0,
                dimension89: 'Trasitional',
                quantity: 1
              }]
            }
          }
        }
      );
    });

    it('should track adding to betslip if bet is valid and user logged in case some data false', () => {
      bet.isValid = true;
      user.status = 'logged';
      component.selectedFormation = {
      }as any;
      component.eventEntity = {
        name: 'Team1 vs Team2',
        sportId: '16',
        typeId: '111',
        liveStreamAvailable: false,
        eventIsLive: true,
        id: '222'
      } as any;
      component.ctaButtonClick();
      expect(bet.addToBetslip).toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('OPEN_LOGIN_DIALOG', { moduleName: 'header' });
      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          event: 'trackEvent',
          eventCategory: 'quickbet',
          eventAction: 'add to quickbet',
          eventLabel: 'success',
          ecommerce: {
            add: {
              products: [{
                name: 'Team1 vs Team2',
                category: '16',
                variant: '111',
                brand: '5-A-Side',
                metric1: 0,
                dimension60: '222',
                dimension62: 0,
                dimension63: 1,
                dimension64: 'EDP',
                dimension65: '5-A-Side',
                dimension86: 0,
                dimension87: 0,
                dimension89: undefined,
                quantity: 1
              }]
            }
          }
        }
      );
    });
  });

  it('closePitch should clear bet and set five-a-side-journey-seen to true in LC', () => {
      component.closePitch();
      expect(bet.clear).toHaveBeenCalled();
      expect(storageService.set).toHaveBeenCalledWith(`five-a-side-journey-seen`, true);
  });

  describe('#addPosition', () => {
    it('should call addPosition method', () => {
      component.addPlayerlabel = 'addPlayerlabel';
      component.selectedFormation = {
        position1: 'position1',
        stat1: {
          title: 'title',
          id: 'id'
        }
      };
      component.addPosition(1, 1, 1, 1);

      expect(component.matrixFormation).toEqual([{
        rowIndex: 1,
        collIndex: 1,
        position: 'position1',
        stat: 'title',
        statId: 'id',
        roleId: 'position2'
      }]);
    });
  });

  it('trackById should return unique identifier for formation ', () => {
    expect(component.trackById(0, { id: '123'} as any)).toEqual('123_0');
  });

  it('trackById should return unique identifier for formation ', () => {
    component.yourcallBetslipShown = true;
    component.handleCloseQuickBet();
    expect(component.yourcallBetslipShown).toBeFalsy();
  });

  describe('#formJourney', () => {
    let staticBlocks, slide1, slide2, slide3, slide100500;
    beforeEach(() => {
      slide1 = {
        title: 'title1',
        htmlMarkup: 'markup1'
      };
      slide2 = {
        title: 'title2',
        htmlMarkup: 'markup2'
      };
      slide3 = {
        title: 'title3',
        htmlMarkup: 'markup3'
      };
      slide100500 = {
        title: 'title3',
        htmlMarkup: 'markup3'
      };
      staticBlocks = {
        'five-a-side-free-bet': slide1,
        'five-a-side-journey-step-1': slide2,
        'five-a-side-journey-step-2': slide3,
        'five-a-side-journey-step-100500': slide100500
      };
    });
    it('free bets is available and journey was not seen', () => {
      component.availableFiveASideFreeBets = true;
      component.isJourneySeen = false;
      const journey = component.formJourney(staticBlocks);

      expect(journey).toEqual([slide1, slide2, slide3, slide100500]);
    });
    it('free bets is available and journey was seen', () => {
      component.availableFiveASideFreeBets = true;
      component.isJourneySeen = true;
      const journey = component.formJourney(staticBlocks);

      expect(journey).toEqual([slide1]);
    });

    it('free bets is unvailable and journey was not seen', () => {
      component.availableFiveASideFreeBets = false;
      component.isJourneySeen = false;
      const journey = component.formJourney(staticBlocks);

      expect(journey).toEqual([slide2, slide3, slide100500]);
    });

    it('should return empty array', () => {
      let journey = component.formJourney(null);
      expect(journey).toEqual([]);

      component.availableFiveASideFreeBets = false;
      component.isJourneySeen = true;
      journey = component.formJourney(staticBlocks);
      expect(journey).toEqual([]);

      component.availableFiveASideFreeBets = true;
      component.isJourneySeen = true;
      delete staticBlocks['five-a-side-free-bet'];
      journey = component.formJourney(staticBlocks);

      expect(journey).toEqual([]);
    });
  });

  describe('#getPitchDetails', () => {
    it('should get pitchdetails when snapshot contains formation', () => {
      activatedRoute.snapshot.children = [{
        paramMap: {
          get: jasmine.createSpy('get').and.callFake((name: string) => {
            if (name === 'formation') {
              return '0-1-2-2';
            } else if (name === 'player1') {
              return 'player-1-5';
            } else if (name === 'player2') {
              return 'player-2-23';
            } else if (name === 'player3') {
              return 'player-3-7';
            }
          })
        },
      }];
      const response = component['getPitchDetails']();
      expect(response).toEqual({'formation':'0-1-2-2','players':[
        { index: 0, player: '5'}, { index: 1, player: '23'}, { index: 2, player: '7'}
      ]});
    });
  });

  describe('#validateFormation', () => {
    it('should set hasThreeInRow flag, if formation array has 3', () => {
      const formation = ['1', '1', '2', '1'];
      component.validateFormation(formation);
      expect(component.hasThreeInRow).toBe(false);
    });
    it('should set hasThreeInRow flag, if formation array has 3', () => {
      const formation = ['1', '1', '3', '1'];
      component.validateFormation(formation);
      expect(component.hasThreeInRow).toBe(true);
      expect(component.hasThreeInRowIndex).toBe(2);
    });
  });
});
