import { fakeAsync, flush } from '@angular/core/testing';

import { EventsByClassesService } from '@sb/services/eventsByClasses/events-by-classes.service';
import { IClassModel } from '@core/models/class.model';

describe('EventsByClassesService', () => {
  let service: EventsByClassesService;

  let ssRequestHelper;
  let ssUtility;

  const classArr = [{ class: { id: '1' } }, { class: { id: '2' } }, { class: { id: '3' } }];
  const classIds: string[] = ['1', '2', '3'];


  beforeEach(() => {
    ssRequestHelper = {
      getClassesByCategory: jasmine.createSpy().and.returnValue(Promise.resolve({}))
    };
    ssUtility = {
      stripResponse: jasmine.createSpy().and.returnValue(Promise.resolve(classArr))
    };

    service = new EventsByClassesService(ssRequestHelper, ssUtility);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getClasses', () => {
    it('should return classes', fakeAsync(() => {
      service
        .getClasses('1')
        .then((resault) => {
          expect(resault).toEqual(classIds);
          expect(ssRequestHelper.getClassesByCategory).toHaveBeenCalledWith({
            categoryId: '1',
            siteChannels: 'M',
            hasOpenEvent: '&simpleFilter=class.hasOpenEvent'
          });
        });
      flush();
    }));

    it('should return classes from specified channels', fakeAsync(() => {
      service
        .getClasses('2', 'CustomChannels')
        .then((resault) => {
          expect(resault).toEqual(classIds);
          expect(ssRequestHelper.getClassesByCategory).toHaveBeenCalledWith({
            categoryId: '2',
            siteChannels: 'CustomChannels',
            hasOpenEvent: '&simpleFilter=class.hasOpenEvent'
          });
        });
      flush();
    }));
  });

  describe('getClassIds', () => {
    it('should return classes ids', () => {
      expect(service['getClassIds'](classArr as IClassModel[])).toEqual(classIds);
    });
  });

  it('should return classes by params', fakeAsync(() => {
    const params = { categoryId: '1' } as any;
    service
      .getClassesByParams(params)
      .then((result) => {
        expect(result).toEqual(classIds);
        expect(ssRequestHelper.getClassesByCategory).toHaveBeenCalledWith({
          categoryId: '1'
        });
      });
    flush();
  }));
});
