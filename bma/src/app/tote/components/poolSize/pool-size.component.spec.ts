import { PoolSizeComponent } from './pool-size.component';
import { UserService } from '@core/services/user/user.service';
import { ToteBetSlipService } from './../../services/toteBetSlip/tote-bet-slip.service';
import { IPool } from './../../models/tote-event.model';

describe('PoolSizeComponent', () => {
  let component: PoolSizeComponent, userService, toteBetslipService, currencyPipe;

  const poolsMock = [
    {
      poolType: 'test_type_1',
      currencyCode: 'USD',
      poolValue: '1'
    },
    {
      poolType: 'test_type_2',
      currencyCode: 'UAH',
      poolValue: '2'
    },
  ] as IPool[];

  const noValPoolsMock = [
    {
      poolType: 'test_type_1',
      currencyCode: 'USD'
    },
    {
      poolType: 'test_type_2',
      currencyCode: 'UAH'
    },
  ] as IPool[];


  beforeEach(() => {
    userService = {
      currency: 'USD',
      currencySymbol: '$'

    } as UserService;

    toteBetslipService = {
      getCurrency: jasmine.createSpy('toteBetslipService.getCurrency').and.returnValue('$')
    } as Partial<ToteBetSlipService>;

    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };

    component = new PoolSizeComponent(userService, toteBetslipService, currencyPipe);
  });

  it('getPoolSize', () => {
    let result;

    component.pools = poolsMock;
    component['formatPoolSize'] = jasmine.createSpy('formatPoolSize').and.returnValue('true');

    result = component.getPoolSize();
    expect(result).toEqual('');

    component.poolType = 'test_type_1';

    result = component.getPoolSize();
    expect(result).toEqual('true');
  });

  it('formatPoolSize', () => {
    let result;

    component.currencyCalculator = {
      currencyExchange: jasmine.createSpy('currencyCalculator').and.returnValue('10')
    };

    result = component['formatPoolSize'](poolsMock[0]);
    expect(result).toBe('1$');

    result = component['formatPoolSize'](noValPoolsMock[0]);
    expect(result).toBeUndefined();

    result = component['formatPoolSize'](poolsMock[1]);
    expect(result).toBe('10$ / 2$');

    result = component['formatPoolSize'](noValPoolsMock[1]);
    expect(result).toBeUndefined();
  });
});
