import { of, throwError } from "rxjs";
import { ILottos } from "../lotto.model";
import { LottoListComponent } from "./lotto-list.component";
import { Order } from '@app/client/private/models/order.model';
import { AppConstants } from "@root/app/app.constants";
import { LOTTO_VALUES } from "../lotto.mock";
describe('LottoListComponent', () => {
    let component: LottoListComponent;
    let lotto = LOTTO_VALUES;
    let router;
    let globalLoaderService;
    let apiClientService;
    let dialogService;
    let brandService;
    let snackBar;
    beforeEach((() => {
        dialogService = {
            showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
              yesCallback();
            }),
            showNotificationDialog: jasmine.createSpy('showNotificationDialog')
          };
        brandService = {
            brand: 'bma'
          }
      
          snackBar = {
            open: jasmine.createSpy('open')
          } as any;
           apiClientService = {
            lottosService : jasmine.createSpy('lottosService').and.returnValue({
                putAllByBrand : jasmine.createSpy('putAllByBrand').and.returnValue(of({ body: lotto })),
                findAllByBrand : jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: lotto })),
                remove: jasmine.createSpy('remove').and.returnValue(of({ body: lotto })),
                reorder: jasmine.createSpy('reorder').and.returnValue(of({ body: lotto }))
            })
          }
    
          globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
          };
          router = {
            navigate: jasmine.createSpy('navigate').and.returnValue(Promise.resolve())
          };
        component = new LottoListComponent(
            router,
            apiClientService,
            snackBar,
            dialogService,
            globalLoaderService,
            brandService,
          );
         
    }))
        it('should save lotto', () => {
          component.mainLotto = {
            globalBannerLink: 'test',
            globalBannerText: 'test',
            dayCount: 2,
            lottoConfig: [{id: '1'}, {id: '2'}, {id: '3'}]
          } as any
          component.sendRequest('putAllByBrand');
      
            component.lotto = { 
                createdAt: ''
            } as any;
            const event = 'save';
            component.actionsHandler(event);
            expect(component.lotto).not.toBeNull();
        })
        it('should edit lotto', () => {
          component.actionButtons = {
            extendCollection: jasmine.createSpy('extendCollection')
          } as any; 
          component.mainLotto = {
            globalBannerLink: 'test',
            globalBannerText: 'test',
            dayCount:2,
            lottoConfig: [{id: '1'}, {id: '2'}, {id: '3'}]
          } as any
          component.sendRequest('putAllByBrand');
            component.lotto = { 
                createdAt: '1234'
            } as any;
            const event = 'save';
            component.actionsHandler(event);
            expect(component.lotto).not.toBeNull();
        })
        it('should edit lotto (with error)', () => {
          component.actionButtons = {
            extendCollection: jasmine.createSpy('extendCollection')
          } as any; 
          component.mainLotto = {
            globalBannerLink: 'test',
            globalBannerText: 'test',
            dayCount: 2,
            lottoConfig: [{id: '1'}, {id: '2'}, {id: '3'}]
          } as any
          component.sendRequest('putAllByBrand');
            component.lotto = {
                createdAt: '1234'
              } as any;
            const event = 'save';
            component.actionsHandler(event);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
              title: 'Success',
              message: 'Your changes have been saved'
            });
        })
        it('should revert faq', () => {
            spyOn(component as any, 'loadInitialData');
            const event = 'revert';
            component.actionsHandler(event);
            expect(component['loadInitialData']).toHaveBeenCalled();
        });
        it('should set default condition', () => {
            spyOn(console, 'error');
            const event = 'racdom';
            component.actionsHandler(event);
            expect(component.lotto).toBeUndefined();
        });
    it('should createLotto', () => {
        component.createLotto();
        expect(router.navigate).toHaveBeenCalledWith(['/lotto/add'])
    });
    it('#reorderHandler should save new lotto order', () => {
        const newOrder: Order = { order: ['123'], id: '321' };
        component.reorderHandler(newOrder);
        expect(snackBar.open).toHaveBeenCalledWith(
          `Segments order saved!`,
          'Ok!',
          {
            duration: AppConstants.HIDE_DURATION,
          }
        );
      });
    it('#removeLotto should show dialog and remove coupon', () => {
        const targetCoupon: ILottos = lotto;
    
        component.removeLotto(targetCoupon);
        expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
          title: 'Remove Segment',
          message: `Are You Sure You Want to Remove ${targetCoupon.label} Segment`,
          yesCallback: jasmine.any(Function)
    });
    })
    
    it('#loadinitialdata() should get lotto', () => {
        component.ngOnInit();
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      });
      it('loadInitialData error scenario', () => {
        component.error = 'test';
        apiClientService.lottosService().findAllByBrand.and.returnValue(throwError({ error: '401' }));
        component['loadInitialData']();
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
      });
      it('sendRequest', () => {
        component.actionButtons = {
          extendCollection: jasmine.createSpy('extendCollection')
        } as any; 
        component.mainLotto = {
              globalBannerLink: 'test',
              globalBannerText: 'test',
              dayCount: 2,
              lottoConfig: [{id: '1'}, {id: '2'}, {id: '3'}]
            } as any;
        component.sendRequest('putAllByBrand');
        
      });
      it('sendReuest error scenario', () => {
        component.mainLotto = {
          globalBannerLink: 'test',
          globalBannerText: 'test',
          dayCount:2,
          lottoConfig: [{id: '1'}, {id: '2'}, {id: '3'}]
        } as any;
        component.error = 'test';
        apiClientService.lottosService().putAllByBrand.and.returnValue(throwError({ error: '401' }));
        component.sendRequest('putAllByBrand');
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
      })
      
      it('should return true', () => {
        const response = component.isValidModel({lottoConfig: [{}], globalBannerText: 'test', globalBannerLink: "test12", dayCount: 30} as any);
        expect(response).toBe(true);
      });
      it('should return false', () => {
        const response = component.isValidModel(null);
        expect(response).toBeFalse
      });
})