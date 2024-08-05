import { VirtualFeatureZoneComponent } from '@app/vsbr/components/virtualFeatureZone/virtual-feature-zone.component';

describe('VirtualFeatureZoneComponent', () => {
    let windowRef, router, carouselService, virtualHubService, gtmService, carouselInstanceMock;
    let component;
    
    beforeEach(() => {
        windowRef = {
            nativeWindow: {
                open: jasmine.createSpy('open').and.callThrough()
            }
        },
        router = {
            navigateByUrl: jasmine.createSpy('navigateByUrl').and.callThrough()
        },
        carouselService = {
            get: jasmine.createSpy('geto').and.callFake(() => carouselInstanceMock),
            remove: jasmine.createSpy('remove').and.callThrough()
        } as any;
        carouselInstanceMock = {
            next: jasmine.createSpy('next'),
            previous: jasmine.createSpy('previous'),
            toIndex: jasmine.createSpy('toIndex')
        };
        virtualHubService = {},
        gtmService = {
            push:  jasmine.createSpy('push').and.callThrough()
        }
        component = new VirtualFeatureZoneComponent(windowRef, router, carouselService, virtualHubService, gtmService);
    })

    describe('ngOnInit', () => {
        it('ngOninit', () => {
            spyOn(component, 'getBGImageUrl');
            component.featuredZoneOffers = [{ Id: 1 }, { Id: 2 }] as any;
            component.virtualHubSystemConfig = { featureZoneBackgroundID: 1 } as any;
            component.ngOnInit();
            expect(component.getBGImageUrl).toHaveBeenCalled();
        })   
    })

    describe('nextSlide', () => {
        it('nextSlide', () => {
            component.nextSlide();
        })
    })

    describe('prevSlide', () => {
        it('prevSlide', () => {
            let showPrevios = component.showPrev;
            let showNext = component.showNext;
            let isOneCard = component.isOneCard;
            let isValidCarousel = component.isValidCarousel;
            component.featuredZoneOffers = ['1']
            component.showPrev = 10;
            component.showNext = 10;
            component.isOneCard = 10;
            component.isValidCarousel = 10;
            component.carousel = '10';
            showPrevios = component.showPrev;
            showNext = component.showNext;
            isOneCard = component.isOneCard;
            isValidCarousel = component.isValidCarousel;
            component.prevSlide();
        })

        it('showPrev', () => {
            carouselInstanceMock = undefined
            component.featuredZoneFilteredOffers = ['1']
            const isOneCard = component.isOneCard;
            const isValidCarousel = component.isValidCarousel;
            const showPrevios = component.showPrev;
            expect(showPrevios).toBeFalsy();
        })

        it('showNext', () => {
            carouselInstanceMock = undefined
            const showNext = component.showNext;
            expect(showNext).toBeFalsy();
        })

        it('should return ngCarouselDisableRightSwipe', () => {
            const result = component.ngCarouselDisableRightSwipe;
            component.carousel = '11';
            expect(result).toEqual(false);
        })
        it('ngCarouselDisableRightSwipe setter method calling', () => {
            component.ngCarouselDisableRightSwipe = true;
            expect(component.ngCarouselDisableRightSwipe).toBe(false);
          })
    })

    describe('onImageClick', () => {
        it('onImageClick link with http', () => {
            spyOn(component, 'onFeatureClickGTMEvent');
            component.onImageClick({link: 'http', target: 'target'});
            expect(router.navigateByUrl).not.toHaveBeenCalled();
        })

        it('onImageClick link with out http', () => {
            spyOn(component, 'onFeatureClickGTMEvent');
            component.onImageClick({link: 'abcs', target: 'target'});
            expect(router.navigateByUrl).toHaveBeenCalled();
        })

        it('onImageClick no link', () => {
            spyOn(component, 'onFeatureClickGTMEvent');
            component.onImageClick({ target: 'target'});
            expect(router.navigateByUrl).not.toHaveBeenCalled();
        })
    })

    describe('getBGImageUrl', () => {
        it('getBGImageUrl 1', () => {
            component.virtualHubSystemConfig = {featureZoneBackgroundID : '1'}
            component.featuredZoneOffers = [{Id: '2', imgUrl: 'imgUrl'}]
            const retVal = component.getBGImageUrl();
            expect(retVal).toBeNull()
        })

        it('getBGImageUrl 2', () => {
            component.virtualHubSystemConfig = {featureZoneBackgroundID : '1'}
            component.featuredZoneOffers = [{Id: '1', imgUrl: 'imgUrl'}];
            const retVal = component.getBGImageUrl();
            expect(retVal).toBe('imgUrl');
        })
    })

    describe('getBGImageUrl', () => {
        it('getBGImageUrl 3', () => {
            const retVal = component.onFeatureClickGTMEvent({itemName: 'itemName', link: 'link'} as any);
            expect(gtmService.push).toHaveBeenCalled();
        })
    })

    describe('ngOnDestroy', () => {
        it('ngOnDestroy', () => {
            const retVal = component.ngOnDestroy();
            expect(carouselService.remove).toHaveBeenCalled();
        })
    })
});
