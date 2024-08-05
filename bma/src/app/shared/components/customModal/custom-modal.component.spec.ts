import { fakeAsync, tick } from '@angular/core/testing';
import { ModalComponent } from './custom-modal.component';

describe('ModalComponent', () => {
    let component: ModalComponent;
    let elementRef;
    let changeDetectorRef;

    beforeEach(() => {
        elementRef = {
            nativeElement: {
                querySelector: jasmine.createSpy().and.returnValue(':scope modal > .modal')
            }
        } as any;
        changeDetectorRef = {
            markForCheck: jasmine.createSpy('markForCheck')
        };
        component = new ModalComponent(elementRef, changeDetectorRef);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('ngOnDestroy', () => {
        component.close = jasmine.createSpy('close');
        component.ngOnDestroy();
        expect(component.close).toHaveBeenCalled();
    })

    it('open', fakeAsync(() => {

        component.open();
        tick();

        expect(component.visibleAnimate).toBeTrue();
    }));

    it('close', fakeAsync(() => {

        component.close();
        tick(200);

        expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    }));

    it('isTopMost', () => {

        component.isTopMost();

        expect(component.isTopMost()).toBeFalsy();
    });

    it('should call close function if all conditions are met', () => {
        component.closeOnOutsideClick = true;
        component.close = jasmine.createSpy('close');
        component.isTopMost = jasmine.createSpy('isTopMost').and.returnValue(true);
        const mouseEvent: any = {
            preventDefault: jasmine.createSpy(),
            target: {
                classList: {
                    contains: jasmine.createSpy().and.returnValue(true)
                }
            }
        };
        component.onContainerClicked(mouseEvent);
        expect(component.close).toHaveBeenCalled();
    });
    it('should not call close function if all conditions are not met', () => {
        component.closeOnOutsideClick = false;
        component.close = jasmine.createSpy('close');
        component.isTopMost = jasmine.createSpy('isTopMost').and.returnValue(true);
        const mouseEvent: any = {
            preventDefault: jasmine.createSpy(),
            target: {
                classList: {
                    contains: jasmine.createSpy().and.returnValue(true)
                }
            }
        };
        component.onContainerClicked(mouseEvent);
        expect(component.close).not.toHaveBeenCalled();
    });

    it('should not call close function if all conditions are  met', () => {

        component.close = jasmine.createSpy('close');
        component.isTopMost = jasmine.createSpy('isTopMost').and.returnValue(true);
        const event: any = {
            key: 'Escape',
        };
        component.onKeyDownHandler(event);
        expect(component.close).toHaveBeenCalled();
    });

    it('should not call close function if all conditions are not met', () => {

        component.close = jasmine.createSpy('close');
        component.isTopMost = jasmine.createSpy('isTopMost').and.returnValue(false);
        const event: any = {
            key: 'Escape',
        };
        component.onKeyDownHandler(event);
        expect(component.close).not.toHaveBeenCalled();
    });
});
