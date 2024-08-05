import {
    FiveASideAnimatedScoreComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideAnimatedScore/fiveaside-animated-score.component';

describe('FiveASideAnimatedScoreComponent', () => {
    let component: FiveASideAnimatedScoreComponent;

    beforeEach(() => {
        component = new FiveASideAnimatedScoreComponent();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });


    describe('#animateDigitCount', () => {
        it('should call numberCounterHandler method with required parameters', () => {
            component.timeDuration = 300;
            component.digit = 123;
            spyOn(component as any, 'numberCounterHandler');
            component['animateDigitCount']();
            expect(component['numberCounterHandler']).toHaveBeenCalled();
        });

        it('should call numberCounterHandler method with default timeDuration', () => {
            component.timeDuration = undefined as any;
            component.digit = 123;
            spyOn(component as any, 'numberCounterHandler');
            component['animateDigitCount']();
            expect(component['numberCounterHandler']).toHaveBeenCalled();
            expect(component.timeDuration).toEqual(1000);
        });

        it('should call numberCounterHandler when input is not a number', () => {
            component.timeDuration = 300;
            component.digit = '1' as any;
            spyOn(component as any, 'numberCounterHandler');
            component['animateDigitCount']();
            expect(component['numberCounterHandler']).toHaveBeenCalled();
        });

        it('should call numberCounterHandler when input is number', () => {
            component.timeDuration = 300;
            component.digit = 1 as any;
            spyOn(component as any, 'numberCounterHandler');
            component['animateDigitCount']();
            expect(component['numberCounterHandler']).toHaveBeenCalled();
        });

        it('should not call numberCounterHandler when input is not a number', () => {
            component.timeDuration = 300;
            component.digit = 's' as any;
            spyOn(component as any, 'numberCounterHandler');
            component['animateDigitCount']();
            expect(component['numberCounterHandler']).not.toHaveBeenCalled();
        });
    });

    describe('#ngAfterViewInit', () => {
        it('should call animateDigitCount when digit is present', () => {
            component.digit = 1;
            spyOn(component as any, 'animateDigitCount');
            component.ngAfterViewInit();
            expect(component['animateDigitCount']).toHaveBeenCalled();
        });
        it('should call animateDigitCount when digit is not present', () => {
            component.digit = undefined as any;
            spyOn(component as any, 'animateDigitCount');
            component.ngAfterViewInit();
            expect(component['animateDigitCount']).not.toHaveBeenCalled();
        });
    });

    describe('#ngOnChanges', () => {
        it('should call ngOnChanges when digit is number', () => {
            spyOn(component as any, 'animateDigitCount');
            component.ngOnChanges({ digit: 1 } as any);
            expect(component['animateDigitCount']).toHaveBeenCalled();
        });
        it('should call ngOnChanges when digit is number', () => {
            spyOn(component as any, 'animateDigitCount');
            component.ngOnChanges({ digit1: 1 } as any);
            expect(component['animateDigitCount']).not.toHaveBeenCalled();
        });
    });

    describe('#numberCounterHandler', () => {
        it('should call numberCounterHandler when digit is number', () => {
            spyOn(global as any, 'requestAnimationFrame');
            component['numberCounterHandler'](3, 1000, { nativeElement: { textContent: '' } });
            expect(requestAnimationFrame).toHaveBeenCalled();
        });

        it('should call numberCounterHandler when element is null', () => {
            spyOn(global as any, 'requestAnimationFrame');
            component['numberCounterHandler'](3, 1000, null as any);
            expect(requestAnimationFrame).not.toHaveBeenCalled();
        });

        it('should call numberCounterHandler when digit has high value', () => {
            spyOn(global as any, 'requestAnimationFrame');
            component['numberCounterHandler'](80, 1000, { nativeElement: { textContent: '' } });
            expect(requestAnimationFrame).toHaveBeenCalled();
        });

        it('should call numberCounterHandler when steps are defined', () => {
            spyOn(global as any, 'requestAnimationFrame');
            component.steps = 12;
            component['numberCounterHandler'](80, 1000, { nativeElement: { textContent: '' } });
            expect(requestAnimationFrame).toHaveBeenCalled();
        });

        it('should call numberCounterHandler when steps are given decimal', () => {
            spyOn(global as any, 'requestAnimationFrame');
            component.steps = 0.5;
            component['numberCounterHandler'](80, 0.005, { nativeElement: { textContent: '' } });
            expect(requestAnimationFrame).not.toHaveBeenCalled();
        });
    });
});
