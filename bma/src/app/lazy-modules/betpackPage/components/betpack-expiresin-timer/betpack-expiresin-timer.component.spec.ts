import { ComponentFixture } from "@angular/core/testing";
import { BetpackExpiresinTimerComponent } from "./betpack-expiresin-timer.component";

describe("BetpacExpiresinTimerComponent", () => {
  let component: BetpackExpiresinTimerComponent;
  let fixture: ComponentFixture<BetpackExpiresinTimerComponent>;
  let timeSyncService;
  let timeService;
  let windowRef;
  let changeDetectorRef;

  beforeEach(() => {
     timeSyncService = {
      getTimeDelta: jasmine.createSpy("getTimeDelta").and.returnValue(123),
    };
     timeService = {
      formatByPattern: jasmine
        .createSpy("getTimeDelta")
        .and.returnValue("formattedTime"),
    };
     windowRef = {
      nativeWindow: {
        _setTimeoutId: 5,
        _setTimeoutCb: null,
        setTimeout: jasmine
          .createSpy("setTimeout")
          .and.callFake((cb, delay) => {
            windowRef.nativeWindow._setTimeoutCb = cb;
            return windowRef.nativeWindow._setTimeoutId;
          }),
        clearTimeout: jasmine.createSpy("clearTimeout"),
      },
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy("markForCheck"),
      detectChanges: jasmine.createSpy("detectChanges"),
    };

    component = new BetpackExpiresinTimerComponent(
      timeSyncService,
      timeService,
      windowRef,
      changeDetectorRef
    );
  });
  it("should create", () => {
    expect(component).toBeTruthy();
  });

  it("should set properties", () => {
    expect((component as any).DURATION).toEqual(86400000);
    expect((component as any).timeDelta).toEqual(123);
    expect(timeSyncService.getTimeDelta).toHaveBeenCalled();
  });

  it("ngOnInit should call init method", () => {
    spyOn(component as any, "init");
    component.ngOnInit();
    expect((component as any).init).toHaveBeenCalled();
  });

  describe("ngOnChanges", () => {
    beforeEach(() => {
      spyOn(component as any, "init");
    });
    it("should call init method", () => {
      component.ngOnChanges({ timer: true } as any);
      expect((component as any).init).toHaveBeenCalled();
    });
    it("should not call init method", () => {
      component.ngOnChanges({ timer: null } as any);
      expect((component as any).init).not.toHaveBeenCalled();
    });
  });

  describe("ngOnDestroy", () => {
    it("should clear timeouts", () => {
      component.nextTick = 1;
      component.postpone = 2;
      component.ngOnDestroy();
      expect(windowRef.nativeWindow.clearTimeout.calls.allArgs()).toEqual([
        [1],
        [2],
      ]);
    });
    it("should not clear timeouts", () => {
      component.nextTick = null;
      component.postpone = null;
      component.ngOnDestroy();
      expect(windowRef.nativeWindow.clearTimeout).not.toHaveBeenCalled();
    });
  });

  describe("init", () => {
    let date;
    beforeEach(() => {
      date = {
        date: Symbol("date"),
        getTime: jasmine.createSpy("getTime").and.returnValue(1234567),
      };
      spyOn(window as any, "Date").and.returnValue(date);
      spyOn(component as any, "getDiff");
      spyOn(component as any, "tick");
    });

    describe("should do nothing", () => {
      it("if timer is unavailable", () => (component.timer = null));
      it("if timer has no startTime", () => (component.timer = '' as any));
      afterEach(() => {
        component.init();
        expect(component.utc).not.toBeDefined();
        expect((component as any).getDiff).not.toHaveBeenCalled();
        expect((component as any).tick).not.toHaveBeenCalled();
        expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
      });
    });

    describe("if timer.startTime is available", () => {
      beforeEach(() => {
        component.timer = "13:52" as any;
      });

      describe("should set utc value to", () => {
        it('"UTC" if truthy', () => {
          component.utc = "yes";
          component.init();
          expect(component.utc).toEqual("UTC");
        });
        it("undefined if falsy", () => {
          component.utc = null;
          component.init();
          expect(component.utc).toEqual(undefined);
        });
      });

      describe("should set displayTime value to", () => {
        it("same value if not undefined", () => {
          component.displayTime = false;
          component.init();
          expect(component.displayTime).toEqual(false);
        });
        it("same value if not undefined", () => {
          component.displayTime = true;
          component.init();
          expect(component.displayTime).toEqual(true);
        });
        it("true if undefined", () => {
          component.displayTime = undefined;
          component.init();
          expect(component.displayTime).toEqual(true);
        });
      });

      describe("should set displayCountdown value to", () => {
        it("same value if not undefined", () => {
          component.displayCountdown = false;
          component.init();
          expect(component.displayCountdown).toEqual(false);
        });
        it("same value if not undefined", () => {
          component.displayCountdown = true;
          component.init();
          expect(component.displayCountdown).toEqual(true);
        });
        it("true if undefined", () => {
          component.displayCountdown = undefined;
          component.init();
          expect(component.displayCountdown).toEqual(true);
        });
      });

      it("should set startTime to timer.startTime parsed time", () => {
        component.init();
        expect((component as any).startTime).toEqual(1234567);
        expect((window as any).Date).toHaveBeenCalledWith("13:52");
        expect(date.getTime).toHaveBeenCalled();
      });

      it("should set startTimeStr to formatted timestring", () => {
        component.utc = "UTC";
        component.init();
        expect((component as any).startTimeStr).toEqual("formattedTime");
        expect((window as any).Date).toHaveBeenCalledWith("13:52");
        expect(timeService.formatByPattern).toHaveBeenCalledWith(
          '13:52',
          "HH:mm",
          "UTC"
        );
      });

      it("should set postpone timeout if getDiff is greater than 45min", () => {
        (component as any).getDiff.and.returnValue(
          (component as any).DURATION + 1
        );
        component.init();
        expect((component as any).getDiff).toHaveBeenCalled();
        expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(
          jasmine.any(Function),
          1
        );
        expect((component as any).tick).not.toHaveBeenCalled();
        windowRef.nativeWindow._setTimeoutCb();
        expect((component as any).tick).toHaveBeenCalled();
      });

      describe("should call tick if getDiff", () => {
        let value;
        it("is equal to 45min", () => {
          value = (component as any).DURATION;
        });
        it("is less than 45min", () => {
          value = (component as any).DURATION - 1;
        });
        afterEach(() => {
          (component as any).getDiff.and.returnValue(value);
          component.init();
          expect((component as any).getDiff).toHaveBeenCalled();
          expect((component as any).tick).toHaveBeenCalled();
          expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
        });
      });
    });
  });

  it("raceCountdown getter should return wCountdown value", () => {
    (component as any).wCountdown = "123";
    expect(component.raceCountdown).toEqual("123");
  });

  // it('raceStartTime getter should return startTimeStr value', () => {
  //   (component as any).startTimeStr = '456';
  //   expect(component.raceStartTime).toEqual('456');
  // });

  // it('status getter should return timer.raceStage value', () => {
  //   (component as any).timer = 'test';
  //   expect(component.status).toEqual('isOff');
  // });

  // it('statusCssClass getter should return status string value', () => {
  //   (component as any).timer = { raceStage: 'isOff' };
  //   expect(component.statusCssClass).toEqual('status-isoff');
  // });

  // describe('isTime', () => {
  //   beforeEach(() => {
  //     spyOn(component as any, 'getDiff');
  //   });
  //   describe('should return false', () => {
  //     it('if displayTime=false', () => component.displayTime = false);
  //     describe('if displayTime=true but', () => {
  //       let value;
  //       beforeEach(() => component.displayTime = true);
  //       it('start time is equal to 45min', () => value = (component as any).DURATION);
  //       it('start time is less than 45min', () => value = (component as any).DURATION - 1);
  //       afterEach(() => (component as any).getDiff.and.returnValue(value));
  //     });
  //     afterEach(() => expect((component as any).isTime()).toEqual(false));
  //   });

  //   it('should return true if start time is greater than 45min', () => {
  //     component.displayTime = true;
  //     (component as any).getDiff.and.returnValue((component as any).DURATION + 1);
  //     expect((component as any).isTime()).toEqual(true);
  //   });
  // });

  describe("isCountdown", () => {
    beforeEach(() => {
      spyOn(component as any, "getDiff");
    });
    describe("should return false", () => {
      it("if displayCountdown=false", () =>
        (component.displayCountdown = false));
      describe("if displayCountdown=true but", () => {
        let value;
        beforeEach(() => (component.displayCountdown = true));
        it("start time is equal 0", () => (value = 0));
        it("start time is equal 45min", () =>
          (value = (component as any).DURATION));
        afterEach(() => (component as any).getDiff.and.returnValue(value));
      });
      afterEach(() => expect((component as any).isCountdown()).toEqual(false));
    });

    it("should return true if start time is less than 45min", () => {
      component.displayCountdown = true;
      (component as any).getDiff.and.returnValue(
        (component as any).DURATION - 1
      );
      expect((component as any).isCountdown()).toEqual(true);
    });
  });

  describe("isOff", () => {
    beforeEach(() => {
      spyOn(component as any, "getDiff");
    });
    describe("should return false", () => {
      let value;
      it("diff is equal 0", () => (value = 0));
      it("diff is greater than 0", () => (value = 1));
      afterEach(() => {
        (component as any).getDiff.and.returnValue(value);
        expect(component.isOff()).toEqual(false);
      });
    });

    it("should return true", () => {
      (component as any).getDiff.and.returnValue(-1);
      expect(component.isOff()).toEqual(true);
    });
  });

  describe("initTimeout", () => {
    beforeEach(() => {
      spyOn(component as any, "isOff");
      spyOn(component as any, "tick");
    });
    it("diff is greater than 0", () => {
      (component as any).isOff.and.returnValue(false);
      component.initTimeout();
      expect((component as any).nextTick).toEqual(5);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(
        jasmine.any(Function),
        1000
      );
      windowRef.nativeWindow._setTimeoutCb();
      expect((component as any).tick).toHaveBeenCalled();
    });

    it("should not start new timeout", () => {
      (component as any).isOff.and.returnValue(true);
      component.initTimeout();
      expect((component as any).nextTick).not.toBeDefined();
      expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
    });
    afterEach(() => {
      expect((component as any).isOff).toHaveBeenCalled();
    });
  });

  describe("tick", () => {
    beforeEach(() => {
      spyOn(component as any, "getCountdown").and.returnValue(12);
      spyOn(component as any, "initTimeout");
    });
    it("should getCountdown and initTimeout", () => {
      component.tick();
      expect((component as any).wCountdown).toEqual(12);
      expect((component as any).getCountdown).toHaveBeenCalled();
      expect((component as any).initTimeout).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  it("format should return formatted string", () => {
    expect(component.format("9")).toEqual("09");
    expect(component.format("15")).toEqual("15");
  });

  it("formatTime should return formatted string", () => {
    expect(component.formatTime(9, 13)).toEqual("09:13");
    expect(component.formatTime(15, 2, "-")).toEqual("15-02");
  });
  it("formatTime should return formatTimebtHrs string", () => {
    expect(component.formatTimebtHrs(9, 13)).toEqual("09h 13m");
    expect(component.formatTimebtHrs(15, 2)).toEqual("15h 02m");
  });

  it("getCurrentTime should return currentTime + delta", () => {
    (component as any).timeDelta = 2345;
    spyOn(Date, "now").and.returnValue(10000);
    expect((component as any).getCurrentTime()).toEqual(12345);
    (Date as any).now.and.callThrough();
  });

  it("getDiff should return startTime - currentTime", () => {
    spyOn(component as any, "getCurrentTime").and.returnValue(2345);
    (component as any).startTime = 12345;
    expect((component as any).getDiff()).toEqual(10000);
    expect((component as any).getCurrentTime).toHaveBeenCalled();
  });

  it("getCountdown should return formatTime", () => {
    spyOn(component as any, "getDiff").and.returnValue(123456);
    spyOn(component as any, "formatTime").and.callThrough();
    expect((component as any).getCountdown()).toEqual("02:03");
    expect((component as any).formatTime).toHaveBeenCalledWith(2, 3);
  });
  
  it("getCountdown should return formatTime esle", () => {
    spyOn(component as any, "getDiff").and.returnValue(123456);
    spyOn(component as any, "formatTimebtHrs").and.callThrough();
    component.betpackReview=true
    expect((component as any).getCountdown()).toEqual("0h 2m");
    expect((component as any).formatTimebtHrs).toHaveBeenCalledWith(0,2);
  });
});
