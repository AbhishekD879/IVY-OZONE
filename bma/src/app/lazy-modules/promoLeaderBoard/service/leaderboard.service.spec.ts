import { LeaderboardService } from './leaderboard.service';
import {
  of as observableOf,
} from 'rxjs';
describe('LeaderboardService', () => {
  let service: LeaderboardService,
    userService,
    httpServiceStub,
    windowRef;
  beforeEach(() => {

    httpServiceStub = {
      post: jasmine.createSpy().and.returnValue(observableOf(null)),
      get: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    userService = {
      bppToken : ''
    }
    windowRef = {
      nativeWindow: {
      }
    };
    service = new LeaderboardService(httpServiceStub, userService, windowRef);
  });

  it('fetchleaderboard', () => {
    const id = '1';
    const custId = '123';
    const userStatus = 'false';
    const topX = 'topx';
    const promotionId = '456';
    service.fetchleaderboard(id,userStatus,topX,promotionId);
    expect(httpServiceStub.post).toHaveBeenCalled();
  });

  it('fetchleaderboard', () => {
    const id = '1';
    const custId = '123';
    const userStatus = 'true';
    const topX = 'topx';
    const promotionId = '456';
    service.fetchleaderboard(id,userStatus,topX,promotionId);
    expect(httpServiceStub.post).toHaveBeenCalled();
  });

 

  it('should post data', () => {
    const leaderboardConfigId = '1';
    windowRef.nativeWindow.clientConfig = {
      vnClaims : {'http://api.bwin.com/v3/user/pg/nameidentifier': '123' }
    }
    const custId = '123';
    const userStatus = 'false';
    const topX = 'topx';
    const promotionId = '456';
    service['fetchleaderboard'](leaderboardConfigId, userStatus, topX, promotionId);

    expect(httpServiceStub.post).toHaveBeenCalled();
  });

  it('should post data', () => {
    const custId='123';
    windowRef.nativeWindow.clientConfig = {
      vnClaims : {'http://api.bwin.com/v3/user/pg/nameidentifier': '123' }
    }
    const userStatus=true;
    service['getCustomerId'](userStatus);
    expect(service['getCustomerId'](userStatus)).toEqual('123');
  });

  it('should post data with empty custid', () => {
    const custId='123';
    windowRef.nativeWindow = {
      clientConfig : {
        vnClaims : {'http://api.bwin.com/v3/user/pg/nameidentifier': '123' }
      }
    }
    const userStatus=false;
    service['getCustomerId'](userStatus);
    expect(service['getCustomerId'](userStatus)).toEqual('');
  });
  it('##getCustomerId if   windowRef.nativeWindow is undefiend', () => {
    windowRef.nativeWindow.clientConfig = undefined;
    const userStatus=false;
    service['getCustomerId'](userStatus);
    expect(service['getCustomerId'](userStatus)).toEqual('');
  });

  it('getAuthenticationHeader  if userStatus is true', () => {

    const userStatus=true;
    service['getAuthenticationHeader'](userStatus);

    expect( service['getAuthenticationHeader'](userStatus)).toBeDefined();
  });

  it('getAuthenticationHeader if userStatus is false', () => {

    const userStatus=false;
    service['getAuthenticationHeader'](userStatus);

    expect( service['getAuthenticationHeader'](userStatus)).toBeDefined();
  });
});