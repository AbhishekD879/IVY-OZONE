import { of } from 'rxjs';
import { FavouritesAddAllButtonComponent } from '@shared/components/favourites/components/addAllButton/favourites-add-all-button.component';

describe('@FavouritesAddAllButtonComponent', () => {
  let component: FavouritesAddAllButtonComponent;
  let favouritesService;
  let deviceService;
  let pubSubService;
  let promiseMock;

  beforeEach(() => {
    promiseMock = {
      cb: { then: [], catch: [] },
      then: (cb, err) => { promiseMock.cb.then.push(cb); promiseMock.cb.catch.push(err); return promiseMock; },
      catch: err => { promiseMock.cb.then.push(undefined); promiseMock.cb.catch.push(err); return promiseMock; }
    };

    deviceService = {
      isWrapper: false
    };
    favouritesService = {
      showFavourites: jasmine.createSpy('showFavourites'),
      syncToNative: jasmine.createSpy('syncToNative'),
      removeCountListener: jasmine.createSpy('removeCountListener'),
      removeEventsArray: jasmine.createSpy('removeEventsArray').and.returnValue(promiseMock),
      addEventsArray: jasmine.createSpy('addEventsArray').and.returnValue(promiseMock),
      isAllFavourite: jasmine.createSpy('isAllFavourite').and.returnValue(promiseMock),
      countListener: jasmine.createSpy('countListener').and.returnValue(promiseMock)
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: { EVENT_ADDED: 'EVENT_ADDED' }
    };
    spyOn(console, 'warn');

    component = new FavouritesAddAllButtonComponent(
      favouritesService,
      deviceService,
      pubSubService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(component.starSelected).toEqual(false);
    expect(component.clickLock).toEqual(true);
    expect(component.isAvailable).toEqual(false);
  });

  it('#ngOnInit should call #initCounter', () => {
    favouritesService.showFavourites.and.returnValue(of(true));
    component.initCounter = jasmine.createSpy();
    component.ngOnInit();

    expect(component.initCounter).toHaveBeenCalledWith('bsReceipt', true);
    expect(component.isAvailable).toEqual(true);
  });

  it('#ngOnInit should do nothing', () => {
    favouritesService.showFavourites.and.returnValue(of(false));
    component.initCounter = jasmine.createSpy();
    component.ngOnInit();

    expect(component.initCounter).not.toHaveBeenCalled();
    expect(component.isAvailable).toEqual(false);
  });

  it('#ngOnDestroy should call #removeCountListener', () => {
    component.isAvailable = true;
    component.ngOnDestroy();

    expect(favouritesService.removeCountListener).toHaveBeenCalledWith('bsReceipt');
  });

  it('#ngOnDestroy should do nothing', () => {
    component.isAvailable = false;
    component.ngOnDestroy();

    expect(favouritesService.removeCountListener).not.toHaveBeenCalled();
  });


  describe('applyAction', () => {
    let event, eventsArray;
    beforeEach(() => {
      eventsArray = [{ id: 1 }, { id: 2 }] as any;
      event = { stopPropagation: jasmine.createSpy('stopPropagation') };
      component.eventsArray = eventsArray;
    });
    it('should call event.stopPropagation and exit if clickLock is true', () => {
      component.clickLock = true;
      component.applyAction(event as any);
      expect(event.stopPropagation).toHaveBeenCalled();
      expect(favouritesService.isAllFavourite).not.toHaveBeenCalled();
    });
    describe('should call favouritesService.isAllFavourite', () => {
      beforeEach(() => {
        component.clickLock = false;
        component.applyAction(event);
      });

      it('when clickLock is false', () => {
        expect(component.clickLock).toEqual(true);
        expect(event.stopPropagation).not.toHaveBeenCalled();
        expect(favouritesService.isAllFavourite).toHaveBeenCalledWith(eventsArray, 'football');
      });

      describe('and call favouritesService method based on resolved value', () => {
        describe('and publish EVENT_ADDED after it is resolved', () => {
          describe('(call favouritesService.removeEventsArray if true)', () => {
            beforeEach(() => {
              promiseMock.cb.then[0](true);
              expect(favouritesService.removeEventsArray)
                .toHaveBeenCalledWith(eventsArray, { sportName: 'football', fromWhere: 'bsreceipt' });
            });
            it('and not call favouritesService.syncToNative for wrapper', () => {});
            it('and call favouritesService.syncToNative for wrapper', () => deviceService.isWrapper = true);
          });
          describe('(call favouritesService.addEventsArray if false)', () => {
            beforeEach(() => {
              promiseMock.cb.then[0](false);
              expect(favouritesService.addEventsArray)
                .toHaveBeenCalledWith(eventsArray, { sportName: 'football', fromWhere: 'bsreceipt' });
            });
            it('and not call favouritesService.syncToNative for wrapper', () => {});
            it('and call favouritesService.syncToNative for wrapper', () => deviceService.isWrapper = true);
          });
          afterEach(() => {
            promiseMock.cb.then[1]();
            expect(pubSubService.publish).toHaveBeenCalledWith('EVENT_ADDED');
            deviceService.isWrapper ? expect(favouritesService.syncToNative).toHaveBeenCalled() :
              expect(favouritesService.syncToNative).not.toHaveBeenCalled();
          });
        });
      });
    });
  });

  describe('initCounter', () => {
    beforeEach(() => {
      spyOn(component, 'initCounter').and.callThrough();
      spyOn(component, 'initIsAllFavourite');
    });
    it('should call favourtesService.counterListener', () => {
      component.initCounter('listener', true);
      expect(favouritesService.countListener).toHaveBeenCalledWith('listener', true);
    });
    it('should call favourtesService.counterListener with default initRefresh argument', () => {
      component.initCounter('listener');
      expect(favouritesService.countListener).toHaveBeenCalledWith('listener', false);
    });

    it('should continue initialization when favouritesService.countListener promise is resolved', () => {
      component.initCounter('listener', true);
      (component as any).initCounter.and.stub();
      promiseMock.cb.then[0]();
      expect(component.initIsAllFavourite).toHaveBeenCalled();
      expect(component.initCounter).toHaveBeenCalledWith('listener');
    });
    it('should re-init counter when favouritesService.countListener promise is failed', () => {
      component.initCounter('listener', true);
      (component as any).initCounter.and.stub();
      promiseMock.cb.catch[0]('error');
      expect(component.initIsAllFavourite).not.toHaveBeenCalled();
      expect(component.initCounter).toHaveBeenCalledWith('listener');
      expect(console.warn).toHaveBeenCalledWith('error');
    });
  });

  describe('initIsAllFavourite', () => {
    let eventsArray;
    beforeEach(() => {
      eventsArray = [{ id: 1 }, { id: 2 }] as any;
      component.eventsArray = eventsArray;
      component.initIsAllFavourite();
    });
    it('should call favourtesService.isAllFavourite', () => {
      expect(favouritesService.isAllFavourite).toHaveBeenCalledWith(eventsArray, 'football');
    });
    it('should set properties when favouritesService.isAllFavourite promise is resolved', () => {
      expect(component.clickLock).toEqual(true);
      promiseMock.cb.then[0](true);
      expect(component.starSelected).toEqual(true);
      expect(component.clickLock).toEqual(false);
    });
  });
});
