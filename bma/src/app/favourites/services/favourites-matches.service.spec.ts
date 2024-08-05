import { fakeAsync, tick } from '@angular/core/testing';

import { FavouritesMatchesService } from './favourites-matches.service';
import { IMatch } from '@sb/components/matchResultsSportTab/match.model';

describe('FavouritesMatchesService', () => {
  let service;

  let eventService;
  let cacheEventsService;
  let templateService;
  let filtersService;
  let channelService;
  let pubSubService;

  beforeEach(() => {
    eventService = {
      favouritesMatches: jasmine.createSpy('favouritesMatches').and.returnValue(Promise.resolve([{}]))
    };

    cacheEventsService = {
      store: jasmine.createSpy('store')
    };

    templateService = {
      addIconsToEvents: jasmine.createSpy('addIconsToEvents'),
      getEventCorectedDay: jasmine.createSpy('getEventCorectedDay'),
      getCorrectedOutcomeMeaningMinorCode: jasmine.createSpy('getCorrectedOutcomeMeaningMinorCode')
    };

    filtersService = {
      orderBy: jasmine.createSpy('orderBy')
    };

    channelService = {
      getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray').and.returnValue({})
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    service = new FavouritesMatchesService(
      eventService,
      cacheEventsService,
      templateService,
      filtersService,
      channelService,
      pubSubService,
    );

  });

  it('#constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#unSubscribeForUpdates', () => {
    it('should unsubscribe from updates', () => {
      service.unSubscribeForUpdates(undefined, false);

      expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'favourites-matches');
    });
    it('should not unsubscribe for updates if channel ids dosen"t exists', () => {
      service.unSubscribeForUpdates(undefined, true);

      expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'favourites-matches-bsTab');
    });
    it('should not unsubscribe for updates if channel ids dosen"t exists', () => {
      service.unSubscribeForUpdates('widget', false);

      expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'favourites-matches-widget');
    });
    it('should not unsubscribe for updates if channel ids dosen"t exists', () => {
      service.unSubscribeForUpdates('widget', true);

      expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'favourites-matches-widget-bsTab');
    });
  });

  it('should removeMatch',  () => {
    const matches = [{id: 1}, {id: 2}] as IMatch[];
    const actualResult = service.removeMatch(matches, 1);

    expect(actualResult).toEqual([{id: 2}]);
  });

  it('should getFavouritesMatches',  fakeAsync(() => {
    service.trimFinishedEvents = jasmine.createSpy('trimFinishedEvents');
    service.applyTemplateProperties = jasmine.createSpy('applyTemplateProperties');

    service.getFavouritesMatches('name', [{id: 1}, {id: 2}] as IMatch[]);
    tick();

    expect(eventService.favouritesMatches).toHaveBeenCalledWith({
      eventsIds: [ 1, 2 ],
      marketsCount: true,
      dispSortName: [ 'MR' ],
      dispSortNameIncludeOnly: [ 'MR' ],
      includeUndisplayed: true
    });
    expect(cacheEventsService.store).toHaveBeenCalledWith('name', [{}]);
    expect(service.trimFinishedEvents).toHaveBeenCalledWith([{}]);
    expect(service.applyTemplateProperties).toHaveBeenCalled();
  }));

  it('should applyTemplateProperties',  () => {
    const events = [
      {
        markets: [
          {
            name: 'marketsName',
            outcomes: [
              {
                isUS: true,
                correctedOutcomeMeaningMinorCode: 1
              }
            ]
          },
          {
            name: 'Match Result',
            outcomes: [
              {
                isUS: true,
                correctedOutcomeMeaningMinorCode: 2
              }
            ]
          }
        ],
        isUS: true,
        startTime: 'startTime',
        eventCorectedDay: 'eventCorectedDay'
      }
    ];
    const expectedResult = [
      {
        markets: [
          {name: 'Match Result', outcomes: undefined},
          {name: 'marketsName', outcomes: [
              {isUS: true, correctedOutcomeMeaningMinorCode: 1}
            ]
          }
        ],
        isUS: true,
        startTime: 'startTime',
        eventCorectedDay: undefined
      }
    ];

    templateService.getCorrectedOutcomeMeaningMinorCode.and.returnValue(1);

    const actualResult = service.applyTemplateProperties(events);

    expect(templateService.addIconsToEvents).toHaveBeenCalled();
    expect(templateService.getCorrectedOutcomeMeaningMinorCode).toHaveBeenCalled();
    expect(filtersService.orderBy).toHaveBeenCalledWith([
      {
        isUS: true,
        correctedOutcomeMeaningMinorCode: 1
      }
    ], ['correctedOutcomeMeaningMinorCode']);
    expect(templateService.getEventCorectedDay).toHaveBeenCalledWith('startTime');
    expect(actualResult).toEqual(expectedResult);
  });

  describe('trimFinishedEvents', () => {
    it('should return trimmed events array',  () => {
      const events = [
        {
          isFinished: true,
          isDisplayed: true,
          markets: [
            {outcomes: [{}, {}]}, {outcomes: [{}, {}]}
          ],
          marketsCount: 2
        },
        {
          isFinished: false,
          isDisplayed: true,
          markets: [
            {outcomes: [{}, {}]}, {outcomes: [{}, {}]}
          ],
          marketsCount: 2
        }
      ];
      const expectedResult = [
        {
          isFinished: true,
          isDisplayed: true,
          markets: [
            {outcomes: []}, {outcomes: []}
          ],
          marketsCount: 0
        },
        {
          isFinished: false,
          isDisplayed: true,
          markets: [
            {outcomes: [{}, {}]}, {outcomes: [{}, {}]}
          ],
          marketsCount: 2
        }
      ];
      const actualResult = service.trimFinishedEvents(events);

      expect(actualResult).toEqual(expectedResult);
    });
  });

  describe('subscribeForUpdates', () => {
    it('should set module property with widget and bsTab ',  () => {
      service.subscribeForUpdates({}, 'widget', true);

      expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith({}, true, true);
      expect(pubSubService.publish).toHaveBeenCalledWith(
        'SUBSCRIBE_LS',
        {
          channel: {},
          module: 'favourites-matches-widget-bsTab'
        }
      );
    });

    it('should set module property without widget and bsTab ',  () => {
      service.subscribeForUpdates({}, '', false);

      expect(pubSubService.publish).toHaveBeenCalledWith(
        'SUBSCRIBE_LS',
        {
          channel: {},
          module: 'favourites-matches'
        }
      );
    });
  });
});
