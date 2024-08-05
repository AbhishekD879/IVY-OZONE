import { RacingYourCallService } from '@core/services/racing/racingYourCall/racing-your-call.service';
describe('UkToteLiveUpdatesService', () => {
  let service: RacingYourCallService;

  let event, outcomes;

  beforeEach(() => {
    event = {
      markets: [
        {
          name: 1,
          selections: [
            {
              id: 2
            }
          ],
          outcomes: [
            {
              id: 6
            }
          ]
        },
        {
          name: 3,
          selections: []
        },
        {
          name: 4,
        }
      ]
    };
    outcomes = [
      {
        id: 5
      }
    ];
    service = new RacingYourCallService();
  });

  it('#clearEmptyMarkets', () => {
    service['clearEmptyMarkets'](event.markets);
    expect(event.markets.length).toBe(1);
  });

  it('#setEventAndMarket', () => {
    service['setEventAndMarket'](event, event.markets[0], outcomes);
    expect(outcomes[0].market).toBeDefined();
    expect(outcomes[0].event).toBeDefined();
  });

  it('#prepareData', () => {
    const data = service.prepareData([], [event]);
    expect(data.length).toBe(1);
  });
});
