import { DevLogComponent } from '@lazy-modules/devLog/components/devLog/dev-log.component';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';


describe('DevLogComponent', () => {
  const devlogCharsMap = [68, 69, 86, 76, 79, 71];
  const wrongDevlogCharsMap = [11, 22, 33];

  const buildInfoMock = {};
  const http: any = {
    get: jasmine.createSpy().and.returnValue(of(buildInfoMock))
  };
  const windowRefService: any = {
    nativeWindow: {
      localStorage: {
        clear: jasmine.createSpy('clear'),
        setItem: jasmine.createSpy('setItem'),
        getItem: jasmine.createSpy('getItem').and.returnValue(null)
      },
      location: {
        search: 'qa=1',
        reload: jasmine.createSpy('reload')
      },
      scrollTo: jasmine.createSpy('scrollTo')
    }
  };

  let component;

  beforeEach(() => {
    component = new DevLogComponent(
      http,
      windowRefService
    );
    spyOn(component, 'openConsole').and.callThrough();
    spyOn(component, 'closeConsole').and.callThrough();
  });

  it('should init with QA parameter in url', fakeAsync(() => {
    component.environment = {
      production: false
    };

    component.ngOnInit();

    expect(component.isNotProduction).toBeTruthy();
    expect(component.openConsole).toHaveBeenCalled();
    expect(component.isOpened).toBeTruthy();
    expect(component.currentEnvironment).toEqual('dev0');

    tick(100);

    expect(component.data).toEqual(buildInfoMock);
  }));

  it('should init with data in LocalStorage', () => {
    component.environment = { production: true };
    component.windowRefService.nativeWindow.location.search = '';
    component.windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.returnValue('devProduction');

    component.ngOnInit();
    expect(component.openConsole).not.toHaveBeenCalled();
    expect(component.currentEnvironment).toEqual('devProduction');
  });

  it('should close panel onClick and change state', () => {
    component.isOpened = true;

    component.closeConsole();

    expect(component.isOpened).toBeFalsy();
  });

  describe('setNewEnvironment', () => {
    it('should set new env and clear query params', () => {
      windowRefService.nativeWindow.location.search = component.consoleOpenQueryKey;
      component.setNewEnvironment('dev1');
      expect(windowRefService.nativeWindow.localStorage.clear).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.localStorage.setItem).toHaveBeenCalledWith('env', 'dev1');
      expect(windowRefService.nativeWindow.location.search).toEqual('');
    });

    it('should set new env and reload page', () => {
      component.setNewEnvironment('dev1');
      expect(windowRefService.nativeWindow.localStorage.clear).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.localStorage.setItem).toHaveBeenCalledWith('env', 'dev1');
      expect(windowRefService.nativeWindow.location.reload).toHaveBeenCalled();
    });
  });

  it('should init on onKeyDown word DEVLOG and closed by Escape BTN', () => {
    devlogCharsMap.forEach(keyCode => {
      component.onKeyDown(keyCode);
    });

    expect(component.openConsole).toHaveBeenCalled();

    component.onKeyDown(27);
    expect(component.closeConsole).toHaveBeenCalled();
  });

  it('should not init on wrong KeyDowns', () => {
    wrongDevlogCharsMap.forEach(keyCode => {
      component.onKeyDown(keyCode);
    });

    expect(component.openConsole).not.toHaveBeenCalled();
  });

  it('should track options by name', () => {
    const optionMock = {
      name: 'optionMockName'
    };

    const result = component.trackByName(optionMock);

    expect(result).toEqual(optionMock.name);
  });
});
