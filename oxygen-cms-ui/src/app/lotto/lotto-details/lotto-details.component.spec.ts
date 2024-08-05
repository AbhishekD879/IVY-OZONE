import {  of, throwError } from "rxjs";
import { LottoDetailsComponent } from "./lotto-details.component";
import { ILottos } from "../lotto.model";
import { LOTTO_VALUES } from "../lotto.mock";
describe('LottoDetailsComponent', () => {
    let component: LottoDetailsComponent;
    let lotto = LOTTO_VALUES;
  let brandService;
  let snackBar;
  let globalLoaderService;
  let apiClientService;
  let dialogService;
  let router;
  let route;
    beforeEach((() => {
                dialogService = {
                showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                    yesCallback();
                }),
                
                showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message }) => { }),
                };
        
                brandService = {
                    isIMActive: jasmine.createSpy('isIMActive'),
                    brand: 'bma'
                };
                snackBar = {
                  open: jasmine.createSpy('open')
              };
                globalLoaderService = {
                    showLoader: jasmine.createSpy('showLoader'),
                    hideLoader: jasmine.createSpy('hideLoader')
                };
                route = {
                  params: {
                    subscribe: jasmine.createSpy('subscribe').and.callFake((cb) => cb({ id: '1' }))
                  }
                };
                
                apiClientService = {
                    lottosService : jasmine.createSpy('lottosService').and.returnValue({
                        getLottery: jasmine.createSpy('getLottery').and.returnValue(of({body: lotto})),
                        saveLotto: jasmine.createSpy('saveLotto').and.returnValue(of({body: lotto})),
                        updateLottoDetails: jasmine.createSpy('updateLottoDetails').and.returnValue(of({})),
                        remove: jasmine.createSpy('remove').and.returnValue(of({})),
                        uploadSvg: jasmine.createSpy('uploadSvg').and.returnValue(of({body: lotto})),
                        putAllByBrand: jasmine.createSpy('putAllByBrand').and.returnValue(of({body: lotto}))
                    }),
                }
                router = {
                  navigate: jasmine.createSpy('navigate').and.returnValue(Promise.resolve())
                };
               
                     
        component = new LottoDetailsComponent(
            brandService,
            globalLoaderService,
            apiClientService,
            snackBar,
            dialogService,
            route,
            router
        );
        component.actionButtons = {
          extendCollection: jasmine.createSpy('extendCollection')
        } as any;
    }))
    describe('actionHandler', () => {
        it('should save lotto', () => {
            component.lotto = { 
                createdAt: ''
            } as any;
            const event = 'save';
            component.actionsHandler(event);
            expect(component.lotto).not.toBeNull();
        });
        it('should edit lotto', () => {
            component.lotto = { 
                createdAt: '1234'
            } as any;
            const event = 'save';
            component.actionsHandler(event);
            expect(component.lotto).not.toBeNull();
        });
        it('should edit lotto (with error)', () => {
            component.lotto = {
                createdAt: '1234'
              } as any;
            const event = 'save';
            component.actionsHandler(event);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
              title: 'Success',
              message: 'Your changes have been saved'
            });
        });
        it('should call remove', () => {
            spyOn(component as any, 'removeModule');
            component['actionsHandler']('remove');
            expect(component['removeModule']).toHaveBeenCalled();
        });
        it('should call default', () => {
          component['actionsHandler']('default');
      });
    });
    it('updateBlurb', () => {
      spyOn(component as any, 'updateBlurb');
      expect(component.updateBlurb).toBeTrue;
    })
    it('#loadinitialdata should get lotto', () => {
        component.ngOnInit();
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
    it("loadInitialData with service error 401", () => {
      apiClientService.lottosService().getLottery.and.returnValue(throwError({ error: { message: '401' } }))
      spyOn(component as any, 'loadInitialData');
    });
  
    it('should revert faq', () => {
        spyOn(component as any, 'loadInitialData');
        const event = 'revert';
        component.actionsHandler(event);
        expect(component['loadInitialData']).toHaveBeenCalled();
    });
    describe('removeModule', () => {
        it('should remove and route to lotto page', () => {
            component.lotto = <ILottos>{id: 'id'};
            component.removeModule();
            expect(apiClientService.lottosService).toHaveBeenCalled();
            expect(router.navigate).toHaveBeenCalledWith(['/lotto']);
        })
    })
    describe('uploadSvgHandler', () => {
      it('should handle image uploading', () => {
        component.lotto = {
          id: '1'
        } as any;
        const setErrorsSpy = jasmine.createSpy('setErrors');
        component.form = {
          controls: {
            originalname: {
              setErrors: setErrorsSpy
            }
          }
        } as any;
        component.uploadSvgHandler({file: 'file'});
      })
      it('should throw error', () => {
        component.lotto = {
          id: '1'
        } as any;
        apiClientService.lottosService().uploadSvg.and.returnValue(throwError({ status: '401' }));
        component.uploadSvgHandler({ file: 'file' });
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
      })
    })
    
      it('#setBreadcrumbsData should create breadcrumbs array', () => {
        component.lotto = lotto;
        component['setBreadcrumbsData']();
        const existingCoupRes = [
          { label: 'Lotto Page', url: '/lotto' },
          { label: 'label', url: '/lotto/5e6f2f85c9e77c000118b4cc' }
        ];
        expect(component.breadcrumbsData).toEqual(existingCoupRes);
    
        component['setBreadcrumbsData'](true);
        const addCoupRes = [
          { label: 'Lotto Page', url: '/lotto' },
          { label: 'New lotto', url: '/lotto/add' }
        ];
        expect(component.breadcrumbsData).toEqual(addCoupRes);
      });
      describe('createFormGroup', () => {
            it('initialize the form', () => {
                  spyOn(component, 'createFormGroup');
                  expect(component.createFormGroup).toBeTrue;
                });
            });
    
            it('#sendNewSegmentInformation should send new info and show notification', () => {
                component.lotto = lotto;
            
                component.sendNewSegmentInformation();
                expect(apiClientService.lottosService().saveLotto).toHaveBeenCalledWith(component.lotto);
                expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                  title: 'Creating Completed',
                  message: 'The Segment is Successfully Created.'
                });
                expect(router.navigate).toHaveBeenCalledWith([
                  `/lotto/${component.lotto.id}`
                ]);
              });
              it('#createSegmen should show dialog and send request', () => {
                component.lotto = {
                  title: 'test title'
                } as any;
                component['updateCouponSegment'] = jasmine.createSpy('updateCouponSegment');
                component['sendNewSegmentInformation'] = jasmine.createSpy('sendNewSegmentInformation');
            
                component.createSegment();
                expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
                  title: `Create Segment: ${component.lotto.label}`,
                  message: `Do You Want to Create a Lotto?`,
                  yesCallback: jasmine.any(Function)
                });
            
                expect(component['sendNewSegmentInformation']).toHaveBeenCalled();
              });
              
      it('should return true', () => {
        const response = component.isValid();
        expect(response).toBeTrue;
      });
      it('should return true', () => {
        const response = component.isValidModel({
            label: 'string',
            infoMessage: 'string',
            nextLink: 'string',
            ssMappingId: 'string',
            svgId: 'string',
        } as any);
        expect(response).toBe(true);
      });

      it('should isNewLottoValid return true', () => {
        const response = component.isNewLottoValid();
        expect(response).toBe(true);
      });
      
      it('sendReuest error scenario', () => {
        component.lotto = {
          brand: 'test'
        } as any;
        component.error = 'test';
        apiClientService.lottosService().updateLottoDetails.and.returnValue(throwError({ error: '401' }));
        component['sendRequest']('updateLottoDetails');
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(lotto).toBeTrue;
      })
})