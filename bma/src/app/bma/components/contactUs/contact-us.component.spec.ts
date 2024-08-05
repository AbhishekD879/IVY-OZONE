import { of as observableOf, throwError } from 'rxjs';
import { ContactUsComponent } from './contact-us.component';

describe('#ContactUsComponent', () => {
  let staticDataMock;
  let component: ContactUsComponent;
  let cmsService;

  beforeEach(() => {
    staticDataMock = {
      title_brand: '',
      uri: '',
      title: '',
      lang: '',
      enabled: true,
      htmlMarkup: '',
    };

    cmsService = {
      getContactUs: jasmine.createSpy('cmsService.getContactUs')
    } as any;

    component = new ContactUsComponent(
      cmsService
    );
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should get content', () => {
      cmsService.getContactUs.and.returnValue(observableOf(staticDataMock));
      component.ngOnInit();
      expect(component.content).toEqual(<any>staticDataMock);
    });

    it('should throw error', () => {
      component.showError = jasmine.createSpy('showError');
      cmsService.getContactUs.and.returnValue(throwError('error'));
      component.ngOnInit();
      expect(component.showError).toHaveBeenCalled();
    });
  });
});

