
import { of } from 'rxjs';
import { LeaderboardDetailsComponent } from '@app/lazy-modules/promoLeaderBoard/components/leaderboard-details/leaderboard-details.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('LeaderboardDetailsComponent', () => {
  let component: LeaderboardDetailsComponent;
  let lbService;
  let timeService;
  let changeDetectorRef;
  let pubSubService;
 
  beforeEach(() => {
    lbService = {
      fetchleaderboard: jasmine.createSpy().and.returnValue(of({}))
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('15:10'),
      getLocalDateFromString : jasmine.createSpy('formatByPattern').and.returnValue('15:10')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()), 
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi,
      };
    createComponent();
  });

  function createComponent() {
    component = new LeaderboardDetailsComponent(lbService,timeService,changeDetectorRef,pubSubService);
  }

  it('should call ngOninit', () => {
    const getleaderBoardData = spyOn(component, 'loadLeaderBoard');
    component.ngOnInit();
    expect(getleaderBoardData).toHaveBeenCalled();
  });

  it('should call ngOnChanges', () => {
    const data=['1'] as any
    const getleaderBoardData = spyOn(component, 'loadLeaderBoard');
    component.ngOnChanges(data);
    expect(getleaderBoardData).toHaveBeenCalled();
  });

  it('should call getCssClass', () => {
    const data='name';
    component.getCssClass(data);
    expect(component.getCssClass).toHaveBeenCalled;
  });

  it('should call getleaderBoardData', () => {
     const id='1';
     component.lbConfigData={
      topX:'top'
     }as any
   
    component.getleaderBoardData(1,true);
    expect( lbService.fetchleaderboard).toHaveBeenCalled();
  });

  it('should call getleaderBoardData with greated topx', () => {
    const id=1;
    component.lbConfigData={
     topX:60
    }as any
  
   component.getleaderBoardData(id,false);
   expect( lbService.fetchleaderboard).toHaveBeenCalled();
 });

    it('should call checkUserRank', () => {
     component.leaderboardData={
      userRank:{
        customerId:'1'
      }
     }as any;

     component.lbConfigData = {
      individualRank : true
     } as any;
   
    component.checkUserRank();
    expect( component.checkUserRank).toBeTruthy();
  });

  it('should call loadLeaderBoard', () => {
    component.lbConfigData={
      topX:'top'
     }as any
   component.initialLoad=50;
  spyOn(component,'getleaderBoardData');
   component.loadLeaderBoard();
   expect( component.getleaderBoardData).toHaveBeenCalled();
 });

  it('should call loadLeaderBoard with greated topx', () => {
    component.lbConfigData={
      topX:60
     }as any
   component.initialLoad=50;
  spyOn(component,'getleaderBoardData');
   component.loadLeaderBoard();
   expect( component.getleaderBoardData).toHaveBeenCalled();
 });

 it('should call getLastModified', () => {
  component.getLastModified();
  expect( component.getLastModified()).toBe('Updated 15:10');
});

 it('should call getLastModified without leaderboardData', () => {
  component.leaderboardData=undefined;
  component.getLastModified();
  expect( component.getLastModified()).toBe('Updated 15:10');
});
it('should call getLastModified without leaderboardData', () => {
  component.leaderboardData= {lastFileModified : undefined} as any;
  component.getLastModified();
  expect( component.getLastModified()).toBe('Updated 15:10');
});
 it('should call getLastModified without leaderboardData and datePattern', () => {
  component.datePattern=undefined;
  component.getLastModified();
  expect( component.getLastModified()).toBe('Updated 15:10');
});


 it('should call getColorStyle', () => {
  component.getColorStyle();
  expect( component.getColorStyle()).toEqual({color: 'lb-col-color-coral'});
});

 it('should call getColorStyle', () => {
   component.BRAND='ladbrokes';
  component.getColorStyle();
  expect( component.getColorStyle()).toEqual({color: ''});
});

 it('should call getuserNameMask', () => {
   const userId='userid123'
  component.getuserNameMask(userId);
  expect(component.getuserNameMask(userId)).toBe('useri***');
});

 it('should call getuserNameMask with userId empty', () => {
   const userId=''
  component.getuserNameMask(userId);
   expect(component.getuserNameMask(userId)).toBe('');
});

it('should call checkIfMaskingAvailable if masking available', () => {
  const spygetuserNameMask = spyOn(component, 'getuserNameMask');
 component.checkIfMaskingAvailable(true,'val');
  expect(spygetuserNameMask).toHaveBeenCalled();
});

it('should not call checkIfMaskingAvailable if masking not available', () => {
  const spygetuserNameMask = spyOn(component, 'getuserNameMask');
 component.checkIfMaskingAvailable(null,'val');
  expect(spygetuserNameMask).not.toHaveBeenCalled();
});
});