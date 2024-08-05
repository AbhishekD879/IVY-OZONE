import { StreamAndBetCategoryComponent } from './stream-and-bet-category.component';

describe('StreamAndBetCategoryComponent', () => {
  let component: StreamAndBetCategoryComponent;
  let dialogService, dialog, globalLoaderService, streamAndBetAPIService;
  beforeEach(() => {
    dialogService = {};
    dialog = {};
    globalLoaderService = {};
    streamAndBetAPIService = {};
    component = new StreamAndBetCategoryComponent(
      dialogService,
      dialog,
      globalLoaderService,
      streamAndBetAPIService
    );
    component.category = {name: 'test', children: [1, 2]} as any;
    component.ngOnInit();
  });

  it('should set initial data', () => {
    expect(component.categoryBackupItems).toEqual(component.category.children);
  });
});
