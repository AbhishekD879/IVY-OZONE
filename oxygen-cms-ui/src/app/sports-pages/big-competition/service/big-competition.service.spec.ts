import {BigCompetitionService} from './big-competition.service';

describe('BigCompetitionService', () => {
  let service;

  beforeEach(() => {
    service = new BigCompetitionService();
  });

  describe('breadcrumbParser', () => {
    beforeEach(() => {
      spyOn(service, 'pushBreadcrumbData').and.callThrough();
    });

    it('should show breadcrumb for competitionId', () => {
      service.breadcrumbParser({}, 'competitionId');

      expect(service.pushBreadcrumbData).toHaveBeenCalledWith(['competition'], jasmine.any(Object));
    });

    it('should show breadcrumb for tabId', () => {
      service.breadcrumbParser({}, 'tabId');

      expect(service.pushBreadcrumbData).toHaveBeenCalledWith(['competition', 'tab'], jasmine.any(Object));
    });

    it('should show breadcrumb for subTabId', () => {
      service.breadcrumbParser({}, 'subTabId');

      expect(service.pushBreadcrumbData).toHaveBeenCalledWith(
        ['competition', 'tab', 'subtab'], jasmine.any(Object));
    });

    it('should show breadcrumb for moduleId', () => {
      service.breadcrumbParser({}, 'moduleId');

      expect(service.pushBreadcrumbData).toHaveBeenCalledWith(
        ['competition', 'tab', 'module'], jasmine.any(Object));
    });

    it('should show breadcrumb for subTabAndModuleId', () => {
      service.breadcrumbParser({}, 'subTabAndModuleId');

      expect(service.pushBreadcrumbData).toHaveBeenCalledWith(
        ['competition', 'tab', 'subtab', 'module'], jasmine.any(Object));
    });
  });
});
