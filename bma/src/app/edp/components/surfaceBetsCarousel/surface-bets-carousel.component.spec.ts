import { EdpSurfaceBetsCarouselComponent } from '@edp/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';

const rawEvents = [
  {
    selectionEvent: {
      markets: [
        {
          outcomes: [{
            prices: [
              {
                id: '2',
                priceDec: 3,
                priceDen: 1,
                priceNum: 2,
                priceType: 'LP'
              }
            ]
          }]

        }
      ]
    },
    price: {
      priceDec: 1.5,
      priceDen: 2,
      priceNum: 1,
      priceType: 'LP'
    },
    svg: '<svg></svg>',
    svgId: 'svgId1',
    title: 'Bet title 1',
    content: 'Bet content 1',
    svgBgId: 'Bet bg id 1',
    svgBgImgPath: 'Svg bg image path 1',
    contentHeader: 'Content header 1'
  },
  {
    selectionEvent: {
      markets: [
        {
          outcomes: [{
            prices: [
              {
                id: '5',
                priceDec: 4.5,
                priceDen: 7,
                priceNum: 2,
                priceType: 'LP'
              }
            ]
          }]

        }
      ]
    },
    price: {
      priceDec: 1.5,
      priceDen: 2,
      priceNum: 1,
      priceType: 'LP'
    },
    svg: '<svg></svg>',
    svgId: 'svgId1',
    title: 'Bet title 2',
    content: 'Bet content 2',
    svgBgId: 'Bet bg id 2',
    svgBgImgPath: 'Svg bg image path 2',
    contentHeader: 'Content header 2'
  }
];

const betEvents = [
  {
    markets: [
      {
        outcomes: [{
          prices: [
            {
              id: '2',
              priceDec: 3,
              priceDen: 1,
              priceNum: 2,
              priceType: 'LP'
            }
          ]
        }]

      }
    ],
    oldPrice: {
      priceDec: 1.5,
      priceDen: 2,
      priceNum: 1,
      priceType: 'LP'
    },
    svg: '<svg></svg>',
    svgId: 'svgId1',
    title: 'Bet title 1',
    content: 'Bet content 1',
    svgBgId: 'Bet bg id 1',
    svgBgImgPath: 'Svg bg image path 1',
    contentHeader: 'Content header 1'
  },
  {
    markets: [
      {
        outcomes: [{
          prices: [
            {
              id: '5',
              priceDec: 4.5,
              priceDen: 7,
              priceNum: 2,
              priceType: 'LP'
            }
          ]
        }]

      }
    ],
    oldPrice: {
      priceDec: 1.5,
      priceDen: 2,
      priceNum: 1,
      priceType: 'LP'
    },
    svg: '<svg></svg>',
    svgId: 'svgId1',
    title: 'Bet title 2',
    content: 'Bet content 2',
    svgBgId: 'Bet bg id 2',
    svgBgImgPath: 'Svg bg image path 2',
    contentHeader: 'Content header 2'
  }
];

describe('EdpSurfaceBetsCarouselComponent', () => {
  let component: EdpSurfaceBetsCarouselComponent,
    cmsService,
    channelService,
    cacheEventsService,
    pubSubService;

  beforeEach(() => {
    cmsService = {
      getEDPSurfaceBets: jasmine.createSpy('getEDPSurfaceBets').and.returnValue(observableOf(rawEvents))
    };
    cacheEventsService = {
      store: jasmine.createSpy('store').and.returnValue(betEvents)
    };
    pubSubService = {
      publish: jasmine.createSpy('publish')
    };
    channelService = {
      getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray').and.returnValue(betEvents)
    };

    component = new EdpSurfaceBetsCarouselComponent(
      cmsService as CmsService,
      channelService as ChannelService,
      cacheEventsService as CacheEventsService,
      pubSubService as PubSubService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should get surface bets', fakeAsync(() => {
    component['subscribeForUpdates'] = jasmine.createSpy('subscribeForUpdates');
    component.eventId = 512;
    component.ngOnInit();
    tick();
    expect(cmsService.getEDPSurfaceBets).toHaveBeenCalledWith(512);
    expect(cacheEventsService.store).toHaveBeenCalledWith('surfaceBetEvents', betEvents);
    expect(component['subscribeForUpdates']).toHaveBeenCalledWith(betEvents as any);
    expect(component.module.data).toEqual(betEvents as any);
    expect(component['eventsDataSubscription']).toBeDefined();
  }));

  describe('ngOnDestroy', () => {
    it('#ngOnDestroy should unsubscribe events', () => {
      component.ngOnDestroy();
      expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'edp-surface-bets');
    });

    it('should unsubscribe from events laod subscription', () => {
      const eventsDataSubscription = jasmine.createSpyObj('eventsDataSubscription', ['unsubscribe']);

      component['eventsDataSubscription'] = eventsDataSubscription;
      component.ngOnDestroy();

      expect(eventsDataSubscription.unsubscribe).toHaveBeenCalled();
    });
  });

  it('#subscribeForUpdates should subscribe to events update', () => {
    component['subscribeForUpdates'](betEvents as any);
    expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith(betEvents);
    expect(pubSubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', {
      channel: betEvents,
      module: 'edp-surface-bets'
    });
  });
});
