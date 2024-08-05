import { AccordionService } from './accordion.service';

describe('AccordionService', () => {
  let storageService;
  let service: AccordionService;

  beforeEach(() => {
    storageService = {
      get: jasmine.createSpy(),
      set: jasmine.createSpy(),
      remove: jasmine.createSpy()
    };

    service = new AccordionService(storageService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['storagePrefix']).toBe('accordion_');
  });

  it('getState', () => {
    service.getState('1');
    expect(storageService.get).toHaveBeenCalledWith(`${service['storagePrefix']}1`);
  });

  it('removeState', () => {
    service.removeState('1');
    expect(storageService.remove).toHaveBeenCalledWith(`${service['storagePrefix']}1`);
  });

  it('saveLocationStates', () => {
    service.saveLocationStates({}, '1');
    expect(storageService.set).toHaveBeenCalledWith(`${service['storagePrefix']}1`, '{}');
  });

  it('saveStateDependsOnParams (without memory location)', () => {
    service['saveState'] = jasmine.createSpy();
    service.saveStateDependsOnParams(true, '1', '');
    expect(service['saveState']).toHaveBeenCalledWith('1', true);
  });

  it('saveStateDependsOnParams (with memory location)', () => {
    service.getLocationStates = jasmine.createSpy().and.returnValue({});
    service.saveLocationStates = jasmine.createSpy();

    service.saveStateDependsOnParams(true, '1', 'M');

    expect(service.getLocationStates).toHaveBeenCalledWith('M');
    expect(service.saveLocationStates).toHaveBeenCalledWith(jasmine.any(Object), 'M');
  });

  it('getLocationStates', () => {
    service.getLocationStates('1');
    expect(storageService.get).toHaveBeenCalledWith(`${service['storagePrefix']}1`);
  });

  it('removeStatesFromLocation (nothing to remove)', () => {
    service.getLocationStates = jasmine.createSpy();

    service.removeStatesFromLocation(null, '1');
    service.removeStatesFromLocation([], '1');
    service.removeStatesFromLocation(['1'], '');

    expect(service.getLocationStates).not.toHaveBeenCalled();
  });

  it('removeStatesFromLocation (state empty)', () => {
    service.getLocationStates = jasmine.createSpy().and.returnValue({});
    service.saveLocationStates = jasmine.createSpy();

    service.removeStatesFromLocation(['1'], '1');

    expect(service.getLocationStates).toHaveBeenCalledWith('1');
    expect(storageService.remove).toHaveBeenCalledWith(`${service['storagePrefix']}1`);
    expect(service.saveLocationStates).not.toHaveBeenCalled();
  });

  it('removeStatesFromLocation (state not empty)', () => {
    const state = { '2': {} };
    service.getLocationStates = jasmine.createSpy().and.returnValue(state);
    service.saveLocationStates = jasmine.createSpy();

    service.removeStatesFromLocation(['1'], '1');

    expect(service.getLocationStates).toHaveBeenCalledWith('1');
    expect(storageService.remove).not.toHaveBeenCalledWith(`${service['storagePrefix']}1`);
    expect(service.saveLocationStates).toHaveBeenCalledWith(state, '1');
  });

  it('saveState', () => {
    service['saveState']('1', true);
    expect(storageService.set).toHaveBeenCalledWith(`${service['storagePrefix']}1`, true);
  });
});
