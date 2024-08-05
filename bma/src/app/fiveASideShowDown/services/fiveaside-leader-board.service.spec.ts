import { of, throwError } from 'rxjs';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';
import environment from '@environment/oxygenEnvConfig';
import { ContestInfo, LeaderboardInfo } from '../models/show-down';
describe('FiveasideLeaderBoardService', () => {
  let service: FiveasideLeaderBoardService;
  let httpClient;
  let localeService;
  let userService, awsService;
  beforeEach(() => {
    httpClient = {
      get: jasmine.createSpy('get').and.returnValue(of()),
      post: jasmine.createSpy('post').and.returnValue(of())
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('string')
    };
    userService = { username: jasmine.createSpy() };
    awsService = {
      addAction: jasmine.createSpy()
    } as any;
    service = new FiveasideLeaderBoardService(httpClient, localeService, userService, awsService);
  });
  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  describe('#getContestInformationById', () => {
    it('should handle success (With Username)', () => {
      const brand = environment.brand;
      const contestInfoObj: ContestInfo = {
        contestId: 'contestId',
        userId: 'userName',
        token: 'bppToken',
        brand: brand
      };
      const CONTEST_INFO_URL = `${environment.SHOWDOWN_MS}/${brand}/leaderboard/contest`;
      service.getContestInformationById('contestId', 'userName', 'bppToken').subscribe();
      expect(httpClient.post).toHaveBeenCalledWith(CONTEST_INFO_URL, contestInfoObj);
    });
    it('should handle success (without username)', () => {
      const brand = environment.brand;
      const contestInfoObj: ContestInfo = {
        contestId: 'contestId',
        userId: null,
        token: null,
        brand: brand
      };
      const CONTEST_INFO_URL = `${environment.SHOWDOWN_MS}/${brand}/leaderboard/contest`;
      service.getContestInformationById('contestId', null, null).subscribe();
      expect(httpClient.post).toHaveBeenCalledWith(CONTEST_INFO_URL, contestInfoObj);
    });
  });
  describe('#getContestPrizeById', () => {
    it('should handle success', () => {
      service.getContestPrizeById('123').subscribe();
      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.SHOWDOWN_MS}/contest/contest-prizes/123`);
    });
  });
  describe('#checkHexColor', () => {
    it('should return color', () => {
      const color = service.checkHexColor('#4da2f9', '123456');
      expect(color).toEqual('#4da2f9');
    });
    it('should return default color', () => {
      const color = service.checkHexColor('123456', '#675d5d');
      expect(color).toEqual('#675d5d');
    });
  });
  describe('#setDefaultTeamColors', () => {
    it('should bind team colors', () => {
      const teams = ['INDIA','AUSTRALIA'];
      const teamColors = [{teamName: 'INDIA'}] as any;
      const response = service.setDefaultTeamColors(teamColors, teams);
      expect(response).not.toBeNull();
    });
    it('should bind team colors (with secondary names(true))', () => {
      const teams = ['INDIA','AUSTRALIA'];
      const teamColors = [{teamName: 'IND'}, {teamName: 'AUS', secondaryNames: ['AUSTRALIA']}] as any;
      const response = service.setDefaultTeamColors(teamColors, teams);
      expect(response).not.toBeNull();
    });
    it('should bind team colors (with secondary names(false))', () => {
      const teams = ['INDIA','AUSTRALIA'];
      const teamColors = [{teamName: 'IND'}, {teamName: 'AUS', secondaryNames: ['AUSTRALI_A']}] as any;
      const response = service.setDefaultTeamColors(teamColors, teams);
      expect(response).not.toBeNull();
    });
  });
  describe('#hasImageForHomeAway', () => {
    it('should return false, if teamColors array length is empty', () => {
      const response = service.hasImageForHomeAway([]);
      expect(response).toBe(false);
    });
    it('should return false, if hasTwoTeams is false', () => {
      const teamColors = [{fiveASideToggle: false, teamsImage: null}] as any;
      const response = service.hasImageForHomeAway(teamColors);
      expect(response).toBe(false);
    });
    it('should return false, if fiveASideToggle is false', () => {
      const teamColors = [{fiveASideToggle: false, teamsImage: null},
        {fiveASideToggle: true, teamsImage: null}] as any;
      const response = service.hasImageForHomeAway(teamColors);
      expect(response).toBe(false);
    });
    it('should return false, if teamsImage is false', () => {
      const teamColors = [{fiveASideToggle: true, teamsImage: null},
        {fiveASideToggle: true, teamsImage: null}] as any;
      const response = service.hasImageForHomeAway(teamColors);
      expect(response).toBe(false);
    });
    it('should return false, if fileName is false', () => {
      const teamColors = [{fiveASideToggle: true, teamsImage: {}},
        {fiveASideToggle: true, teamsImage: {}}] as any;
      const response = service.hasImageForHomeAway(teamColors);
      expect(response).toBe(false);
    });
    it('should return true, if all conditions satisfy', () => {
      const teamColors = [{fiveASideToggle: true, teamsImage: {filename: 'abc'}},
        {fiveASideToggle: true, teamsImage: {filename: 'abc'}}] as any;
      const response = service.hasImageForHomeAway(teamColors);
      expect(response).toBe(true);
    });
  });
  describe('#getLeaderBoardInformation', () => {
    it('should handle success', () => {
      const leaderboradInfoObj: LeaderboardInfo = {
        userId: 'userName',
        token: 'bppToken',
        brand: 'ladbrokes'
      };
      const LOBYY_CONTESTS_URL = `${environment.SHOWDOWN_MS}/ladbrokes/leaderboard-widget`;
      service.getLeaderBoardInformation('userName', 'bppToken').subscribe();
      expect(httpClient.post).toHaveBeenCalled();
    });
  });
  describe('#setLeaderBoardData', () => {
    beforeEach(() => {
      spyOn(service as any, 'validateLeaderboardType');
    });
    it('should not validateLeaderboardType, if 1st condition fails', () => {
      const mock = {} as any;
      service.setLeaderBoardData(mock);
      expect(service['validateLeaderboardType']).not.toHaveBeenCalled();
      expect(mock.hasInvalidEntity).toBe(true);
    });
    it('should not validateLeaderboardType, if 2nd condition fails', () => {
      const mock = {} as any;
      service.setLeaderBoardData(mock);
      expect(service['validateLeaderboardType']).not.toHaveBeenCalled();
    });
    it('should not validateLeaderboardType, if 3rd condition fails', () => {
      const mock = {} as any;
      service.setLeaderBoardData(mock);
      expect(service['validateLeaderboardType']).not.toHaveBeenCalled();
    });
    it('should validateLeaderboardType, if all conditions pass', () => {
      const mock = { eventDetails: {started: true, regularTimeFinished: true}} as any;
      service.setLeaderBoardData(mock);
      expect(service['validateLeaderboardType']).toHaveBeenCalled();
    });
  });
  describe('#validateLeaderboardType', () => {
    it('should set leaderboard state to pre', () => {
       const leaderboard = {isStarted: false} as any;
       service['validateLeaderboardType'](leaderboard);
       expect(leaderboard.type).toEqual('pre');
    });
    it('should set leaderboard state to live', () => {
      const leaderboard = {isStarted: true, isResulted: false} as any;
      service['validateLeaderboardType'](leaderboard);
      expect(leaderboard.type).toEqual('live');
    });
    it('should set leaderboard state to post', () => {
      const leaderboard = {isStarted: true, isRegularTimeFinished: true} as any;
      service['validateLeaderboardType'](leaderboard);
      expect(leaderboard.type).toEqual('post');
    });
  });
  describe('#getPostContestInformationById', () => {
    it('should handle success (With Username)', () => {
      const postContestInfoObj: ContestInfo = {
        contestId: 'contestId',
        userId: 'userName',
        token: 'bppToken'
      };
      const POST_CONTEST_INFO_URL = `${environment.SHOWDOWN_MS}/postcontest`;
      service.getPostContestInformationById('contestId', 'userName', 'bppToken').subscribe();
      expect(httpClient.post).toHaveBeenCalledWith(POST_CONTEST_INFO_URL, postContestInfoObj);
    });
    it('should handle success (without username)', () => {
      const postContestInfoObj: ContestInfo = {
        contestId: 'contestId',
        userId: null,
        token: null
      };
      const POST_CONTEST_INFO_URL = `${environment.SHOWDOWN_MS}/postcontest`;
      service.getPostContestInformationById('contestId', null, null).subscribe();
      expect(httpClient.post).toHaveBeenCalledWith(POST_CONTEST_INFO_URL, postContestInfoObj);
    });
  });

  describe('#getLegsForEntryId', () => {
    it('should handle success', () => {
      service.getLegsForEntryId('123455,123455,123455,123455,123455').subscribe();
      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.SHOWDOWN_MS}/postcontest/outcome/123455,123455,123455,123455,123455`);
    });
  });
  describe('#isFulltime', () => {
    it('should return false', () => {
      const request = {} as any;
      const result = service.isFulltime(request);
      expect(result).toEqual(false);
    });
    it('should return false(Case 2)', () => {
      const request = { clock: { matchTime: 'HT' } } as any;
      const result = service.isFulltime(request);
      expect(result).toEqual(false);
    });
    it('should return true', () => {
      const request = { clock: { matchTime: 'FT' } } as any;
      const result = service.isFulltime(request);
      expect(result).toEqual(true);
    });
  });
  it('should form flag name', () => {
    const response = service.formFlagName('England');
    expect(response).toEqual('string');
  });
  describe('#getDynamicClass', () => {
    it('getClass return class', () => {
      const mockEntry = 12;
      expect(service.getDynamicClass(mockEntry)).toBe('defaultrankStyle');
    });
    it('getClass return class', () => {
      const mockEntry = 456;
      expect(service.getDynamicClass(mockEntry)).toBe('digitThree');
    });
    it('getClass return class', () => {
      const mockEntry = 3567;
      expect(service.getDynamicClass(mockEntry)).toBe('digitThree');
    });
    it('getClass return class', () => {
      const mockEntry = 56789;
      expect(service.getDynamicClass(mockEntry)).toBe('digitFive');
    });
    it('getClass return class', () => {
      const mockEntry = 656789;
      expect(service.getDynamicClass(mockEntry)).toBe('digitSix');
    });
    it('getClass return class', () => {
      const mockEntry = 7678789;
      expect(service.getDynamicClass(mockEntry)).toBe('digitSeven');
    });
    it('getClass return class', () => {
      const mockEntry = 1;
      expect(service.getDynamicClass(mockEntry)).toBe('defaultrankStyle');
    });
  });

  describe('#postOptInUserContestInfo', () => {
    it('should call httpClient post', () => {
      const mockEntry = 12;
      service.postOptInUserContestInfo({} as any);
      expect(httpClient.post).toHaveBeenCalled();
    });
  });

  describe('#optInUserIntoTheContest', () => {
    it('should call postOptInUserContestInfo method', () => {
      const contestData = { isInvitationalContest: true, isPrivateContest: true, } as any;
      spyOn(service, 'postOptInUserContestInfo').and.returnValue(of(null));
      userService.username.and.returnValue('abc');
      service.optInUserIntoTheContest(contestData);
      expect(service.postOptInUserContestInfo).toHaveBeenCalled();
      expect(awsService.addAction).toHaveBeenCalled();
    });
    it('should not call postOptInUserContestInfo when username is null', () => {
      const contestData = { isInvitationalContest: true, isPrivateContest: true, } as any;
      spyOn(service, 'postOptInUserContestInfo').and.returnValue(of());
      userService.username = null;
      service.optInUserIntoTheContest(contestData);
      expect(service.postOptInUserContestInfo).not.toHaveBeenCalled();
      expect(awsService.addAction).not.toHaveBeenCalled();
    });
    it('should not call postOptInUserContestInfo when isPrivateContest is false', () => {
      const contestData = { isInvitationalContest: true, isPrivateContest: false, } as any;
      spyOn(service, 'postOptInUserContestInfo').and.returnValue(of());
      userService.username.and.returnValue(null);
      service.optInUserIntoTheContest(contestData);
      expect(service.postOptInUserContestInfo).not.toHaveBeenCalled();
      expect(awsService.addAction).not.toHaveBeenCalled();
    });
    it('should not call postOptInUserContestInfo when isInvitationalContest is false', () => {
      const contestData = { isInvitationalContest: false, isPrivateContest: false, } as any;
      spyOn(service, 'postOptInUserContestInfo').and.returnValue(of());
      userService.username.and.returnValue(null);
      service.optInUserIntoTheContest(contestData);
      expect(service.postOptInUserContestInfo).not.toHaveBeenCalled();
      expect(awsService.addAction).not.toHaveBeenCalled();
    });
    it('should call awsService addAction when the request failed', () => {
      const contestData = { isInvitationalContest: true, isPrivateContest: true, } as any;
      spyOn(service, 'postOptInUserContestInfo').and.returnValue(throwError({ status: 404 }));
      userService.username.and.returnValue('abc');
      service.optInUserIntoTheContest(contestData);
      expect(service.postOptInUserContestInfo).toHaveBeenCalled();
      expect(awsService.addAction).toHaveBeenCalled();
    });
  });
});
