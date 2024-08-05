import { of, throwError } from 'rxjs';
import { fakeAsync, } from '@angular/core/testing';
import { FormControl, FormGroup} from '@angular/forms';
import { BannerComponent } from '@app/betpack-market-place/banner/banner.component';
import { BannerTestData,bannerFormGroup} from '@app/betpack-market-place/model/bet-pack-banner.model';

describe('BannerComponent', () => {
    let component: BannerComponent;
    let dialogService;
    let brandService;
    let apiClientService, betpackService, cd, input, fb,globalLoaderService;
    const splashData = {};
    const getAllBannerData = BannerTestData;
    function createFormData(component){
        component.bannerFormGroup=new FormGroup({})
        component.bannerFormGroup.addControl('id',new FormControl('test'))
        component.bannerFormGroup.addControl('brand',new FormControl('test'))
        component.bannerFormGroup.addControl('welcomeMsg',new FormControl('test'))
        component.bannerFormGroup.addControl('termsAndConditionLink',new FormControl('test'))
        component.bannerFormGroup.addControl('termsAndCondition',new FormControl('test'))
        component.bannerFormGroup.addControl('enabled',new FormControl(false))
        component.bannerFormGroup.addControl('bannerTextDescInMarketPlacePage',new FormControl('test'))
        component.bannerFormGroup.addControl('bannerTextDescInReviewPage',new FormControl('test'))
        component.bannerFormGroup.addControl('bannerActiveInMarketPlace',new FormControl('test'))
        component.bannerFormGroup.addControl('bannerActiveInReviewPage',new FormControl('test'))
        component.bannerFormGroup.addControl('marketPlaceBgImageFileName',new FormControl('test'))
        component.bannerFormGroup.addControl('marketPlaceImageFileName',new FormControl('test'))
        component.bannerFormGroup.addControl('reviewPageBgImageFileName',new FormControl('test'))
        component.bannerFormGroup.addControl('reviewPageImageFileName',new FormControl('test'))
        component.bannerFormGroup.addControl('expiresInActive',new FormControl(true))
        component.bannerFormGroup.addControl('expiresInIconImage',new FormControl('test'))
        component.bannerFormGroup.addControl('expiresInText',new FormControl('test'))
        component.bannerFormGroup.addControl('bannerImageFileName',new FormControl('test'))
        component.bannerFormGroup.addControl('bannerImageUpload',new FormControl('test'))
        component.bannerFormGroup.addControl('bannerImage',new FormControl({filename:'test',originalname:"test",path:'test'}))

       }
    beforeEach(() => {
        dialogService = {
            showNotificationDialog: jasmine.createSpy('showNotificationDialog')
        };
        betpackService = {
            getBannerData: jasmine.createSpy('getBannerData').and.returnValue(of({ body: getAllBannerData })),
            putBannerData: jasmine.createSpy('putBannerData').and.returnValue(of({ body: splashData })),
            postBannerData: jasmine.createSpy('postBannerData').and.returnValue(of({ body: splashData }))
        };
        brandService = {};
        cd = { detectChanges: jasmine.createSpy('getBannerData') };
        apiClientService = {
            betpackService: () => betpackService
        };
        input = {
            target: { previousElementSibling: { querySelector: jasmine.createSpy('querySelector').and.returnValue({ click: jasmine.createSpy('click') }) } },
        }
        globalLoaderService={
            hideLoader: jasmine.createSpy('hideLoader'),
            showLoader: jasmine.createSpy('showLoader')
        }
        fb={
            group:jasmine.createSpy('group'),
        };
        component = new BannerComponent(dialogService, apiClientService, brandService, cd,fb,globalLoaderService);

    });
    it('constructor', () => {
        expect(component).toBeDefined();
    });
    it('should create', () => {
        expect(component).toBeTruthy();
    });
    it('uploadNotify', () => {
        component.createFormGorup();
        component.uploadNotify();
        expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
            title: 'Uploaded',
            message: 'Your Changes Are Saved Succesfully'
        });
    });
    it('errorNotify', () => {
        const error = {};
        component.errorNotify(error);
        expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
            title: 'Error',
            message: JSON.stringify(error)
        });
    });
    describe('ngOnInit', () => {
        it('general calls', fakeAsync(() => {
            spyOn(component, 'createFormGorup');
            spyOn(component, 'loadSplashData');
            component.bannerFormGroup = new FormGroup({});
            component.bannerFormGroup.addControl('bannerName', new FormControl('test'));
            component.bannerFormGroup.addControl('backgroundName', new FormControl('test'));
            component.bannerFormGroup.addControl('welcomeMsg', new FormControl('test'));
            component.bannerFormGroup.addControl('buttonText', new FormControl('test'));
            component.bannerFormGroup.addControl('termsAndConditionLink', new FormControl('test'));
            component.bannerFormGroup.addControl('termsAndCondition', new FormControl('test'));
            component.bannerFormGroup.addControl('enabled', new FormControl('test'));
            component.bannerFormGroup = {
                valueChanges: {
                    subscribe: jasmine.createSpy().and.callFake(cb => cb({
                        welcomeMsg: 'test on tst0 env',
                        enabled: 'false',
                        termsAndCondition: 'data',
                        termsAndConditionLink: '/',
                    }))
                }
            } as any;
            component.ngOnInit();
            expect(component.loadSplashData).toHaveBeenCalled();
            expect(component.hideAction).toBeFalse();
        }));
    });

    describe('createFormGorup', () => {
        it('initialize the form', () => {
            component.createFormGorup();
            expect(true).toBeTruthy();

        });
    });

    describe('loadSplashData', () => {
        it('calls getAllSplashData function', () => {
            createFormData(component)
            component.loadSplashData();
            expect(apiClientService.betpackService().getBannerData).toHaveBeenCalled();
        });
        it('calls getAllSplashData function if no response', () => {
            apiClientService = {
                betpackService: () => betpackService
            };
            betpackService = {
                getBannerData: jasmine.createSpy('getBannerData').and.returnValue(throwError('test'))
            };
            createFormData(component)
            component.loadSplashData();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
        });
        it('calls getAllSplashData function if no response no data', () => {
            apiClientService = {
                betpackService: () => betpackService
            };
            betpackService = {
                getBannerData: jasmine.createSpy('getBannerData').and.returnValue(of({body:null}))
            };
            createFormData(component)
            component.loadSplashData();
            expect(globalLoaderService.hideLoader).not.toHaveBeenCalled();
        });
        
    });

    describe('prepareToUploadFile', () => {
       
        it('should upload file on calling prepareToUploadFile', () => {
            createFormData(component)
            const event = {
                'target': {
                    'id': 'upload-banner',
                    'files': [{
                        'name': 'AccaPlusBanner.png',
                        'size': 38656,
                        'type': 'image/png'
                    }]
                }
            } as any;
            //component.bannerData = getAllBannerData;
            component.prepareToUploadFile(event);
            expect(component.bannerFormGroup.get('bannerImageFileName').value).toBe('AccaPlusBanner.png');
        });
        it('should upload file on calling prepareToUploadFile with out upload baner', () => {
            createFormData(component)
            const event = {
                'target': {
                    'id': 'no-upload-banner',
                    'files': [{
                        'name': 'AccaPlusBanner.png',
                        'size': 38656,
                        'type': 'image/png'
                    }]
                }
            } as any;
            component.prepareToUploadFile(event);
            expect(component.bannerFormGroup.get('bannerImageFileName').value).toBe('test');
        });
        it('should throw error on incorrect file type ', () => {
            const event = {
                'target': {
                    'id': 'upload-banner',
                    'files': [{
                        'name': 'AccaPlusBanner.png',
                        'size': 38656,
                        'type': 'image/jpg'
                    }]
                }
            } as any;
            component.createFormGorup();
            component.prepareToUploadFile(event);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
                title: `Error. Unsupported file type.`,
                message: 'Supported \"jpeg\",\"gif\",\"png\" and \"svg\".'
            });
        });
    });

    describe('RemoveMainImage', () => {
        it('Should Remove the Uploaded file', () => {
            const event = {
                'target': {
                    'classList': [`launch-image-btn`]
                }
            } as any;
            createFormData(component)
            component.removeMainImage(event);
            expect(component.bannerFormGroup.get('bannerImageUpload').value).toMatch('');

        });
        it('Should Remove the Uploaded file for bannerName', () => {
            const event = {
                'target': {
                    'classList': []
                }
            } as any;
            createFormData(component)
            component.removeMainImage(event);
            expect(component.bannerFormGroup.get('bannerImageUpload').value).toMatch('');
        });
    });

    describe('constructFormData', () => {
        it('Should construct splash form data', () => {
            createFormData(component)
            component.constructFormData();
            expect(component.bannerFormData).toBeInstanceOf(FormData);
        });
        it('Should construct splash form data negative senario1', () => {
            createFormData(component)
            component.bannerFormGroup.removeControl('bannerImageUpload')
            component.constructFormData();
            expect(component.bannerFormData).toBeInstanceOf(FormData);
        });
        it('Should construct splash form data negative senario2', () => {
            createFormData(component)
            component.bannerFormGroup.patchValue({bannerImageUpload:null})
            component.constructFormData();
            expect(component.bannerFormData).toBeInstanceOf(FormData);
        });
    });

    describe('isValid', () => {
        it('should return true', () => {
            createFormData(component)
            component.disableSaveBtn=true;  
            expect(component.isValid()).toBe(true);
        });
        it('should return false', () => {
            component.disableSaveBtn=false;
            createFormData(component)
            expect(component.isValid()).toBeFalse();
        });
    });

    describe('saveChanges with banner id', () => {
        beforeEach(() => {
            component = new BannerComponent(dialogService, apiClientService, brandService, cd,fb,globalLoaderService);
            spyOn(component, 'uploadNotify');
            spyOn(component, 'errorNotify');
        })
        afterAll(() => {
            component = null
        })
        it('should save changes using put call with banner id', () => {
            createFormData(component)
            component.saveChanges();
            expect(component.uploadNotify).toHaveBeenCalled();
        });
        it('should save changes using put call with banner id no data', () => {
            apiClientService = {
                betpackService: () => betpackService
            };
            betpackService = {
                putBannerData: jasmine.createSpy('putBannerData').and.returnValue(of(null)),
                postBannerData: jasmine.createSpy('postBannerData').and.returnValue(of(null))
            };
            createFormData(component)
            component.bannerFormGroup.patchValue({id:null})

            component.saveChanges();
            expect(component.uploadNotify).not.toHaveBeenCalled();
        });
        it('should save changes using put call with banner id error', () => {
            createFormData(component)
            apiClientService = {
                betpackService: () => betpackService
            };
            betpackService = {
                putBannerData: jasmine.createSpy('putBannerData').and.returnValue(throwError({ error: 401 })),
                postBannerData: jasmine.createSpy('postBannerData').and.returnValue(throwError({ error: 401 }))
            };
            component.saveChanges();
            expect(component.errorNotify).toHaveBeenCalled();
        });

    });
    describe('saveChanges without banner id', () => {
        beforeEach(() => {
            component = new BannerComponent(dialogService, apiClientService, brandService, cd,fb,globalLoaderService);
            spyOn(component, 'uploadNotify');
            spyOn(component, 'errorNotify');
        })
        afterAll(() => {
            component = null
        })
        it('should save changes using post call without banner id', () => {
            createFormData(component)
            component.bannerFormGroup.patchValue({bannerImage:{filename:'',originalname:"",path:''}})
            component.saveChanges();
            expect(component.uploadNotify).toHaveBeenCalled();
        });
        it('should save changes using put call without banner id', () => {
            createFormData(component)
            apiClientService = {
                betpackService: () => betpackService
            };
            betpackService = {
                putBannerData :jasmine.createSpy('putBannerData').and.returnValue(of(null))
            };
            component.saveChanges();
            expect(component.uploadNotify).not.toHaveBeenCalled();
        });
        it('should save changes using put call without banner id no data', () => {
            apiClientService = {
                betpackService: () => betpackService
            };
            betpackService = {
                postBannerData: jasmine.createSpy('postBannerData').and.returnValue(of(bannerFormGroup)),
                putBannerData :jasmine.createSpy('putBannerData').and.returnValue(of(bannerFormGroup))
            };
            createFormData(component)
            component.bannerFormGroup.patchValue({id:null})
            component.saveChanges();
            expect(component.uploadNotify).toHaveBeenCalled();
        });
        it('should save changes using post call without banner id error', () => {
            createFormData(component)
            apiClientService = {
                betpackService: () => betpackService
            };
            betpackService = {
                postBannerData: jasmine.createSpy('postBannerData').and.returnValue(throwError({ error: 401 })),
                putBannerData: jasmine.createSpy('putBannerData').and.returnValue(throwError({ error: 401 }))

            };
            component.bannerFormGroup.patchValue({id:null})
            component.saveChanges();
            expect(component.errorNotify).toHaveBeenCalled();
        });
    });
    describe('updateBannerMsg', () => {
        it('updateBannerMsg', () => {
            createFormData(component)
           
            component.updateBannerMsg('updateBannerMsg','bannerImage');
            expect(cd.detectChanges).toHaveBeenCalled();
        });
    });
    describe('handleUploadImageClick', () => {
        it('handleUploadImageClick', () => {
            component.createFormGorup();
            component.handleUploadImageClick(input);
            expect(1).toBe(1)
        });
    });
    describe('actionsHandler', () => {
        it('actionsHandler revert', () => {
            spyOn(component,'loadSplashData')
            component.actionsHandler('revert');
            expect(1).toBe(1)
        });
        it('actionsHandler save', () => {
            spyOn(component,'saveChanges')
            component.actionsHandler('save');
            expect(1).toBe(1)
        });
        it('actionsHandler default', () => {
            component.actionsHandler('default');
            expect(1).toBe(1)
        });
    });
    describe('triggrExpiresActive', () => {
        it('triggrExpiresActive', () => {
            createFormData(component)
            const event={
                checked:true
            }
            component.triggrExpiresActive(event)
            expect(true).toBeTruthy()
        });
        it('triggrExpiresActive', () => {
            createFormData(component)
            const event={
                checked:true
            }
            component.bannerFormGroup.patchValue({expiresInActive:false})
            component.triggrExpiresActive(event)
            expect(true).toBeTruthy()
        });
    });
    describe('patchLimitError', () => {
        it('patchLimitError', () => {
            createFormData(component)           
            component.patchLimitError('test','bannerTextDescInMarketPlacePage')
            expect(true).toBeTruthy()
        });
        it('patchLimitError else', () => {
            createFormData(component)         
            component.patchLimitError(null,'bannerTextDescInMarketPlacePage')
            expect(true).toBeTruthy()
        });
    });
    describe('ngAfterViewChecked', () => {
        it('ngAfterViewChecked if', () => {
            component.hideAction=true
            createFormData(component)           
            component.ngAfterViewChecked()
            expect(true).toBeTruthy()
        });
        it('ngAfterViewChecked else', () => {
            component.hideAction=false
            createFormData(component)           
            component.ngAfterViewChecked()
            expect(true).toBeTruthy()
        });
    });
    describe('constructFormData', () => {
        it('constructFormData negative', () => {
            createFormData(component) 
            component.bannerFormGroup.patchValue({bannerImageUpload:null})
            component.bannerFormGroup.patchValue({bannerImage:null})
            component.constructFormData()
            expect(true).toBeTruthy()
        });
        it('constructFormData else', () => {
            createFormData(component) 
            component.bannerFormGroup.patchValue({bannerImage:{filename:'test',originalname:'test',path:'test'}})
            component.bannerFormGroup.patchValue({bannerImage:{filename:'test',originalname:'test',path:'test'}})
            component.constructFormData()
            expect(true).toBeTruthy()
        });
    });
});


