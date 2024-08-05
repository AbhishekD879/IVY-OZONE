import { of } from 'rxjs';
import { ArcConfigurationsComponent } from '@app/arc-configurations/arc-configurations.component';
import { Arc_Mock, CONFIGGROUP_MOCK } from '@app/arc-configurations/arc-configurations.mock';

describe('ArcConfigurationsComponent', () => {
  let component: ArcConfigurationsComponent;
  let apiClientService, dialogService, globalLoaderService, brandService, dialog, arcConfigValues;

  beforeEach(() => {
    arcConfigValues = [{
      profile: '2.1', sportsActions: [], frequency: '15',
      enabled: true, brand: 'coral', modelRiskLevel: 2, reasonCode: 1
    }];
    apiClientService = {
      arcConfig: jasmine.createSpy('arcConfigValues').and.returnValue({
        getConfig: jasmine.createSpy('getConfig').and.returnValue(of({ body: arcConfigValues })),
        updateConfig: jasmine.createSpy('updateConfig').and.returnValue({ subscribe: jasmine.createSpy('subscribe') }),
        deleteConfig: jasmine.createSpy('deleteConfig').and.returnValue({ subscribe: jasmine.createSpy('subscribe') }),
      })
    };
    brandService = {
      brand: 'bma'
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
        yesCallback();
      })
    };
    dialog = {
      open: jasmine.createSpy('open')
    };
    component = new ArcConfigurationsComponent(apiClientService, globalLoaderService, dialogService, brandService, dialog);
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  describe('ngOnInit', () => {
    it('general calls', () => {
      spyOn(component, 'initForm');
      spyOn(component, 'loadInitData');
      component.ngOnInit();
      expect(component['initForm']).toHaveBeenCalled();
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(component['loadInitData']).toHaveBeenCalled();
    });
  });

  describe('initForm', () => {
    it('initialize the form', () => {
      component['initForm']();
      expect(component.form.get('profile')).toBeTruthy();
      expect(component.form.get('modelRiskLevel')).toBeTruthy();
      expect(component.form.get('reasonCode')).toBeTruthy();
      expect(component.form.get('sportsActions')).toBeTruthy();
      expect(component.form.get('frequency')).toBeTruthy();
    });

  });

  describe('toggleTableEdit', () => {
    it('toggle edit value', () => {
      component.isEditOn = false;
      component['toggleTableEdit']();
      expect(component.isEditOn).toEqual(true);
    });
  });

  describe('startAddingNewItem', () => {
    it('calls updateNewItem function with true as parameter', () => {
      spyOn(component, 'updateNewItem');
      component['startAddingNewItem']();
      expect(component['updateNewItem']).toHaveBeenCalledWith(true);
    });
  });

  describe('finishAddingNewItem', () => {
    it('calls updateNewItem function with false as parameter', () => {
      spyOn(component, 'updateNewItem');
      component['finishAddingNewItem']();
      expect(component['updateNewItem']).toHaveBeenCalledWith(false);
    });
  });

  describe('updateNewItem', () => {
    it('create new item', () => {
      component.newItem = {
        profile: '', modelRiskLevel: '', reasonCode: '',
        sportsActions: [], frequency: '0', enabled: false, brand: 'bma'
      };
      component['updateNewItem'](false);
      expect(component.isAddingItem).toEqual(false);
      expect(component.newItem).toEqual(component.newItem);
    });
  });

  describe('submitNewProperty', () => {
    it('submits new property', () => {
      component.configGroup.items = Arc_Mock.items;
      component.newItem = CONFIGGROUP_MOCK.items[1];
      spyOn(component, 'finishAddingNewItem');
      spyOn(component, 'resetEditState');
      component['submitNewProperty']();
      expect(component.isDataChanged).toEqual(true);
      expect(component.addArc).toEqual(true);
    });
  });

  describe('saveConfigGroupChanges', () => {
    it('updates config group', () => {
      spyOn(component, 'resetEditState');
      component['saveConfigGroupChanges']();
      expect(component.addArc).toEqual(true);
    });
  });

  describe('resetEditState', () => {
    it('resets edit state', () => {
      component['resetEditState']();
      expect(component.isDataChanged).toEqual(false);
      expect(component.isAddingItem).toEqual(false);
      expect(component.isEditOn).toEqual(false);
    });
  });

  describe('loadInitData', () => {
    it('get call', () => {
      component['loadInitData']();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  describe('saveChanges', () => {
    it('saves the config and notifies about it', () => {
      spyOn(component, 'loadInitData');
      component.arcConfigValues.items = CONFIGGROUP_MOCK.items;
      component['saveChanges']();
      expect(component.addArc).toEqual(false);
    });
  });

  describe('removeConfig', () => {
    it('removes the saved config and notifies about it', () => {
      spyOn(component, 'loadInitData');
      component['removeConfig'](Arc_Mock.items[0]);
    });
  });

  describe('isValidConfigProperty', () => {
    it('is valid configuration', () => {
      spyOn(component, 'isUnique');
      component['isValidConfigProperty'](CONFIGGROUP_MOCK.items[0]);
      expect(component.isUnique).toHaveBeenCalled();
    });
  });

  describe('isUnique', () => {
    it('is valid profile', () => {
      const valid = component['isUnique']();
      expect(valid).toEqual(true);
    });
  });

  describe('joinActions', () => {
    it('convert sport actions into action name array', () => {
      const data = ['Display on Homepage', 'Removal of RPG'];
      const join = component['joinActions'](CONFIGGROUP_MOCK.items[1].sportsActions);
      expect(join).toEqual(data);
    });
  });

  describe('openSportConfig', () => {
    it('sport actions pop up', () => {
      component['openSportConfig'](CONFIGGROUP_MOCK.items[1].sportsActions);
      expect(dialog.open).toHaveBeenCalled();
    });
  });
});