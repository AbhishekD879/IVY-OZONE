
import { CmsToolsService } from '@core/services/cms/cms.tools';

describe('CmsToolsService', () => {
  let service: CmsToolsService;

  let filtersService, navigationUriService, items;

  beforeEach(() => {
    items = [
      {
        targetUri: 'targetTest',
        svgId: 'svgTest'
      }
    ];
    filtersService = {
      filterLink: jasmine.createSpy().and.callFake(el => `${el}1`)
    }; 
 
    navigationUriService = {
      isAbsoluteUri: jasmine.createSpy('isAbsoluteUri')
    };
    service = new CmsToolsService(filtersService, navigationUriService);
  });

  it('#processResult should process the result', () => {
    const defer = {
      resolve: jasmine.createSpy('deferResolve')
    };
    const initialSvgValue = items[0].svgId;
    const processedData = service.processResult(items, defer);
    expect(`${processedData[0].targetUriCopy}1`).toBe(items[0].targetUri);
    expect(`${processedData[0].sportName}1`).toBe(items[0].targetUri);
    expect(navigationUriService.isAbsoluteUri).toHaveBeenCalled();
    expect(processedData[0].svgId).toBe(`${initialSvgValue}`);
    expect(defer.resolve).toHaveBeenCalled();
  });

  it('#modifyLink should modify the link', () => {
    const initialSvgValue = items[0].svgId;
    service.CMS_ROOT_URI = 'https://test.com';
    service['modifyLink'](items[0], ['svgId']);
    expect(items[0].svgId).toBe(service.CMS_ROOT_URI + initialSvgValue);
  });

  it('#filterLinks should filter the links', () => {
    service['filterLinks'](items[0]);
    expect(items[0].targetUri).toBe('targetTest1');
    expect(items[0].svgId).toBe('svgTest');
  });

});
