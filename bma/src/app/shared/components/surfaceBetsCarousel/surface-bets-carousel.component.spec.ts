import { SurfaceBetsCarouselComponent } from './surface-bets-carousel.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync } from '@angular/core/testing';

describe('SurfaceBetsCarouselComponent', () => {
  let changeDetRef;
  let pubsub;
  let component: SurfaceBetsCarouselComponent;

  beforeEach(() => {
    changeDetRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    pubsub = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    component = new SurfaceBetsCarouselComponent(changeDetRef, pubsub);
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(pubsub.subscribe).toHaveBeenCalledTimes(1);
    expect(pubsub.subscribe).toHaveBeenCalledWith(component.carouselName, 'OUTCOME_UPDATED', jasmine.any(Function));
  });

  it('ngOnInit', fakeAsync(() => {
    pubsub.subscribe.and.callFake((file, method, cb) => {
      if (method === 'OUTCOME_UPDATED') {
        cb();
      }
    });

    component.ngOnInit();

    expect(changeDetRef.detectChanges).toHaveBeenCalled();
  }));

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsub.unsubscribe).toHaveBeenCalledTimes(1);
    expect(pubsub.unsubscribe).toHaveBeenCalledWith(component.carouselName);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#trackById should return unique id', () => {
    expect(component.trackByCard(1, { id: 31 } as any)).toEqual('1_31');
  });

  it('#isOneCard should return boolean', () => {
    component.module = undefined;
    expect(component['isOneCard']).toBeFalsy();

    component.module = { data: [] } as any;
    expect(component['isOneCard']).toBeFalsy();

    component.module = { data: [{ id: 1 }] } as any;
    expect(component['isOneCard']).toBeTruthy();

    component.module = { data: [{ id: 1 }, { id: 2 }] } as any;
    expect(component['isOneCard']).toBeFalsy();
  });

  describe('ngOnChanges', () => {
    it('should be equal 3', () => {
      component.module = {
        data: [
          { markets: [ 1 ] },
          { markets: [ 1 ] },
          { markets: [ 1 ] },
        ]
      } as any;
      const changes = {
      } as any;
      component.ngOnChanges(changes);
      expect(component.slides).toEqual(3);
    });

    it('should be equal 2', () => {
      component.module = {
        data: [
          { markets: [ 1 ] },
          { markets: [] },
          { markets: [ 1 ] },
        ]
      } as any;
      const changes = {
      } as any;
      component.ngOnChanges(changes);
      expect(component.slides).toEqual(2);
    });
  });
});
