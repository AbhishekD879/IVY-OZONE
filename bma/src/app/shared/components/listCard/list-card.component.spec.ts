import { ListCardComponent } from '@shared/components/listCard/list-card.component';

describe('ListCardComponent', () => {
  let component: ListCardComponent;
  let router, pubSubService, sessionStorageService;

  const event = {
    preventDefault: jasmine.createSpy()
  } as any;

  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy()
    };
    sessionStorageService = {
      set: jasmine.createSpy('set')
    };
    pubSubService = {
      publish: jasmine.createSpy('publish')
    };
    component = new ListCardComponent(router, pubSubService, sessionStorageService);
    component.link = '/horse-racing/featured';
  });

  describe('#gotToPage', () => {

    it('should navigate to page', () => {
      component.gotToPage(event);

      expect(router.navigateByUrl).toHaveBeenCalledWith(component.link);
      expect(event.preventDefault).toHaveBeenCalled();
    });

    it('should emit event to Func is it is exist', () => {
      Object.defineProperty(component.clickFunction, 'observers', { value: [''] });
      spyOn(component.clickFunction, 'emit');
      component.gotToPage(event);

      expect(component.clickFunction.emit).toHaveBeenCalled();
      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(event.preventDefault).toHaveBeenCalled();
    });

    it('should emit isEventOverlay content', () => {
      Object.defineProperty(component.clickFunction, 'observers', { value: [] });
      spyOn(component.clickFunction, 'emit');
      spyOn(component.overlayContent, 'emit');
      component['isEventOverlay'] = true;
      component.gotToPage(event);

      expect(component.overlayContent.emit).toHaveBeenCalled();
      expect(event.preventDefault).toHaveBeenCalled();
    });
  });
});
