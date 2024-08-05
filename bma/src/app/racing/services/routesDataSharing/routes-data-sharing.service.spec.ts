import { RoutesDataSharingService } from '@racing/services/routesDataSharing/routes-data-sharing.service';

describe('RoutesDataSharingService', () => {
  let service: RoutesDataSharingService;

  beforeEach(() => {
    service = new RoutesDataSharingService();
  });

  it('setRacingTabs', () => {
    service.setRacingTabs('horseracing', [1, 2]);
    expect(service.availableTabs.horseracing).toEqual([1, 2]);
  });

  it('getRacingTabs', () => {
    service.setRacingTabs('horseracing', [1, 2]);
    expect(service.getRacingTabs('horseracing')).toEqual([1, 2]);
  });

  it('activeTabId', () => {
    service['activeTabIdSource'] = {
      next: jasmine.createSpy()
    } as any;
    service.updatedActiveTabId('1');
    expect(service['activeTabIdSource'].next).toHaveBeenCalledWith('1');
  });

  it('updatedHasSubHeader', () => {
    service['hasSubHeaderSource'] = {
      next: jasmine.createSpy()
    } as any;
    service.updatedHasSubHeader(true);
    expect(service['hasSubHeaderSource'].next).toHaveBeenCalledWith(true);
  });
});
