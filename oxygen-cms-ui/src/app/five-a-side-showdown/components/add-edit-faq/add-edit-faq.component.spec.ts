import { of, throwError } from 'rxjs';
import { FAQS } from '@app/five-a-side-showdown/components/faq/faq.component.mock';
import {
  AddEditFaqComponent
} from '@app/five-a-side-showdown/components/add-edit-faq/add-edit-faq.component';

describe('AddEditFaqComponent', () => {
  let component: AddEditFaqComponent;
  let activatedRoute;
  let globalLoaderService;
  let apiClientService;
  let router;
  let dialogService;
  let faqService;
  let brandService;
  let errorService;

  beforeEach(() => {
    faqService = {
      createFAQ: jasmine.createSpy('createFAQ').and.returnValue(of({
        body: FAQS[1]
      })),
      removeFAQForId: jasmine.createSpy('removeFAQForId').and.returnValue(of({
        id: 1
      })),
      getFAQForId: jasmine.createSpy('getFAQForId').and.returnValue(of({
        body: FAQS[0]
      })),
      editFAQById: jasmine.createSpy('editFAQById').and.returnValue(of({
        body: FAQS[0]
      }))
    };
    brandService = { brand: 'bma' };
    activatedRoute = {
      snapshot: {
        params: {
          id: 'abc123'
        }
      }
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    apiClientService = {
      faqService: () => faqService
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new AddEditFaqComponent(brandService, activatedRoute, globalLoaderService,
      apiClientService, router, dialogService, errorService);
    component.actionButtons = {
        extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should handle create scenario', () => {
      activatedRoute.snapshot.params.id = null;
      component.ngOnInit()
      expect(component.faq.brand).toEqual('bma');
    });
    it('should handle edit scenario', () => {
      spyOn(component as any, 'loadInitData');
      component.ngOnInit()
      expect(component['loadInitData']).toHaveBeenCalled();
    });
  });

  describe('#updateBlurb', () => {
    it('should update question field when not empty', () => {
      component.faq = {
        question: null
      } as any;
      component['updateBlurb']('new Text', 'question');
      expect(component.faq.question).toEqual('new Text');
    });
    it('should not update question field when empty', () => {
      component.faq = {
        question: null
      } as any;
      component['updateBlurb'](null, 'question');
      expect(component.faq.question).toBeNull();
    });
  });

  describe('#actionsHandler', () => {
    it('should remove faq', () => {
      spyOn(component as any, 'removeFAQ');
      const event = 'remove';
      component.faq = {
        id: 'abc123'
      } as any;
      component.actionsHandler(event);
      expect(component['removeFAQ']).toHaveBeenCalled();
    });
    it('should save faq', () => {
      component.isEdit = false;
      spyOn(component as any, 'saveFAQ');
      const event = 'save';
      component.actionsHandler(event);
      expect(component['saveFAQ']).toHaveBeenCalled();
    });
    it('should edit faq', () => {
      component.isEdit = true;
      spyOn(component as any, 'editFAQ');
      const event = 'save';
      component.actionsHandler(event);
      expect(component['editFAQ']).toHaveBeenCalled();
    });
    it('should revert faq', () => {
      spyOn(component as any, 'revertChanges');
      const event = 'revert';
      component.actionsHandler(event);
      expect(component['revertChanges']).toHaveBeenCalled();
    });
    it('should set default condition', () => {
      spyOn(console, 'error');
      const event = 'racdom';
      component.actionsHandler(event);
      expect(component.faq).toBeUndefined();
    });
  });

  describe('#saveFAQ', () => {
    it('should save faq', () => {
      component['saveFAQ']();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    });
    it('should not save faq, if the service throws error', () => {
      faqService.createFAQ.and.returnValue(throwError({error: '401'}));
      component['saveFAQ']();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  describe('#revertChanges', () => {
    it('should revert changes in edit scenrio', () => {
      spyOn(component as any, 'loadInitData');
      component.isEdit = true;
      component['revertChanges']();
      expect(component['loadInitData']).toHaveBeenCalled();
    });
    it('should revert changes in non edit scenrio', () => {
      spyOn(component as any, 'loadInitData');
      component.isEdit = false;
      component['revertChanges']();
      expect(component.faq.brand).toEqual('bma');
    });
  });

  describe('#editFAQ', () => {
    it('should edit faq', () => {
      component['editFAQ']();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    });
    it('should not edit faq, if the service throws error', () => {
      faqService.editFAQById.and.returnValue(throwError({error: '401'}));
      component['editFAQ']();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  describe('#removeFAQ', () => {
    it('should remove faq', () => {
      component.faq = {
        id: 1
      } as any;
      component['removeFAQ']();
      expect(router.navigate).toHaveBeenCalledWith(['/five-a-side-showdown/faq']);
    });
    it('should not remove faq, if the service throws error', () => {
      component.faq = {
        id: 1
      } as any;
      faqService.removeFAQForId.and.returnValue(throwError({error: '401'}));
      component['removeFAQ']();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  describe('#loadInitData', () => {
    it('should fetch details by id', () => {
      component['loadInitData']();
      expect(component.faq).not.toBeNull();
      expect(component.isLoading).toBeFalse();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
    it('should not fetch details, if the service throws error', () => {
      faqService.getFAQForId.and.returnValue(throwError({error: '401'}));
      component['loadInitData']();
      expect(component.faq).toBeUndefined();
      expect(component.isLoading).toBeFalse();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });
});
