import { InPlayStorageService } from './in-play-storage.service';
import { InPlayStorageService as AppInPlayStorageService } from '@app/inPlay/services/inplayStorage/in-play-storage.service';

describe('InPlayStorageService', () => {
  let service: InPlayStorageService;
  let windowRefService;
  let pubSubService;
  let wsUpdateEventService;
  let cmsService;
  let routingState;
  let germanSupportInPlayService;
  const ribbonData = {
    items: [
      { id: 1, categoryId: 19 }, // GH
      { id: 2, categoryId: 21 }, // HR
      { id: 3, categoryId: 161 }, // INT Tote
      { id: 4, categoryId: 16 }, // football
    ]
  };

  const structureData = {
    data: {
      liveStream: {
        eventCount: 2,
        eventsBySports: [],
        eventsIds: [1, 2]
      },
      livenow: {
        eventCount: 2,
        eventsBySports: [],
        eventsIds: [1, 2]
      },
      upcoming: {
        eventCount: 2,
        eventsBySports: [],
        eventsIds: [1, 2]
      }
    }
  };

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy()
      }
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      API: {
        EVENT_COUNT_UPDATE: 'EVENT_COUNT_UPDATE'
      }
    };

    wsUpdateEventService = {
      subscribe: jasmine.createSpy()
    };

    routingState = {
      getCurrentUrl: jasmine.createSpy()
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy()
    };

    routingState = {
      getCurrentUrl: jasmine.createSpy().and.returnValue('fakeUrl')
    };

    germanSupportInPlayService = {
      getGeFilteredRibbonItemsForInPlay: jasmine.createSpy().and.returnValue(ribbonData),
      applyFiltersToStructureData: jasmine.createSpy().and.returnValue(ribbonData)
    };

    service = new InPlayStorageService(
      windowRefService,
      pubSubService,
      wsUpdateEventService,
      cmsService,
      routingState,
      germanSupportInPlayService
    );
  });

  it('#updateRibbonData - should run german support filters and run inherited updateRibbonData', () => {
    const items = ribbonData.items;
    spyOn(AppInPlayStorageService.prototype, 'updateRibbonData');

    service.updateRibbonData(<any>ribbonData);

    expect(service['germanSupportInPlayService'].getGeFilteredRibbonItemsForInPlay).toHaveBeenCalledWith(items as any);
    expect(AppInPlayStorageService.prototype.updateRibbonData).toHaveBeenCalledWith(ribbonData as any);
  });

  it('#onStructureUpdate - should run german support filters and run inherited onStructureUpdate', () => {
    const data = structureData.data;
    spyOn(AppInPlayStorageService.prototype, 'onStructureUpdate');

    service.onStructureUpdate(<any>structureData);

    expect(service['germanSupportInPlayService'].applyFiltersToStructureData).toHaveBeenCalledWith(data);
    expect(AppInPlayStorageService.prototype.onStructureUpdate).toHaveBeenCalledWith(structureData as any);
  });

});
