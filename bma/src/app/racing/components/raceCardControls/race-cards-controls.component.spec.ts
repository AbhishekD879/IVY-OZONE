import { RaceCardsControlsComponent } from '@racing/components/raceCardControls/race-cards-controls.component';

describe('RaceCardsControlsComponent', () => {
  let component: RaceCardsControlsComponent;
  let pubSubService;
  let gtmService;
  let locale;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('getString').and.callFake(value => value)
    } as any;
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SORT_BY_OPTION: 'SORT_BY_OPTION'
      }
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    component = new RaceCardsControlsComponent (pubSubService, gtmService, locale);
    component.market = {
      outcomes: []
    } as any;
  });

  describe('#ngOnInit', () => {
    it('ngOnInit', () => {
      spyOn(component.toggleShowOptions, 'emit');
      const marketData = {
        outcomes: [
          {
            racingFormOutcome: {
              id: '1233'
            },
            timeformData: {
              id: '1245'
            }
          }
        ]
      } as any;
      component.market = marketData;
      component.ngOnInit();

      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('RaceCardsControlsComponent', 'SORT_BY_OPTION', jasmine.any(Function));
    });

    it('ngOninit when eventId present', () => {
      pubSubService.subscribe.and.callFake((a, b, cb) => cb && cb());
      component.eventEntityId = '123124';
      spyOn(component.toggleShowOptions, 'emit');
      const marketData = {
        outcomes: [
          {
            racingFormOutcome: null,
            timeformData: {
              id: '1245'
            }
          }
        ]
      } as any;
      component.market = marketData;
      component.ngOnInit();

      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('RaceCardsControlsComponent', 'SORT_BY_OPTION123124', jasmine.any(Function));
    });
  });

  describe('ngOnChanges', () => {
    it('ngOnChanges market', () => {
      const changes = { market: true } as any;
      component.toggleShowOption = jasmine.createSpy('toggleShowOption');

      component.ngOnChanges(changes);
      expect(component.toggleShowOption).toHaveBeenCalled();
    });

    it('ngOnChanges isInfoHidden true', () => {
      const changes = { isInfoHidden: {
        currentValue: true
      } } as any;

      component.ngOnChanges(changes);
      expect(component.toggleInfoText).toEqual('racing.showInfo');
      expect(component.showMore).toEqual(false);
    });

    it('ngOnChanges market (Case: changes.isInfoHidden.currentValue = undefined)', () => {
      const changes = {
        isInfoHidden: {
          currentValue: undefined
        }
      } as any;
      component.ngOnChanges(changes);
      expect(component.showMore).toBeFalsy();
    });

    it('ngOnChanges market (Case: changes.isInfoHidden.currentValue.info = true)', () => {
      const changes = {
        isInfoHidden: {
          currentValue: {
            info: true
          }
        }
      } as any;
      component.ngOnChanges(changes);
      expect(component.showMore).toBe(true);
    });

    it(`showMore should be false`, () => {
      component.showMore = true;
      const changes = {
        isInfoHidden: {
          currentValue: {
            info: false
          }
        }
      } as any;

      component.ngOnChanges(changes);

      expect(component.showMore).toEqual(false);
    });
  });

  it('should unsubscribe from pubSub', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('RaceCardsControlsComponent');
  });
  describe('#ngOnInit', () => {
    it('ngOnInit', () => {
      spyOn(component.toggleShowOptions, 'emit');
      component.ngOnInit();
      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('RaceCardsControlsComponent', 'SORT_BY_OPTION', jasmine.any(Function));
    });
    it('ngOninit when eventId present', () => {
      pubSubService.subscribe.and.callFake((a, b, cb) => cb && cb());
      component.eventEntityId = '123124';
      spyOn(component.toggleShowOptions, 'emit');
      component.ngOnInit();
      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('RaceCardsControlsComponent', 'SORT_BY_OPTION123124', jasmine.any(Function));
    });
    it('toggleShowOption', () => {
      spyOn(component.toggleShowOptions, 'emit');
      component.showMore = true;
      component.toggleShowOption();
      expect(component.showMore).toEqual(false);
      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
    });
    it('ngOnChanges isInfoHidden true', () => {
      const changes = {
        isInfoHiddeninfo: {
          currentValue: {
            info:true
          }
        }
      } as any;
      component.ngOnChanges(changes);
      expect('racing.hideInfo').toEqual('racing.hideInfo');
      expect(component.showMore).toEqual(false);
    });
    it('ngOnChanges isInfoHidden false', () => {
      const changes = { isInfoHidden: {
        currentValue: {
          info:false
        }
      } } as any;
      component.ngOnChanges(changes);
      expect(component.toggleInfoText).toEqual('racing.showInfo');
      expect(component.showMore).toEqual(false);
    });
  });
  describe('#toggleShowOption', () => {
    it('Should hide, if value is not given', () => {
      spyOn(component.toggleShowOptions, 'emit');
      component.showMore = true;
      component.toggleShowOption();
      expect(component.showMore).toEqual(false);
      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
    });
    it('should show, if value is given', () => {
      spyOn(component.toggleShowOptions, 'emit');
      component.showMore = true;
      component.toggleShowOption(true);
      expect(component.showMore).toEqual(true);
      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(true);
    });
  });
  it('toggleShowOptionChange', () => {
    spyOn(component.toggleShowOptions, 'emit');
    spyOn(component.toggleShowOptionsGATracking, 'emit');
    component.showMore = true;
    component.toggleShowOptionChange(undefined);

    expect(component.showMore).toEqual(false);
    expect(component.toggleShowOptionsGATracking.emit).toHaveBeenCalledWith(false);
  });
});
