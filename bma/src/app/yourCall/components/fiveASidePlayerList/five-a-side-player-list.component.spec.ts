import { FiveASidePlayerListComponent } from '@yourcall/components/fiveASidePlayerList/five-a-side-player-list.component';

describe('FiveASidePlayerListComponent', () => {
  let component: FiveASidePlayerListComponent;

  let fiveASideService: any;
  let gtmService;
  let windowRefService;

  beforeEach(() => {
    fiveASideService = {
      sortPlayers: jasmine.createSpy('sortPlayers').and.returnValue([]),
      hideView: jasmine.createSpy(),
      activeItem:  {
        stat: 'goals'
      },
      saveDefaultStat: jasmine.createSpy('saveDefaultStat'),
      playerListScrollPosition: 5
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          scroll: jasmine.createSpy()
        })
      }
    };

    component = new FiveASidePlayerListComponent(fiveASideService, gtmService,
      windowRefService);
    component.playerFormation = {
      stat: 'goals'
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('trackById should return unique identifier for player', () => {
    expect(component.trackById(0, { id: 159 } as any)).toEqual('0_159');
  });

  describe('#ngOnInit', () => {
    it('should call ngOnInit', () => {
      spyOn(component as any, 'setPlayer');
      component.playerFormation = undefined;
      component.ngOnInit();

      expect(component.playersList).toEqual([]);
      expect(fiveASideService.sortPlayers).toHaveBeenCalledWith({
        stat: 'goals'
      });
    });

    it('should call ngOnInit for goalkeeper markets', () => {
      spyOn(component as any, 'setPlayer');
      fiveASideService.activeItem.stat = 'To Keep A Clean Sheet';
      fiveASideService.sortPlayers.and.returnValue([{ isGK: false }, { isGK: true }]);
      component.playerFormation = undefined;
      component.ngOnInit();

      expect(component.playersList).toEqual([{ isGK: true }] as any);
      expect(fiveASideService.sortPlayers).toHaveBeenCalledWith({
        stat: 'To Keep A Clean Sheet'
      });
    });
  });

  describe('#handleTabClick', () => {
    it('should call handleTabClick', () => {
      component.handleTabClick('home');

      expect(fiveASideService.sortPlayers).toHaveBeenCalledWith({
        stat: 'goals'
      }, 'home');
      expect(component.filter).toEqual('home');
    });
  });

  describe('#hide', () => {
    it('should call hide', () => {
      component.hide();

      expect(fiveASideService.hideView).toHaveBeenCalled();
    });
  });

  describe('#formSwitchers', () => {
    it('should call formSwitchers', () => {
      component['formSwitchers']();
      component.switchers.forEach(switcher => {
        switcher.onClick();
      });

      expect(fiveASideService.sortPlayers).toHaveBeenCalledTimes(3);
    });
  });

  describe('#setPlayer', () => {
    it('should set player, if playerlist is not empty', () => {
      component.player = null;
      component.playersList = [{
        id: '1'
      }] as any;
      component['setPlayer']();
      expect(component.player).not.toBeNull();
    });
    it('should not set player, if playerlist is null', () => {
      component.player = null;
      component.playersList = null;
      component['setPlayer']();
      expect(component.player).toBeNull();
    });
    it('should not set player, if playerlist is null', () => {
      component.player = null;
      component.playersList = [];
      component['setPlayer']();
      expect(component.player).toBeNull();
    });
  });

  describe('#changeStat', () => {
    it('should assign stat value whenever there is change in stat', () => {
      const request = {
        title: 'Goals',
        id: 4
      } as any;
      component.playerFormation = {
        rowIndex: 0,
        stat: 'Assists',
        statId: 5
      } as any;
      component.changeStat(request);
      expect(fiveASideService.saveDefaultStat).toHaveBeenCalled();
    });
  });

  describe('#ngAfterViewInit', () => {
    it('should persist scroll position if exists', () => {
      component.ngAfterViewInit();
      expect(windowRefService.document.querySelector).toHaveBeenCalledWith('five-a-side-player-list .drawer-body');
    });
    it('should persist scroll position if exists', () => {
      fiveASideService.playerListScrollPosition = null;
      component.ngAfterViewInit();
      expect(windowRefService.document.querySelector).not.toHaveBeenCalledWith('five-a-side-player-list .drawer-body');
    });
  });
});
