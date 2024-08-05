import { EuroLoyaltyDashboardComponent } from '@app/special-pages/euro-loyalty/euro-loyalty-dashboard/euro-loyalty-dashboard.component';
import { of } from 'rxjs/observable/of';
import { CONFIGGROUP_MOCK, EUROLOYAL_MOCK, MESSAGES_MOCK, NEWCONFIGGROUPSET2_MOCK, NEWCONFIGGROUPSET_MOCK, NEWCONFIG_MOCK, NEWITEM_MOCK, WRONGCONFIG_MOCK } from '@app/special-pages/constants/euro-dashboard';
import { fakeAsync, tick } from '@angular/core/testing';
import { throwError } from 'rxjs';

describe('EuroLoyaltyDashboardComponent', () => {
    let component: EuroLoyaltyDashboardComponent;

    let apiClientService,
        dialogService,
        globalLoaderService,
        brandService,
        euroLoyaltyValidationService,
        specialPagesValidationService,
        euroLoyalty;

    beforeEach(() => {
        euroLoyalty = EUROLOYAL_MOCK;
        apiClientService = {
            euroLoyalty: jasmine.createSpy('euroLoyalty').and.returnValue({
                getConfig: jasmine.createSpy('getConfig').and.returnValue(of({ body: euroLoyalty })),
                updateConfig: jasmine.createSpy('getConfig').and.returnValue(of({ body: euroLoyalty })),
                saveConfig: jasmine.createSpy('getConfig').and.returnValue(of({ body: euroLoyalty })),
                deleteConfig: jasmine.createSpy('getConfig').and.returnValue(of({}))
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
        euroLoyaltyValidationService = {
            isValidConfigProperty: jasmine.createSpy('isValidConfigProperty').and.returnValue(true)
        };
        specialPagesValidationService = {
            isUnique: jasmine.createSpy('isUnique').and.returnValue(true)
        };

        component = new EuroLoyaltyDashboardComponent(
            apiClientService,
            euroLoyaltyValidationService,
            globalLoaderService,
            dialogService,
            brandService,
            specialPagesValidationService
            );
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
            component.euroLoyalty.brand = 'bma';
            const brand = 'bma';
            component['initForm']();
            expect(component.form.get('tierName')).toBeTruthy();
            expect(component.form.get('offerIdSeq')).toBeTruthy();
            expect(component.form.get('freeBetPositionSequence')).toBeTruthy();
            expect(component.form.get('fullTermsURI')).toBeTruthy();
            expect(component.form.get('howItWorks')).toBeTruthy();
            expect(component.form.get('termsAndConditions')).toBeTruthy();
            expect(component.euroLoyalty.brand).toEqual(brand);
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
                tierName: '',
                offerIdSeq: '',
                freeBetPositionSequence: ''
            };
            component['updateNewItem'](false);
            expect(component.isAddingItem).toEqual(false);
            expect(component.newItem).toEqual(component.newItem);
        });
    });

    describe('updateLocationOrder', () => {
        it('sorts the values paseed', () => {
            component['updateLocationOrder']('5,3,9');
            expect(component.updateLocationOrder('5,3,9')).toEqual([3, 5, 9]);
        });
    });

    describe('submitNewProperty', () => {
        it('submits new property', () => {
            euroLoyalty.tierInfo = [
                {
                    tierName: '1',
                    offerIdSeq: [11],
                    freeBetPositionSequence: [12345, 23456]
                },
                {
                    tierName: '2',
                    offerIdSeq: [12],
                    freeBetPositionSequence: [12245, 23256]
                }];
            component.configGroup.items = euroLoyalty.tierInfo;
            component.newItem = NEWITEM_MOCK;
            const newConfig = NEWCONFIG_MOCK;
            spyOn(component, 'updateEuroLoyaltyTierInfo');
            spyOn(component, 'sortConfig');
            spyOn(component, 'finishAddingNewItem');
            spyOn(component, 'resetEditState');
            component['submitNewProperty']();
            expect(component.isDataChanged).toEqual(true);
            expect(euroLoyalty.tierInfo).toEqual(newConfig.items);
            expect(component.configGroupBackup).toEqual(newConfig);
        });
    });

    describe('saveConfigGroupChanges', () => {
        it('updates config group', () => {
            component.configGroup = CONFIGGROUP_MOCK;
            spyOn(component, 'updateEuroLoyaltyTierInfo');
            spyOn(component, 'sortConfig');
            spyOn(component, 'resetEditState');

            component['saveConfigGroupChanges']();
            expect(component.euroLoyalty.tierInfo).toEqual(component.configGroup.items);
            expect(component.configGroupBackup).toEqual(component.configGroup);
        });
        it('does not updates config group when data is incorrect', () => {
            component.configGroup = WRONGCONFIG_MOCK;

            spyOn(component, 'updateEuroLoyaltyTierInfo');
            spyOn(component, 'sortConfig');
            spyOn(component, 'resetEditState');
            euroLoyaltyValidationService.isValidConfigProperty = jasmine.createSpy('isValidConfigProperty').and.returnValue(false);
            component['saveConfigGroupChanges']();
            expect(euroLoyalty.tierInfo).not.toEqual(component.configGroup.items);
            expect(component.configGroupBackup).not.toEqual(component.configGroup);
        });
    });

    describe('removePropertyFromGroup', () => {
        it('displays removed property popup', () => {
            component.configGroup = CONFIGGROUP_MOCK;

            spyOn(component, 'sortConfig');
            component['removePropertyFromGroup'](1);
            expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
                title: `Remove Property from Group`,
                message: `Are You Sure You Want to Remove This Property?`,
                yesCallback: jasmine.any(Function)
            });
            expect(component.euroLoyalty.tierInfo).toEqual(component.configGroup.items);
        });
        it('does not delete the property if length of items is 1', () => {
            component.configGroup.items.length = 1;
            component['removePropertyFromGroup'](0);
            expect(component.isEditOn).toEqual(true);
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
        it('failed get call', fakeAsync(() => {
            apiClientService.euroLoyalty().getConfig.and.returnValue(throwError(new Error('message')));
            component['loadInitData']();
            tick();
            tick();
            expect(apiClientService.euroLoyalty().getConfig).toHaveBeenCalled();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
            expect(component.updateForm).toBeTrue();
        }));
    });

    describe('updateText', () => {
        it('should update howItWorks text', () => {
            component.updateText(euroLoyalty.howItWorks, 'how-it-works-text');
            expect(euroLoyalty.howItWorks).toEqual(euroLoyalty.howItWorks);
        });

        it('should update termsAndConditions text', () => {
            component.updateText(euroLoyalty.termsAndConditions, 'terms-and-conditions-text');
            expect(euroLoyalty.termsAndConditions).toEqual(euroLoyalty.termsAndConditions);
        });
    });

    describe('checkLimit', () => {
        it('sets limitExceed msg', () => {
            component['checkLimit']('Limit exceeded');
            expect(component.limitExceeded).toEqual(true);
        });
    });

    describe('actionsHandler', () => {
        it('should delegate to save config option', () => {
            spyOn(component, 'saveChanges');
            component.actionsHandler('save');
            expect(component['saveChanges']).toHaveBeenCalled();
        });

        it('should delegate to revert config option', () => {
            spyOn(component, 'loadBackupForm');
            component.actionsHandler('revert');
            expect(component['loadBackupForm']).toHaveBeenCalled();
        });

        it('should delegate to remove config option', () => {
            spyOn(component, 'removeConfig');
            component.actionsHandler('remove');
            expect(component['removeConfig']).toHaveBeenCalled();
        });
    });

    describe('hideLoading', () => {
        it('calls hideLoader method of globalLoaderService', () => {
            component['hideLoading']();
            expect(globalLoaderService.hideLoader).toHaveBeenCalled();
        });
    });

    describe('saveChanges', () => {
        it('updates tierInfo', () => {
            component.configGroupBackup = CONFIGGROUP_MOCK;
            spyOn(component, 'saveConfig');
            component['saveChanges']();
            expect(component.euroLoyalty.tierInfo).toEqual(component.configGroupBackup.items);
        });
        it('updates the form', () => {
            component.updateForm = true;
            spyOn(component, 'updateConfig');
            component['saveChanges']();
            expect(component['updateConfig']).toHaveBeenCalled();
        });
        it('saves the form', () => {
            component.updateForm = false;
            spyOn(component, 'saveConfig');
            component['saveChanges']();
            expect(component['saveConfig']).toHaveBeenCalled();
        });
    });

    describe('loadBackupForm', () => {
        it('loads backup form', () => {
            const backupEuroLoyalty = euroLoyalty;
            spyOn(component, 'loadBackupForm');
            component['loadBackupForm']();
            expect(euroLoyalty).toEqual(backupEuroLoyalty);
        });
    });

    describe('updateConfig', () => {
        it('updates the config and notifies about it', () => {
            component.actionButtons = jasmine.createSpyObj(['extendCollection']);
            component['updateConfig']();
            expect(apiClientService.euroLoyalty().updateConfig).toHaveBeenCalled();
            expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(euroLoyalty);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
                {
                title: MESSAGES_MOCK.configTitle,
                message: MESSAGES_MOCK.configUpdateMsg
                });
        });
    });

    describe('saveConfig', () => {
        it('saves the config and notifies about it', () => {
            component.actionButtons = jasmine.createSpyObj(['extendCollection']);
            component['saveConfig']();
            expect(apiClientService.euroLoyalty().saveConfig).toHaveBeenCalled();
            expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(euroLoyalty);
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
                {
                title: MESSAGES_MOCK.configTitle,
                message: MESSAGES_MOCK.configSaveMsg
                });
            expect(component.updateForm).toBeTrue();
        });
    });

    describe('removeConfig', () => {
        it('removes the saved config and notifies about it', () => {
            spyOn(component, 'loadInitData');
            component['removeConfig']();
            expect(apiClientService.euroLoyalty().deleteConfig).toHaveBeenCalled();
            expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
                {
                    title: MESSAGES_MOCK.removeConfigTitle,
                    message: MESSAGES_MOCK.configRemoveMsg
                });
            expect(component.updateForm).toBeFalse();
            expect(component.deleteButton).toBeFalse();
        });
    });

    describe('isValidForm', () => {
        it('return value based on parameters', () => {
            component.configGroupBackup = CONFIGGROUP_MOCK;
            component['isValidForm'](component.euroLoyalty);
            expect(component.isValidForm(euroLoyalty)).toEqual(true);
        });
    });

    describe('updateEuroLoyaltyTierInfo', () => {
        it('converts offerIdSeq and freeBetPositionSequence into array of numbers', () => {
            component.configGroup = {
                items : [
                    {
                        tierName: '1',
                        offerIdSeq: '11',
                        freeBetPositionSequence: '12345, 23456'
                    },
                    {
                        tierName: '2',
                        offerIdSeq: '12',
                        freeBetPositionSequence: '12245, 23256'
                    }
                ]
            };
            component['updateEuroLoyaltyTierInfo'](component.configGroup.items);
            expect(component.configGroup.items).toEqual(NEWCONFIGGROUPSET2_MOCK.items);
        });
    });

    describe('sortConfig', () => {
        it('sorts config based on tierName', () => {
            component.configGroup = {
                items : [
                    {
                        tierName: '3',
                        offerIdSeq: [13],
                        freeBetPositionSequence: [12345, 23356]
                    },
                    {
                        tierName: '1',
                        offerIdSeq: [11],
                        freeBetPositionSequence: [12345, 23456]
                    }
                ]
            };
            component['sortConfig'](component.configGroup.items, 'tierName');
            expect(component.configGroup.items).toEqual(NEWCONFIGGROUPSET_MOCK.items);
        });
    });

});
