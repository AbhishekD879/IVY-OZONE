import { fakeAsync, flush } from '@angular/core/testing';

import { EnhancedMultiplesService } from '@sb/services/enhancedMultiples/enhanced-multiples.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { TimeService } from '@core/services/time/time.service';
import { EventService } from '@sb/services/event/event.service';
import { TemplateService } from '@shared/services/template/template.service';
import environment from '@environment/oxygenEnvConfig';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { IEnhancedConfig } from '@sb/models/enhanced-multiples.model';
import { of } from 'rxjs';

describe('EnhancedMultiplesService', () => {
  let service: EnhancedMultiplesService;
  let siteServerServiceStub = {};
  let timeServiceStub;
  let eventServiceStub;
  let templateServiceStub;
  let sportsConfigService;

  const testStr = 'TestString';

  beforeEach(() => {
    timeServiceStub = {
      createTimeRange: jasmine.createSpy().and.returnValue({
        startDate: testStr,
        endDate: `End${testStr}`
      }),
      getSuspendAtTime: jasmine.createSpy().and.returnValue(testStr)
    };
    siteServerServiceStub = {
      getEnhancedMultiplesEvents: jasmine.createSpy().and.returnValue(Promise.resolve(Array(3))),
      getCategories: {},
      getEventsByClass: jasmine.createSpy('getEventsByClass').and.returnValue(of([])),
    };
    templateServiceStub = {
      isMultiplesEvent: jasmine.createSpy('isMultiplesEvent'),
      addIconsToEvents: jasmine.createSpy().and.returnValue(Promise.resolve([{ svgId: testStr }])),
      getEventCorectedDay: jasmine.createSpy().and.returnValue(testStr),
    };
    eventServiceStub = {
      cachedEvents: jasmine.createSpy().and
        .returnValue(() => Promise.resolve([{ startTime: testStr }])),
      cachedEventsByFn: jasmine.createSpy().and
        .returnValue(() => Promise.resolve([{ id: 1, events: [{ startTime: testStr }] }])),
    };

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.callFake((sportName: string) => {
        return of({
          sportConfig: {
            config: {
              request: {
                categoryId: sportName === 'squash' ? '' : '21'
              }
            }
          }
        });
      })
    };

    service = new EnhancedMultiplesService(
      siteServerServiceStub as SiteServerService,
      timeServiceStub as TimeService,
      eventServiceStub as EventService,
      templateServiceStub as TemplateService,
      sportsConfigService as SportsConfigService
    );
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getEnhancedMultiplesEvents', () => {
    it(`should set 'eventCorectedDay' property for each event`, fakeAsync(() => {
      service.getEnhancedMultiplesEvents(null)
        .subscribe(res => {
          expect(res).toEqual(jasmine.arrayContaining([jasmine.objectContaining({ eventCorectedDay: jasmine.any(String) })]) as any);
        });

      flush();
    }));
  });

  describe('getRacingEnhancedMultiplesEvents', () => {
    it(`should set 'eventCorectedDay' property for each event`, fakeAsync(() => {
      service.getRacingEnhancedMultiplesEvents('horseracing')
        .subscribe(res => {
          expect(res).toEqual(jasmine.arrayContaining([jasmine.objectContaining({ eventCorectedDay: jasmine.any(String) })]) as any);
        });
      flush();
    }));
  });

  describe('enhancedRacingMultiplesEvents', () => {
    it(`should set requestParams to getEventsByClass and filter events`, fakeAsync(() => {
      service['enhancedRacingMultiplesEvents']({})
        .subscribe(res => {
          expect(service['siteServerService'].getEventsByClass).toHaveBeenCalledWith({});
          expect(res).toEqual([]);
        });
      flush();
    }));
  });

  describe('getAllEnhancedMultiplesEvents', () => {
    it(`should set 'eventCorectedDay' property for each event`, fakeAsync(() => {
      service.getAllEnhancedMultiplesEvents()
        .subscribe(() => {
          expect(service['templateService'].addIconsToEvents)
            .toHaveBeenCalledWith(jasmine.arrayContaining([jasmine.objectContaining({ eventCorectedDay: jasmine.any(String) })]));
        });

      flush();
    }));

    it(`should flatten events`, fakeAsync(() => {
      service['eventService'].cachedEventsByFn = jasmine.createSpy().and
        .returnValue(() => Promise.resolve([{
          events: [
            { id: 1 },
            [[{ id: 2 }], { id: 3 }]
          ]
        }]));

      service.getAllEnhancedMultiplesEvents()
        .subscribe(() => {
          expect(service['templateService'].addIconsToEvents)
            .toHaveBeenCalledWith(jasmine.arrayContaining([jasmine.objectContaining({ id: 3 })]));
        });

      flush();
    }));

    it(`should add icons to events`, fakeAsync(() => {
      service.getAllEnhancedMultiplesEvents()
        .subscribe(() => {
          expect(service['templateService'].addIconsToEvents).toHaveBeenCalledTimes(1);
        });

      flush();
    }));
  });

  describe('enhancedMultiplesHomeEvents', () => {
    const sportEventStub = [{ categoryId: '1' }, { categoryId: '2' }, { categoryId: '3' }];
    const categoryIds = ['1', '2', '3'];

    it('should return categoryIds', fakeAsync(() => {
      spyOn<any>(service, 'enhancedMultiplesEvents')
        .and.returnValue(Promise.resolve(sportEventStub));
      spyOn<any>(service['siteServerService'], 'getCategories')
        .and.returnValue(Promise.resolve([]));

      service['enhancedMultiplesHomeEvents']({})
        .then(() => {
          expect(service['siteServerService'].getCategories)
            .toHaveBeenCalledWith(categoryIds);
        });

      flush();
    }));

    it(`should filter events by 'categoryId'`, fakeAsync(() => {
      const categoriesStub = [{ id: '2', events: sportEventStub.slice() }];
      const categoriesRez = [{ id: '2', events: [{ categoryId: '2' }] }];

      spyOn<any>(service, 'enhancedMultiplesEvents')
        .and.returnValue(Promise.resolve(sportEventStub));
      spyOn<any>(service['siteServerService'], 'getCategories')
        .and.returnValue(Promise.resolve(categoriesStub));

      service['enhancedMultiplesHomeEvents']({})
        .then((result) => {
          expect(result).toEqual(categoriesRez as any);
        });

      flush();
    }));

    it(`should return empty array if events has Not 'categoryId'`, fakeAsync(() => {
      spyOn<any>(service, 'enhancedMultiplesEvents')
        .and.returnValue(Promise.resolve([]));

      service['enhancedMultiplesHomeEvents']({})
        .then((result) => {
          expect(result).toEqual([]);
        });

      flush();
    }));

  });

  describe('enhancedMultiplesEvents', () => {
    it(`should set 'startTime' & 'endTime' for requestParams`, () => {
      service['enhancedMultiplesEvents']({});

      expect(service['siteServerService'].getEnhancedMultiplesEvents)
        .toHaveBeenCalledWith({
          startTime: testStr,
          endTime: `End${ testStr }`,
          suspendAtTime: testStr
        });
    });

    it(`should set 'suspendAtTime' for requestParams`, () => {
      timeServiceStub.createTimeRange = jasmine.createSpy('createTimeRange').and.returnValue({});
      service['enhancedMultiplesEvents']({});

      expect(service['siteServerService'].getEnhancedMultiplesEvents)
        .toHaveBeenCalledWith({ suspendAtTime: testStr });
    });

    it('should return all events if all are Multiple', fakeAsync(() => {
      service['templateService']['isMultiplesEvent'] = jasmine.createSpy().and.returnValue(true);

      service['enhancedMultiplesEvents']({})
        .then(res => {
          expect(res.length).toEqual(3);
        });
      flush();
    }));

    it('should return empty array if all events are Not Multiple', fakeAsync(() => {
      service['enhancedMultiplesEvents']({})
        .then(res => {
          expect(res).toEqual([]);
        });
      flush();
    }));
  });

  describe('formConfig', () => {
    it('should add extensions data if it available', fakeAsync(() => {
      const categoryId = '21';

      service['formConfig'](testStr).subscribe((config: IEnhancedConfig) => {
        expect(config).toEqual(jasmine.objectContaining({ categoryId }));
      });

      flush();
    }));

    it('should return object contain horseracing.id', fakeAsync(() => {
      const categoryId = environment.CATEGORIES_DATA.racing.horseracing.id;

      service['formConfig']('horseracing').subscribe((config: IEnhancedConfig) => {
        expect(config).toEqual(jasmine.objectContaining({ categoryId }));
      });

      flush();
    }));

    it(`should return object contained date with adding 'Multiples' word`, fakeAsync(() => {
      const date = `${testStr}Multiples`;

      service['formConfig'](null, testStr).subscribe((config: IEnhancedConfig) => {
        expect(config).toEqual(jasmine.objectContaining({ date }));
      });

      flush();

      // expect(service['formConfig'](null, testStr))
      //   .toEqual(jasmine.objectContaining({ date }));
    }));

    it(`should return enhancedConfig`, fakeAsync(() => {
      const date = `${testStr}Multiples`;
      const categoryId = environment.CATEGORIES_DATA.racing.horseracing.id;
      const enhancedConfigStub = {
        siteChannels: 'M',
        isNotStarted: true,
        typeName: '|Enhanced Multiples|',
        categoryId,
        display: testStr,
        date
      };

      service['formConfig']('horseracing', testStr).subscribe((config: IEnhancedConfig) => {
        expect(config).toEqual(enhancedConfigStub);
      });

      flush();
    }));

    it(`should return enhancedConfig with no categoryId`, fakeAsync(() => {
      const date = `${testStr}Multiples`;
      const enhancedConfigStub = {
        siteChannels: 'M',
        isNotStarted: true,
        typeName: '|Enhanced Multiples|',
        categoryId: '',
        display: testStr,
        date
      };

      service['formConfig']('squash', testStr).subscribe((config: IEnhancedConfig) => {
        expect(config).toEqual(enhancedConfigStub);
      });

      flush();
    }));
  });
});
