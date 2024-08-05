import { EditMyAccaRemoveIconComponent } from './edit-my-acca-remove-icon.component';

describe('EditMyAccaRemoveIconComponent', () => {
  let editMyAccaService, component: EditMyAccaRemoveIconComponent;

  beforeEach(() => {
    editMyAccaService = {
      removeLeg: jasmine.createSpy('removeLeg'),
      undoRemoveLegs: jasmine.createSpy('undoRemoveLegs'),
      canRemoveLegs: jasmine.createSpy('canRemoveLegs'),
      canUndoRemoveLegs: jasmine.createSpy('canUndoRemoveLegs'),
      isLegResulted: jasmine.createSpy('isLegResulted'),
      hasLegsWithLostStatus: jasmine.createSpy('hasLegsWithLostStatus')
    };
    component = new EditMyAccaRemoveIconComponent(editMyAccaService);
    component.bet = {} as any;
  });

  it('removeLeg', () => {
    const event: any = { stopPropagation: jasmine.createSpy() };

    component['removingDisabled'] = () => true;
    component.removeLeg(event);

    component['removingDisabled'] = () => false;
    component.removeLeg(event);

    expect(event.stopPropagation).toHaveBeenCalledTimes(2);
    expect(editMyAccaService.removeLeg).toHaveBeenCalledTimes(1);
  });

  it('undoRemoveLegs', () => {
    const event: any = { stopPropagation: jasmine.createSpy() };

    component['isUndoDisabled'] = () => true;
    component.undoRemoveLeg(event);

    component['isUndoDisabled'] = () => false;
    component.undoRemoveLeg(event);

    expect(event.stopPropagation).toHaveBeenCalledTimes(2);
    expect(editMyAccaService.undoRemoveLegs).toHaveBeenCalledTimes(1);
  });

  it('removingDisabled', () => {
    component.removingDisabled();
    expect(editMyAccaService.canRemoveLegs).toHaveBeenCalledTimes(1);
  });

  it('isUndoDisabled', () => {
    component.isUndoDisabled();
    expect(editMyAccaService.canUndoRemoveLegs).toHaveBeenCalledTimes(1);
  });

  describe('isShown', () => {
    it('should check if isShown (true)', () => {
      component.bet = { eventSource: {} } as any;
      component.leg = { removedLeg: false } as any;
      expect(component.isShown()).toEqual(true);
    });

    it('should return false if leg is suspended', () => {
      component.bet = { eventSource: {} } as any;
      component.leg = { removedLeg: false, status : 'suspended' } as any;
      expect(component.isShown()).toEqual(false);
    });

    it('should check if isShown (false removed leg)', () => {
      component.bet = { eventSource: {} } as any;
      component.leg = { removedLeg: true } as any;
      expect(component.isShown()).toEqual(false);
    });

    it('should check if isShown (false)', () => {
      editMyAccaService.hasLegsWithLostStatus.and.returnValue(true);
      component.bet = { eventSource: {} } as any;
      component.leg = { removedLeg: false } as any;
      expect(component.isShown()).toEqual(false);
    });
  });
});
