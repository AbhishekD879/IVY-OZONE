import { fakeAsync, tick } from '@angular/core/testing';
import { YourCallStaticBlockComponent } from './your-call-static-block.component';

describe('BybCustomComponent', () => {
    let component, yourCallService, domSanitizer;

    beforeEach(() => {
        yourCallService = {
            getStaticBlocks: jasmine.createSpy('getStaticBlocks').and.returnValue(Promise.resolve(true as any)),
            getStaticBlock: jasmine.createSpy('getStaticBlock').and.returnValue({htmlMarkup : 'ABC'})
        };

        domSanitizer = {
            bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue(true as any)
        };
        component = new YourCallStaticBlockComponent(yourCallService, domSanitizer);
    });

    describe('ngOnInit', () => {
        it('should call ngOnInit and call domsantiser', fakeAsync(() => {
            component.staticType = true;
            yourCallService.keys =  {page : true};
            component.trustAsHtml = true;
            component.ngOnInit();
            tick();
            expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalled();
        }));

        it('should call ngOnInit and staticType false', fakeAsync(() => {
            component.staticType = false;
            yourCallService.keys =  {page : false};
            component.trustAsHtml = true;
            component.ngOnInit();
            tick();
            expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalled();
        }));

        it('should call with out trust', fakeAsync(() => {
            component.staticType = true;
            component.trustAsHtml = false;
            component.ngOnInit();
            tick();
            expect(domSanitizer.bypassSecurityTrustHtml).not.toHaveBeenCalled();
        }));

        it('should call with a number as type', fakeAsync(() => {
            component.staticType = true;
            component.trustAsHtml = true;
            yourCallService.getStaticBlock = jasmine.createSpy('getStaticBlock').and.returnValue({htmlMarkup : 1});
            component.ngOnInit();
            tick();
            expect(domSanitizer.bypassSecurityTrustHtml).not.toHaveBeenCalled();
        }));
    });
});
