import { SbCounterComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/counter/sb-counter.component'

describe('SbCounterComponent', () => {
    let component: SbCounterComponent;
    beforeEach(() => {
        component = new SbCounterComponent();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('ngOnInit', () => {
        it('should assign disableminus', () => {
            component.teamScores = [0, 1, 2, 3];
            component.counterValueEmitter.emit = jasmine.createSpy('counterValueEmitter.emit');
            component.ngOnInit();
            expect(component.selectedValue).toEqual(0);
            expect(component.disableMinus).toBeTrue();
            expect(component.counterValueEmitter.emit).toHaveBeenCalledWith(0);
        });
        it('should assign disablePlus', () => {
            component.teamScores = [1];
            component.ngOnInit();
            expect(component.selectedValue).toEqual(1);
            expect(component.disablePlus).toBeTrue();
        });
    });

    describe('scoreChange', () => {
        it('should assign the update value and disable minus and plus to true and false', () => {
            component.selectedValue = 0;
            component.teamScores = [0, 1, 2, 3];
            component.counterValueEmitter.emit = jasmine.createSpy('counterValueEmitter.emit');
            component.scoreChange(0);
            expect(component.disableMinus).toBeTrue();
            expect(component.disablePlus).toBeFalse();
            expect(component.counterValueEmitter.emit).toHaveBeenCalledWith(0);
        });
        it('should assign the update value and disable plus and minus to true and false', () => {
            component.selectedValue = 3;
            component.teamScores = [0, 1, 2, 3];
            component.counterValueEmitter.emit = jasmine.createSpy('counterValueEmitter.emit');
            component.scoreChange(0);
            expect(component.disablePlus).toBeTrue();
            expect(component.disableMinus).toBeFalse();
            expect(component.counterValueEmitter.emit).toHaveBeenCalledWith(3);
        });
        it('should assign the update value and disable plus and minus to false and false', () => {
            component.teamScores = [];
            component.scoreChange(0);
            expect(component.disablePlus).toBeFalse();
            expect(component.disableMinus).toBeFalse();
        });
    });
});