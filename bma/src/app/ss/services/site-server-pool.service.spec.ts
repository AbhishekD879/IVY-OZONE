import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { LoadByPortionsService } from '@ss/services/load-by-portions.service';
import { SiteServerUtilityService } from '@core/services/siteServerUtility/site-server-utility.service';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import { SiteServerPoolService } from '@ss/services/site-server-pool.service';

describe('SiteServerPoolService', () => {
  let service,
    ssRequestHelper: SiteServerRequestHelperService,
    simpleFilters: SimpleFiltersService,
    loadByPortions: LoadByPortionsService,
    ssUtility: SiteServerUtilityService,
    buildUtility: BuildUtilityService;

  const genFilterParams = {
    poolProvider: 'poolProviderFilter',
    poolIsActive: 'poolIsActiveFilter',
    poolTypes: 'poolTypesFilter',
  };

  beforeEach(() => {
    ssRequestHelper = {
      getPool: jasmine.createSpy(),
      getPoolForEvent: jasmine.createSpy(),
      getPoolForClass: jasmine.createSpy(),
      getPoolToPoolValue: jasmine.createSpy()
    } as any;
    simpleFilters = {
      genFilters: jasmine.createSpy().and.returnValue({
        genFilters: 'genFilters'
      })
    } as any;
    loadByPortions = {
      get: jasmine.createSpy().and.callFake(
        (method, reqparams, idsPropName, ids) => {
          method('test_data');
          return Promise.resolve({});
        }
      )
    } as any;
    ssUtility = {
      queryService: jasmine.createSpy()
        .and.callFake((method, reqParams) => {
          method();
          return Promise.resolve({});
        })
    } as any;
    buildUtility = {
      poolsBuilder: jasmine.createSpy()
    } as any;

    service = new SiteServerPoolService(
      ssRequestHelper,
      simpleFilters,
      loadByPortions,
      ssUtility,
      buildUtility
    );
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  it('#getPools should get all pools without any id', () => {
    const params = Object.assign({
      idsPropName: 'idsPropName'
    }, genFilterParams);

    service.getPools(params).subscribe(() => {
      expect(simpleFilters.genFilters).toHaveBeenCalledWith(genFilterParams as any);
      expect(ssUtility.queryService).toHaveBeenCalledWith(
        jasmine.any(Function),
        { simpleFilters: { genFilters: 'genFilters' } }
      );
      expect(buildUtility.poolsBuilder).toHaveBeenCalledWith({} as any);
      expect(ssRequestHelper.getPool).toHaveBeenCalled();
    });
  });

  it('#getPoolsForEvent should get pools for certain event using class ids', () => {
    const params = Object.assign({
      idsPropName: 'idsPropName',
      classIds: 'classIdsValue'
    }, genFilterParams);

    service.getPoolsForEvent(params).subscribe(() => {
      expect(simpleFilters.genFilters).toHaveBeenCalledWith(genFilterParams as any);
      expect(loadByPortions.get).toHaveBeenCalledWith(
        jasmine.any(Function),
        { simpleFilters: { genFilters: 'genFilters' } },
        'classIds',
        'classIdsValue' as any
      );
      expect(buildUtility.poolsBuilder).toHaveBeenCalledWith({} as any);
      expect(ssRequestHelper.getPoolForEvent).toHaveBeenCalledWith('test_data' as any);
    });
  });

  it('#getPoolsForClass should get pools using events ids', () => {
    const params = Object.assign({
      idsPropName: 'idsPropName',
      classIds: 'classIdsValue',
      eventsIds: 'eventsIdsValue'
    }, genFilterParams);

    service.getPoolsForClass(params).subscribe(() => {
      expect(simpleFilters.genFilters).toHaveBeenCalledWith(genFilterParams as any);
      expect(loadByPortions.get).toHaveBeenCalledWith(
        jasmine.any(Function),
        { simpleFilters: { genFilters: 'genFilters' } },
        'eventsIds',
        'eventsIdsValue' as any
      );
      expect(buildUtility.poolsBuilder).toHaveBeenCalledWith({} as any);
      expect(ssRequestHelper.getPoolForClass).toHaveBeenCalledWith('test_data' as any);
    });
  });

  it('#getPoolToPoolValue should get pools by pool ids', () => {
    const params = Object.assign({
      idsPropName: 'idsPropName',
      classIds: 'classIdsValue',
      eventsIds: 'eventsIdsValue',
      poolsIds: 'poolsIdsValue'
    }, genFilterParams);

    service.getPoolToPoolValue(params).then(() => {
      expect(simpleFilters.genFilters).toHaveBeenCalledWith(genFilterParams as any);
      expect(loadByPortions.get).toHaveBeenCalledWith(
        jasmine.any(Function),
        { simpleFilters: { genFilters: 'genFilters' } },
        'poolsIds',
        'poolsIdsValue' as any
      );
      expect(buildUtility.poolsBuilder).toHaveBeenCalledWith({} as any);
      expect(ssRequestHelper.getPoolToPoolValue).toHaveBeenCalledWith('test_data' as any);
    });
  });
});
