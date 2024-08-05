import { DatePickerComponent } from './date-picker.component';

describe('DatePickerComponent - ', () => {
  let component: DatePickerComponent;
  let timeService;
  let rendererService;
  let dateMock;
  let DateSpy;

  beforeEach(() => {
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern')
    };
    rendererService = {
      renderer: {
        createElement: jasmine.createSpy('createElement'),
        setAttribute: jasmine.createSpy('setAttribute')
      }
    };
    dateMock = {
      setHours: jasmine.createSpy('setHours'),
      getTime: jasmine.createSpy('getTime')
    };
    DateSpy = spyOn(window as any, 'Date').and.returnValue(dateMock);
    component = new DatePickerComponent(timeService, rendererService);
    component.date = { value: null };
  });

  it('should be created', () => {
    expect(component).toBeDefined();
  });

  describe('ngOnInit', () => {
    it('should call setDate', () => {
      spyOn((component as any), 'setDate').and.callThrough();
      component.ngOnInit();
      expect((component as any).setDate).toHaveBeenCalled();
    });
  });

  describe('#onChange', () => {
    beforeEach(() => {
      spyOn((component as any), 'setDate');
      spyOn((component as any), 'validateDate');
      spyOn(component, 'setInactive');
    });

    it('should not set or validate date if it is not provided' , () => {
      component.onChange(null);
      expect((window as any).Date).not.toHaveBeenCalled();
      expect(component.setInactive).not.toHaveBeenCalled();
      expect((component as any).validateDate).not.toHaveBeenCalled();
      expect((component as any).setDate).not.toHaveBeenCalled();
    });

    describe('it should set and validate date', () => {
      it('for hyphen-separated string', () => {
        component.onChange('2019-14-09');
        expect((window as any).Date).toHaveBeenCalledWith('2019-14-09');
      });
      it('for slash-separated string', () => {
        component.onChange('09/14/2019');
        expect((window as any).Date).toHaveBeenCalledWith(2019, 13, 9);
      });
      afterEach(() => {
        expect(component.date.value).toEqual(dateMock);
        expect(component.setInactive).toHaveBeenCalled();
        expect((component as any).validateDate).toHaveBeenCalled();
        expect((component as any).setDate).toHaveBeenCalled();
      });
    });
  });

  describe('setActive', () => {
    it('should set isDatePickerOpened to true', () => {
      component.setActive();
      expect(component.isDatePickerOpened).toEqual(true);
    });
  });
  describe('setInactive', () => {
    it('should set isDatePickerOpened to false', () => {
      component.setInactive();
      expect(component.isDatePickerOpened).toEqual(false);
    });
  });

  describe('formatDate', () => {
    it('should return formatted string form TimeService', () => {
      component.formatDate({ date: 'date' } as any, 'MM/yy');
      expect(timeService.formatByPattern).toHaveBeenCalledWith({ date: 'date' }, 'MM/yy');
    });
    it('should return formatted string form TimeService (default args)', () => {
      component.formatDate();
      expect(timeService.formatByPattern).toHaveBeenCalledWith(dateMock, 'dd/MM/yyyy');
      expect(DateSpy).toHaveBeenCalled();
    });
  });

  describe('isDateSupports getter', () => {
    describe('should creating dummy input element and set attributes', () => {
      let input;

      beforeEach(() => {
        input = { value: '', tagName: 'input' };
        rendererService.renderer.createElement.and.returnValue(input);
      });
      it('and return true if input value is not changed by input-date behavior', () => {
        rendererService.renderer.setAttribute.and.callFake((el, attr, value) => el[attr] = value);
        expect(component.isDateSupports).toEqual(false);
      });
      it('and return false if input value is changed by input-date behavior', () => {
        rendererService.renderer.setAttribute.and.callFake((el, attr, value) => el[attr] = attr === 'value' ? 'changed' : value);
        expect(component.isDateSupports).toEqual(true);
      });
      afterEach(() => {
        expect(rendererService.renderer.createElement).toHaveBeenCalledWith('input');
        expect(rendererService.renderer.setAttribute.calls.allArgs()).toEqual([
          [input, 'type', 'date'],
          [input, 'value', 'not-a-date']
        ]);
      });
    });
  });

  describe('setDate', () => {
    describe('should only update date.value to current Date if it equals', () => {
      it('null', () => component.date.value = null);
      it('undefined', () => component.date.value = undefined);
      afterEach(() => {
        (component as any).setDate();
        expect(DateSpy).toHaveBeenCalledWith();
        expect(DateSpy).toHaveBeenCalledTimes(1);
      });
    });

    describe('if data is defined, should set date.value to ', () => {
      let newDate;

      beforeEach(() => {
        newDate = { data: 'newDate' };
        DateSpy.and.returnValue(newDate);
        component.date.value = dateMock;
        dateMock.setHours.and.returnValue(12345670000);
      });
      it('start of the day if it is defined and dateType equals "startDate"', () => {
        component.dateType = 'startDate';
        (component as any).setDate();
        expect(dateMock.setHours).toHaveBeenCalledWith(0, 0, 0, 0);
      });

      it('end of the day if it is defined and dateType equals "startDate"', () => {
        component.dateType = 'not-startDate';
        (component as any).setDate();
        expect(dateMock.setHours).toHaveBeenCalledWith(23, 59, 59, 999);
      });
      afterEach(() => {
        expect(dateMock.setHours).toHaveBeenCalledBefore(DateSpy);
        expect(component.date.value).toEqual(newDate as any);
        expect(DateSpy).toHaveBeenCalledWith(12345670000);
      });
    });
  });

  describe('validateDate', () => {
    beforeEach(() => {
      (component as any).errorStateData = { emit: jasmine.createSpy('emit') };
      component.dateType = 'dateType';
      component.date.value = dateMock;
      dateMock.setHours.and.returnValue(12345670000);
      dateMock.getTime.and.returnValue(12345670001);
    });

    it('should set errorState.dateTypeInFuture to true', () => {
      (component as any).validateDate();
      expect((component as any).errorState['dateTypeInFuture']).toEqual(true);
    });

    it('should set errorState.dateTypeInFuture to false', () => {
      dateMock.getTime.and.returnValue(12345670000);
      (component as any).validateDate();
      expect((component as any).errorState['dateTypeInFuture']).toEqual(false);
    });

    it('should set errorState.isValiddateType to true', () => {
      (component as any).validateDate();
      expect((component as any).errorState['isValiddateType']).toEqual(true);
    });

    it('should set errorState.isValiddateType to false', () => {
      dateMock.getTime.and.returnValue(null);
      (component as any).validateDate();
      expect((component as any).errorState['isValiddateType']).toEqual(false);
    });

    afterEach(() => {
      expect((component as any).errorStateData.emit).toHaveBeenCalledWith((component as any).errorState);
    });
  });
});
