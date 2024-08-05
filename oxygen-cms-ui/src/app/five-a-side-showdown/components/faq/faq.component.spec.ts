import { of, throwError } from 'rxjs';
import { FaqComponent } from '@app/five-a-side-showdown/components/faq/faq.component';
import { FAQS } from '@app/five-a-side-showdown/components/faq/faq.component.mock';

describe('FaqComponent', () => {
  let component: FaqComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let errorService;
  let router;
  let snackBar;
  let faqService;

  beforeEach(() => {
    errorService = {
      emitError: jasmine.createSpy('emitError')
    }
    faqService = {
      postNewOrder: jasmine.createSpy('postNewOrder').and.returnValue(of({})),
      getFAQs: jasmine.createSpy('getFAQs').and.returnValue(of({
        body: FAQS
      })),
      removeFAQForId: jasmine.createSpy('removeFAQForId').and.returnValue(of({}))
    };
    apiClientService = {
      faqService: () => faqService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and.callFake((dialogComponent, {
        width, title, yesOption, noOption, yesCallback
      }) => {
        yesCallback(FAQS[0]);
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/racing-edp-markets/1'
    };
    snackBar = {
      open: jasmine.createSpy('open')
    } as any;
    component = new FaqComponent(apiClientService, globalLoaderService, errorService,
      router, snackBar, dialogService)
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should fetch all the faqs', () => {
      component.ngOnInit();
      expect(component.faqs).not.toBe(null);
      expect(component.isLoading).toBe(false);
    });
    it('should not fetch faqs if the service throws error', () => {
      faqService.getFAQs.and.returnValue(throwError({error: '401'}));
      component.ngOnInit();
      expect(component.faqs.length).toBe(0);
      expect(component.isLoading).toBe(false);
    });
  });

  it('should createFAQ', () => {
    component.createFAQ();
    expect(router.navigate).toHaveBeenCalledWith(['/five-a-side-showdown/faq/add-edit'])
  });

  it('#reorderHandler should save new FAQ order', () => {
    const newOrder = { order: ['123'], id: '321' };
    component.reorderHandler(newOrder);
    expect(snackBar.open).toHaveBeenCalledWith(
      `New FAQ Order Saved!!`,
      'OK!',
      {
        duration: 3000,
      }
    );
  });

  it('should remove FAQ', () => {
    const mockFAQ = FAQS[0] as any;
    component.faqs = FAQS;
    const length = component.faqs.length;
    component.removeFAQ(mockFAQ);
    expect(component.faqs.length).toBe(length - 1);
  });
});
