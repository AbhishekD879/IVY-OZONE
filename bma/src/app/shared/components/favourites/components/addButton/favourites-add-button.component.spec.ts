import { FavouritesAddButtonComponent } from './favourites-add-button.component';
import { of } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('@FavouritesAddButtonComponent', () => {
  let component: FavouritesAddButtonComponent;
  let pubSubService;
  let favouritesService;
  let title;
  let promiseMock;
  let cdRef;

  beforeEach(() => {
    promiseMock = {
      cb: { then: [], catch: [] },
      then: (cb, err) => { promiseMock.cb.then.push(cb); promiseMock.cb.catch.push(err); return promiseMock; },
      catch: err => { promiseMock.cb.then.push(undefined); promiseMock.cb.catch.push(err); return promiseMock; }
    };

    pubSubService = {
      pubSubCbMap: {},
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((name, listeners, handler) =>
        listeners.forEach(event => pubSubService.pubSubCbMap[event] = handler)),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    favouritesService = {
      deRegisterListener: jasmine.createSpy('deRegisterListener'),
      add: jasmine.createSpy('add').and.returnValue(promiseMock),
      registerListener: jasmine.createSpy('registerListener').and.returnValue(promiseMock),
      showFavourites: jasmine.createSpy('showFavourites').and.returnValue(of(true)),
      isFavourite: jasmine.createSpy('isFavourite').and.returnValue(promiseMock)
    };

    cdRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    }

    component = new FavouritesAddButtonComponent(
      favouritesService,
      pubSubService,
      cdRef
    );
    component.event = { id: '123' } as any;
    component.id = '456';
    component.config = { config: 'data' };
    component.sportName = 'sportName';
    title = 'favourites-button-456-123';

    spyOn(console, 'warn');
  });

  it('should set properties', () => {
    expect(component.isDisabled).toEqual(true);
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      spyOn(component, 'initListener').and.callThrough();
      spyOn(component as any, 'checkIsFavourite').and.callThrough();
    });
    it('should set title property', () => {
      component.ngOnInit();
      expect(component.title).toEqual(title);
    });

    it('should call favouritesService.showFavourites', () => {
      component.ngOnInit();
      expect(favouritesService.showFavourites).toHaveBeenCalled();
    });

    describe('if favouritesService.showFavourites resolved as true', () => {
      beforeEach(() => {
        spyOn(Math, 'random').and.returnValue(0.123456789);
        component.ngOnInit();
      });
      it('should set isDisabled property to false', () => {
        expect(component.isDisabled).toEqual(false);
      });
      it('should set id property', () => {
        expect(component.id).toEqual('4fzzzxjylrx');
      });
      it('should call initListener', () => {
        expect(component.initListener).toHaveBeenCalled();
      });
      it('should call checkIsFavourite', () => {
        expect((component as any).checkIsFavourite).toHaveBeenCalled();
      });
    });
    describe('if favouritesService.showFavourites resolved as false', () => {
      beforeEach(() => {
        favouritesService.showFavourites.and.returnValue(of(false));
        component.ngOnInit();
      });
      it('should set isDisabled property to true', () => {
        expect(component.isDisabled).toEqual(true);
      });
      it('should not update id property', () => {
        expect(component.id).toEqual('456');
      });
      it('should not call initListener', () => {
        expect(component.initListener).not.toHaveBeenCalled();
      });
      it('should not call checkIsFavourite', () => {
        expect((component as any).checkIsFavourite).not.toHaveBeenCalled();
      });
    });
  });

  describe('ngOnDestroy', () => {
    beforeEach(() => { component.title = title; });
    it('should unsubscribe from PubSub and deRegisterListener of FavouritesService if not disabled', () => {
      component.isDisabled = false;
      component.ngOnDestroy();
      expect(favouritesService.deRegisterListener).toHaveBeenCalledWith({ id: '123' } as any, '456');
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(title);
    });
    it('should do nothing if disabled', () => {
      component.isDisabled = true;
      component.ngOnDestroy();
      expect(favouritesService.deRegisterListener).not.toHaveBeenCalled();
      expect(pubSubService.unsubscribe).not.toHaveBeenCalled();
    });
  });

  describe('initListener', () => {
    beforeEach(() => {
      component.title = title;
      spyOn(component, 'initListener').and.callThrough();
      spyOn(component, 'setClickLock').and.callThrough();
      spyOn(component as any, 'checkIsFavourite').and.callThrough();
    });

    describe('should subscribe to PubSub', () => {
      beforeEach(() => {
        component.initListener();
        expect(pubSubService.subscribe).toHaveBeenCalledWith(title, ['SUCCESSFUL_LOGIN'], jasmine.any(Function));
        expect(pubSubService.subscribe).toHaveBeenCalledWith(title, ['SESSION_LOGOUT'], jasmine.any(Function));
      });
      it('SUCCESSFUL_LOGIN and execute checkIsFavourite in subscription', () => {
        pubSubService.pubSubCbMap['SUCCESSFUL_LOGIN']();
        expect((component as any).checkIsFavourite).toHaveBeenCalled();
      });
      it('SESSION_LOGOUT and set isFavourite to false in subscription', () => {
        component.isFavourite = undefined;
        pubSubService.pubSubCbMap['SESSION_LOGOUT']();
        expect(component.isFavourite).toEqual(false);
      });
    });

    describe('should call FavouritesService.registerListener', () => {
      describe('should pass the promise result to setClickLock, and call initListener', () => {
        beforeEach(() => {
          component.initListener();
          (component as any).initListener.and.stub();
        });
        it('and update isFavourite property, when promise is resolved with is "added"', () => {
          promiseMock.cb.then[0]('added');
          expect((component as any).setClickLock).toHaveBeenCalledWith('added');
          expect(component.isFavourite).toEqual(true);
        });
        it('and update isFavourite property, when promise is resolved with is not "added"', () => {
          promiseMock.cb.then[0]('not-added');
          expect((component as any).setClickLock).toHaveBeenCalledWith('not-added');
          expect(component.isFavourite).toEqual(false);
        });
        it('and handle error when promise is rejected', () => {
          promiseMock.cb.catch[0]('error message');
          expect((component as any).setClickLock).toHaveBeenCalledWith('error');
          expect(console.warn).toHaveBeenCalledWith('error message');
        });
        afterEach(() => {
          expect(component.initListener).toHaveBeenCalledTimes(2);
        });
      });
      afterEach(() => {
        expect(favouritesService.registerListener).toHaveBeenCalledWith({ id: '123' }, '456');
      });
    });
  });

  describe('setClickLock', () => {
    it('should set clickLock property to true', () => {
      component.setClickLock('pending');
      expect(component.clickLock).toEqual(true);
    });
    it('should set clickLock property to false', () => {
      component.setClickLock('not-pending');
      expect(component.clickLock).toEqual(false);
    });
  });

  describe('add', () => {
    beforeEach(() => {
      component.clickLock = true;
    });
    it('should exit if clickLock is true', () => {
      component.add();
      expect(favouritesService.add).not.toHaveBeenCalled();
    });
    describe('if clickLock is false', () => {
      beforeEach(() => {
        component.clickLock = false;
      });
      it('should call favouritesService.add and do nothing on success', () => {
        component.add();
      });
      it('should call favouritesService.add and handle errors', () => {
        component.add();
        promiseMock.cb.catch[0]('error');
        expect(console.warn).toHaveBeenCalledWith('error');
      });
      afterEach(() => {
        expect(favouritesService.add).toHaveBeenCalledWith({ id: '123' }, 'sportName', { config: 'data' });
      });
    });
  });

  describe('checkIsFavourite should call favouritesService.isFavourite', () => {
    it('and update isFavourite property on success', () => {
      (component as any).checkIsFavourite();
      promiseMock.cb.then[0]();
      expect(component.isFavourite).toEqual(true);
    });
    it('and handle error (no action)', () => {
      (component as any).checkIsFavourite();
      promiseMock.cb.catch[1]();
      expect(component.isFavourite).toEqual(undefined);
    });
    afterEach(() => {
      expect(favouritesService.isFavourite).toHaveBeenCalledWith({ id: '123' }, 'sportName');
    });
  });

  afterAll(() => {
    promiseMock = null;
  });
});
