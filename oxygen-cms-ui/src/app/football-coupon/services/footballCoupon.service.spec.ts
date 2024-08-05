import { FootballCouponService } from '@app/football-coupon/services/footballCoupon.service';
import { Observable } from 'rxjs/Observable';

describe('Coupon Segments Service unit tests', () => {
  let service: FootballCouponService;
  const httpClient: any = {};

  beforeEach(() => {
    service = new FootballCouponService(httpClient, '', 'x');
    spyOn<any>(service, 'sendRequest').and.returnValue(Observable.of([]));
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['uri']).toBe('coupon-segment');
  });

  it('#findAllByBrand', () => {
    service.findAllByBrand().subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('get', 'coupon-segment/brand/x', null);
    });
  });

  it('#remove', () => {
    service.remove('1').subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('delete', 'coupon-segment/1', null);
    });
  });

  it('#add', () => {
    const obj: any = {};
    service.add(obj).subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('post', 'coupon-segment', obj);
    });
  });

  it('#getById', () => {
    service.getById('1').subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('get', 'coupon-segment/1', null);
    });
  });

  it('#edit', () => {
    const obj: any = {
      id: 1
    };
    service.edit(obj).subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('put', 'coupon-segment/1', obj);
    });
  });

  it('#reorder', () => {
    const obj: any = {};
    service.reorder(obj).subscribe( () => {
      expect(service['sendRequest']).toHaveBeenCalledWith('post', 'coupon-segment/ordering', obj);
    });
  });
});
