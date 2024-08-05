import { FiveASideEventNameHeaderComponent } from './five-a-side-event-name-header.component';
import { of } from 'rxjs';

describe('FiveASideEventNameHeaderComponent', () => {
  let component: FiveASideEventNameHeaderComponent;
  let fiveASideService;
  let changeDetectorRef;
  let cmsService;
  let gtmServiceMock;

  const teams = {
    ARSENAL: {
      primaryColour: '#EF0107',
      secondaryColour: '#E8E8E8'
    },
    LIVERPOOL: {
      primaryColour: '#C8102E',
      secondaryColour: '#A60D26'
    }
  };

  beforeEach(() => {
      fiveASideService = {
        initTeamsColors: jasmine.createSpy('initTeamsColors').and.returnValue(of(teams)),
        teamsColors: teams,
        isLineupAvailable: jasmine.createSpy('isLineupAvailable').and.returnValue(true),
        setLineUps: jasmine.createSpy('setLineUps'),
        imagesExistOnHomeAway: []
      };
      cmsService = {
        getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({
          enabled: true,
          title: 'Open Lineup'
        } as any))
      };
      changeDetectorRef = {
        markForCheck: jasmine.createSpy('markForCheck')
      };
      gtmServiceMock = {
        push: jasmine.createSpy('push')
      };
      component = new FiveASideEventNameHeaderComponent(
        fiveASideService,
        changeDetectorRef,
        cmsService,
        gtmServiceMock
      );
    }
  );

  it('should create FiveASideEventNameHeaderComponent', () => {
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
    const expectedResult = [
      {teamName: 'ARSENAL' , colors: {primaryColour: '#EF0107', secondaryColour: '#E8E8E8'}},
      {teamName: 'LIVERPOOL', colors: {primaryColour: '#C8102E', secondaryColour: '#A60D26'}}];
    it('should get team names and colors', () => {
      component.ngOnInit();
      expect(component.teamsColors).toEqual(expectedResult);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    it('should not call unsubscribe if subscription does not exist', () => {
      component['lineupsSubscription'] = null;
      component.ngOnDestroy();
      expect(component['lineupsSubscription']).toBeNull();
    });
    it('should call unsubscribe if subscription exist', () => {
      component['lineupsSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();
      expect(component['lineupsSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('#toggleLineups', () => {
    it('should set showLineup true', () => {
      component.showLineUp = false;
      component.toggleLineups();
      expect(component.showLineUp).toBe(true);
    });
    it('should set showLineup false', () => {
      component.showLineUp = true;
      component.toggleLineups();
      expect(component.showLineUp).toBe(false);
    });
    it('should call gtm service for GA tracking on toggle lineups', () => {
      const gtmData = {
        eventCategory: '5-A-Side',
        eventAction: 'click',
        eventLabel: 'Line Ups Not Available'
      };
      component.toggleLineups();
      expect(gtmServiceMock.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });
  });

  it('should call gtm service for GA tracking on open line up', () => {
    component.eventId = 12345,
    component.eventCategory = 'FOOTBALL';
    component.onOpenLineUp();
    expect(fiveASideService.setLineUps).toHaveBeenCalled();
  });

  it('should set line ups', () => {
    const gtmData = {
      eventCategory: '5-A-Side',
      eventAction: 'click',
      eventLabel: 'Line Ups Button'
    };
    component.onOpenLineUp();
    expect(gtmServiceMock.push).toHaveBeenCalledWith('trackEvent', gtmData);
  });

  describe('#setLineupsTooltip', () => {
    it('should not set lineupstooltip, if both conditions does not satisfy', () => {
      const config = {};
      cmsService.getFeatureConfig.and.returnValue(of(config));
      component['setLineupsTooltip']();
      expect(component['lineupsTooltip']).toBe(undefined);
    });
    it('should not set lineupstooltip, if only one condition satisfy', () => {
      const config = {
          enabled: false
      };
      cmsService.getFeatureConfig.and.returnValue(of(config));
      component['setLineupsTooltip']();
      expect(component['lineupsTooltip']).toBe(undefined);
    });
    it('should set lineupstooltip, if both condition satisfy(length > 200)', () => {
      const config = {
          enabled: true,
          title: `Look below to find out what other markets are available Look below to find out what other markets hie, Look below to find
           out what other markets are available Look below to find out what other markets hie`
      };
      cmsService.getFeatureConfig.and.returnValue(of(config));
      component['setLineupsTooltip']();
      expect(component['lineupsTooltip']).toBe(`${config.title.substring(0,200)}...`);
    });
    it('should set lineupstooltip, if both condition satisfy(lngth < 200)', () => {
      const config = {
          enabled: true,
          title: 'welcome'
      };
      cmsService.getFeatureConfig.and.returnValue(of(config));
      component['setLineupsTooltip']();
      expect(component['lineupsTooltip']).toBe(config.title);
    });
  });
});
