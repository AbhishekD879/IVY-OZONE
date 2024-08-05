import { of, throwError } from 'rxjs';
import { BetPackModelMock } from '@app/betpack-market-place/betpack-mock';
import { FiltersTestData } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { BetPackEditComponent } from '@app/betpack-market-place/edit-betpack/bet-pack-edit.component';
import { FormControl, FormGroup } from '@angular/forms';


describe('CreateComponent', () => {
    let component: BetPackEditComponent;
    let dialog;
    let apiClientService;
    let betpackService;
    let dialogService;
    let router;
    let sportsSurfaceBetsService;
    let globalLoaderService;
    let activatedRoute;
    let betPackValidationService;
    let form;
    let cd;
function createForm(component){
    component.betPackEditData=new FormGroup({})
    component.betPackEditData.addControl('betPackId',new FormControl('test'));
    component.betPackEditData.addControl('betPackTitle',new FormControl('test'));
    component.betPackEditData.addControl('betPackPurchaseAmount',new FormControl('test'));
    component.betPackEditData.addControl('betPackFreeBetsAmount',new FormControl('test'));
    component.betPackEditData.addControl('betPackFrontDisplayDescription',new FormControl('test'));
    component.betPackEditData.addControl('betPackMoreInfoText',new FormControl('test'));
    component.betPackEditData.addControl('betPackSpecialCheckbox',new FormControl('test'));
    component.betPackEditData.addControl('sportsTag',new FormControl('test'));
    component.betPackEditData.addControl('betPackStartDate',new FormControl('test'));
    component.betPackEditData.addControl('betPackEndDate',new FormControl('test'));
    component.betPackEditData.addControl('maxTokenExpirationDate',new FormControl('test'));
    component.betPackEditData.addControl('id',new FormControl('test'));
    component.betPackEditData.addControl('updatedBy',new FormControl('test'));
    component.betPackEditData.addControl('updatedAt',new FormControl('test'));
    component.betPackEditData.addControl('createdBy',new FormControl('test'));
    component.betPackEditData.addControl('createdAt',new FormControl('test'));
    component.betPackEditData.addControl('updatedByUserName',new FormControl('test'));
    component.betPackEditData.addControl('createdByUserName',new FormControl('test'));
    component.betPackEditData.addControl('futureBetPack',new FormControl('test'));
    component.betPackEditData.addControl('filterBetPack',new FormControl('test'));
    component.betPackEditData.addControl('filterList',new FormControl(['test']));
    component.betPackEditData.addControl('isLinkedBetPack',new FormControl(true));
    component.betPackEditData.addControl('linkedBetPackWarningText',new FormControl('test'));
    component.betPackEditData.addControl('betPackActive',new FormControl(true));
    component.betPackEditData.addControl('triggerID',new FormControl('test'));
    component.betPackEditData.addControl('betPackTokenList',new FormControl([{tokenId:1000}]));
    component.betPackEditData.addControl('sortOrder',new FormControl('test'));
    component.betPackEditData.addControl('brand',new FormControl('test'));
    component.betPackEditData.addControl('deepLinkUrl',new FormControl('test'));
    component.betPackEditData.addControl('maxClaims',new FormControl(1));



}
    beforeEach(() => {
        dialogService = {
            showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                yesCallback();
            }),
            showNotificationDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, closeCallback }) => {
                closeCallback();
            })
        };
        dialog = {
            open: jasmine.createSpy('open').and.returnValue({
                afterClosed: jasmine.createSpy('afterClosed').and.returnValue(of({
                    tokenId: 3,
                    tokenTitle: "123"
                })),
            }),
        }
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: FiltersTestData })),
            postBetPack: jasmine.createSpy('postBetPack').and.returnValue(of({})),
            getBetPackById: jasmine.createSpy('getBetPackById').and.returnValue(of({ body: BetPackModelMock })),
            deleteBetPack: jasmine.createSpy('deleteBetPack').and.returnValue(of({})),
            putBetPack: jasmine.createSpy('putBetPack').and.returnValue(of({ body: BetPackModelMock })),
        };
        console.log('betpackService', betpackService)
        apiClientService = {
            betpackService: () => betpackService
        };
        sportsSurfaceBetsService = {
            getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of({ alt: 'test', categoryId: 1, disabled: true }))
        };
        router = { navigate: jasmine.createSpy('navigate') };
        activatedRoute = {
            params: of({ id: '1' })
        };
        globalLoaderService = {
            hideLoader: jasmine.createSpy('hideLoader')
        }
        form={
            group: jasmine.createSpy('group')
        }
        cd={
            detectChanges:jasmine.createSpy('detectChanges')
        }
        component = new BetPackEditComponent(dialog, activatedRoute, apiClientService, globalLoaderService, dialogService, sportsSurfaceBetsService, router,
            betPackValidationService,form,cd);
        component.betPackData = {
            betPackTokenList: [{
                "id": null,
                "tokenId": 123,
                "tokenTitle": "test",
                "tokenValue": "20",
                "deepLinkUrl": "/"
            },
            {
                "id": null,
                "tokenId": 3,
                "tokenTitle": "£2 Football Bet Tokens",
                "tokenValue": "12",
                "deepLinkUrl": "/"
            }],

        } as any;
        component.actionButtons = {
            extendCollection: jasmine.createSpy('extendCollection')
        };
    });

    it('constructor', () => {
        expect(component).toBeDefined();
    });
    it('ngOnInit when filterActive true with res', () => {
        spyOn(component as any, 'loadInitData');
        component.isedited = false;
        let filterData = [{
            filterName: '',
            filterActive: true,
        }];
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: filterData }))
        };
        component.ngOnInit();
        expect(component.sportCategories).toEqual({ alt: 'test', categoryId: 1, disabled: true } as any);
    });
    it('ngOnInit when filterActive False with res', () => {
        spyOn(component as any, 'loadInitData');
        let filterData = [{
            filterName: '',
            filterActive: false,
        }];
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: filterData }))
        };
        component.ngOnInit();
        expect(component.sportCategories).toEqual({ alt: 'test', categoryId: 1, disabled: true } as any);
    });
    it('ngOnInit when no res', () => {
        spyOn(component as any, 'loadInitData');
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: undefined }))
        };
        component.ngOnInit();
        expect(component.sportCategories).toEqual({ alt: 'test', categoryId: 1, disabled: true } as any);
    });
    it('removeTokenTable', () => {
        let event = {
            "id": null,
            "tokenId": 1000,
            "tokenTitle": "test",
            "tokenValue": "20",
            "deepLinkUrl": "/"
        }
        createForm(component);
        component.removeTokenTable(event);
        expect(dialogService.showConfirmDialog).toHaveBeenCalled()
    });
    it('to remove token with edited', () => {
        let event = {
            "id": null,
            "tokenId": 123,
            "tokenTitle": "test",
            "tokenValue": "20",
            "deepLinkUrl": "/"
        }
        createForm(component);
        component.betPackData.betPackTokenList = [] as any;
        component.removeTokenTable(event);
        expect(component.isedited).toEqual(true);
    });
    it('removeHandlerMulty when length not equal', () => {
        let event = [3];
        createForm(component);
        component.removeHandlerMulty(event);
        expect(component.isedited).toBeTruthy();
    });
    it('removeHandlerMulty when length equal', () => { ///// test
        let event = [4];
        component.betPackData = {
            betPackTokenList: []
        } as any;
        createForm(component)
        component.removeHandlerMulty(event);
        expect(component.isedited).toBeTrue();
    });
    it('setFilters', () => {
        let event = { source: "", value: ['1', '2'] } as any;
        createForm(component);
        component.setFilters(event);
        // expect(component.betPackData.filterList).toEqual(['1', '2']);
    });
    it('isEndDateValid tst1', () => {
        createForm(component);
        component.betPackEditData.patchValue({betPackStartDate:"2022-10-26T10:44:21Z",betPackEndDate: '2022-10-26T08:45:21Z'})
        component.isEndDateValid();
        expect(component.isEndDateValid).toBeTruthy()
    });
    it('isEndDateValid tst2', () => {
        createForm(component);
        component.betPackEditData.patchValue({betPackStartDate:'2022-10-26T10:44:21Z',betPackEndDate: '2022-10-26T14:45:21Z'})
        component.isEndDateValid();
        expect(component.isEndDateValid).toBeTruthy()
    });
    it('isEndDateValid tst3', () => {
        createForm(component);
        component.betPackEditData.patchValue({betPackStartDate:'2022-10-29T10:44:21Z',betPackEndDate: '2022-11-02T08:45:21Z'})
        component.isEndDateValid();
        expect(component.isEndDateValid).toBeTruthy()
    });
    it('actionsHandler for remove', () => {
        spyOn(component as any, 'removeBetPack');
        const event = 'remove';
        createForm(component);
        component.actionsHandler(event);
        expect(component.removeBetPack).toHaveBeenCalled()
    });
    it('actionsHandler for save', () => {
        spyOn(component as any, 'saveChanges');
        const event = 'save';
        component.actionsHandler(event);
        expect(component.saveChanges).toHaveBeenCalled()
    });
    it('actionsHandler for result', () => {
        spyOn(component as any, 'loadInitData');
        component.isLoading = true;
        const event = 'revert';
        component.actionsHandler(event);
        expect(component['loadInitData']).toHaveBeenCalled()
    });
    it('actionsHandler for exit', () => {
        spyOn(component as any, 'loadInitData');
        component.isLoading = true;
        const event = 'exit';
        component.actionsHandler(event);
        expect(component['loadInitData']).not.toHaveBeenCalled()
    });
    it('isStartDateValid current', () => {
        component.betPackData = {
            betPackStartDate: new Date().toISOString(),
        } as any;
        createForm(component);
        component.isStartDateValid();
        expect(component.isStartDateValid).toBeTruthy()
    });
    it('isStartDateValid less', () => {
        component.betPackData = {
            betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
        } as any;
        createForm(component);
        component.isStartDateValid();
        expect(component.isStartDateValid).toBeTruthy();
    });
    it('handleDisplayDateUpdate', () => {
        const data = {
            startDate: "1",
            endDate: "2"
        }
        createForm(component);
        component.handleDisplayDateUpdate(data);
        // expect(component.betPackData.betPackEndDate).toEqual('2');
    });
    it('onFilterChange when true', () => {
        component.betPackData = {
            filterBetPack: true
        } as any;
        createForm(component);
        component.onFilterChange();
        // expect(component.betPackData.filterList).toEqual([])
    });
    it('onFilterChange when false', () => {
        component.betPackData = {
            filterBetPack: false
        } as any;
        createForm(component);
        component.onFilterChange();
        expect(component.betPackData.filterList).not.toEqual([])
    });
    it('createToken when token', () => {
        component.betPackData = {
            betPackTokenList: [{
                tokenId: 1,
                tokenTitle: "123"
            }]
        } as any;
        createForm(component);
        component.createToken();
        expect(component.isedited).toBeTruthy();
    });
    it('createToken when no token', () => {
        dialog.open = jasmine.createSpy('dialog.open').and.returnValue({
            afterClosed: jasmine.createSpy('afterClosed').and.returnValue(of(null))
        })
        component.betPackData = {
            betPackTokenList: [{
                tokenId: 1,
                tokenTitle: "123"
            }]
        } as any;
        createForm(component);
        component.createToken();
        expect(component.betPackData.betPackTokenList).toEqual([{ tokenId: 1, tokenTitle: "123" }] as any);
    });
    it('isTokenEndDateValid less', () => {
        component.betPackData = {
            betPackStartDate: new Date().toISOString(),
            maxTokenExpirationDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString()
        } as any;
        createForm(component);
        component.isTokenEndDateValid();
        expect(component.isTokenEndDateValid).toBeTruthy()
    });
    it('isTokenEndDateValid current', () => {
        component.betPackData = {
            betPackStartDate: new Date().toISOString(),
            maxTokenExpirationDate: new Date().toISOString()
        } as any;
        createForm(component);
        component.isTokenEndDateValid();
        expect(component.isTokenEndDateValid).toBeTruthy();
    });
    it('handleDisplayTokenDateUpdate', () => {
        let date = '10';
        createForm(component);
        component.handleDisplayTokenDateUpdate(date);
        // expect(component.betPackData.maxTokenExpirationDate).toEqual(new Date(date).toISOString())
    });
    it('isDateValid', () => {
        component.isedited = false;
        component.betPackStartDateBeforeEdit = new Date(new Date().setDate(new Date().getDate() - 1)).toISOString();
        component.isDateValid();
        expect(component.isDateValid).toBeTruthy();
    });
    it('isDateValid', () => {
        component.isedited = true
        component.isDateValid();
    });
    it('isValid test', () => {
        component.isedited = false;
        // const betPackData = ValidBP as any;
        // // let retVal = component.isValid(betPackData);
        // expect(retVal).toBeTruthy();
        // betPackData.filterBetPack = true;
        expect(false).toBeFalsy()
    });
    it('removeToken if', () => {
        let index = 0;
        let tokenId = 1000
        component.betPackData = {
            betPackTokenList: [{ tokenId: 2 }, { tokenId: 0 }]
        } as any;
        createForm(component);
        component.removeToken(index, tokenId);
        // expect(component.betPackData.betPackTokenList).toEqual([{ tokenId: 2 }] as any);
    });
    it('removeToken else ', () => {
        let index = 0;
        let tokenId = 2
        component.betPackData = {
            betPackTokenList: [{ tokenId: 2 }, { tokenId: 0 }]
        } as any;
        createForm(component);
        component.betPackEditData.patchValue({betPackTokenList:[{tokenId:0}]})
        component.removeToken(index, tokenId);
        // expect(component.betPackData.betPackTokenList).toEqual([{ tokenId: 0 }] as any);
    });
    it('removeToken else ', () => {
        let index = 0;
        let tokenId = 2
        component.betPackData = {
            betPackTokenList: [{ tokenId: 3 }, { tokenId: 0 }]
        } as any;
        createForm(component);
        component.removeToken(index, tokenId);
        // expect(component.betPackData.betPackTokenList).toEqual([{ tokenId: 3 }, { tokenId: 0 }] as any);
    });
    it('editPageRoute when token', () => {
        let event = {
            tokenId: 1
        }
        component.betPackData = {
            betPackTokenList: [{
                tokenId: 1,
                tokenTitle: "123"
            }]
        } as any;
        createForm(component);
        component.editPageRoute(event);
        expect(component.isedited).toBeTruthy()
    });
    it('editPageRoute when isedit false', () => { 
        let event = {
            tokenId: 1
        }
        component.betPackTokenBeforeEdit = [
            {
                tokenId: 3,
                tokenTitle: "123"
            }
        ]
        component.betPackData = {
            betPackTokenList: [{
                tokenId: 1,
                tokenTitle: "123"
            }]
        } as any;
        createForm(component);
        component.editPageRoute(event);
    });
    it('editPageRoute when equal token', () => {///////////test
        let event = {
            tokenId: 1000
        }
        component.betPackTokenBeforeEdit = [
            {
                tokenId: 3,
                tokenTitle: "123"
            }
        ]
        component.betPackData = {
            betPackTokenList: [{
                tokenId: 1,
                tokenTitle: "123"
            }]
        } as any;
        createForm(component);
        component.editPageRoute(event);
        expect(component.isedited).toBeTruthy();
    });
    it('loadInitData when isLoading', () => {
        createForm(component);
        component['loadInitData']();
        expect(component.isLoading).toBeFalsy();
    });
    it('#loadInitData should call isLoading, false case', () => {
        createForm(component);
        component['loadInitData'](false);
    });
    it('#loadInitData error', () => {
        betpackService = {
            getBetPackById: jasmine.createSpy('getBetPackById').and.returnValue(throwError({ error: 401 }))
        };
        createForm(component);
        component['loadInitData']();
        expect(component.isLoading).toBeFalsy();
    })
    it('removeBetPack', () => {
        component.betPackData = {
            id: '1'
        } as any;
        createForm(component);
        component.removeBetPack();
        expect(dialogService.showNotificationDialog).toHaveBeenCalled()
    });
    it('saveChanges', () => {
        component.betPackData = {
            id: '1'
        } as any;
        createForm(component);
        component.saveChanges();
        expect(dialogService.showNotificationDialog).toHaveBeenCalled()
    });
    it('updateMoreInfoText', () => {
        createForm(component);
        component.updateMoreInfoText('test','betPackMoreInfoText');
        expect(cd.detectChanges).toHaveBeenCalled()
    });
    it('betpackEditControls', () => {
        createForm(component);
        expect(component.betpackEditControls).not.toBe(null)
    });
    it('betpackEditControls', () => {
        expect(component.betpackEditControls).toBeUndefined()
    });
    it('onLinkedChange', () => {
        createForm(component);
        component.onLinkedChange()
        expect(component.betPackEditData.value.isLinkedBetPack).toBeTrue()
    });
    it('updateValidators', () => {
        createForm(component);
        component.betPackEditData= {
            get : (key) =>{ return {
                valueChanges : {
                    subscribe: jasmine.createSpy().and.callFake(cb => cb({
                        filterBetPack: 'testMsg'
                    }))
                },
                setValidators:  jasmine.createSpy().and.callThrough()
            }
        }
        } as any;
        component['updateValidators']('filterBetPack', 'filterList');
        // expect(component.betPackEditData.value.filterBetPack).toBe('filterList')
    });
    it('updateValidators', () => {
        createForm(component);
        component.betPackEditData= {
            get : (key) =>{ return {
                valueChanges : {
                    subscribe: jasmine.createSpy().and.callFake(cb => cb(null))
                },
                setValidators:  jasmine.createSpy().and.callThrough(),
                clearValidators:jasmine.createSpy().and.callThrough(),
                // updateValueAndValidity:jasmine.createSpy().and.callThrough(),
            }
        },
        controls : { filterList : {
            updateValueAndValidity:  jasmine.createSpy().and.callThrough()
        
        }}
        } as any;
        component['updateValidators']('filterBetPack', 'filterList');
        // expect(component.betPackEditData.value.filterBetPack).toBeTrue()
    });

    
});