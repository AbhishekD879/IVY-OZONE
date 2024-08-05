import { YcStaticBlocksListComponent } from './yc-static-blocks-list.component';
import { of } from 'rxjs';

describe('YcStaticBlocksListComponent', () => {
  let component: YcStaticBlocksListComponent;
  let dialog, dialogService, router, staticBlockAPIService;

  beforeEach(() => {
    dialog = {};
    dialogService = {};
    router = {};
    staticBlockAPIService = {
      getStaticBlocksList: jasmine.createSpy('getStaticBlocksList').and.returnValue(of({ body: 'test' }))
    };
    component = new YcStaticBlocksListComponent(
      dialog,
      dialogService,
      staticBlockAPIService,
      router
    );

    component.ngOnInit();

  });

  it('should call getStaticBlocksList', () => {
    const data = 'test' as any;
    expect(staticBlockAPIService.getStaticBlocksList).toHaveBeenCalled();
    expect(component.yourCallStaticBlockData).toEqual(data);
  });
});
