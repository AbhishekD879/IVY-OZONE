import { of } from 'rxjs';
import { BetPackCreateComponent } from '@app/betpack-market-place/create-betpack/bet-pack-create.component';
import { FiltersTestData } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { BetpackData } from '@app/betpack-market-place/betpack-mock';
import {  FormBuilder, FormControl, FormGroup } from "@angular/forms";
import { fakeAsync, tick } from '@angular/core/testing';

describe('CreateComponent', () => {
    let component: BetPackCreateComponent;
    let dialog;
    let apiClientService, betpackService;
    let dialogService;
    let router;
    let sportsSurfaceBetsService;
    let brandService;
    let betPackValidationService;
    let form;
    let cd;

    beforeEach(() => {
        brandService = {};
        dialogService = {
            showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                yesCallback();
            }),
            showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
                closeCallback();
            })
        };
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: FiltersTestData })),
            postBetPack: jasmine.createSpy('postBetPack').and.returnValue(of({}))
        };
        apiClientService = {
            betpackService: () => betpackService
        };
        sportsSurfaceBetsService = {
            getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of({ alt: 'test', categoryId: 1, disabled: true }))
        };
        dialog = {
            open: jasmine.createSpy('open').and.returnValue({ 
                afterClosed :  jasmine.createSpy('afterClosed').and.returnValue(of('1')),
            }),
        }
        router = { navigate: jasmine.createSpy('navigate') };
        betPackValidationService = {
            checkIfInteger :  jasmine.createSpy('checkIfInteger').and.returnValue(true)
        };
        form =
        () => ({ group: object => ({}) });
        cd={
            detectChanges:jasmine.createSpy('detectChanges')
        }
        component = new BetPackCreateComponent(dialog, dialogService, apiClientService, sportsSurfaceBetsService, brandService, router, betPackValidationService,form,cd);
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
    });
    it('constructor', () => {
        expect(component).toBeDefined();
    });
    describe('editFormGorup', () => {
        it('general calls', fakeAsync(() => {
          component['form'] = new FormBuilder()
          component['betpackCreateGroup']();
          expect(component.betPackCreateData.value.betPackId).toBe(null);
        }));
      });
    it('removeTokenTable', () => {
        let event = {
            "id": null,
            "tokenId": 123,
            "tokenTitle": "test",
            "tokenValue": "20",
            "deepLinkUrl": "/"
        }
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 3,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
          });
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
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([])
          });
        component.betPackCreateData.value.betPackTokenList = [] as any;
        component.removeTokenTable(event);
        expect(component.isedited).toEqual(false);
    });
    it('with tokens and edited true', () => {
        spyOn(component as any, 'setErrors');
        let event = {
            "id": null,
            "tokenId": 3,
            "tokenTitle": "test",
            "tokenValue": "20",
            "deepLinkUrl": "/"
        }
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 3,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                },
                {
                    "id": null,
                    "tokenId": 4,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
        });
        component.removeTokenTable(event);
        expect(component['setErrors']).toHaveBeenCalled();
    });
    it('removeHandlerMulty', () => {
        let event = [3];
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 3,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
          });

        component.removeHandlerMulty(event);
        expect(component.betPackCreateData.value.betPackTokenList.length).toEqual(0);
    });
    it('removeHandlerMulty when no length', () => {
        let event = [2];
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 3,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                },
                {
                    "id": null,
                    "tokenId": 4,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
        });
        component.isedited = true;
        component.removeHandlerMulty(event);
        expect(component.isedited).toBeTruthy();
    });
    it('setFilters', () => {
        let event = { source: "", value: ['1', '2'] } as any;
        component.betPackCreateData = new FormGroup({
            filterList: new FormControl(),
          });
        component.setFilters(event);
        expect(component.betPackCreateData.value.filterList).toEqual(['1', '2']);
    });
    it('finishBetPackCreation', () => {
        component.isedited = false;
        component.betPackCreateData = new FormGroup({
            id: new FormControl(),
          });
        component.finishBetPackCreation();
        expect(dialogService.showNotificationDialog).toHaveBeenCalled()
    });
    it('isEndDateValid', () => {
        component.betPackCreateData = new FormGroup({
            betPackStartDate: new FormControl('2022-10-26T04:44:21Z'),
            betPackEndDate: new FormControl('2022-11-01T08:45:21Z')
        })
        component.isEndDateValid();
        expect(component.isEndDateValid).toBeTruthy()
    });
    it('handleDisplayDateUpdate', () => {
        spyOn(component as any, 'setErrors');
        const data = {
            startDate: '11-1-2022',
            endDate: '11-21-2022'
        } as any;
        component.betPackCreateData = new FormGroup({ betPackStartDate: new FormBuilder().group({ betPackStartDate: new FormControl('') }) });
        component.handleDisplayDateUpdate(data);
        expect(component['setErrors']).toHaveBeenCalled();
    });
    it('onFilterChange when true', () => {
        component.betPackCreateData = new FormGroup({
            filterBetPack: new FormControl(true),
            filterList: new FormControl({reset: () => true}),
          });
        component.onFilterChange();
        expect(component.betPackCreateData.value.filterList).toEqual([])
    });
    it('onFilterChange when false', () => {
        component.betPackCreateData = new FormGroup({
            filterBetPack: new FormControl(false),
          });
        component.onFilterChange();
        expect(component.betPackCreateData.value.filterList).not.toEqual([])
    });
    it('isTokenEndDateValid', () => {
        spyOn(component as any, 'setErrors');
        component.betPackCreateData = new FormGroup({
            betPackStartDate: new FormControl('11-1-2022'),
            betPackEndDate: new FormControl('11-21-2022'),
          });
        component.isTokenEndDateValid();
        expect(component.isEndDateValid).toBeTruthy()
    });
    it('handleDisplayTokenDateUpdate', () => {
        let date = '11-1-2022';
        component.betPackCreateData = new FormGroup({
            maxTokenExpirationDate: new FormControl()
        });
        component.handleDisplayTokenDateUpdate(date);
        expect(component.betPackCreateData.value.maxTokenExpirationDate).toEqual(new Date(component.betPackCreateData.value.maxTokenExpirationDate).toISOString())
    });
    it('ngOnInit when filterActive true with res', () => {
        component.betPackData = BetpackData;
        spyOn(component as any, 'betpackCreateGroup');
        spyOn(component as any, 'updateValidators');
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 3,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
            filterList: new FormControl([{
                filterName: '',
                filterActive: false,
            }]),
        });
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
        spyOn(component as any, 'betpackCreateGroup');
        spyOn(component as any, 'updateValidators');
        let filterData = [{
            filterName: '',
            filterActive: false,
        }];
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 3,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
            filterList: new FormControl([{
                filterName: '',
                filterActive: false,
            }]),
        });
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: filterData }))
        };
        component.ngOnInit();
        expect(component.sportCategories).toEqual({ alt: 'test', categoryId: 1, disabled: true } as any);
    });
    it('ngOnInit when no res', () => {
        spyOn(component as any, 'betpackCreateGroup');
        spyOn(component as any, 'updateValidators');
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 3,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
            filterList: new FormControl([{
                filterName: '',
                filterActive: false,
            }]),
        });
        betpackService = {
            getFilters: jasmine.createSpy('getFilters').and.returnValue(of({ body: undefined }))
        };
        component.ngOnInit();
        expect(component.sportCategories).toEqual({ alt: 'test', categoryId: 1, disabled: true } as any);
    });
    it('saveBetPackChanges', () => {
        spyOn(component as any, 'finishBetPackCreation');
        let betpackData = {
            id: '1',
            filterActive: false,
        };
        component.betPackCreateData = new FormGroup({
            id: new FormControl(1),
          });
        betpackService = {
            postBetPack: jasmine.createSpy('postBetPack').and.returnValue(of({ body:betpackData}))
        };
        component.saveBetPackChanges();
        expect(component.hideAction).toBeTruthy();
    });
    it('createToken when token', () => {
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 1,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
          });
        component.createToken();
        expect(component.isedited).toBeTruthy();
    });
    it('createToken when no token', () => {
        dialog.open =  jasmine.createSpy('dialog.open').and.returnValue({
            afterClosed: jasmine.createSpy('afterClosed').and.returnValue(of(null))
        })
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 3,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
          });
        component.createToken();
        expect(component.isedited).toBeTruthy();
    });
    it('editPageRoute when token', () => {
        let event = {
            tokenId : 1
        }
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 1,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
          });
        component.editPageRoute(event);
        expect(component.isedited).toBeTruthy();
    });
    it('editPageRoute when diff token', () => {
        let event = {
            tokenId : 3
        }
        component.betPackCreateData = new FormGroup({
            betPackTokenList: new FormControl([
                {
                    "id": null,
                    "tokenId": 1,
                    "tokenTitle": "£2 Football Bet Tokens",
                    "tokenValue": "12",
                    "deepLinkUrl": "/"
                }]),
          });
        component.editPageRoute(event);
        expect(component.isedited).toBeTruthy();
    });
    
    it('isValid test in case of no filters added', () => {
        component.isedited = true;
        component.betPackData = {
            betPackId: '1',
            betPackPurchaseAmount: 2,
            betPackEndDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
            betPackFreeBetsAmount: 1,
            betPackStartDate: new Date().toISOString(),
            triggerID: 'a',
            betPackFrontDisplayDescription: 'qwertyui',
            betPackTitle: 'qwertyui',
            betPackTokenList: ['1'],
            sportsTag: ['1', '2'],
            filterBetPack: false,
            filterList: [],
            betPackMoreInfoText: 'qwerty',
            maxClaims:1,
            maxTokenExpirationDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
            linkedBetPackWarningText:'test',
            isLinkedBetPack:true
        } as any;
        // let retVal = component.isValid();
        // expect(retVal).toBeFalsy();
    });

    it('isValid test in case of filters added', () => {
        component.isedited = true;
        component.betPackData = {
            betPackId: '1',
            betPackPurchaseAmount: 2,
            betPackEndDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
            betPackFreeBetsAmount: 1,
            betPackStartDate: new Date().toISOString(),
            triggerID: 'a',
            betPackFrontDisplayDescription: 'qwertyui',
            betPackTitle: 'qwertyui',
            betPackTokenList: ['1'],
            sportsTag: ['1', '2'],
            filterBetPack: true,
            filterList: ['1'],
            betPackMoreInfoText: 'qwerty',
            maxClaims:1,
            maxTokenExpirationDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
            linkedBetPackWarningText:'',
            isLinkedBetPack:false
        } as any;
        // let retVal = component.isValid();
        // expect(retVal).toBeFalsy();
    });
    describe('updateValidators', () => {
        it('updateValidators', fakeAsync(() => {
            const key = 'filterBetPack';
            const dependentKey = 'filterList';
            component.betPackCreateData = new FormGroup({
                filterBetPack: new FormControl(true),
                filterList: new FormControl([1,2])
            });
            component.betPackCreateData = {
                get : (key) =>{ return {
                    valueChanges : {
                        subscribe: jasmine.createSpy().and.callFake(cb => cb({
                            test: 'testMsg'
                        }))
                    },
                    setValidators:  jasmine.createSpy().and.callThrough()
                }
            }
            } as any;
            component['updateValidators'](key,dependentKey);
            tick();


        }))

        it('updateValidators', fakeAsync(() => {
            const key = 'filterBetPack';
            const dependentKey = 'filterList';
            component.betPackCreateData = new FormGroup({
                filterBetPack: new FormControl(true),
                filterList: new FormControl([1,2])
            });
            component.betPackCreateData = {
                get : (key) =>{ return {
                    valueChanges : {
                        subscribe: jasmine.createSpy().and.callFake(cb => cb(null))
                    },
                    setValidators:  jasmine.createSpy().and.callThrough(),
                    clearValidators:  jasmine.createSpy().and.callThrough()
                }
            },
            controls : { filterList : {
                updateValueAndValidity:  jasmine.createSpy().and.callThrough()
            
            }}
            } as any;
            component['updateValidators'](key,dependentKey);
            tick();


        }))
    })
    describe('setInfoText', () => {
        it('setInfoText', () => {
            const event = 'Hello';
            component.betPackCreateData = new FormGroup({
                betPackMoreInfoText: new FormControl(),
            });
            component.setInfoText(event);
            expect(component['cd'].detectChanges).toHaveBeenCalled()
        })
    })
    describe('bpIsValid', () => {
        it('bpIsValid', () => {
            component.betPackCreateData = {
                valid : true
            } as any;
            const retVal = component.bpIsValid();
            expect(retVal).toBeTruthy();
        })
        it('bpIsValid', () => {
            const retVal = component.bpIsValid();
            expect(retVal).toBeUndefined();
        })
    })
    describe('betpackDataControls', () => {
        it('betpackDataControls', () => {
            component.betPackCreateData = {
                controls : true
            } as any;
            expect(component.betpackDataControls).toBeTruthy();
        })
        it('betpackDataControls', () => {
            expect(component.betpackDataControls).toBeUndefined();
        })
    })
});