import { FreeRideDomService } from './freeRideDom.service';

describe('@FreeRideDomService', () => {

    let service: FreeRideDomService,
        rendererService;

    beforeEach(() => {

        rendererService = {
            renderer: {

                removeChild: jasmine.createSpy(),
                createElement: jasmine.createSpy().and.returnValue({ id: 1 }),
                setProperty: jasmine.createSpy(),
                addClass: jasmine.createSpy(),
                appendChild: jasmine.createSpy(),
            }
        };


        service = new FreeRideDomService(
            rendererService

        );
    });

    afterEach(() => {
        service = null;
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    describe('removeElem', () => {
        it('should call renderer.removeChild if both elements available', () => {
            const el1: HTMLElement = { scrollIntoView: () => { } } as any;
            const el2: HTMLElement = { scrollIntoView: () => { } } as any;

            service.removeElem(el1, el2);

            expect(service['rendererService'].renderer.removeChild).toHaveBeenCalled();
        });

        it('should call renderer.removeChild if both elements available', () => {
            const el1: HTMLElement = { scrollIntoView: () => { } } as any;
            let el2: HTMLElement;

            service.removeElem(el1, el2);

            expect(service['rendererService'].renderer.removeChild).not.toHaveBeenCalled();
        });
    });

    describe('createDOMElements', () => {
        it('should create Element with  elemText', () => {
            service.createDOMElements([{ 'elem': ['div', 'msg', 'question', 1] }]);
            expect(service['rendererService'].renderer.createElement).toHaveBeenCalled();
            expect(service['rendererService'].renderer.setProperty).toHaveBeenCalled();
        });
        it('should not call renderer.setProperty if msg is not given', () => {
            service.createDOMElements([{ 'elem': ['div', undefined, 'question', 1] }]);
            expect(service['rendererService'].renderer.setProperty).not.toHaveBeenCalled();
        });
        it('should not call renderer.addClass if question is not given', () => {
            service.createDOMElements([{ 'elem': ['div', 'msg', undefined, 1] }]);
            expect(service['rendererService'].renderer.addClass).not.toHaveBeenCalled();
        });
        it('should not call renderer.addClass if stepNum is not given', () => {
            service.createDOMElements([{ 'elem': ['div', 'msg', 'question'] }]);
            expect(service['rendererService'].renderer.addClass).toHaveBeenCalled();
        });
        it('should set listOfElementsCreated if 2 data is given', () => {
            service.createDOMElements([{ 'elem': ['div', 'msg', 'question', 1] }, { 'elem1': ['div', 'msg', 'question1', 1] }]);
            expect(service['rendererService'].renderer.createElement).toHaveBeenCalled();
            expect(service['rendererService'].renderer.setProperty).toHaveBeenCalled();
        });
    });

    describe('appendDomElems', () => {
        it('should call renderer.appendChild if both element has been given', () => {
            const el1: HTMLElement = { scrollIntoView: () => { } } as any;
            const el2: HTMLElement = { scrollIntoView: () => { } } as any;

            service.appendDomElems([{ parentElem: el1, childElem: el2 }]);
            expect(service['rendererService'].renderer.appendChild).toHaveBeenCalled();
        });

        it('should not call renderer.appendChild if childElement is not given', () => {
            const el1: HTMLElement = { scrollIntoView: () => { } } as any;
            let el2: HTMLElement;

            service.appendDomElems([{ parentElem: el1, childElem: el2 }]);
            expect(service['rendererService'].renderer.appendChild).not.toHaveBeenCalled();
        });
    });
});