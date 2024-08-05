import { LadbrokesRaceCardsControlsComponent } from '@ladbrokesMobile/racing/components/race-cards-controls/race-cards-controls.component';

describe('LadbrokesRaceCardsControlsComponent', () => {
  let component: LadbrokesRaceCardsControlsComponent;
  let pubSubService;

  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SORT_BY_OPTION: 'SORT_BY_OPTION'
      }
    };

    component = new LadbrokesRaceCardsControlsComponent(pubSubService);
    component.market = {
      outcomes: []
    } as any;
  });

  describe('#ngOnInit', () => {
    it('ngOnInit', () => {
      spyOn(component.toggleShowOptions, 'emit');
      component.ngOnInit();

      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('LadbrokesRaceCardsControlsComponent', 'SORT_BY_OPTION', jasmine.any(Function));
    });

    it('ngOninit when eventId present', () => {
      pubSubService.subscribe.and.callFake((a, b, cb) => cb && cb());
      component.eventEntityId = '123124';
      spyOn(component.toggleShowOptions, 'emit');
      component.ngOnInit();

      expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('LadbrokesRaceCardsControlsComponent', 'SORT_BY_OPTION123124', jasmine.any(Function));
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
        currentValue: { info: true }
      } } as any;

      component.ngOnChanges(changes);
      expect(component.toggleInfoText).toEqual('Hide Info');
      expect(component.showMore).toEqual(true);
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

    it('ngOnChanges isInfoHidden false', () => {
      const changes = {
        isInfoHidden: {
          currentValue: {
            info: false
          }
        }
      } as any;

      component.ngOnChanges(changes);
      expect(component.toggleInfoText).toEqual('Show Info');
      expect(component.showMore).toEqual(false);
    });

  });


  it('toggleShowOption', () => {
    spyOn(component.toggleShowOptions, 'emit');
    component.showMore = true;
    component.toggleShowOption();

    expect(component.showMore).toEqual(false);
    expect(component.toggleShowOptions.emit).toHaveBeenCalledWith(false);
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
