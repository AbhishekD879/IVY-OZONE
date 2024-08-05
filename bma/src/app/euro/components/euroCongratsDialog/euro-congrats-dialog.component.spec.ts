import { EuroCongratsDialogComponent } from './euro-congrats-dialog.component';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

describe('EuroCongratsDialogComponent', () => {
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

    component = new EuroCongratsDialogComponent(router, deviceService, windowRef, loc);
  });

  it(`should be instance of 'AbstractDialog'`, () => {
    expect(AbstractDialogComponent).isPrototypeOf(component);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('open', () => {

    it('should display congrats pop-up', () => {
      const openSpy = spyOn(EuroCongratsDialogComponent.prototype['__proto__'], 'open');
      const params = { data: { freeTokenMessage: ['Congratulation'] } };
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(component.freeTokenMessage).toEqual(['Congratulation']);
    });

    it('should not have some data', () => {
      const openSpy = spyOn(EuroCongratsDialogComponent.prototype['__proto__'], 'open');
      const params = undefined;
      AbstractDialogComponent.prototype.setParams(params);
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(component.freeTokenMessage).toBe(undefined);
    });
  });

});
