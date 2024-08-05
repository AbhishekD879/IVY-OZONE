import { MarketSelectorService } from '@app/football-coupon/services/marketSelector.service';
import { Observable } from 'rxjs/Observable';

describe('Market Selector Service unit tests', () => {
  let service: MarketSelectorService;
  const httpClient: any = {};

  beforeEach(() => {
    service = new MarketSelectorService(httpClient, '', 'x');
    spyOn<any>(service, 'sendRequest').and.returnValue(Observable.of([]));
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['uri']).toBe('coupon-market-selector');
  });

  it('#findAllByBrand', () => {
    service.findAllByBrand().subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('get', 'coupon-market-selector/brand/x', null);
    });
  });

  it('#delete', () => {
    service.delete('1').subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('delete', 'coupon-market-selector/1', null);
    });
  });

  it('#add', () => {
    const obj: any = {};
    service.add(obj).subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('post', 'coupon-market-selector', obj);
    });
  });

  it('#getById', () => {
    service.getById('1').subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('get', 'coupon-market-selector/1', null);
    });
  });

  it('#edit', () => {
    const obj: any = {
      id: 1
    };
    service.edit(obj).subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('put', 'coupon-market-selector/1', obj);
    });
  });

  it('#reorder', () => {
    const obj: any = {};
    service.reorder(obj).subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('post', 'coupon-market-selector/ordering', obj);
    });
  });

  it('#getUsedMarketTemplateNames: should get used templateMarketNames', () => {
    spyOn<any>(service, 'findAllByBrand').and.returnValue(Observable.of({
      body: [{
        templateMarketName: 'a'
      }]
    }));
    service.getUsedMarketTemplateNames().subscribe( (arr: string[]) => {
      expect(service.findAllByBrand).toHaveBeenCalled();
      expect(arr).toEqual(['a']);
    });
  });
});
