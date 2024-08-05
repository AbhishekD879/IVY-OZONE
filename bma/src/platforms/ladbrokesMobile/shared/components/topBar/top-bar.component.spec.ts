import { TopBarComponent } from './top-bar.component';

describe('TopBarComponent', () => {
  let component: TopBarComponent;
  let localeService;
  let changeDetectorRef;
  let pubSubService;
  let domToolsService;
  let elementRef;
  let seoDataService;

  beforeEach(() => {
    localeService = {};
    changeDetectorRef = {};
    pubSubService = {};
    domToolsService = {};
    elementRef = {};
    component = new TopBarComponent(localeService, changeDetectorRef, pubSubService, domToolsService, elementRef, seoDataService);
  });

  it('should create extended component', () => {
    expect(component).toBeDefined();
  });
});
