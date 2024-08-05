import { of } from 'rxjs/observable/of';
import { QueryList } from '@angular/core';

import { EventCreateComponent } from './event.create.component';
import { SvgOptionModel } from '@app/client/private/models/svgOption.model';

describe('EventCreateComponent', () => {
  let component: EventCreateComponent;
  let gameAPIService;
  let teamKitAPIService;
  let dialogService;
  let snackBar;

  const responseEvent = {
    body: {
      home: {
        name: 'team1',
        displayName: 'team1',
        teamKitIcon: '/images/uploads/teamKit/brighton.svg'
        },
      away: {
        name: 'team2',
        displayName: 'team2',
        teamKitIcon: '/images/uploads/teamKit/liverpool1.svg'
        },
      brand: 'bma',
      gameId: '5c1bb19ec9e77c000161d863',
      tvIcon: 'BBC',
      eventId: '564734',
      startTime: '2018-12-20T15:13:34.426Z',
      sortOrder: 0
    }
  };

  const responseKits = {
    body: {
      brand: 'bma',
      createdAt: '2019-01-23T11:49:54.391Z',
      createdBy: '54905d04a49acf605d645271',
      createdByUserName: null,
      id: '5c4854e2c9e77c0001309429',
      path: '/images/uploads/teamKit/liverpool.svg',
      svg: '<symbol id="2dedadfa-52f0-37d4-b8d0-38f3a1823a98" viewBox="0 0 200 200"><g fill="none" fill-rule="evenodd' +
           'xmlns="http://www.w3.org/2000/svg"><path d="M119 3H81v.781C81 6.662 99.987 18 99.987 18S119 6.662 119 3.781V3z"' +
           'fill="#D31818"/><path d="M100 140h50l8 44c.784 3.856.37 6.308-4 7l-41 7c-4.37.692-6.216-1.145-7-5l-5.999-24-.001-29z"' +
           'fill="#79081B"/><path d="M100 140H50l-7.682 43.892c-.78 3.846-.367 6.292 3.979 6.982l40.774 6.983c4.346.69 6.182-1.142' +
           +'6.962-4.988l5.966-23.94L100 140z""fill="#831124"/></g></symbol>',
      svgId: '#2dedadfa-52f0-37d4-b8d0-38f3a1823a98',
      teamName: 'Blackburn Rovers',
      updatedAt: '2019-01-23T11:49:54.391Z',
      updatedBy: '54905d04a49acf605d645271',
      updatedByUserName: null,
    },
  };

  const event = responseEvent.body;

  const game = {
    body: {
        brand: 'bma',
        createdAt: '2018-12-20T15:13:34.426Z',
        createdBy: '54905d04a49acf605d645271',
        disabled: false,
        createdByUserName: 'test.admin@coral.co.uk',
        displayFrom: '2018-12-20T15:13:27.653Z',
        displayTo: '2018-12-20T15:13:26Z',
        events: [],
        prizes: [],
        id: '5c1bb19ec9e77c000161d863',
        title: null,
        updatedAt: '2018-12-20T15:13:34.426Z',
        updatedBy: '54905d04a49acf605d645271',
        updatedByUserName: 'test.admin@coral.co.uk',
        sortOrder: 0,
        status: '',
        highlighted: true,
        enabled: true
    }
  };

  const notificationMessage = {
    title: 'Save Error',
    message: 'Event not found'
  };

  beforeEach(() => {
    gameAPIService = {
      getEventById: jasmine.createSpy('getEventById').and.returnValue(of(event)),
      uploadImage: jasmine.createSpy('uploadImage').and.returnValue(of(event)),
      hideLoader: jasmine.createSpy('hideLoader'),
      deleteImage: jasmine.createSpy('deleteImage'),
      putGamesChanges: jasmine.createSpy('putGamesChanges').and.returnValue(of(responseEvent)),
    };

    teamKitAPIService = {
      getTeamKitsByTeamName: jasmine.createSpy('getTeamKitsByTeamName').and.returnValue(of(event)),
    };

    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };

    snackBar = {
      open: jasmine.createSpy('open')
    };

    component = new EventCreateComponent(
      gameAPIService,
      teamKitAPIService,
      dialogService,
      snackBar
    );
    component.game = { ...game.body } as any;
    component.homeComponents = new QueryList();
    component.awayComponents = new QueryList();
  });

  it('should add event into the game', () => {
    component.game = {...game.body, events: [event]} as any;
    component['getEventThrottled'] = component.getEventHandler;
    component.getEvent();
    expect(component.game.events.length).toBe(1);
  });

  it('should splice array of events', () => {
    component.game = {...game.body, events: [event, event, event, event]} as any;
    component.removeEvent(1);
    expect(component.game.events.length).toBe(3);
  });

  it('should return false after calling isValidEventId', () => {
    component.eventId = '';
    expect(component.isValidEventId()).toBe(false);
  });

  it('should return true after calling isValidEventId', () => {
    component.eventId = '45673';
    expect(component.isValidEventId()).toBe(true);
  });

  it('should not call loadInitialData', () => {
    component.eventId = '';
    component['getEventThrottled'] = component.getEventHandler;
    component.getEvent();
    expect(gameAPIService.getEventById).not.toHaveBeenCalled();
  });

  it('should call loadInitialData', () => {
    gameAPIService.getEventById.and.returnValue(of(responseEvent));
    component.eventId = '4556';
    component['getEventThrottled'] = component.getEventHandler;
    component.getEvent();
    expect(gameAPIService.getEventById).toHaveBeenCalled();
  });

  it('should call showNotificationDialog', () => {
    component.eventId = '777';
    component['getEventThrottled'] = component.getEventHandler;
    component.getEvent();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(notificationMessage);
  });

  it('should call game events.length toBeDefined and to be 1', () => {
    component.eventId = '4556';
    component['getEventThrottled'] = component.getEventHandler;
    component.game.events = [{}];
    component.getEvent();
    expect(component.game.events.length).toBeDefined();
    expect(component.game.events.length).toBe(1);
  });

  it('should upload team kits', () => {
    const spyOnUploadTeamKits = spyOn<any>(component, 'uploadTeamKits');
    component.ngOnInit();
    expect(spyOnUploadTeamKits).toHaveBeenCalled();
  });

  it('should clear all name path option', () => {
    const spyOnClear = spyOn(component.namePathsOptions, 'clear');
    component['uploadTeamKits']();
    expect(spyOnClear).toHaveBeenCalled();
  });

  it('should get name path option', () => {
    const spyOnGet = spyOn(component.namePathsOptions, 'get');
    teamKitAPIService.getTeamKitsByTeamName.and.returnValue(of({
      body: [responseKits.body]
    }) as any);
    component.game.events = [{
      home: { name: 'home' }, away: { name: 'away' }
    }];
    component['uploadTeamKits']();
    expect(spyOnGet).toHaveBeenCalled();
  });

  it('should get team kits been called', () => {
    teamKitAPIService.getTeamKitsByTeamName.and.returnValue(of([responseKits]) as any);
    component.game.events = [{
      home: {}, away: {}
    }];
    component['uploadTeamKits']();
    expect(teamKitAPIService.getTeamKitsByTeamName).toHaveBeenCalled();
  });

  it('should fill team kits', () => {
    const spyOnFillTeamKits = spyOn<any>(component, 'fillTeamKits');
    component.game.events = [event];
    component['uploadTeamKits']();
    expect(spyOnFillTeamKits).toHaveBeenCalled();
  });

  it('should namePathsOptions shoud be seted', () => {
    const { path, svg, svgId, teamName } = responseKits.body;
    const testPath = [new SvgOptionModel(path, path, svg, svgId, path)];
    component['uploadTeamKits']();
    expect(component.namePathsOptions.get(teamName)).toBe(undefined);
    component.namePathsOptions.set(teamName, testPath);
    expect(component.namePathsOptions.get(teamName)).toBe(testPath);
  });

  it('should call updateSelection, updateGameEventOnRemoveUploadSvg, showNotification, hideLoader', () => {
    const spyOnUpdateGameEventOnUploadSvg = spyOn(component, 'updateGameEventOnUploadSvg');
    const spyOnShowNotification = spyOn(component, 'showNotification');
    gameAPIService.uploadImage.and.returnValue(of(responseEvent));
    component.uploadSvgHandler('file', 456, 'fileName', 'teamType');
    expect(spyOnUpdateGameEventOnUploadSvg).toHaveBeenCalled();
    expect(spyOnShowNotification).toHaveBeenCalled();
    expect(gameAPIService.hideLoader).toHaveBeenCalled();
  });

  it('it should call updateGameEventOnRemoveUploadSvg, showNotification', () => {
    const spyOnUpdateGameEventOnRemoveSvg = spyOn(component, 'updateGameEventOnRemoveSvg');
    const spyOnShowNotification = spyOn(component, 'showNotification');
    gameAPIService.deleteImage.and.returnValue(of(responseEvent));
    component.removeSvgHandler(456, 'teamName');
    expect(spyOnUpdateGameEventOnRemoveSvg).toHaveBeenCalled();
    expect(spyOnShowNotification).toHaveBeenCalled();
  });

  it('should update event in the game', () => {
    event.eventId = '564734';
    component.game.events = [event];
    component.updateGameEventOnRemoveSvg('564734', event, null);
    expect(component.game.events[0]).toEqual(event);
  });

  it('shouldn`t update event in the game', () => {
    event.eventId = '564734';
    component.game.events = [event];
    component.updateGameEventOnRemoveSvg('56473', {}, null);
    expect(component.game.events[0]).not.toEqual({});
  });

  it('should update game event on upload svg', () => {
    const testEvent = {
      home: {
        name: 'team1',
        displayName: 'team1',
        teamKitIcon: '/images/uploads/teamKit/test.svg'
        },
      away: {
        name: 'team2',
        displayName: 'team2',
        teamKitIcon: '/images/uploads/teamKit/test1.svg'
        },
      brand: 'bma',
      gameId: '5c1bb19ec9e77c000161d863',
      tvIcon: 'BBC',
      eventId: '564734',
      startTime: '2018-12-20T15:13:34.426Z',
      sortOrder: 0
    };
    event.eventId = '564734';
    component.game.events = [event];
    component.updateGameEventOnUploadSvg('564734', testEvent);
    expect(component.game.events[0]).toEqual(jasmine.objectContaining(testEvent));
  });

  it('shouldn`t update game event on upload svg', () => {
    event.eventId = '564734';
    component.game.events = [event];
    component.updateGameEventOnUploadSvg('56473', {});
    expect(component.game.events[0]).not.toEqual({});
  });

  it('should set previous team kit', () => {
    const testEvent = {
      home: {
        name: 'team1',
        displayName: 'team1',
        teamKitIcon: '/images/uploads/teamKit/test.svg'
        },
      away: {
        name: 'team2',
        displayName: 'team2',
        teamKitIcon: null
        },
      brand: 'bma',
      gameId: '5c1bb19ec9e77c000161d863',
      tvIcon: 'BBC',
      eventId: '564734',
      startTime: '2018-12-20T15:13:34.426Z',
      sortOrder: 0
    };
    event.eventId = '564734';
    component.game.events = [{
      eventId: '564734',
      home: {},
      away: { teamKitIcon: '/images/uploads/teamKit/test1.svg' }
    }];
    component.updateGameEventOnUploadSvg('564734', testEvent);
    expect(component.game.events[0].away.teamKitIcon).toBe('/images/uploads/teamKit/test1.svg');
  });

  it('should set new team kit', () => {
    const testEvent = {
      home: {
        name: 'team1',
        displayName: 'team1',
        teamKitIcon: '/images/uploads/teamKit/test.svg'
        },
      away: {
        name: 'team2',
        displayName: 'team2',
        teamKitIcon: '/images/uploads/teamKit/test3.svg'
        },
      brand: 'bma',
      gameId: '5c1bb19ec9e77c000161d863',
      tvIcon: 'BBC',
      eventId: '564734',
      startTime: '2018-12-20T15:13:34.426Z',
      sortOrder: 0
    };
    event.eventId = '564734';
    component.game.events = [{
      eventId: '564734'
    }];
    component.updateGameEventOnUploadSvg('564734', testEvent);
    expect(component.game.events[0].away.teamKitIcon).toBe('/images/uploads/teamKit/test3.svg');
  });

  it('should notify admin about already exist event on Adding New Event', () => {
   const alreadyExistMessage = {
     title: 'Event Fetching Error',
     message: 'Event with such ID already added'
   };
    event.eventId = '4556';
    component['getEventThrottled'] = component.getEventHandler;
    component.game.events = [event];
    component.eventId = '4556';
    component.getEvent();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(alreadyExistMessage);
  });

  it('should call update selection 2 times', () => {
    const spyOnSetSelectionToComponent = spyOn(component, 'setSelectionToComponent');
    const homeComponent = { id: '457', svgList: { reinitSvgElement: () => {} }, selected: {} };
    component.homeComponents = [homeComponent] as any;
    component.game.events = [event, event];
    component.updateSelection();
    expect(spyOnSetSelectionToComponent).toHaveBeenCalledTimes(2);
  });

  it('should call update selection 1 time', () => {
    const spyOnSetSelectionToComponent = spyOn(component, 'setSelectionToComponent');
    const homeComponent = { id: '457', svgList: { reinitSvgElement: () => {} }, selected: {} };
    component.homeComponents = [homeComponent] as any;
    component.game.events = [event];
    component.updateSelection();
    expect(spyOnSetSelectionToComponent).toHaveBeenCalledTimes(1);
  });

  it('should call get selected', () => {
    const spyOnSetSelectionToComponent = spyOn(component, 'getSelected');
    const myEvent = { eventId: '456', away: 'ars' };
    const homeComponent = { id: '456' };
    component.setSelectionToComponent(homeComponent, myEvent, 'away');
    expect(spyOnSetSelectionToComponent).toHaveBeenCalled();
  });

  it('shouldn`t call get selected', () => {
    const spyOnSetSelectionToComponent = spyOn(component, 'getSelected');
    let myEvent = { eventId: '457', away: 'ars' };
    let homeComponent = { id: '456' };
    component.setSelectionToComponent(homeComponent, myEvent, 'away');
    expect(spyOnSetSelectionToComponent).not.toHaveBeenCalled();
    myEvent = { eventId: '457', away: 'ars' };
    homeComponent = { id: '456' };
    component.setSelectionToComponent(homeComponent, myEvent, 'bla');
    expect(spyOnSetSelectionToComponent).not.toHaveBeenCalled();
  });

  it('should show dialog', () => {
    component.showNotification('sevad');
    expect(snackBar.open).toHaveBeenCalled();
  });

  it('should call get selected and set kit icon', () => {
    const homeComponent = { id: '457', svgList: { reinitSvgElement: () => {} }, selected: {}, fullPath: 'path' };
    const spyOnSetSelectionToComponent = spyOn(component, 'getSelected').and.returnValue(homeComponent as any);
    component.homeComponents = [homeComponent] as any;
    component.game = game.body;
    component.game.events = [{ eventId: '457', home: {}, away: {} }];
    component.onChange('image', '457', 'home');
    expect(component.game.events[0].home.teamKitIcon).toBeTruthy();
    expect(spyOnSetSelectionToComponent).toHaveBeenCalled();
  });

  it('shouldn`t call get selected because of differences ids', () => {
    const homeComponent = { id: '456', svgList: { reinitSvgElement: () => {} }, selected: {} };
    const spyOnSetSelectionToComponent = spyOn(component, 'getSelected').and.returnValue(homeComponent as any);
    component.homeComponents = [homeComponent] as any;
    component.game = game.body as any;
    component.game.events = [{ eventId: '457', home: {}, away: {} }];
    component.onChange('image', '457', 'home');
    expect(component.game.events[0].home.teamKitIcon).toBeUndefined();
    expect(spyOnSetSelectionToComponent).not.toHaveBeenCalled();
  });

  it('should not sat image because of nonexistent event', () => {
    const homeComponent = { id: '456', svgList: { reinitSvgElement: () => {} }, selected: {} };
    const spyOnSetSelectionToComponent = spyOn(component, 'getSelected').and.returnValue(homeComponent as any);
    component.homeComponents = [homeComponent] as any;
    component.game = game.body;
    component.game.events = [{ eventId: '457', home: {}, away: {} }];
    component.onChange('image', '999', 'away');
    expect(component.game.events[0].home.teamKitIcon).toBe(undefined);
    expect(spyOnSetSelectionToComponent).not.toHaveBeenCalled();
  });

  it('should parse full name', () => {
    const fullName = '/images/uploads/teamKit/bma/liverpool1.svg';
    let displayName = component.parseSvgName(fullName);
    expect(displayName).toBe('liverpool1.svg');
    displayName = component.parseSvgName('');
    expect(displayName).toBe('');
  });
});
