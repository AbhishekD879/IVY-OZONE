import { of } from 'rxjs';
import { FavouritesCounterComponent } from '@shared/components/favourites/components/favouritesCounter/favourites-counter.component';

describe('@FavouritesCounterComponent', () => {
  let component: FavouritesCounterComponent;
  let favouritesService;
  let promiseMock;
  let windowRefService;

  beforeEach(() => {
    windowRefService = {
      document: {
        getElementById: jasmine.createSpy('getElementById').and.returnValue({
          classList: {
            add: jasmine.createSpy().and.returnValue('fav-icon-active'),
            remove: jasmine.createSpy().and.returnValue('fav-icon-inactive')
          }
        })
      }
    };
    promiseMock = {
      cb: { then: [], catch: [] },
      then: (cb, err) => { promiseMock.cb.then.push(cb); promiseMock.cb.catch.push(err); return promiseMock; },
      catch: err => { promiseMock.cb.then.push(undefined); promiseMock.cb.catch.push(err); return promiseMock; }
    };

    favouritesService = {
      showFavourites: jasmine.createSpy('showFavourites').and.returnValue(of(true)),
      removeCountListener: jasmine.createSpy('removeCountListener'),
      countListener: jasmine.createSpy('countListener').and.returnValue(promiseMock)
    };

    spyOn(console, 'warn');
    component = new FavouritesCounterComponent(favouritesService, windowRefService);
    component.listenerName = 'footballInPlay';
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(component.isAvailable).toEqual(false);
  });

  it('should call favIconDown', () => {
    component.iconClicked();
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('icon');
  })

  it('should call favIconUp', () => {
    component.iconClickRemove();
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('icon');
  })

  describe('ngOnInit', () => {
    beforeEach(() => {
      spyOn(component, 'initCounter').and.callThrough();
    });
    it('#ngOnInit should call #initCounter', () => {
      component.ngOnInit();
      expect(component.isAvailable).toEqual(true);
      expect(component.initCounter).toHaveBeenCalledWith('footballInPlay', true);

    });

    it('#ngOnInit should only set isAvailable to false', () => {
      component.isAvailable = true;
      favouritesService.showFavourites.and.returnValue(of(false));
      component.ngOnInit();
      expect(component.isAvailable).toEqual(false);
      expect(component.initCounter).not.toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should call favouritesService.removeCountListener', () => {
      component.isAvailable = true;
      component.ngOnDestroy();
      expect(favouritesService.removeCountListener).toHaveBeenCalledWith('footballInPlay');
    });
      it('should call favouritesService.removeCountListener', () => {
      component.isAvailable = false;
      component.ngOnDestroy();
      expect(favouritesService.removeCountListener).not.toHaveBeenCalled();
    });
  });

  describe('initCounter', () => {
    it('should call favouritesService.countListener', () => {
      component.initCounter('listenerName', true);
      expect(favouritesService.countListener).toHaveBeenCalledWith('listenerName', true);
    });
    it('should call favouritesService.countListener (default argument)', () => {
      component.initCounter('listenerName');
      expect(favouritesService.countListener).toHaveBeenCalledWith('listenerName', false);
    });

    describe('when favouritesService.countListener', () => {
      beforeEach(() => {
        component.initCounter('listenerName');
        spyOn(component, 'initCounter').and.stub();
      });
      it('is resolved, should update count and re-call initCounter', () => {
        promiseMock.cb.then[0](12);
        expect(component.count).toEqual(12);
      });

      it('is rejected, should handle error and re-call initCounter', () => {
        promiseMock.cb.catch[0]('error');
        expect(console.warn).toHaveBeenCalledWith('error');
      });
      afterEach(() => {
        expect((component as any).initCounter).toHaveBeenCalledWith('listenerName');
      });
    });
  });
});
