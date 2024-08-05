import { YourCallPlayerStatsGTMService } from '@edp/components/markets/playerStats/your-call-player-stats-grm.service';

describe('YourCallPlayerStatsGTMService', () => {
  let service: YourCallPlayerStatsGTMService;
  let GTM;

  beforeEach(() => {
    GTM = {
      push: jasmine.createSpy()
    };

    service = new YourCallPlayerStatsGTMService(GTM);
  });

  it('should create service and define route', () => {
    expect(service).toBeDefined();
    expect(service.route).toEqual('');
  });

  it('sendChangeStatisticGTM', () => {
    const statisticInfo = {
      playerName: 'Player Name',
      playerStat: 'Player Stat',
      playerStatNum: 10,
    };
    service.sendChangeStatisticGTM(statisticInfo as any);
    expect(GTM.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'ds in play player stat',
      eventLabel: 'update statistic',
      playerName: statisticInfo.playerName,
      playerStat: statisticInfo.playerStat,
      playerStatNum: statisticInfo.playerStatNum
    });
  });

  it('sendTeamSwitcherGTM', () => {
    spyOn<any>(service, 'sendGTM');
    service.sendTeamSwitcherGTM('Team A');
    expect(service['sendGTM']).toHaveBeenCalledWith('switch team - Team A');
  });

  it('sendGTMData', () => {
    spyOn<any>(service, 'sendGTM');
    spyOn<any>(service, 'cutEventAction').and.returnValue('someAction');
    service.sendGTMData('eventLabel', 'action');
    expect(service['cutEventAction']).toHaveBeenCalledWith(`action ${service['route']}`);
    expect(service['sendGTM']).toHaveBeenCalledWith('eventLabel someAction');
  });

  it('cutEventAction', () => {
    expect(service['cutEventAction']('any_action')).toEqual('any_action');
    expect(service['cutEventAction']('Player_Stats_action')).toEqual('action');
  });

  it('sendGTM', () => {
    expect(service['sendGTM']('eventAction'));
    expect(GTM.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'ds in play player stat',
      eventLabel: 'eventAction'
    });
  });
});
