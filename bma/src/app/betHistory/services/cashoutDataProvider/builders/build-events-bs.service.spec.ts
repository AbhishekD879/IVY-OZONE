import { BuildEventsBsService } from './build-events-bs.service';
import { FiltersService } from '@core/services/filters/filters.service';

describe('BuildEventsBsService', () => {
  let filterService: FiltersService;
  let service: BuildEventsBsService;
  const eventsArray: any[] = [
    {
      id: 111,
      name: 'name',
      categoryId: '22',
      markets: [
        {
          name: 'name',
          outcomes: [
            {
              name: 'name',
              prices: [
                {
                  priceType: 'price type',
                  id: '01'
                }
              ]
            }
          ]
        }
      ]
    }
  ];

  beforeEach(() => {
    filterService = {
      clearEventName: jasmine.createSpy().and.returnValue('name')
    } as any;

    service = new BuildEventsBsService(filterService);
  });

  it('build', () => {
    const result = service.build(eventsArray);

    expect(result).toBeDefined();
    expect(result[0].markets[0].outcomes[0].price).toBeDefined();
    expect(result[0].markets[0].outcomes[0].prices).not.toBeDefined();
    expect(filterService.clearEventName).toHaveBeenCalledWith('name');
  });
});
