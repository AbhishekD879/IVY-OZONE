import { FiveASideJourneyComponent } from './five-a-side-journey.component';

describe('#FiveASideJourneyComponent', () => {
    let component;
    let carouselService;
    let rendererService;
    let element;
    let changeDetectorRef;
    let storageService;

    beforeEach(() => {
        carouselService = {
            get: jasmine.createSpy('get').and.returnValue('current-carousel'),
            remove: jasmine.createSpy('remove')
        };

        element = {
            nativeElement: {}
        };

        rendererService = {
            renderer: {
                setStyle: jasmine.createSpy('setStyle')
            }
        };

        changeDetectorRef = {
            detectChanges: jasmine.createSpy()
        };

        storageService = {
            set: jasmine.createSpy('set')
        };

        component = new FiveASideJourneyComponent(
            element,
            carouselService,
            rendererService,
            changeDetectorRef,
            storageService
        );
    });

    it('should create component instance', () => {
        expect(component).toBeTruthy();
        expect(component.carouselName).toBe('five-a-side-journey-carousel');
    });

    it('should call ngOnInit method', () => {
        component.slides = [{ title: 'title' }];
        component.ngOnInit();
        expect(component.carouselMode).toBe('Next');
    });

    it('trackBySlide: should return tracking value', () => {
        let i = 0;
        const el = { title: 'title' };
        let result = component.trackBySlide(i, el);
        expect(result).toBe('0_title');

        i = 1;
        el.title = 'title1';
        result = component.trackBySlide(i, el);
        expect(result).toBe('1_title1');
    });

    it('trackByDot: should return tracking value', () => {
        let i = 0;
        const el = { title: 'title' };
        let result = component.trackByDot(i, el);
        expect(result).toBe('0_title');

        i = 1;
        el.title = 'title1';
        result = component.trackByDot(i, el);
        expect(result).toBe('1_title1');
    });

    it('onCarouselInitChangeStatus: should set carousel status', () => {
        const status = 'status';
        component.onCarouselInitChangeStatus(status);
        expect(component.isCarouselInit).toBe(status);
    });

    describe('#navigateToSlide', () => {
        beforeEach(() => {
            spyOnProperty(component, 'slideIndex').and.returnValue(0);
            spyOnProperty(component, 'currentCarousel').and.returnValue({
                toIndex: jasmine.createSpy('toIndex')
            });
        });
        it('should not update carousel index', () => {
            const index = 0;

            component.navigateToSlide(index);
            expect(component.currentCarousel.toIndex).not.toHaveBeenCalled();
        });
        it('should update carousel index', () => {
            const index = 1;

            component.navigateToSlide(index);
            expect(component.currentCarousel.toIndex).toHaveBeenCalledWith(1);
        });
    });

    describe('#navigateToNextSlide', () => {
        beforeEach(() => {
            spyOnProperty(component, 'currentCarousel').and.returnValue({
                toIndex: jasmine.createSpy('toIndex')
            });
            spyOnProperty(component, 'slideIndex').and.returnValue(0);
            component.onClose = jasmine.createSpy('onClose');
        });
        it('should update carousel index', () => {
            component.carouselMode = 'Next';
            component.navigateToNextSlide();

            expect(component.onClose).not.toHaveBeenCalled();
            expect(component.currentCarousel.toIndex).toHaveBeenCalledWith(1);
        });
        it('should close panel', () => {
            component.carouselMode = 'Done';
            component.navigateToNextSlide();

            expect(component.onClose).toHaveBeenCalled();
            expect(component.currentCarousel.toIndex).not.toHaveBeenCalled();
        });
    });

    describe('#setCarouselMode', () => {
        let slideIndexSpy;
        beforeEach(() => {
            slideIndexSpy = spyOnProperty(component, 'slideIndex');
            component.slides = [1, 2, 3];
        });
        it('should set mode to Next', () => {
            slideIndexSpy.and.returnValue(3);
            component.setCarouselMode();

            expect(component.carouselMode).toBe('Next');
            expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
        });
        it('should set mode to Done', () => {
            slideIndexSpy.and.returnValue(2);
            component.setCarouselMode();

            expect(component.carouselMode).toBe('Done');
            expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
        });
    });

    it('ngOnDestroy: should remove carousel', () => {
        component.ngOnDestroy();
        expect(carouselService.remove).toHaveBeenCalledWith(component.carouselName);
    });

    it('onClose: should close panel', () => {
        component.onClose();

        expect(storageService.set).toHaveBeenCalledWith('five-a-side-journey-seen', true);
        expect(component.showJourney).toBeFalsy();
    });

    describe('#currentCarousel', () => {
        it('should return current carousel', () => {
            component.isCarouselInit = true;
            const result = component.currentCarousel;

            expect(result).toBe('current-carousel');
        });
        it('should return null', () => {
            component.isCarouselInit = false;
            const result = component.currentCarousel;

            expect(result).toBe(null);
        });
    });

    describe('#slideIndex', () => {
        it('should return current slide', () => {
            spyOnProperty(component, 'currentCarousel').and.returnValue({
                currentSlide: 'slide'
            });
            expect(component.slideIndex).toBe('slide');
        });
        it('should return null', () => {
            spyOnProperty(component, 'currentCarousel').and.returnValue(null);
            expect(component.slideIndex).toBe(null);
        });
    });
});
