import { of, throwError } from 'rxjs';
import { BetpackOnboardingComponent } from './betpack-onboarding.component';
import environment from '@environment/oxygenEnvConfig';
import { Carousel } from '@app/shared/directives/ng-carousel/carousel.class';
import { BetPackCMSMockData } from '@app/lazy-modules/betpackOnboarding/mock-data/betpack-mockdata';

const betPackCMSMockData = BetPackCMSMockData;
const betPackImage = betPackCMSMockData.images[0];

describe('BetpackOnboardingComponent', () => {
    let component: BetpackOnboardingComponent;
    let betpackCmsService;
    let storageService;
    let userService;
    let rendererService; 
    let carouselService;
    let carousel;
    let windowRef;
    let device;
    let gtmService;

    beforeEach(() => {

        userService = {
            username: 'testUser'
        };

        betpackCmsService = {
            getBetPackOnboarding: jasmine.createSpy('getBetPackOnboarding').and.returnValue(of(betPackCMSMockData))
        };

        storageService = {
            set: jasmine.createSpy('storageService.set'),
            get: jasmine.createSpy('storageService.get')
        };

        rendererService = {
            renderer: {
                listen: jasmine.createSpy(),
                removeClass: jasmine.createSpy(),
                addClass: jasmine.createSpy()
            }
        };

        carousel = {
            currentSlide: 3,
            slidesCount: 4,
            next: jasmine.createSpy('next').and.returnValue(2),
            previous: jasmine.createSpy('previous').and.returnValue(1),
        };

        carouselService = {
            get: jasmine.createSpy('get').and.returnValue(carousel)
        };

        windowRef = {
            nativeWindow: {
                localStorage: {
                    setItem: jasmine.createSpy('setItem'),
                },
                innerWidth: '430'
            }
        };

        device = {
            mobileWidth: 767
        };

        gtmService = {
            push: jasmine.createSpy('push')
          };

        component = new BetpackOnboardingComponent(
            carouselService,
            betpackCmsService,
            storageService,
            rendererService,
            userService,
            windowRef,
            device,
            gtmService
        );

    });

    it('should create component instance', () => {
        expect(component).toBeTruthy();
    });

    describe('#ngOnInit', () => {
        it('#ngOnInit on load should call getBetPackOnboarding for mobile screens', () => {
            component.ngOnInit();
            expect(betpackCmsService.getBetPackOnboarding).toHaveBeenCalled();
            expect(component.onboardingInfo).toEqual(betPackCMSMockData);
            expect(component.isLoading).toBeFalse;
        });

        it('#ngOnInit on load should call OnBoardingIsActiveCheck for non-mobile screens', () => {
            windowRef.nativeWindow.innerWidth = '820';
            spyOn(component.closeOnboardingEmitter, 'emit');
            component.ngOnInit();
            expect(component.closeOnboardingEmitter.emit).toHaveBeenCalledWith('');
        });

        it('#ngOnInit on load should call OnBoardingIsActiveCheck when service call returns error', () => {
            betpackCmsService.getBetPackOnboarding.and.returnValue(throwError(null));

            component = new BetpackOnboardingComponent(
                carouselService,
                betpackCmsService,
                storageService,
                rendererService,
                userService,
                windowRef,
                device,
                gtmService
            );

            spyOn(component.closeOnboardingEmitter, 'emit');
            component.ngOnInit();
            expect(component.closeOnboardingEmitter.emit).toHaveBeenCalledWith('');
        });

        it('should set onBoardingTutorial in localstorage on load when onBoardingType is onBoarding', () => {
            component.ngOnInit();
            component.onBoardingType = 'betPack';
            const onBoardingData = { 'betPack-testUser': true };
            expect(onBoardingData[`${component.onBoardingType}-${userService.username}`]).toBeTruthy;
            expect(storageService.set).toHaveBeenCalledWith('onBoardingTutorial', onBoardingData)
        });

        it('should call closeOnboardingEmitter when boarding info is undefined', () => {

            betpackCmsService = {
                getBetPackOnboarding: jasmine.createSpy('getBetPackOnboarding').and.returnValue(of({}))
            };

            component = new BetpackOnboardingComponent(
                carouselService,
                betpackCmsService,
                storageService,
                rendererService,
                userService,
                windowRef,
                device,
                gtmService
            );

            spyOn(component.closeOnboardingEmitter, 'emit');

            component.ngOnInit();
            expect(component.closeOnboardingEmitter.emit).toHaveBeenCalledWith('');
        });

        it('should set onBoardingTutorial in localstorage on load when onBoardingType is betReceipt', () => {
            component.ngOnInit();
            component.onBoardingType = 'betReceipt';
            const onBoardingData = { 'betReceipt-testUser': true };
            expect(onBoardingData[`${component.onBoardingType}-${userService.username}`]).toBeTruthy;
            expect(storageService.set).toHaveBeenCalled();
        });
    });


    describe('on next slide click', () => {
        beforeEach(() => {
            spyOn(component.closeOnboardingEmitter, 'emit');
        });

        it('should close the onboarding screen when finish nextCTAButtonLabel is clicked', () => {
            betPackImage.nextCTAButtonLabel = 'Finish'
            component.nextSlide(betPackImage, 1);
            expect(component.closeOnboardingEmitter.emit).toHaveBeenCalledWith('');

        });
        it('should show next slide when next nextCTAButtonLabel  is clicked', () => {
            betPackImage.nextCTAButtonLabel = 'Next'
            const carouselName: string = 'betpack-onboarding';
            component.nextSlide(betPackImage, 1);
            expect(carouselService.get).toHaveBeenCalledWith(carouselName);
            expect(component.closeOnboardingEmitter.emit).not.toHaveBeenCalled();
        });
        it('should show next slide when next nextCTAButtonLabel  is clicked and no index', () => {
            betPackImage.nextCTAButtonLabel = 'Next';
            const carouselName: string = 'betpack-onboarding';
            component.onBoardingType = 'betreview';
            component.nextSlide(betPackImage, null);
            expect(carouselService.get).toHaveBeenCalledWith(carouselName);
            expect(component.closeOnboardingEmitter.emit).not.toHaveBeenCalled();
        });
    });


    describe('on previous slide click', () => {
        it('should show prev slide when prev button  is clicked', () => {
            const carouselName: string = 'betpack-onboarding';
            component.prevSlide();
            expect(carouselService.get).toHaveBeenCalledWith(carouselName);
        });
    });

    describe('on close button click', () => {
        beforeEach(() => {
            spyOn(component.closeOnboardingEmitter, 'emit');
        });
        it('should close the onboarding screen and invoke GAtracking for finish when close button is clicked', () => {
            const event: any = '';
            betPackImage.nextCTAButtonLabel = 'finish';
            component.onBoardingType = 'onboarding';
            component.onCloseOnboardingOverlay(event, betPackImage);
            expect(component.closeOnboardingEmitter.emit).toHaveBeenCalledWith(event);
        });

        it('should call handleGATracking with close ', () => {
            const event: any = '';
            betPackImage.nextCTAButtonLabel = 'finish';
            component.onBoardingType = '';
            spyOn(component as any,'handleGATracking');
            component.onCloseOnboardingOverlay(event, betPackImage);
            expect(component['handleGATracking']).toHaveBeenCalledWith('close');
        });

        it('should close the onboarding screen and invoke GAtracking for close when close button is clicked', () => {
            const event: any = '';
            component.onCloseOnboardingOverlay(event, betPackImage);
            expect(component.closeOnboardingEmitter.emit).toHaveBeenCalledWith(event);
        });
    });

    describe('generate image url', () => {
        it('should get image s3 bucket url', () => {
            const cmsUri = environment.CMS_ROOT_URI;
            const result = component.getImageSrc(betPackImage);
            const bpmpOnboardingImage = `${cmsUri}${betPackImage.onboardImageDetails.path}/${betPackImage.onboardImageDetails.filename}`;
            expect(result).toEqual(bpmpOnboardingImage);
        });
    });

    describe(' setters and getters', () => {
        it('bannersCarousel setter and getter', () => {
            const carouselName: string = 'betpack-onboarding';
            let htmlElement: any;
            let domTools: any;
            component['bannersCarousel'] = new Carousel(5, {}, htmlElement, domTools);
            const actualResult = component['bannersCarousel'];
            expect(carouselService.get).toHaveBeenCalledWith(carouselName);
        });
    });

    describe('#ngOnDestroy', () => {
        it('remove class when destoryed', () => {
            component.ngOnDestroy();
            expect(rendererService.renderer.removeClass).toHaveBeenCalled();
        });
    });
});

