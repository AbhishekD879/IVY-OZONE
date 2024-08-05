import { RacingGaService } from '@racing/services/racing-ga.service';

describe('RacingGaService', () => {
  let service;
  let gtm;
  let locale;
  let pubsub;

  const raceDataMock = [
    {
      id: 123,
      markets: [
        {
          id: '12345',
          outcomes: []
        }
      ],
      categoryId: 9337,
      typeId: 2031
    }
  ];

  beforeEach(() => {
    gtm = {
      push: jasmine.createSpy('push')
    };
    locale = { getString: jasmine.createSpy('getString') };
    pubsub = {
      publish: jasmine.createSpy(),
      API: {
        PUSH_TO_GTM: 'PUSH_TO_GTM'
      }
    };

    service = new RacingGaService(gtm, locale, pubsub);
    service.flag = new Map();
    service.flag.clear = jasmine.createSpy();
  });

  it('sendGTM: eventAction should be next races', () => {
    const eventLabel = 'show more';
    const eventCategory = 'widget';
    const gtmParams = [
      'trackEvent',
      {
        eventCategory,
        eventAction: 'next races',
        eventLabel
      }
    ];
    service.sendGTM(eventLabel, eventCategory);

    expect(pubsub.publish).toHaveBeenCalledWith('PUSH_TO_GTM', gtmParams);
  });

  
  it('sendGTM: eventAction should be next races for virtuals', () => {
    const eventLabel = 'show more';
    const eventCategory = 'widget';
    const gtmParams = [
      'trackEvent',
      {
        eventCategory,
        eventAction: 'next races',
        eventLabel,
        positionEvent: 'virtual' 
      }
    ];
    service.sendGTM(eventLabel, eventCategory, true);

    expect(pubsub.publish).toHaveBeenCalledWith('PUSH_TO_GTM', gtmParams);
  });

  it('should test trackEvent function (happy path)', () => {
    const event = {
      eventCategory: 'horseracing',
      eventAction: 'testAction',
      eventLabel: 'testLabel',
    };
    spyOn(service, 'normalizeCategory');
    service.trackEvent(event);
    expect(service.normalizeCategory).toHaveBeenCalledWith(event);
    expect(service.gtm.push).toHaveBeenCalledWith('trackEvent', event);
  });

  it('should test trackEvent function (not happy path)', () => {
    const event = {
      eventCategory: 'notHorseRacing'
    };
    spyOn(service, 'normalizeCategory');
    service.trackEvent(event);
    expect(service.normalizeCategory).not.toHaveBeenCalled();
    expect(service.gtm.push).not.toHaveBeenCalled();
  });

  it('should properly normalize category', () => {
    const event = {
      eventCategory: 'horseracing',
    };
    service.normalizeCategory(event);
    expect(event.eventCategory).toEqual('horse racing');
    // not happy path
    event.eventCategory = 'some test';
    service.normalizeCategory(event);
    expect(event.eventCategory).toEqual('some test');
  });

  it('should test trackModule function', () => {
    service.flag.set('featured', false);
    spyOn(service, 'trackEvent');
    service.trackModule('featured', 'football');
    expect(service.trackEvent).toHaveBeenCalled();
  });

  it('should test trackNextRace function ', () => {
    spyOn(service, 'trackEvent');
    service.trackNextRace('Horse Racing');
    expect(service.trackEvent).toHaveBeenCalledWith({
      eventCategory: 'horseracing',
      eventAction: 'next 4 races',
      eventLabel: 'full race card'
    });
  });

  it('should test trackNextRacesCollapse function ', () => {
    service.flag.set('next 4 races', false);
    spyOn(service, 'trackEvent');
    service.trackNextRacesCollapse('horseracing');
    expect(service.trackEvent).toHaveBeenCalledWith({
      eventCategory: 'horseracing',
      eventAction: 'next 4 races',
      eventLabel: 'collapse'
    });
  });

  it('should test trackYourcallTwitter function ', () => {
    service.trackYourcallTwitter();
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'tweet now',
      eventLabel: 'horse racing'
    });
  });

  it('should test trackYourcallSpecials function ', () => {
    service.trackYourcallSpecials();
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'your call',
      eventLabel: 'more your call specials'
    });
  });

  it('should clear flag map ', () => {
    service.reset();
    expect(service.flag.clear).toHaveBeenCalled();
  });

  it('should call updateGATracking with race data, Price and isGreyhound true', () => {
    service.updateGATracking(raceDataMock, 'Price', true);
    expect(service.gtm.push).toHaveBeenCalled();
  });

  it('should call updateGATracking with race data, not Price and isGreyhound false', () => {
    service.updateGATracking(raceDataMock, 'NotPrice', false);
    expect(service.gtm.push).toHaveBeenCalled();
  });

  it('should call toggleShowOptionsGATracking with race data, showOption and isGreyhound true', () => {
    service.toggleShowOptionsGATracking(raceDataMock, true, true);
    expect(service.gtm.push).toHaveBeenCalled();
  });

  it('should call toggleShowOptionsGATracking with race data, showOption and isGreyhound false', () => {
    service.toggleShowOptionsGATracking(raceDataMock, false, false);
    expect(service.gtm.push).toHaveBeenCalled();
  });
});
