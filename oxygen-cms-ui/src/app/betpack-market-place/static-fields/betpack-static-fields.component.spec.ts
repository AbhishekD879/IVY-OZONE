import { of } from 'rxjs';
import { LabelsTestData, } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { StaticFieldComponent } from '@app/betpack-market-place/static-fields/betpack-static-fields.component';
import { FormControl, FormGroup } from '@angular/forms';

describe('StaticFieldComponent', () => {
    let component: StaticFieldComponent;
    let apiClientService, betpackService, fb;
    let dialogService;
    let brandService;

    const splashData = {};

    
    function constructForm(component){
      component.bpLables=new FormGroup({})
      component.bpLables.addControl('id',new FormControl('test'))
      component.bpLables.addControl('brand',new FormControl('test'))
      component.bpLables.addControl('createdBy',new FormControl('test'))
      component.bpLables.addControl('createdAt',new FormControl('test'))
      component.bpLables.addControl('updatedBy',new FormControl('test'))
      component.bpLables.addControl('updatedAt',new FormControl(false))
      component.bpLables.addControl('updatedByUserName',new FormControl('test'))
      component.bpLables.addControl('createdByUserName',new FormControl('test'))
      component.bpLables.addControl('buyButtonLabel',new FormControl('test'))
      component.bpLables.addControl('buyBetPackLabel',new FormControl('test'))
      component.bpLables.addControl('gotoMyBetPacksLabel',new FormControl('test'))
      component.bpLables.addControl('depositMessage',new FormControl('test'))
      component.bpLables.addControl('kycArcGenericMessage',new FormControl('test'))
      component.bpLables.addControl('useByLabel',new FormControl('test'))
      component.bpLables.addControl('maxBetPackPerDayBannerLabel',new FormControl(true))
      component.bpLables.addControl('betPackAlreadyPurchasedPerDayBannerLabel',new FormControl('test'))
      component.bpLables.addControl('betPackMarketplacePageTitle',new FormControl('test'))
      component.bpLables.addControl('errorTitle',new FormControl('test'))
      component.bpLables.addControl('errorMessage',new FormControl('test'))
      component.bpLables.addControl('goToBettingLabel',new FormControl('test'))
      component.bpLables.addControl('goBettingURL',new FormControl('test'))
      component.bpLables.addControl('goToBettingLabel',new FormControl('test'))
      component.bpLables.addControl('moreInfoLabel',new FormControl('test'))
      component.bpLables.addControl('buyNowLabel',new FormControl('test'))
      component.bpLables.addControl('betPackReview',new FormControl('test'))
      component.bpLables.addControl('maxPurchasedLabel',new FormControl('test'))
      component.bpLables.addControl('limitedLabel',new FormControl('test'))
      component.bpLables.addControl('soldOutLabel',new FormControl('test'))
      component.bpLables.addControl('endingSoonLabel',new FormControl('test'))
      component.bpLables.addControl('expiresInLabel',new FormControl('test'))
      component.bpLables.addControl('endedLabel',new FormControl('test'))
      component.bpLables.addControl('maxOnePurchasedLabel',new FormControl('test'))
      component.bpLables.addControl('reviewErrorMessage',new FormControl('test'))
      component.bpLables.addControl('reviewErrorTitle',new FormControl('test'))
      component.bpLables.addControl('reviewGoBettingURL',new FormControl('test'))
      component.bpLables.addControl('reviewGoToBettingLabel',new FormControl('test'))
      component.bpLables.addControl('betPackInfoLabel',new FormControl('test'))
      component.bpLables.addControl('lessInfoLabel',new FormControl('test'))
      component.bpLables.addControl('betPackSuccessMessage',new FormControl('test'))
      component.bpLables.addControl('maxPurchasedTooltip',new FormControl('test'))
      component.bpLables.addControl('limitedTooltip',new FormControl('test'))
      component.bpLables.addControl('soldOutTooltip',new FormControl('test'))
      component.bpLables.addControl('endingSoonTooltip',new FormControl('test'))
      component.bpLables.addControl('expiresInTooltip',new FormControl('test'))
      component.bpLables.addControl('endedTooltip',new FormControl('test'))
      component.bpLables.addControl('maxOnePurchasedTooltip',new FormControl('test'))
      component.bpLables.addControl('featuredBetPackBackgroundLabel',new FormControl('test'))
      component.bpLables.addControl('serviceError',new FormControl('test'))
      component.bpLables.addControl('goToReviewText',new FormControl('test'))
      component.bpLables.addControl('goToBetbundleText',new FormControl('test'))
      component.bpLables.addControl('allFilterPillMessage',new FormControl('test'))
      component.bpLables.addControl('isDailyLimitBannerEnabled',new FormControl('test'))
      component.bpLables.addControl('allFilterPillMessageActive',new FormControl('test'))
      component.bpLables.addControl('comingSoon',new FormControl('test'))
      component.bpLables.addControl('comingSoonSvg',new FormControl('test'))
    }
    dialogService = {
        showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
        showConfirmDialog: jasmine.createSpy('showConfirmDialog')
    };
    brandService = {
        brand:'test'
    };
    betpackService = {
        getLabelsData: jasmine.createSpy('getLabelsData').and.returnValue(of({ body: LabelsTestData })),
        postLabelsData: jasmine.createSpy('postLabelsData').and.returnValue(of({ body: splashData })),
        putLabelsData: jasmine.createSpy('putLabelsData').and.returnValue(of({ body: splashData })),
        postBackgroundData: jasmine.createSpy('postBackgroundData').and.returnValue(of({ body: splashData })),
        deleteBackgroundData: jasmine.createSpy('postBackgroundData').and.returnValue(of({ body: splashData })),
    };
    apiClientService = {
        betpackService: () => betpackService
    };
    fb={
        group: jasmine.createSpy('group')
    }
    beforeEach(() => {       
        component = new StaticFieldComponent(apiClientService, dialogService, brandService,fb);
    });
    describe('constructor',()=>{
        it('constructor', () => {
            const buildForm =spyOn(component,'buildForm')
            constructForm(component);
            component.constructor();
            expect(component).toBeDefined();
            expect(buildForm).toHaveBeenCalled();
    
        });
        it('saveNotify', () => {
            dialogService = {
                showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
                    closeCallback();
                }),
                showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                    yesCallback();
                })
            };
            component = new StaticFieldComponent(apiClientService, dialogService, brandService,fb);
            spyOn(component, 'load');
            component.saveNotify();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: `Labels Saving`,
                message: `Labels are Saved.`,
                closeCallback: jasmine.any(Function)
            });
        });
    });
    describe('ngOnInit',()=>{        
        it('ngOnInit', () => {
            spyOn(component, 'load');
            component.ngOnInit();
            expect(component.load).toHaveBeenCalled();
        });
    })
    describe('saveNotify',()=>{       
        it('saveNotify', () => {
            dialogService = {
                showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
                    closeCallback();
                }),
                showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                    yesCallback();
                })
            };
            component = new StaticFieldComponent(apiClientService, dialogService, brandService,fb);
            spyOn(component, 'load');
            component.saveNotify();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: `Labels Saving`,
                message: `Labels are Saved.`,
                closeCallback: jasmine.any(Function)
            });
        });
    });
    describe('#action Handler', () => {
        it('#actionHandler should call correct method', () => {
            spyOn(component, 'saveChanges');
            component.actionsHandler('save');
            expect(component.saveChanges).toHaveBeenCalled();

            spyOn(component, 'load');
            component.actionsHandler('revert');
            expect(component.load).toHaveBeenCalled();
        });
        it('#actionHandler should do nothing if wrong event', () => {
            spyOn(component, 'saveChanges');
            spyOn(component, 'load');
            component.actionsHandler('test-event');
            expect(component.saveChanges).not.toHaveBeenCalled();
            expect(component.load).not.toHaveBeenCalled();
        });
    });
    describe('Handle Upload ImageClick', () => {
               it('handleUploadImageClick', () => { 
            dialogService = {
                showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
                    closeCallback();
                }),
                showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                    yesCallback();
                })
            }; 
            component = new StaticFieldComponent(apiClientService, dialogService, brandService,fb);
            const event={target:{previousElementSibling:{querySelector:jasmine.createSpy('querySelector').and.returnValue({click:jasmine.createSpy('click')})}}}
            component.handleUploadImageClick(event)
             expect(dialogService.showConfirmDialog).toHaveBeenCalled();
        });
    });
    describe('construct FormData', () => {
        it('constructFormData without backgroundImage', () => {  
            component.backgroundImage=undefined;
            expect(component.constructFormData()).toEqual(new FormData);
        });
    });
    describe('bpControls', () => {
        it('bpControls has been called', () => {  
            constructForm(component)
            expect( component.bpControls).not.toEqual(null);
        });
        it('bpControls has been called null point', () => {  
            expect( component.bpControls).toBeUndefined();
        });
    });
    describe('bpIsValid', () => {
        it('bpIsValid has been called', () => {  
            constructForm(component)
            expect( component.bpIsValid()).toBeFalse();
        });
        it('bpIsValid has been called null point', () => {  
            expect( component.bpIsValid()).toBeUndefined();
        });
    });
    describe('ngAfterViewChecked', () => {
        it('ngAfterViewChecked has been called', () => {  
            constructForm(component);
            component.ngAfterViewChecked();
            expect(true).toBeTruthy();
        });
    });
    describe('saveChanges', () => {
        it('saveChanges post call has been called', () => {  
            constructForm(component);
            component.emptyLabels=true;
            component.saveChanges();
            expect(betpackService.postLabelsData).toHaveBeenCalled();
        });
    });
    describe('saveChanges', () => {
        it('saveChanges pull call has been called', () => {  
            constructForm(component);
            component.emptyLabels=false;
            component.saveChanges();
            expect(betpackService.putLabelsData).toHaveBeenCalled();
        });
    });
    describe('prepareToUploadFile', () => {
       beforeEach(()=>{
        dialogService = {
            showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
            showConfirmDialog: jasmine.createSpy('showConfirmDialog')
        };
        component = new StaticFieldComponent(apiClientService, dialogService, brandService,fb);

       })
        it('prepareToUploadFile', () => {            
            constructForm(component);
            const event={target:{files:[{type:"image/svg+xml",name:'test'}]}}
            component.emptyLabels=false;
            component.prepareToUploadFile(event);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({title: `Uploaded`,
            message: `Background Image uploaded Succesfully.`});
        });
        it('prepareToUploadFile negative', () => {  
            constructForm(component);
            const event={target:{files:[{type:"test",name:'test'}]}}
            component.emptyLabels=false;
            component.prepareToUploadFile(event);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({title: `Error. Unsupported file type.`,
            message: 'Supported "jpeg","gif","png" and "svg".'});
        });
    });
    describe('removeMainImage', () => {
        beforeEach(()=>{
            dialogService = {
                showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
                showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                    yesCallback();
                })
            };
        })
         it('removeMainImage', () => {            
             component = new StaticFieldComponent(apiClientService, dialogService, brandService,fb);
             constructForm(component);
             component.removeMainImage(event);
             expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({title: `Removed`,
             message: `Background Image removed Succesfully.`});
         });
     });
     describe('load', () => {
        it('load', () => {  
            constructForm(component)
            component.load()
            expect(component.emptyLabels).toBeFalse();
        });
       
    });
});
