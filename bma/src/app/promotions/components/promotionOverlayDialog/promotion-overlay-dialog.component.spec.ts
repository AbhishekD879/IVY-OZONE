import { PromotionOverlayDialogComponent } from './promotion-overlay-dialog.component';
import { of } from 'rxjs';

describe('PromotionOverlayDialogComponent', () => {
  let router;
  let windowRef;
  let dialog;
  let domToolsService;
  let component: PromotionOverlayDialogComponent;

  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    dialog = {};
    windowRef = { document: { body: { classList: { add: jasmine.createSpy('add') } } } };
    domToolsService = {
      scrollPageTop: jasmine.createSpy('scrollPageTop')
    };
    component = new PromotionOverlayDialogComponent(
      router,
      domToolsService,
      dialog,
      windowRef
    );
    component.dialog = {
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') },
      close: jasmine.createSpy()
    };
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('#checkRedirect', () => {
    it('should redirect if URL is presents', () => {
      component.checkRedirect({
        target: {
          dataset: {
            routerlink: 'sport/football'
          }
        }
      } as any);

      expect(router.navigateByUrl).toHaveBeenCalledWith('sport/football');
    });

    it('should not redirect if URL is not present', () => {
      component.checkRedirect({
        target: {
          dataset: {
            routerlink: ''
          }
        }
      } as any);

      expect(router.navigateByUrl).not.toHaveBeenCalledWith();
    });
  });

  describe('getPromotion desktop scroll top', () => {
    beforeEach(() => {
      component.params = {
        flag: true,
        getSpPromotionData: jasmine.createSpy('getSpPromotionData').and.returnValue(of([{
          marketLevelFlag: true
        }])),
        decorateLinkAndTrust: jasmine.createSpy('decorateLinkAndTrust').and.returnValue(of([{
          marketLevelFlag: true
        }]))
      };
    });
    it('apply scroll', () => {
      component['device'].isDesktop = true;
      component.getPromotion();
      expect(domToolsService.scrollPageTop).toHaveBeenCalledTimes(1);
      expect(domToolsService.scrollPageTop).toHaveBeenCalledWith(0);
    });
    it('no scroll', () => {
      component['device'].isDesktop = false;
      component.getPromotion();
      expect(domToolsService.scrollPageTop).not.toHaveBeenCalled();
    });

    it('promo uriMedium should be directFileUrl', () => {
      component.params.getSpPromotionData =  jasmine.createSpy('getSpPromotionData').and.returnValue(of([{
        marketLevelFlag: true,
        useDirectFileUrl: true,
        uriMedium: '',
        directFileUrl: 'directFileUrl',
        htmlMarkup: 'htmlMarkup',
        description: 'description'
      }]));
      component['device'].isDesktop = false;
      component['promoHtmlMarkup'] = 'markup';
      component['promoDescription'] = 'markup';
      component.getPromotion();
      expect(component['promo'].uriMedium).toEqual('directFileUrl');
    });

    it('domToolsService scrollPageTop should not be called', () => {

      component.params.getSpPromotionData =  jasmine.createSpy('getSpPromotionData').and.returnValue(of([{
        marketLevelFlag: false,
        useDirectFileUrl: false,
        uriMedium: '',
        directFileUrl: 'directFileUrl'
      }]));

      component['device'].isDesktop = false;
      component.getPromotion();

      expect(domToolsService['scrollPageTop']).not.toHaveBeenCalled();
    });
  });

  describe('open', () => {
    beforeEach(() => {
      component.params = {
        flag: true,
        getSpPromotionData: jasmine.createSpy('getSpPromotionData').and.returnValue(of([{
          marketLevelFlag: true
        }])),
        decorateLinkAndTrust: jasmine.createSpy('decorateLinkAndTrust')
      };
    });
    it('open should call getPromotion', () => {
      component['getPromotion'] = jasmine.createSpy();
      component.open();
      expect(component['getPromotion']).toHaveBeenCalled();
    });
  });

  describe('closeThisDialog', () => {
    it('should call closeDialog', () => {
      component['closeDialog'] = jasmine.createSpy('closeDialog');
      component.closeThisDialog();
      expect(component['dialog'].close).toHaveBeenCalled();
    });
  });
});

