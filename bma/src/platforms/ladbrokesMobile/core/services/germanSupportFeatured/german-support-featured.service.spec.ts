import { GermanSupportFeaturedService } from './german-support-featured.service';
import { featuredModuleMock, featuredDataMock } from './german-support-featured.mock';

describe('GermanSupportFeaturedService', () => {
  let service: GermanSupportFeaturedService;
  let germanSupportService;
  let coreTools;

  beforeEach(() => {
    germanSupportService = {
      isGermanUser: jasmine.createSpy().and.returnValue(true),
      restrictedSportsCategoriesIds: ['19', '21', '161'] // 19 - GH, 21 - HR, 161 - INT TOTE
    };

    coreTools = {
      deepClone: d => JSON.parse(JSON.stringify(d))
    };
    spyOn(console, 'warn');

    service = new GermanSupportFeaturedService(germanSupportService, coreTools);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#restrictedSportsCategoriesIds should contain restricted sport categories IDs', () => {
    expect(service['restrictedSportsCategoriesIds']).toEqual(['19', '21', '161']);
  });

  it('#nonDataModuleFilter should return module unmodified', () => {
    expect(service['nonDataModuleFilter'](<any>{ asd: 'asd', zxc: 'zxc' })).toEqual(<any>{ asd: 'asd', zxc: 'zxc' });
  });

  it('#isEntityAllowed should return false when module or event in module belongs to restricted category', () => {
    expect(service['isEntityAllowed'](<any>{ asd: 'asd', categoryId: '21' })).toEqual(false);
  });

  it('#isEntityAllowed should return true when module or event in module NOT belongs to restricted category', () => {
    expect(service['isEntityAllowed'](<any>{ asd: 'asd', categoryId: '15' })).toEqual(true);
  });

  it('#isEntityAllowed should return true when module or event in module NOT have categoryId property', () => {
    expect(service['isEntityAllowed'](<any>{ asd: 'asd' })).toEqual(true);
  });

  it('#eventsModuleFilter should NOT filter modules with type = EventsModule', () => {
    expect(service['eventsModuleFilter'](<any>{ '@type': 'asd' })).toEqual(true);
  });

  it('#eventsModuleFilter should NOT filter modules with type = EventsModule if module with NOT restricted categoryId', () => {
    expect(service['eventsModuleFilter'](<any>{ '@type': 'asd', categoryId: '15' })).toEqual(true);
  });

  it('#eventsModuleFilter should filter modules with type = EventsModule if module with restricted categoryId', () => {
    expect(service['eventsModuleFilter'](<any>{ '@type': 'asd', categoryId: '21' })).toEqual(true);
  });

  it('#dataModuleFilter should filter events within the modules with restricted categoryId and ' +
    'return null if all events were filtered and module became empty', () => {
    const featuredmodule = coreTools.deepClone(featuredModuleMock);
    featuredmodule.data[0].categoryId = '21';
    featuredmodule.data[1].categoryId = '21';
    featuredmodule.data[2].categoryId = '21';
    expect(service['dataModuleFilter'](featuredmodule)).toEqual(null);
  });

  it('#dataModuleFilter should filter events within the modules with restricted categoryIds', () => {
    const featuredmodule = coreTools.deepClone(featuredModuleMock);
    featuredmodule.data[0].categoryId = '21';
    expect(service['dataModuleFilter'](featuredmodule).data.length).toEqual(2);
  });

  describe('#moduleFilterHandler', () => {
    it('should NOT filter data', () => {
      const featuredmodule = coreTools.deepClone(featuredModuleMock);
      featuredmodule['@type'] = 'unKnownModuleType';

      expect(service['moduleFilterHandler'](featuredmodule)).toEqual(featuredmodule);
    });

    it('should filter data with correct method', () => {
      const featuredmodule = coreTools.deepClone(featuredModuleMock);
      featuredmodule['@type'] = 'SurfaceBetModule';
      service['modulesFilters'].SurfaceBetModule = jasmine.createSpy();

      service['moduleFilterHandler'](featuredmodule);
      expect(service['modulesFilters'].SurfaceBetModule).toHaveBeenCalled();
    });
  });

  it('#filterData should NOT filter modules when no featured data', () => {
    expect(service['filterData'](null)).toEqual(null);
  });

  it(`#filterData should filter modules and events within the modules -> only 1 should be filtered because in
      module[2] still left some not restricted events`, () => {
    const featuredData = coreTools.deepClone(featuredDataMock);
    featuredData.modules[0].categoryId = '21';
    featuredData.modules[2].data[0].categoryId = '21';
    expect(service['filterData'](featuredData).modules.length).toEqual(2);
  });

  it(`#filterData should filter modules and events within the modules -> only 2 should be filtered because in
      module[2] all restricted events were filtered`, () => {
    const featuredData = coreTools.deepClone(featuredDataMock);
    featuredData.modules[0].categoryId = '21';
    featuredData.modules[2].data[0].categoryId = '21';
    featuredData.modules[2].data[1].categoryId = '21';
    featuredData.modules[2].data[2].categoryId = '21';
    expect(service['filterData'](featuredData).modules.length).toEqual(1);
  });

  it(`#getInitialData should NOT filter data when user is NOT from German`, () => {
    const featuredData = coreTools.deepClone(featuredDataMock);
    service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);
    expect(service['getInitialData'](featuredData)).toEqual(featuredData);
    expect(service['getInitialData'](featuredData).modules.length).toEqual(3);
  });

  it(`#getInitialData should filter data when user is from German`, () => {
    const featuredData = coreTools.deepClone(featuredDataMock);
    featuredData.modules[0].categoryId = '21';
    featuredData.modules[2].data[0].categoryId = '21';
    featuredData.modules[2].data[1].categoryId = '21';
    featuredData.modules[2].data[2].categoryId = '21';
    expect(service['getInitialData'](featuredData).modules.length).toEqual(1);
  });

  describe('#getActualData', () => {

    it('should NOT return any data on init - in chase when no latestFeaturedData', () => {
      expect(service['getActualData']()).toEqual(null);
    });

    it('should NOT return any data if user Was German and now he is still german', () => {
      service['latestFeaturedData'] = coreTools.deepClone(featuredDataMock);
      service['userWasGerman'] = true;
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(true);
      expect(service['getActualData']()).toEqual(null);
    });

    it('should NOT return any data if user Was NOT German and now he is still NOT german', () => {
      service['latestFeaturedData'] = coreTools.deepClone(featuredDataMock);
      service['userWasGerman'] = false;
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);
      expect(service['getActualData']()).toEqual(null);
    });

    it('should return data if user Was German and now he is NOT german', () => {
      const featuredData = coreTools.deepClone(featuredDataMock);
      service['latestFeaturedData'] = featuredData;
      service['userWasGerman'] = true;
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);
      const data = service['getActualData']();
      expect(data).toEqual(featuredData);
      expect(data.modules.length).toEqual(3);
      expect(service['userWasGerman']).toEqual(false);
    });

    it('should return data if user Was NOT German and now he is german', () => {
      const featuredData = coreTools.deepClone(featuredDataMock);
      featuredData.modules[0].categoryId = '21';
      featuredData.modules[2].data[0].categoryId = '21';
      featuredData.modules[2].data[1].categoryId = '21';
      featuredData.modules[2].data[2].categoryId = '21';
      service['latestFeaturedData'] = featuredData;
      service['userWasGerman'] = false;
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(true);
      const data = service['getActualData']();
      expect(data).toEqual(service['filterData'](featuredData));
      expect(data.modules.length).toEqual(1);
      expect(service['userWasGerman']).toEqual(true);
    });

  });
});
