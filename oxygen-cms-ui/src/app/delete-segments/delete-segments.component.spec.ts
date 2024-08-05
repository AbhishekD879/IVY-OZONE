import { Observable, of } from "rxjs";
import { DeleteSegmentsComponent } from "./delete-segments.component";

describe('DisableSegmentsComponent', () => {
    let component: DeleteSegmentsComponent;
    let globalLoaderService;
    let apiClientService;
    let dialogService;

    beforeEach(() => {
        globalLoaderService = {
          showLoader: jasmine.createSpy('showLoader'),
          hideLoader: jasmine.createSpy('hideLoader')
        };

        apiClientService = {
            segmentMethods: jasmine.createSpy('segmentMethods').and.returnValue({
              getSegments: jasmine.createSpy('getSegments').and.returnValue(of({ body: [{ 'name': 'Universal','id':'001' },
                        {'name': 'Cricket','id':'002'},
                        {'name': 'FootBall','id':'003'},
                        {'name': 'Hockey','id':'004'}] })),
              deleteSegments: jasmine.createSpy('deleteSegments').and.returnValue(of({ body: {} }))
            }),
        };

        dialogService = {
            showConfirmDialog: jasmine.createSpy('showConfirmDialog')
                .and.returnValue(Observable.of({}))
                .and.callFake(({ title, message, yesCallback }) => {
                yesCallback();
            })
        };

        component = new DeleteSegmentsComponent(
          globalLoaderService, apiClientService, dialogService
        );
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should call segments in onInit', () => {
        component.ngOnInit();
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(apiClientService.segmentMethods().getSegments).toHaveBeenCalled();
        expect(component.segmentsList.length).toBe(3);
        expect(component.filteredSegments.length).toBe(3);
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    })

    it('should filter the segments on input', () => {
        component.ngOnInit();
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(apiClientService.segmentMethods().getSegments).toHaveBeenCalled();
        expect(component.segmentsList.length).toBe(3);
        expect(component.filteredSegments.length).toBe(3);

        // Giving input 'ck' to filter 'Cricket' and 'Hockey'
        component.onChange('ck');
        expect(component.segmentsList.length).toBe(3);
        expect(component.filteredSegments.length).toBe(2);
    })

    it('should clear the selected segments on', () => {
        component.selectedSegments = ['FootBall','Hockey','Cricket'];
        expect(component.selectedSegments.length).toBe(3);
        expect(component.selectedSegments).toEqual(['FootBall','Hockey','Cricket']);
        component.onClear();

        expect(component.selectedSegments.length).toBe(0);
        expect(component.selectedSegments).toEqual([]);
    })

    it('should remove item from chip', () => {
        component.segmentInput = {
            nativeElement : {
              value: ''
            }
          } as any;
        component.ngOnInit();

        component.selectedSegments = ['FootBall','Hockey','Cricket'];
        expect(component.selectedSegments.length).toBe(3);
        expect(component.selectedSegments).toEqual(['FootBall','Hockey','Cricket']);

        component.removeItem(1);
        expect(component.selectedSegments.length).toBe(2);
        expect(component.selectedSegments).toEqual(['FootBall','Cricket']);
    })

    it('should delete single selected segment', () => {
        apiClientService.segmentMethods().deleteSegments.and.returnValue(of({}));
        component.selectedSegments = ['Cricket'];

        component.ngOnInit();
        expect(component.segmentsList.length).toBe(3);
        expect(component.segmentsList).toEqual(['Cricket','FootBall','Hockey']);
        apiClientService.segmentMethods().getSegments.and.returnValue(of({ body: [{ 'name': 'Universal','id':'001' },
        {'name': 'FootBall','id':'003'},
        {'name': 'Hockey','id':'004'}] }))

        component.delete({name: 'Cricket', selected: true}); //Cricket
        expect(apiClientService.segmentMethods().deleteSegments).toHaveBeenCalledWith('002');
        expect(apiClientService.segmentMethods().getSegments).toHaveBeenCalled();
        expect(component.segmentsList.length).toBe(2);
        expect(component.segmentsList).toEqual(['FootBall','Hockey']);
        expect(component.selectedSegments.length).toBe(0);
        expect(component.selectedSegments).toEqual([]);
    })

    it('should delete multiple selected segments', () => {
        apiClientService.segmentMethods().deleteSegments.and.returnValue(of({}));
        component.selectedSegments = ['Cricket','FootBall'];

        component.ngOnInit();
        expect(component.segmentsList.length).toBe(3);
        expect(component.segmentsList).toEqual(['Cricket','FootBall','Hockey']);
        apiClientService.segmentMethods().getSegments.and.returnValue(of({ body: [{ 'name': 'Universal','id':'001' },
        {'name': 'Hockey','id':'004'}] }))

        component.delete();
        expect(apiClientService.segmentMethods().deleteSegments).toHaveBeenCalledWith('002,003');
        expect(apiClientService.segmentMethods().getSegments).toHaveBeenCalled();
        expect(component.segmentsList.length).toBe(1);
        expect(component.segmentsList).toEqual(['Hockey']);
        expect(component.selectedSegments.length).toBe(0);
        expect(component.selectedSegments).toEqual([]);
    })
});