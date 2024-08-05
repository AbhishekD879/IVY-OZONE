import { BybHomeService } from '@yourcall/components/bybHome/byb-home.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

describe('#BybHomeComponent', () => {
  let service;
  let yourCallProvider;
  let cms;
  let yourCallService;

  beforeEach(() => {
    yourCallProvider = {
      useOnce: jasmine.createSpy('useOnce').and.callFake(() => {
        return {
          getUpcomingLeagues: () => {
            return []; // getLeagues() -> result[0]
          }
        };
      })
    };
    cms = {
      // eslint-disable-next-line max-len
      getCmsYourCallLeaguesConfig: jasmine.createSpy('getCmsYourCallLeaguesConfig').and.returnValue(of([])) // getLeagues() -> result[1]
    };
    yourCallService = {
      getClassData: jasmine.createSpy('getClassData').and.returnValue(Promise.resolve([]))
    };

    service = new BybHomeService(yourCallProvider, cms, yourCallService);
  });

  it('should create service instance', () => {
    expect(service).toBeTruthy();
    expect(service.cmsLeagues).toEqual(null);
    expect(service.upcomingLeagues).toEqual(null);
    expect(service.todayLeagues).toEqual(null);
    expect(service.orderedLeaguesIds).toEqual(null);
    expect(service.msLeagues).toEqual([]);
    expect(service.leaguesStatuses).toEqual({});
    expect(service.classData).toEqual({});
  });

  describe('#getLeagues', () => {
    it('should call getLeagues', fakeAsync(() => {

      service.getLeagues();
      tick(100);

      expect(yourCallService.getClassData).toHaveBeenCalled();
      expect(yourCallProvider.useOnce).toHaveBeenCalled();
    }));
  });

  describe('#fillLeagues', () => {
    beforeEach(() => {
      service.msLeagues = [{
        period: 'today',
        obTypeId: 3
      }, {
        period: 'today',
        obTypeId: 2
      }, {
        period: 'today',
        obTypeId: 1
      }];
      service.orderedLeaguesIds = [1, 2, 3];
    });
    it('should call fillLeagues', () => {

      service.fillLeagues();

      expect(service.todayLeagues).toEqual([{
        period: 'today',
        obTypeId: 3
      }, {
        period: 'today',
        obTypeId: 2
      }, {
        period: 'today',
        obTypeId: 1
      }]);
      expect(service.upcomingLeagues).toEqual([]);
    });
  });

  describe('#parseClassData', () => {
    it('should call parseClassData', () => {

      service.parseClassData([{
        class: {
          categoryId: '16',
          categoryName: 'categoryName',
          name: 'name',
          children: [
            {
              type: {
                name: 'name',
                id: '123214'
              }
            }
          ]
        }
      }]);

      expect(service.classData).toEqual({
        '123214': {
          categoryId: '16',
          categoryName: 'categoryName',
          className: 'name',
          typeName: 'name'
        }
      });
    });
  });

  describe('#getCMSLeagues', () => {
    it('should call getCMSLeagues', () => {
      service.getCMSLeagues();

      expect(cms.getCmsYourCallLeaguesConfig).toHaveBeenCalled();
    });
  });

  describe('#getLeaguesClassData', () => {
    beforeEach(() => {
      service.parseClassData = jasmine.createSpy('parseClassData');
      yourCallService.getClassData = jasmine.createSpy('getClassData')
        .and.returnValue(Promise.resolve({}));
     });

    it('should get Leagues Class Data', fakeAsync( () => {
      const upcomingLeagues = {
        data: [{
          homeTeam: {},
          visitingTeam: {},
          obEventId: 789,
          obTypeId: 7
        }, {
          homeTeam: {},
          visitingTeam: {},
          obEventId: 345,
          obTypeId: 9
        }]}  as any,
        cmsLeagues =  {
          name: 'leagues1'
        }  as any;
      service.getLeaguesClassData(upcomingLeagues, cmsLeagues);
      tick();

      expect(yourCallService.getClassData).toHaveBeenCalledWith([7, 9]);
    }));
  });

  describe('#prepareLeagues', () => {

    it('should call fillLeagues and return true', () => {
      service.fillLeagues = jasmine.createSpy();
      const upcomingLeagues = {
          data: []
        } as any,
        cmsLeagues =  {
          name: 'leagues1'
        }  as any;

      const res = service.prepareLeagues(upcomingLeagues, cmsLeagues);

      expect(service.fillLeagues).toHaveBeenCalled();
      expect(res).toEqual(true);
    });

    it('should define cmsLeagues and leaguesStatuses', () => {
      const upcomingLeagues = {
          data: []
        } as any,
        cmsLeagues = [{
          name: 'leagues1',
          typeId: 1,
          enabled: true }, {
          name: 'leagues2',
          typeId: 2,
          enabled: false
          }] as any;
      service.prepareLeagues(upcomingLeagues, cmsLeagues);

      expect(service.cmsLeagues).toEqual([{
        name: 'leagues1',
        typeId: 1,
        enabled: true }, {
        name: 'leagues2',
        typeId: 2,
        enabled: false }
      ]);
      expect(service.orderedLeaguesIds).toEqual([ 2, 1 ]);
      expect(service.leaguesStatuses[1]).toEqual(true);
    });

    it('should prepareLeagues', () => {
      const upcomingLeagues = {
        data: []
        } as any,
        cmsLeagues =  [{
          name: 'leagues1',
          typeId: 12,
          enabled: true
        }, {
          name: 'leagues2',
          typeId: 32,
          enabled: false
        }] as any;
      service.prepareLeagues(upcomingLeagues, cmsLeagues);

      expect(service.msLeagues).toEqual([]);
      expect(service.leaguesStatuses).toEqual({ 12: true, 32: false });
    });

    it('should should prepareLeagues and push obj to msLeagues', () => {
      const upcomingLeagues = {
        data: [{
          title: 't1',
          obTypeId: 678
        }, {
          title: 't2',
          obTypeId: 688
        }]} as any,
        cmsLeagues =  [{
          name: 'leagues1',
          typeId: 12,
          enabled: true
        }, {
          name: 'leagues2',
          typeId: 32,
          enabled: false
        }] as any;
      service.classData = {
        [688]: {
        categoryId: 1,
        categoryName: 'name',
        className: 'class',
        typeName: 'type'
        }
      };
      service.prepareLeagues(upcomingLeagues, cmsLeagues);

      expect(service.msLeagues).toEqual(['t1', 678, 't2', 688]);
    });

    it('should prepareLeagues and push obj to msLeagues in case this.classData[league.obTypeId]', () => {
      const upcomingLeagues = {
        data: [{
          title: {
            obTypeId: 678
          },
            obTypeId: 678
          }, {
            title: 't2',
            obTypeId: 688
          }]
        } as any,
        cmsLeagues =  [{
          name: 'leagues1',
          typeId: 12,
          enabled: true
          }, {
          name: 'leagues2',
          typeId: 32,
          enabled: false
          }
        ] as any;
      service.classData = {
        [678]: {
          categoryId: 1,
          categoryName: 'name',
          className: 'class',
          typeName: 'type'
        }
      };
      service.prepareLeagues(upcomingLeagues, cmsLeagues);

      expect(service.msLeagues).toEqual([{
        obTypeId: 678,
        period: 0,
        categoryId: 1,
        categoryName: 'name',
        className: 'class',
        typeName: 'type',
        normilized: true}, 678, 't2', 688]);
    });
  });

  describe('#getUpcomingLeagues', () => {
    it('should call getUpcomingLeagues', () => {
      service.getUpcomingLeagues();

      expect(yourCallProvider.useOnce).toHaveBeenCalledWith('BYB');
    });
  });

  describe('#sortLeagues', () => {
    it('should sort  Leagues', () => {
      service.msLeagues = [
        {
          name: 'leagues1',
          obTypeId: 12
        },
        {
          name: 'leagues2',
          obTypeId: 32
        }
      ] as any;

      const res = service['sortLeagues']('today');
      expect(res).toEqual([]);
    });
  });
});
