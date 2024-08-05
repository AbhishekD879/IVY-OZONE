import { of, throwError } from 'rxjs';
import { BetPackListComponent } from '@app/betpack-market-place/list-betpack/bet-pack-list.component';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';
import { BetPackModel ,IToken} from '@app/betpack-market-place/model/bet-pack-banner.model';
import { Base } from 'app/client/private/models/base.model';

describe('bet-pack-list', () => {
    let component: BetPackListComponent;
    let snackBar;
    let apiClientService, betpackService;
    let dialogService;
    let router;
    let globalLoaderService;
    let betpackToken:IToken
    let betpacks:BetPackModel[]
    let base:Base
    beforeEach(() => {
        betpackToken={tokenId: 1,
            tokenTitle: 'test',
            deepLinkUrl: 'test',
            tokenValue: 'test',
            id: 'test'}
           base={
                id: 'test',
                brand: 'test',
                createdBy: 'test',
                createdAt: 'test',
                updatedBy: 'test',
                updatedAt: 'test',
                updatedByUserName: 'test',
                createdByUserName: 'test'
            }
        betpacks=[{
            ...base,
            betPackId: 'test',
            betPackTitle: 'test',
            betPackPurchaseAmount: 1,
            betPackFreeBetsAmount: 1,
            betPackFrontDisplayDescription: 'test',
            sportsTag: ['test'],
            betPackStartDate: 'test',
            betPackEndDate: 'test',
            maxTokenExpirationDate: 'test',
            futureBetPack: false,
            filterBetPack: false,
            betPackSpecialCheckbox: false,
            betPackMoreInfoText: 'test',
            filterList: ['test'],
            betPackActive: true,
            triggerID: 'test',
            betPackTokenList: [betpackToken],
            sortOrder: 1,
            maxClaims:1}];

        dialogService = {
            showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message }) => { }),
            showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
                yesCallback();
            })
        };
        betpackService = {
            getBetPackData: jasmine.createSpy('getBetPackData').and.returnValue(of({ body: undefined })),
            deleteBetPack: jasmine.createSpy('deleteBetPack').and.returnValue(of({})),
            reorderBetPack: jasmine.createSpy('reorderBetPack').and.returnValue(of({}))
        };
        apiClientService = {
            betpackService: () => betpackService
        };
        router = { navigateByUrl: jasmine.createSpy('navigateByUrl') };
        snackBar = {
            open: jasmine.createSpy('open')
        };
        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader')
        };

        component = new BetPackListComponent(router, dialogService, apiClientService, snackBar, globalLoaderService);
    });

    it('constructor', () => {
        expect(component).toBeDefined();
    });
    it('ngOnInit', () => {
        spyOn(component, 'loadBetPacks');
        component.ngOnInit();
        expect(component.loadBetPacks).toHaveBeenCalled();
    });

    it('removeBetPack', () => {
        spyOn(component, 'sendRemoveRequest');
        component.removeBetPack(undefined);
        expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
            title: 'Remove BetPack',
            message: 'Are You Sure You Want to Remove BetPack?',
            yesCallback: jasmine.any(Function)
        });
    });
    it('reorderHandler', () => {
        component.reorderHandler({ order: [], id: '' });
        expect(snackBar.open).toHaveBeenCalled();
    });
    it('openCreateBetPack', () => {
        component.openCreateBetPack();
        expect(router.navigateByUrl).toHaveBeenCalled();
    });
    it('sendRemoveRequest', () => {
        const bet = { id: '1' } as any;
        spyOn(component, 'loadBetPacks');
        component.sendRemoveRequest(bet);
        expect(component.loadBetPacks).toHaveBeenCalled();
        expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
            title: 'Remove Completed',
            message: 'BetPack is Removed.'
        });
    });
    describe('betPackAmount',()=>{
        it('betPackAmount', () => {
            component.betPackData=betpacks;
            const data:ActiveInactiveExpired={active:1,inactive:0
            } 
            expect(component.betPackAmount).toEqual(data);
        });
    });
    describe('loadFilters',()=>{
    it('loadFilters if condition', () => {
        betpackService = {
        getBetPackData: jasmine.createSpy('getBetPackData').and.returnValue(of({ body: betpacks })),
        };
        component.loadBetPacks();
        expect(component.betPackData).toEqual(betpacks);
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();


    });
    it('loadFilters error ', () => {
        betpackService = {
        getBetPackData: jasmine.createSpy('getBetPackData').and.returnValue(throwError({ error: 401 })),
        };
        component.loadBetPacks();
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
    it('loadFilters No Active betpacks', () => {
        let responce=betpacks
        responce[0].betPackActive=false
        betpackService = {
         getBetPackData: jasmine.createSpy('getBetPackData').and.returnValue(of({ body: responce })),
        };
        component.loadBetPacks();
        expect(component.betPackData).toEqual(betpacks);
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();


    });
    it('loadFilters grater than twenty betpacks', () => {
        let responce=[]
        for(let i=0; i<20; i++){
            responce.push(betpacks[0])
        }
        console.log(responce.length)
        betpackService = {
         getBetPackData: jasmine.createSpy('getBetPackData').and.returnValue(of({ body: responce })),
        };
        component.loadBetPacks();
        expect(globalLoaderService.showLoader).toHaveBeenCalled();
        expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
    })
});
