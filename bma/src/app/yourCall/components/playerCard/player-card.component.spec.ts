import { of, throwError } from 'rxjs';

import { PlayerCardComponent } from './player-card.component';

describe('PlayerCardComponent', () => {
  let component: PlayerCardComponent;
  let fiveASideService;
  let infoDialogService;
  let localeService;
  let item;
  let player;
  let eventEntity;
  let windowRefService;

  beforeEach(() => {
    item = {
      rowIndex: 1,
      collIndex: 1,
      position: 'Position',
      stat: 'Passes',
      statId: 1,
      roleId: '1'
    };

    player = {
      name: 'Player name',
      passes: 10,
      teamColors: {
        primaryColour: 'primaryColour',
        secondaryColour: 'secondaryColour'
      }
    };

    eventEntity = {
      id: 101
    };

    fiveASideService = {
      showView: jasmine.createSpy('showView'),
      activeItem : {
        rowIndex: 1,
        collIndex: 1,
        position: 'Position',
        stat: 'Passes',
        statId: 1,
        roleId: '1'
      },
      playerListScrollPosition: jasmine.createSpy(),
      loadPlayerStats: jasmine.createSpy('loadPlayerStats').and.returnValue(of([])),
      getPlayerStats: jasmine.createSpy('getPlayerStats'),
      imagesExistOnHomeAway: []
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          scroll: jasmine.createSpy(),
          scrollTop: 5
        })
      }
    };

    component = new PlayerCardComponent(fiveASideService, infoDialogService, localeService,
      windowRefService);
    component.player = player;
    component.eventEntity = eventEntity;
  });

  it('should create PlayerCardComponent', () => {
    expect(component).toBeTruthy();
  });

  describe('#teamsImgExistOnHomeAway', () => {
    it('should return true if images exist on both teams', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: true},
      'teamtwo': {filename: 'img2', fiveASideToggle: true}};
      expect(component.teamsImgExistOnHomeAway).toBeTruthy();
    });
    it('should return false if images exist on both teams', () => {
      fiveASideService.imagesExistOnHomeAway = {};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: true},
      'teamtwo': {filename: 'img2', fiveASideToggle: false}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: false},
      'teamtwo': {filename: 'img2', fiveASideToggle: true}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: false},
      'teamtwo': {filename: 'img2', fiveASideToggle: false}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: '', fiveASideToggle: true},
      'teamtwo': {filename: 'img2', fiveASideToggle: true}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
    it('should return false if images exist toggle flag false', () => {
      fiveASideService.imagesExistOnHomeAway = {'teamone':{filename: 'img1', fiveASideToggle: true},
      'teamtwo': {filename: '', fiveASideToggle: true}};
      expect(component.teamsImgExistOnHomeAway).toBeFalsy();
    });
  });

  describe('#ngOnInit', () => {
    it('#ngOnInit', () => {
      component.ngOnInit();

      expect(component.playerFormation).toEqual(item);
      expect(component.statValue).toEqual(10);
      expect(component['value']).toEqual(10);
      expect(component.primaryColour).toEqual('primaryColour');
      expect(component.secondaryColour).toEqual('secondaryColour');
    });

    it('#ngOnInit stat value undefinded', () => {
      player.passes = undefined;
      component.ngOnInit();

      expect(component.playerFormation).toEqual(item);
      expect(component.statValue).toEqual('N/A');
      expect(component['value']).toEqual(undefined);
      expect(component.primaryColour).toEqual('primaryColour');
      expect(component.secondaryColour).toEqual('secondaryColour');
    });

    it('#ngOnInit stat value null', () => {
      player.passes = null;
      component.ngOnInit();

      expect(component.statValue).toEqual('N/A');
      expect(component['value']).toEqual(null);
    });

    it('#ngOnInit should set empty string for the teamsImage', () => {
      player.teamColors.teamsImage = undefined;
      player.teamColors.fiveASideToggle = false;
      component.ngOnInit();
      expect(component.teamsImage).toBe('');
      expect(component.fiveASideToggle).toBe(false);
    });

    it('#ngOnInit should  set image string for the teamsImage', () => {
      player.teamColors.teamsImage = {
        filename: 'image1.svg',
        imagespath: 'api/images/uploads'
      };
      player.teamColors.fiveASideToggle = true;
      component.ngOnInit();
      expect(component.teamsImage).toBe('https://cms.coral.co.uk/cms//images/uploads/svg/image1.svg');
      expect(component.fiveASideToggle).toBe(true);
    });
  });

  describe('#ngOnChanges', () => {
    it('should set player card, if it contains changes related to item', () => {
      spyOn(component as any, 'setPlayerCard');
      component.ngOnChanges({ playerFormation: {}} as any);
      expect(component['setPlayerCard']).toHaveBeenCalled();
    });
    it('should not set player card, if it doesnt contain changes related to item', () => {
      spyOn(component as any, 'setPlayerCard');
      component.ngOnChanges({ player: {}} as any);
      expect(component['setPlayerCard']).not.toHaveBeenCalled();
    });
  });

  describe('showPlayerPage', () => {
    beforeEach(() => {
      component.playerFormation = item;
    });

    it('should show player page', () => {
      fiveASideService.loadPlayerStats.and.returnValue(of([{ id: item.statId }]));
      component.showPlayerPage();
      expect(fiveASideService.loadPlayerStats).toHaveBeenCalledWith(eventEntity.id, player.id);
      expect(fiveASideService.showView).toHaveBeenCalledWith({ view: 'player-page', player, item });
      expect(windowRefService.document.querySelector).toHaveBeenCalledWith('five-a-side-player-list .drawer-body');
    });

    it('should not show player page', () => {
      infoDialogService.openInfoDialog.and.callFake((...params) => params[4]());
      component.showPlayerPage();
      expect(fiveASideService.loadPlayerStats).toHaveBeenCalledWith(eventEntity.id, player.id);
      expect(fiveASideService.showView).not.toHaveBeenCalled();
      expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.cantSelectPlayer.caption');
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.cantSelectPlayer.text');
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.cantSelectPlayer.okBtn');
    });

    it('should handle error', () => {
      fiveASideService.loadPlayerStats.and.returnValue(throwError('error'));
      component.showPlayerPage();
      expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.error');
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.serverError');
    });
  });

  describe('setUnavailable', () => {
    beforeEach(() => {
      component.playerFormation = item;
    });

    it('should set false', () => {
      component['setUnavailable']();
      expect(component.unavailable).toBeFalsy();
    });

    it('should set true', () => {
      fiveASideService.getPlayerStats.and.returnValue([99]);
      component['setUnavailable']();
      expect(component.unavailable).toBeTruthy();
    });
  });
});
