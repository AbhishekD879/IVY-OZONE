import { of } from 'rxjs';
import { BetpackFeaturepageComponent } from '@app/betpackMarket/components/betpackFeaturePage/betpack-featurepage.component';

describe('BetpackFeaturepageComponent', () => {
    let component: any;
    let carouselService: any;
    let liveServConnectionService: any;
    let pubSubService: any;
    let betpackCmsService: any;
    let carouselInstanceMock: any;
    let fakeConnection;
    let gtmService;
    let arcUserService;
    let userService;

    beforeEach(() => {
        liveServConnectionService = {
            connect: jasmine.createSpy('connect').and.returnValue(of(fakeConnection)),
            unsubscribeBP: jasmine.createSpy('unsubscribeBP').and.returnValue(of({})),
            subscribeBP: jasmine.createSpy('subscribe').and.returnValue(of({})),
        };
        pubSubService = {
            publish: jasmine.createSpy('publish')
        };
        carouselService = {
            get: jasmine.createSpy('get').and.callFake(() => carouselInstanceMock)
        } as any;
        carouselInstanceMock = {
            next: jasmine.createSpy('next'),
            previous: jasmine.createSpy('previous'),
            toIndex: jasmine.createSpy('toIndex')
        };
        fakeConnection = {
            connected: true,
            id: 10
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        betpackCmsService = {
            socketStorage: {
                delete: jasmine.createSpy('delete')
            }
        };
        
        component = new BetpackFeaturepageComponent(
            carouselService, 
            liveServConnectionService, 
            pubSubService, 
            betpackCmsService, 
            gtmService,
            userService,
            arcUserService
            );
    });

    describe('nextSlide', () => {
        it('#nextSlide should scroll carousel', () => {
            component.nextSlide();
            expect(component.bannersCarousel.next).toHaveBeenCalled();
        });
    });

    describe('prevSlide', () => {
        it('#previousSlide should scroll carousel', () => {
            component.prevSlide();
            expect(component.bannersCarousel.previous).toHaveBeenCalled();
        });
    });
    
    describe('gotToSlide', () => {
        it('#gotToSlide should scroll carousel', () => {
            component.gotToSlide();
            expect(component.bannersCarousel.toIndex).toHaveBeenCalled();
        });
    });

    describe('handleActiveSlide', () => {
        it('handleActiveSlide', () => {
            const slideIndex = 1;
            component.isSlided = true;
            component.filteredBetPack = [{ id: '1', active: true }, { id: '2', active: false }];
            component.handleActiveSlide(slideIndex);
            expect(component.isSlided).toEqual(true);
        });

        it('should not show slider for invalid index', () => {
            const slideIndex = 'test';
            component.handleActiveSlide(slideIndex);
            expect(component.activeSlideIndex).toBe(0);
        });

        it('should set isSlided when not available', () => {
            const slideIndex = 2;
            component.isSlided = false;
            component.filteredBetPack = [{ id: '1', active: true }, { id: '2', active: false }];
            component.handleActiveSlide(slideIndex);
            expect(component.isSlided).toBeTruthy();
        });
    });
});