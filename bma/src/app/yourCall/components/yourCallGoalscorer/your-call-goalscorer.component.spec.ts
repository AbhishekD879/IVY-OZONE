
import { of, Subject } from 'rxjs';
import { storage } from '../YourcallPlayerBets/your-call-player-bets.mock';
import { YourCallGoalscorerComponent } from './your-call-goalscorer.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('YourCallGoalscorerComponent', () => {
  let yourCallMarketsService, dialogService, infoDialogService, localeService;
  let changeDetector, bybSelectedSelectionsService, WindowRefService;
  let component: YourCallGoalscorerComponent;

  beforeEach(() => {
    yourCallMarketsService = {
      addSelection: jasmine.createSpy('addSelection'),
      removeSelection: jasmine.createSpy('removeSelection'),
      selectValue: jasmine.createSpy('selectValue'),
      selectedSelectionsSet: new Set(),
      goalscorerSubject$: new Subject<any>(),
      betRemovalsubject$: new Subject<any>(),
      loadMarketSelections: jasmine.createSpy('loadMarketSelections').and.returnValue({
        then: () => {
        }
      }),
    }
    changeDetector = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('string')
    };
    WindowRefService = {
      nativeWindow: {
        localStorage: {
          getItem: jasmine.createSpy('getItem').and.returnValue(true)
        }
      }
    };
    bybSelectedSelectionsService = {
      callGTM: jasmine.createSpy('callGTM').and.returnValue(true),
      betPlacementSubject$: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true)),
        complete: jasmine.createSpy('complete').and.returnValue(of(true)),
      }
    }

    component = new YourCallGoalscorerComponent(yourCallMarketsService, dialogService, infoDialogService, localeService,
      changeDetector, bybSelectedSelectionsService, WindowRefService)
  })

  describe('#ngOninit', () => {
    it("should call betPlacementSubject", fakeAsync(() => {
      spyOn(component, "check");
      component.id = 1;
      yourCallMarketsService.selectedSelectionsSet.add(1)
      yourCallMarketsService.goalscorerSubject$ = new Subject();
      bybSelectedSelectionsService.betPlacementSubject$ = new Subject();
      component.ngOnInit();
      bybSelectedSelectionsService.betPlacementSubject$.next(true);
      yourCallMarketsService.goalscorerSubject$.next({ id: 1, name: '. ronaldo' } as any)
      tick()
      expect(component.showCardPlayersDup.RONALDO).toBeFalsy();
    }));
    it("should call betPlacementSubject", fakeAsync(() => {
      spyOn(component, "check");
      component.id = 2;
      yourCallMarketsService.selectedSelectionsSet.add(2)
      yourCallMarketsService.goalscorerSubject$ = new Subject();
      bybSelectedSelectionsService.betPlacementSubject$ = new Subject();
      component.ngOnInit();
      bybSelectedSelectionsService.betPlacementSubject$.next(false);
      yourCallMarketsService.goalscorerSubject$.next({ id: 1, name: 'ronaldo' } as any)
      tick()
      expect(component.showCardPlayersDup.RONALDO).toBeTruthy();
    }));
  })

  describe('callLocalStorageToFetchPlayerBets', () => {
    it('when callLocalStorageToFetchPlayerBets called when undefined', () => {
      component.eventEntity = { id: 16 } as any;
      WindowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('OX.yourCallStoredData').and.returnValue(JSON.stringify(storage));
      // spyOn(component.localStorage, 'getItem').and.returnValue(JSON.stringify(storage));
      component.callLocalStorageToFetchPlayerBets();
      expect(yourCallMarketsService.selectedSelectionsSet.size).toBeGreaterThan(0);
    });
  });

  describe('#check', () => {
    it("it isteamSelected true", () => {
      spyOn(component, 'addGSSelection');
      spyOn(component, 'selectedGSMarket');
      spyOn(component, 'isteamSelectedGS').and.returnValue(false);
      component.check({} as any, {} as any);
      expect(changeDetector.detectChanges).toHaveBeenCalled()
    })
    it("it isteamSelected true", () => {
      spyOn(component, 'addGSSelection');
      spyOn(component, 'selectedGSMarket');
      spyOn(component, 'isteamSelectedGS').and.returnValue(true);
      component.check({} as any, {} as any);
      expect(changeDetector.detectChanges).toHaveBeenCalled()
    })
  })

  describe('#isteamSelected', () => {
    it('should call isteamSelected method 3', () => {
      const team = [{
        "abbreviation": null,
        "title": "Both Teams",
        "players": null
      }];
      component.selectedGS = [];
      const result = component.isteamSelectedGS(team);
      expect(result).toBe(false);
    });
  });

  describe('#addSelectionGs', () => {
    it('should call addSelection method single', () => {
      component.addGSSelection({} as any);

      expect(component.selectedGS[0]).toEqual({});
    });
    it('should call addSelection method multi', () => {
      component.multi = true;
      component.addGSSelection({} as any);

      expect(component.selectedGS).toEqual([{}]);
    });
  });

  describe('#playerAvailabe', () => {
    it('should call playerAvailabe method single', () => {
      component.enabled = undefined;
      component.playerAvailabe();
      expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    });
  });

  describe('#selectedGSMarket', () => {
    it('should call selectedGSMarket when selection . AG true', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'LAZAZETTE': true };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'A. Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(true);
    }));
    it('should call selectedGSMarket when selection . AG true', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'LAZAZETTE': true };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(true);
    }));
    it('should call selectedGSMarket when selection . AG False ', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(3);
      component.showCardPlayersDup = { 'LAZAZETTE': false };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'A. Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(false);
    }));
    it('should call selectedGSMarket when selection . AG False ', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(3);
      component.showCardPlayersDup = { 'LAZAZETTE': false };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(false);
    }));
    it('should call selectedGSMarket when selection AG true ', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'LAZAZETTE': true };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'A. Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(true);
    }));
    it('should call selectedGSMarket when selection AG true ', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'LAZAZETTE': true };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(true);
    }));
    it('should call selectedGSMarket when selection AG false ', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(2);
      component.showCardPlayersDup = { 'LAZAZETTE': false };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'A. Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(false);
    }));
    it('should call selectedGSMarket when selection AG false ', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(2);
      component.showCardPlayersDup = { 'LAZAZETTE': false };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(false);
    }));
    it('should call selectedGSMarket when selection . group true', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "group", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'LAZAZETTE': true };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'A. Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(true);
    }));
    it('should call selectedGSMarket when selection . group true', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "group", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'LAZAZETTE': true };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(true);
    }));
    it('should call selectedGSMarket when selection . group fasle', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "group", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(3);
      component.showCardPlayersDup = { 'LAZAZETTE': false };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'A. Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(false);
    }));
    it('should call selectedGSMarket when selection . group fasle', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "group", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(3);
      component.showCardPlayersDup = { 'LAZAZETTE': false };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(false);
    }));
    it('should call selectedGSMarket when selection group true', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "group", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'LAZAZETTE': true };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'A. Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(true);
    }));
    it('should call selectedGSMarket when selection group true', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "group", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'LAZAZETTE': true };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(true);
    }));
    it('should call selectedGSMarket when selection group false', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "group", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(3);
      component.showCardPlayersDup = { 'LAZAZETTE': false };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'A. Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(false);
    }));
    it('should call selectedGSMarket when selection group false', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "group", bettingValue2: 1 }] as any;
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }
      component.selection = { id: 1 } as any;
      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.selectedSelectionsSet.add(3);
      component.showCardPlayersDup = { 'LAZAZETTE': false };
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [{ title: 'Lacazette', id: component.selection.id }] }]))),
        component.selectedGSMarket(player as any, team);
      tick();
      expect(component.showCardPlayersDup["LAZAZETTE"]).toBe(false);
    }));
    it('should call selectedGSMarket when no . AG selection ', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      spyOn(component, "playerAvailabe");
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }

      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [] }])));
      component.selectedGSMarket(player as any, team);
      tick();
      expect(component.playerAvailabe).toHaveBeenCalled();
    }));
    it('should call selectedGSMarket when no .AG selection ', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Anytime Goalscorer", bettingValue2: 1 }] as any;
      spyOn(component, "playerAvailabe");
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }

      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [] }])));
      component.selectedGSMarket(player as any, team);
      tick();
      expect(component.playerAvailabe).toHaveBeenCalled();
    }));
    it('should call selectedGSMarket when no . g selection', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Group", bettingValue2: 1 }] as any;
      spyOn(component, "playerAvailabe");
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }

      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [] }])));
      component.selectedGSMarket(player as any, team);
      tick();
      expect(component.playerAvailabe).toHaveBeenCalled();
    }));
    it('should call selectedGSMarket when  no g selection', fakeAsync(() => {
      component.marketsSet = [{ id: 1, grouping: "Anytime Goalscorer", key: "Group", bettingValue2: 1 }] as any;
      spyOn(component, "playerAvailabe");
      const player = {
        "id": 1,
        "name": "Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      };
      const team = {
        "id": "31",
        "title": "Anytime",
        "marketName": "Anytime Goalscorer"
      }

      component.eventEntity = { id: 123 } as any;
      yourCallMarketsService.loadMarketSelections.and.returnValue(Promise.resolve(([{ selections: [] }])));
      component.selectedGSMarket(player as any, team);
      tick();
      expect(component.playerAvailabe).toHaveBeenCalled();
    }));
  });

  describe('#done', () => {
    it('should call done method single1', () => {
      const player = { name: "A. Lacazette" };
      component.marketSelected = { grouping: {} };
      component.selection = { id: 1, title: "group" } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.showCardPlayersDup = { 'A. Lacazette': false };
      component.done(player as any);
      expect(component.showCardPlayersDup['LACAZETTE']).toBe(false);
    });
    it('should call done method single2', () => {
      const player = { name: "leno" };
      component.marketSelected = { grouping: {} };
      component.selection = { id: 1, title: "group" } as any;
      yourCallMarketsService.selectedSelectionsSet.add(component.selection.id);
      component.selection = { id: 1 } as any;
      component.showCardPlayersDup = { 'leno': false };
      component.done(player as any);
      expect(component.showCardPlayersDup['LENO']).toBe(false);
    });
    it('should call player method no id 1', () => {
      const player = { name: "A. Lacazette" };
      component.marketSelected = { grouping: {} };
      component.selection = { id: 1, title: "group" } as any;
      yourCallMarketsService.selectedSelectionsSet.add(2);
      component.showCardPlayersDup = { 'LACAZETTE': true };
      component.selection = { id: 1 } as any;
      component.done(player as any);
      expect(component.showCardPlayersDup['LACAZETTE']).toBe(true);
    });
    it('should call player method no id 2', () => {
      const player = { name: "Lacazette" };
      component.marketSelected = { grouping: {} };
      component.selection = { id: 1, title: "group" } as any;
      yourCallMarketsService.selectedSelectionsSet.add(2);
      component.showCardPlayersDup = { 'LACAZETTE': true };
      component.selection = { id: 1 } as any;
      component.done(player as any);
      expect(component.showCardPlayersDup['LACAZETTE']).toBe(true);
    });
  });

  describe('getShowCardDup', () => {
    it('backup should return show card player status', () => {
      component.showCardPlayersDup = { 'RONALD': true };
      const result = component.getShowCardDup('. RONALD');
      expect(result).toBe(true);
    });
  });

  describe('getShowCardDup', () => {
    it('backup should return show card player status', () => {
      component.showCardPlayersDup = { 'RONALD': true };
      const result = component.getShowCardDup('RONALD');
      expect(result).toBe(true);
    });
  });


});