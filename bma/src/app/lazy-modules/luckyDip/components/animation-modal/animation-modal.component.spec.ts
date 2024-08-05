import { AnimationModalComponent } from './animation-modal.component';
import { of } from 'rxjs';
import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
describe('AnimationModalComponent', () => {
  let component: AnimationModalComponent, deviceService, windowRefService,
    httpClient, domSanitizer, user, luckyDipCMSService, changeDetectorRef;
  beforeEach(() => {
    httpClient = {
      get: jasmine.createSpy('get').and.returnValue(of(
        {
          body: [],
        }))
    }
    domSanitizer = {
      sanitize: jasmine.createSpy().and.returnValue('test'),
      bypassSecurityTrustHtml: () => { },
      bypassSecurityTrustStyle: () => { },
      bypassSecurityTrustScript: () => { },
      bypassSecurityTrustUrl: () => { },
      bypassSecurityTrustResourceUrl: () => { }
    },
      deviceService = {
        isIos: true,
        isDesktopWindows: false,
        isMobile: false,
        isTablet: false,
        isWrapper: false,
        isDesktop: false
      },
      windowRefService = {
        document: {

          getElementById: jasmine.createSpy().and.returnValue({}),
          body: {
            classList: {
              add: jasmine.createSpy('add'),
              remove: jasmine.createSpy('remove')
            }
          },

        },

      }

    user = {
      currencySymbol: '$'
    };

    luckyDipCMSService = {
      getLuckyDipCMSAnimationData: jasmine.createSpy('getLuckyDipCMSAnimationData').and.returnValue(of('<svg></svg>'))
    }
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    }

    component = new AnimationModalComponent(
      deviceService, windowRefService,
      httpClient, user
    );
  });

  describe('open', () => {

    it('should open popup', () => {
      const openSpy = spyOn(AnimationModalComponent.prototype['__proto__'], 'open');
      const params = {
        data: {
          eventName: ['a vs b', 'c vs d'],
          suspension: ''
        }
      };
      AbstractDialogComponent.prototype.setParams(params);
      component.params = {
        data: {
          value:
          {
            cmsConfig: {
              playerPageBoxImgPath: '',
              playerCardDesc: '',
              potentialReturnsDesc: ''
            },
            playerData: {
              playerName: '',
              odds: '',
              amount: ''
            }

          }
        }
      } as any;


      component.open();
      expect(component.animationData).toBeDefined();

    });
  });
  describe('updateanimation content', () => {

    it('should  removeattribute', () => {
      const d = {
        cmsConfig: {
          playerPageBoxImgPath: '',
          playerCardDesc: '',
          potentialReturnsDesc: '',
          gotItCTAButton: ''
        },
        playerData: {
          playerName: '',
          odds: '',
          amount: ''
        },
        svg: '<svg></svg'
      }

      const element = document.createElement('span');
      element.id = 'path'
      component.animationData = d;
      element.querySelector = jasmine.createSpy().and.returnValue(element);
      element.removeAttribute = jasmine.createSpy();
      spyOn(component, 'addLabelText');
      windowRefService.document.getElementById = jasmine.createSpy().and.returnValue(element);
      component.updateAnimationContent();
      expect(element.removeAttribute).toHaveBeenCalled();
    })
  })

  describe('addLabelText', () => {
    const bgPath = {
      getBBox: jasmine.createSpy('getBBox').and.returnValue({
        X: 10, y: 10, width: 10, height: 10
      }),
      after: jasmine.createSpy('after'),
      namespaceURI: ''
    } as any;
    it('should call after ', () => {
      component.addLabelText(bgPath, 'c1', '10');
      expect(bgPath.after).toHaveBeenCalled();
    })

  })
  describe('closeAnimationDialog', () => {
    it('should call openBetReceipt', () => {
      component.params.data.openBetReceipt = jasmine.createSpy('openBetReceipt');
      component.closeAnimationDialog()
      expect(component.params.data.openBetReceipt).toHaveBeenCalled();
    })
  })

  it('ngAfterViewInit', done => {
    const spyUpdateAnimationContent = spyOn(component, 'updateAnimationContent');
    component.ngAfterViewInit();
    // luckyDipCMSService.getLuckyDipCMSAnimationData().subscribe()
    setTimeout(() => {
      expect(spyUpdateAnimationContent).toHaveBeenCalled()
      done();
    }, 200);
  });

  describe('isIOSsafari', () => {
    it('should call isIOSsafari', () => {
      deviceService.isIos = true;
      deviceService.isWrapper = true;
      deviceService.isSafari = true;

      component.isIOSsafari()
      expect(component.isIOSsafari()).toBeFalsy();
    })
    it('should call isIOSsafari', () => {
      deviceService.isIos = false;
      deviceService.isWrapper = false;
      deviceService.isSafari = true;
      component.isIOSsafari()
      expect(component.isIOSsafari()).toBeFalsy();
    })
    it('should call isIOSsafari', () => {
      deviceService.isIos = false;
      deviceService.isWrapper = true;
      deviceService.isSafari = false;
      component.isIOSsafari()
      expect(component.isIOSsafari()).toBeFalsy();
    })
    it('should call isIOSsafari', () => {
      deviceService.isIos = true;
      deviceService.isWrapper = false;
      deviceService.isSafari = true;
      component.isIOSsafari()
      expect(component.isIOSsafari()).toBeTruthy();
    })
  })
});
