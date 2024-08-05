import { fakeAsync, tick, discardPeriodicTasks } from '@angular/core/testing';
import { SimpleChange, SimpleChanges } from '@angular/core';
import { OddsBoostUpcomingHeaderComponent } from './odds-boost-upcoming-header.component';

describe('OddsBoostUpcomingHeaderComponent', () => {
  let component;
  let windowRef;


  const changeDetectorRef = {detectChanges : () => true} as any;
  windowRef = {
    nativeWindow: {
      clearInterval: window.clearInterval, setInterval: window.setInterval,
      setTimeout:window.setTimeout, clearTimeout:window.clearTimeout
    }
  },
  beforeEach(() => {
    component = new OddsBoostUpcomingHeaderComponent(changeDetectorRef, windowRef);
  });

  it('should init countdown', fakeAsync(() => {
    const timerRegex = /^(?:2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9]$/;
    const date: Date = new Date('10/10/2025');
    const changesObj: SimpleChanges = {
      countDownDate: new SimpleChange(date, date, false)
    };
    component.ngOnChanges(changesObj);
    tick(2000);
    expect(timerRegex.test(component.countDown)).toBe(true);
    discardPeriodicTasks();
  }));

  it('shoud not init countdown', () => {
    spyOn(component, 'initCountdown');
    component.ngOnChanges({ countDownDate: {} });
    expect(component.initCountdown).not.toHaveBeenCalled();
  });

  it('should stop countdown', fakeAsync(() => {
    const date: Date = new Date();
    date.setSeconds(date.getSeconds() + 1);
    const changesObj: SimpleChanges = {
      countDownDate: new SimpleChange(date, date, false)
    };
    component.ngOnChanges(changesObj);
    tick(3000);
    expect(component.countDown).toBe('00:00:00');
    discardPeriodicTasks();
  }));

  it('should stop countdown', fakeAsync(() => {
    const changes = {type : {
      currentValue: true
    }}
    spyOn(component, 'expireOrAvailableSameTimeExpiry');
    spyOn(component, 'availableSameTime');
    component.ngOnChanges(changes);
    expect(component.availableSameTime).toHaveBeenCalled();

  }));

  it('ngOnDestroy', fakeAsync(() => {
    component.ngOnDestroy();
  }));

  it('ngOnDestroy', fakeAsync(() => {
    spyOn(component, 'initCountdown');
    component.nextCountDown(new Date());
    tick(2000)
    discardPeriodicTasks();
  }));

  it('expireOrAvailableSameTimeExpiry', () => {
    component.isLads = true;
    component.tab = true;
    component.list = false;
    component.timer = true;
    component.type = 'Available';
    component.expireOrAvailableSameTimeExpiry();
    expect(component.isDisplayedHeaderTextAvailable).toBeTruthy();
  });

  it('delayDisplay', fakeAsync(() => {
    component.delayDisplay();
    tick(1000);
    expect(component.isDisplayedHeaderText).toBeDefined();
  }));


  describe('padNumber() padding', () => {
    it('pad Number with less than 10 number', () => {
      const padnumber = component.padNumber(3);
      expect(padnumber).toEqual('03');
    });
    it('pad Number with more than 10 number', () => {
      const padnumber = component.padNumber(53);
      expect(padnumber).toEqual('53');
    });
    it('pad Number with null number ', () => {
      const padnumber = component.padNumber(null);
      expect(padnumber).toEqual('0null')
    });
    it('pad Number with undefined number ', () => {
      const padnumber = component.padNumber('undefined');
      expect(padnumber).toEqual('undefined');
    });
  });

  it('should call expireOrAvailableSameTimeExpiry and availableSameTime when sameTimeExpiry changes', () => {
    const changes = {
      sameTimeExpiry: {
        currentValue: true,
      },
    };

    spyOn(component, 'expireOrAvailableSameTimeExpiry');
    spyOn(component, 'availableSameTime');

    component.ngOnChanges(changes);

    expect(component.expireOrAvailableSameTimeExpiry).not.toHaveBeenCalled();
    expect(component.availableSameTime).not.toHaveBeenCalled();
  });

  it('should call expireOrAvailableSameTimeExpiry and availableSameTime when sport changes', () => {
    const changes = {
      sport: {
        currentValue: 'Football',
      },
    };

    spyOn(component, 'expireOrAvailableSameTimeExpiry');
    spyOn(component, 'availableSameTime');

    component.ngOnChanges(changes);

    expect(component.expireOrAvailableSameTimeExpiry).not.toHaveBeenCalled();
    expect(component.availableSameTime).not.toHaveBeenCalled();
  });

  it('should not call expireOrAvailableSameTimeExpiry and availableSameTime when other properties change', () => {
    const changes = {
      otherProperty: {
        currentValue: true,
      },
    };

    spyOn(component, 'expireOrAvailableSameTimeExpiry');
    spyOn(component, 'availableSameTime');

    component.ngOnChanges(changes);

    expect(component.expireOrAvailableSameTimeExpiry).not.toHaveBeenCalled();
    expect(component.availableSameTime).not.toHaveBeenCalled();
  });

  it('should call expireOrAvailableSameTimeExpiry and availableSameTime when sameTimeExpiry is false and sport is MultiSport', () => {
    component.sameTimeExpiry = false;
    component.sport = 'MultiSport';

    spyOn(component, 'expireOrAvailableSameTimeExpiry');
    spyOn(component, 'availableSameTime');

    component.ngOnChanges({
      sameTimeExpiry: {
        currentValue: component.sameTimeExpiry,
      },
      sport: {
        currentValue: component.sport,
      },
    });

    expect(component.expireOrAvailableSameTimeExpiry).not.toHaveBeenCalled();
    expect(component.availableSameTime).not.toHaveBeenCalled();
  });

  it('should set isDisplayedListText to true for expireOrAvailable when all conditions are met', () => {
    component.isLads = true;
    component.list = true;
    component.tab = true;
    component.timer = true;

    component.expireOrAvailable();

    expect(component.isDisplayedListText).toBeTrue();
  });

  it('should set isDisplayedListText to false for expireOrAvailable when any condition is not met', () => {
    component.isLads = true;
    component.list = true;
    component.tab = true;
    component.timer = false;
    // component.isDisplayedHeaderTextAvailable = true;
    component.type = 'Available';

    component.expireOrAvailable();

    expect(component.isDisplayedListText).toBeFalse();
  });

  it('should set isDisplayedHeaderText to true for expireOrAvailableSameTimeExpiry when all conditions are met', () => {
    component.isLads = true;
    // component.isDisplayedHeaderTextUpcoming = true;
    component.tab = false;
    component.list = false;
    component.timer = true;
    component.type = 'Upcoming'

    component.expireOrAvailableSameTimeExpiry();

    expect(component.isDisplayedHeaderTextUpcoming).toBeTrue();
  });

  it('should set isDisplayedHeaderText to false for expireOrAvailableSameTimeExpiry when any condition is not met', () => {
    component.isLads = true;
    component.tab = false;
    component.list = false;
    component.timer = true;
    component.type = 'Upcoming';
    component.expireOrAvailableSameTimeExpiry();
    expect(component.isDisplayedHeaderTextUpcoming).toBeTruthy();
  });

  it('should return true for headerText when isLads is true and headerTimeText is truthy', () => {
    component.isLads = true;
    component.headerTimeText = true;

    const result = component.headerText();

    expect(result).toBeTrue();
  });

  it('should return false for headerText when isLads is false', () => {
    component.isLads = false;
    component.headerTimeText = true;

    const result = component.headerText();

    expect(result).toBeFalse();
  });

  it('should return false for headerText when headerTimeText is falsy', () => {
    component.isLads = true;
    component.headerTimeText = false;

    const result = component.headerText();

    expect(result).toBeFalse();
  });


  it('should set headerTimeText correctly when sameTimeExpiry is true and isDisplayedHeaderText is true', () => {
    spyOn(component, 'delayDisplay');
    component.sameTimeExpiry = '1';
    component.isDisplayedHeaderTextAvailable = true;
    component.availableSameTime();
    expect(component.headerTimeText).toBe('1 of your Odds Boosts will expire in');
  });

  it('should set headerTimeText correctly when sameTimeExpiry is true and isDisplayedHeaderText is false', () => {
    component.isDisplayedHeaderTextUpcoming = true;
    component.sameTimeExpiry  = '1';
    component.availableSameTime();
    expect(component.headerTimeText).toBe('Your next 1 Odds Boosts are available in');
  });

  it('should set headerTimeText correctly when sport is provided and isDisplayedHeaderText is true', () => {
    component.sport = 'football';
    component.isDisplayedHeaderTextAvailable = true;
    component.availableSameTime();
    expect(component.headerTimeText).toBe('One of your football Odds Boost will expire in');
  });

  it('should set headerTimeText correctly when sport is provided and isDisplayedHeaderText is false', () => {
    component.sport = 'football'
    component.isDisplayedHeaderTextUpcoming = true;
    component.availableSameTime();
    expect(component.headerTimeText).toBe('Your next football Odds Boost is available in');
  });

  it('should set headerTimeText correctly when sameTimeExpiry and sport are not provided and isDisplayedHeaderText is true', () => {
    component.sport = 'MultiSport';
    component.isDisplayedHeaderTextAvailable = true;
    component.sameTimeExpiry = '1';
    component.availableSameTime();
    expect(component.headerTimeText).toBe('1 of your Odds Boosts will expire in');
  });

  it('should set headerTimeText correctly when sameTimeExpiry and sport are not provided and isDisplayedHeaderText is false', () => {
    component.sport = 'MultiSport';
    component.isDisplayedHeaderTextUpcoming = true;
    component.availableSameTime();
    expect(component.headerTimeText).toBe('Your next Odds Boosts are available in');
  });

  it('should set headerTimeText correctly when sport is provided and isDisplayedHeaderText is false', () => {
    component.sport = 'MultiSport'
    component.isDisplayedHeaderTextAvailable = true;
    component.availableSameTime();
    expect(component.headerTimeText).toBe('One of your Odds Boosts will expire in');
  });

  it('should not proceed further if timerStart is "00:00:00" and isLads is true', () => {
    component.timerStart = '00:00:00';
    component.isLads = true;
    const date = new Date();

    spyOn(component, 'checkTokenDate');

    component.initCountdown(date);

    expect(component.checkTokenDate).toHaveBeenCalled();
  });


  it('should not initialize the countdown when timerStart is "00:00:00" and isLads is true', () => {
    component.timerStart = '00:00:00';
    component.isLads = true;

    const futureDate = new Date('2023-07-07T12:00:00');
    component.initCountdown(futureDate);

    expect(component.countDown).toBe('00:00:00');
  });

  it('should initialize the countdown when timerStart is not "00:00:00" and isLads is true', () => {
    component.timerStart = '01:30:00';
    component.isLads = true;

    const futureDate = new Date('2023-07-07T12:00:00');
    component.initCountdown(futureDate);

    expect(component.countDown).toBe('00:00:00');
  });

  it('should set the countDown variable when the condition is met and isLads is true', () => {
    component.isLads = true;
    component.currentDeference = '01:00:00';
    component.timerStart = '02:00:00';
    const futureDate = new Date();
    const nowDate = new Date();
    component.initCountdown(futureDate, nowDate);

    const expectedCountDown = '00:00:00';
    expect(component.countDown).toBe(expectedCountDown);
  });

  it('should set countDown correctly when isLads is true and currentDeference is less than timerStart', () => {
    component.timerStart = '30:00:00';
    component.isLads = true;

    const futureDate = new Date();
    futureDate.setHours(futureDate.getHours() + 1);

    component.currentDeference = '00:30:00';

    component.initCountdown(futureDate);

  });

  it('should set timer to false when isLads is true and currentDeference is not less than timerStart', () => {
    component.timerStart = '01:00:00';
    component.isLads = true;
    component.list = true;

    const futureDate = new Date();
    futureDate.setHours(futureDate.getHours() + 1);

    component.currentDeference = '01:30:00';

    component.initCountdown(futureDate);

    expect(component.timer).toBeDefined();
  });

});
