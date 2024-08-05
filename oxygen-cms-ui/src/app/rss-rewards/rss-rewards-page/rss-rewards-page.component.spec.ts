import { of, throwError } from "rxjs";
import { RssRewardsPageComponent } from "./rss-rewards-page.component";

describe('RssRewardsPageComponent', () => {
    let component: RssRewardsPageComponent, rssRewardsApiService, brandService, dialogService, globalLoaderService;
    const rssRewardsMock =  {
        brand: 'bma',
        id: '12345',
        createdAt: 'test',
        createdBy: 'test',
        createdByUserName: 'test',
        updatedAt: 'test',
        updatedBy: 'test',
        updatedByUserName: 'test',
        enabled: false,
        coins: 20,
        communicationType: 'Inbox',
        sitecoreTemplateId: 'testId',
        source: 'Sports',
        subSource: 'RSS',
        product: 'Sportsbook'
    };
    beforeEach(() => {
        dialogService = {
            showNotificationDialog: jasmine.createSpy('showNotificationDialog')
        };
        rssRewardsApiService = {
            get: jasmine.createSpy('get').and.returnValue(of({body: rssRewardsMock})),
            create: jasmine.createSpy('create').and.returnValue(of({body: rssRewardsMock})),
            update: jasmine.createSpy('update').and.returnValue(of({body: rssRewardsMock}))
        };
        brandService = {
            brand: 'bma'
        };
        globalLoaderService = {
            showLoader: jasmine.createSpy('showLoader'),
            hideLoader: jasmine.createSpy('hideLoader'),
        };
        component = new RssRewardsPageComponent(dialogService, brandService, rssRewardsApiService, globalLoaderService);
        component.actionButtons = {
            extendCollection: jasmine.createSpy('extendCollection')
        } as any;
    });
    it('ngOnInit', () => {
        component.ngOnInit();
        expect(component.rssRewards).toEqual(rssRewardsMock);
    });
    it('verifyrssRewardsData', () => {
        expect(component.verifyrssRewardsData(rssRewardsMock)).toBeTrue();
    });
    describe('actionsHandler', () =>{
        it('save', () => {
            component['save'] = jasmine.createSpy('save').and.callThrough();
            component.actionsHandler('save');
            expect(component['save']).toHaveBeenCalled();
        });
        it('revert', () => {
            component.actionsHandler('revert');
            expect(component.rssRewards).toEqual(rssRewardsMock)
        });
        it('test', () => {
            component['save'] = jasmine.createSpy('save');
            component['load'] = jasmine.createSpy('load');
            component.actionsHandler('test');
            expect(component['save']).not.toHaveBeenCalled();
            expect(component['load']).not.toHaveBeenCalled();
        });
    });
    it('canDeactivate', () => {
        component.rssRewards = rssRewardsMock;
        component.rssRewardsCopy = rssRewardsMock;
        expect(component.canDeactivate()).toBeTrue();
    });
    describe('save', () => {
        it('update', () => {
            component['sendRequest'] = jasmine.createSpy().and.callThrough();
            component.rssRewards = rssRewardsMock;
            component['save']();
            expect(component['sendRequest']).toHaveBeenCalledWith('update');
        });
        it('create', () => {
            component['sendRequest'] = jasmine.createSpy().and.callThrough();
            component.rssRewards.createdAt = null;
            component['save']();
            expect(component['sendRequest']).toHaveBeenCalledWith('create');
        });
    });
    describe('load', () => {
        it('error 404', () => {
            component['empty'] = jasmine.createSpy();
            rssRewardsApiService.get = jasmine.createSpy('get').and.returnValue(throwError({ status: 404 }));
            component['load']();
            expect(component['empty']).toHaveBeenCalled();
        });
        it('error', () => {
            rssRewardsApiService.get = jasmine.createSpy('get').and.returnValue(throwError({ status: 500 }));
            component['load']();
            expect(dialogService.showNotificationDialog).toHaveBeenCalled();
        });
    });
    describe('sendRequest', () => {
        it('success', () => {
            component.rssRewards.brand = null;
            component['sendRequest']('create');
            expect(component.actionButtons.extendCollection).toHaveBeenCalled();
            expect(dialogService.showNotificationDialog).toHaveBeenCalled();
        });
        it('error', () => {
            rssRewardsApiService.create = jasmine.createSpy('create').and.returnValue(throwError({ status: 500 }));
            component['sendRequest']('create');
            expect(component.actionButtons.extendCollection).not.toHaveBeenCalled();
            expect(dialogService.showNotificationDialog).toHaveBeenCalled();
        });
    });
});