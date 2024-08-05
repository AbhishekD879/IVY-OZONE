
import { SortByOptionsComponent } from './sort-by-options.component';

describe('SortByOptionsComponent', () => {
  let component: SortByOptionsComponent;
  let pubSubService;
  let gtmService;
  let sortByOptionsService;

  beforeEach(() => {
    pubSubService = {
      API: {
        CLOSE_SORT_BY: 'CLOSE_SORT_BY',
        SORT_BY_OPTION: 'SORT_BY_OPTION'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        channelFunction(true);
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };
    sortByOptionsService = {
      set: jasmine.createSpy('set')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    component = new SortByOptionsComponent(pubSubService, sortByOptionsService,gtmService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(pubSubService.subscribe)
      .toHaveBeenCalledWith(component['name'], pubSubService.API.CLOSE_SORT_BY, jasmine.any(Function));
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['name']);
  });

  it('selectSortByOption', () => {
    const option = 'price';
    component.selectSortByOption(option);
    expect(sortByOptionsService.set).toHaveBeenCalledWith(option);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SORT_BY_OPTION, option);
    expect(component['sortBy']).toBe(option);
  });

  it('selectSortByOption with event id', () => {
    const option = 'price';
    component.eventEntityId = '12345';
    component.selectSortByOption(option);

    expect(sortByOptionsService.set).toHaveBeenCalledWith(option);
    expect(pubSubService.publish).toHaveBeenCalledWith('SORT_BY_OPTION12345', option);
    expect(component['sortBy']).toBe(option);
  });

  it('showDropdown', () => {
    component.showDropdown(true);

    expect(component['showSortBy']).toBe(true);
  });

  it('indexNumber', () => {
    expect(component.indexNumber(1)).toBe(1);
  });
});
