import { EuroDialogComponent } from './euro-dialog.component';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

describe('EuroDialogComponent', () => {
  let component, deviceService, windowRef, router, loc;

  beforeEach(() => {
    deviceService = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('classList.add'),
            remove: jasmine.createSpy('classList.remove')
          }
        }
      },
      nativeWindow: {
        location: {
          href: '/promotions'
        }
      }
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };

    loc = {
      onPopState: jasmine.createSpy('onPopState')
    };

    component = new EuroDialogComponent(router, deviceService, windowRef, loc);
  });

  it(`should be instance of 'AbstractDialogComponent'`, () => {
    expect(AbstractDialogComponent).isPrototypeOf(component);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('open', () => {
    it('should get data', () => {
      const openSpy = spyOn(EuroDialogComponent.prototype['__proto__'], 'open');
      const params = {data : { howItWorks: `<p>Place one qulaifying Bet</p>
      <p>Do something else</p><p></p><p>Do one more thing again to see changes</p>`}};
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(windowRef.document.body.classList.add).toHaveBeenCalledWith('howItWorks-modal-open');
    });
  });

  describe('openPromotions', () => {
    it(`should call 'openPromotion`, () => {
      const linkDestination = '/promotions';
      const params = {data : { howItWorksLink: '/promotions' }};
      AbstractDialogComponent.prototype.setParams(params);
      component.openPromotions();
      expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('howItWorks-modal-open');
    });
  });

});
