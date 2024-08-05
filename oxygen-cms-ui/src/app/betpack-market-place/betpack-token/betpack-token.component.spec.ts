import { fakeAsync, tick } from '@angular/core/testing';
import { BetPackTokenComponent } from '@app/betpack-market-place/betpack-token/betpack-token.component';
import { FormControl, FormGroup } from '@angular/forms';
import { IToken } from '@app/betpack-market-place/model/bet-pack-banner.model';

describe('BetPackTokenComponent', () => {
    let component: BetPackTokenComponent;
    let dialogRef;
    let data
    describe('betpackToken', () => {
        beforeEach(() => {
            data = {
                event: [{
                    "id": null,
                    "tokenId": 123,
                    "tokenTitle": "test",
                    "tokenValue": "20",
                    "deepLinkUrl": "/"
                }],
                tokenArr: ['123', '134', '345'],
                createEdit: false
            }
            dialogRef = {
                close: jasmine.createSpy('close')
            };

            component = new BetPackTokenComponent(data, dialogRef);

        });
        afterAll(() => {
            component = null
        })
        it('constructor', () => {
            expect(component).toBeDefined();
        });
        describe('ngOninit', () => {
            it('ngOninit if', fakeAsync(() => {
                data.createEdit = true;
                component.form = new FormGroup({});
                component.form.addControl('tokenId', new FormControl('test'));
                component.form.addControl('tokenTitle', new FormControl('test'));
                component.form.addControl('tokenValue', new FormControl('test'));
                component.form.addControl('deepLinkUrl', new FormControl('test'));
                tick();
                component.ngOnInit();
                expect(component.form.get('tokenId')).toBeTruthy();
                expect(component.form.get('tokenTitle')).toBeTruthy();
                expect(component.form.get('tokenValue')).toBeTruthy();
                expect(component.form.get('deepLinkUrl')).toBeTruthy();
            }));
            it('ngOninit else', fakeAsync(() => {
                component.form = new FormGroup({});
                component.form.addControl('tokenId', new FormControl('test'));
                component.form.addControl('tokenTitle', new FormControl('test'));
                component.form.addControl('tokenValue', new FormControl('test'));
                component.form.addControl('deepLinkUrl', new FormControl('test'));
                tick();
                component.ngOnInit();
                expect(component.form.get('tokenId')).toBeTruthy();
                expect(component.form.get('tokenTitle')).toBeTruthy();
                expect(component.form.get('tokenValue')).toBeTruthy();
                expect(component.form.get('deepLinkUrl')).toBeTruthy();
            }));
        })
        describe('tokenDuplicateCheck',()=>{
            it('tokenDuplicateCheck include token id', () => {
                let tokenID = '123'
                component.isTokenDuplicated = false;
                component.tokenDuplicateCheck(tokenID);
                expect(component.isTokenDuplicated).toEqual(true);
            });
            it('tokenDuplicateCheck exclude token id', () => {
                let tokenID = '1234'
                component.tokenDuplicateCheck(tokenID);
                expect(component.isTokenDuplicated).toEqual(false);
            });
        })        
        describe('getTemplate', () => {
            it('getTemplate called', fakeAsync(() => {
                component.token = {} as IToken;
                component.form = new FormGroup({});
                component.form.addControl('tokenId', new FormControl('123456'));
                component.form.addControl('tokenTitle', new FormControl(123));
                component.form.addControl('tokenValue', new FormControl('20'));
                component.form.addControl('deepLinkUrl', new FormControl('/'));
                tick();
                expect(component.getTemplate()).toEqual(component.token);
            }));
        })
        describe('close dialog', () => {
            it('close dialog if condition', fakeAsync(() => {
                data.createEdit = true;
                component.closeDialog()
                expect(dialogRef.close).toHaveBeenCalled();
            }));
            it('close dialog else condition', fakeAsync(() => {
                component.closeDialog()
                expect(dialogRef.close).toHaveBeenCalled();
            }));
        });
        describe('getControlValue', () => {
            it('getControlValue', fakeAsync(() => {
                component.form = new FormGroup({});
                component.form.addControl('tokenId', new FormControl('test'));
                component.form.addControl('tokenTitle', new FormControl('test'));
                component.form.addControl('tokenValue', new FormControl('test'));
                component.form.addControl('deepLinkUrl', new FormControl('test'));
                expect( component.getControlValue('tokenValue')).toEqual(4);
            }));
            it('getControlValue with no form', fakeAsync(() => {
                component.form = undefined
                expect( component.getControlValue('tokenValue')).toEqual(undefined);
            }));
        })
        describe('isDisable', () => {
            it('isDisable createEdit false', fakeAsync(() => {
                component.form = new FormGroup({});
                component.form.addControl('tokenId', new FormControl('test'));
                component.form.addControl('tokenTitle', new FormControl('test'));
                component.form.addControl('tokenValue', new FormControl('test'));
                component.form.addControl('deepLinkUrl', new FormControl('test'));
                expect( component.isDisable()).toBeFalsy();
            }));
            it('isDisable  createEdit true' , fakeAsync(() => {
                data.event={
                    id: null,
                    tokenId: 123,
                    tokenTitle: "test",
                    tokenValue: "20",
                    deepLinkUrl: "/"
                } as IToken
                
                data.createEdit=true
                component.isTokenDuplicated=true
                component.form = new FormGroup({});
                component.form.addControl('tokenId', new FormControl(123));
                component.form.addControl('tokenTitle', new FormControl('test'));
                component.form.addControl('tokenValue', new FormControl('20'));
                component.form.addControl('deepLinkUrl', new FormControl('/'));
                expect( component.isDisable()).toBeTruthy();
            }));
            it('isDisable  createEdit true isTokenDuplicated false'  , fakeAsync(() => {
                data.event={
                    id: null,
                    tokenId: 123,
                    tokenTitle: "test",
                    tokenValue: "20",
                    deepLinkUrl: "/"
                } as IToken
                
                data.createEdit=true
                component.isTokenDuplicated=false
                component.form = new FormGroup({});
                component.form.addControl('tokenId', new FormControl('test'));
                component.form.addControl('tokenTitle', new FormControl('test1'));
                component.form.addControl('tokenValue', new FormControl('test'));
                component.form.addControl('deepLinkUrl', new FormControl('test'));
                expect( component.isDisable()).toBeFalsy();
            }));
        })
    })
});