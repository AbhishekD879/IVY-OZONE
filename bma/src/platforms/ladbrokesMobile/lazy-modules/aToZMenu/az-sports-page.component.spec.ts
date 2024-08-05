import { category } from '@ladbrokesDesktop/desktop/components/leftMenu/category.mock';
import { of } from 'rxjs';
import { AzSportsPageLadbrokesMobileComponent } from './az-sports-page.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { FANZONE_CONFIG } from '@app/sb/components/sportMatchesTab/mockdata/sport-matches-tab.component.mock';

describe('AzSportsPageLadbrokesMobileComponent -', () => {
    let moduleExtensionsStorageService;
    let cmsService;
    let casinoLinkService;
    let germanSupportService;
    let pubSubService;
    let storageService;
    let component;
    let menuItems;
    let user;
    let bonusSuppressionService;
    let filtersService;

    const menuItemsMock = [
        {
            id: '000',
            svgId: '000',
            disabled: true,
            hasEvents: true,
            showInAZ: false,
            isTopSport: false
        },
        {
            id: '111',
            svgId: '111',
            disabled: false,
            hasEvents: true,
            showInAZ: true,
            isTopSport: true
        },
        {
            id: '222',
            svgId: '222',
            disabled: false,
            hasEvents: true,
            showInAZ: false,
            isTopSport: true
        },
        {
            id: '333',
            svgId: '333',
            imageTitle: '333',
            disabled: false,
            hasEvents: true,
            showInAZ: true,
            isTopSport: true
        },
        {
            id: '777',
            svgId: '777',
            imageTitle: '777',
            disabled: false,
            hasEvents: true,
            showInAZ: true,
            isTopSport: true,
            title: 'Fanzone',
            categoryId: 160,
            selectedFanzone: FANZONE_CONFIG
        },
        {
            id: '444',
            imageTitle: '444',
            disabled: false,
            hasEvents: true,
            showInAZ: true,
            isTopSport: false
        },
        {
            id: '555',
            imageTitle: '555',
            disabled: false,
            hasEvents: true,
            showInAZ: true,
            isTopSport: false
        },
        {
            id: '666',
            disabled: false,
            hasEvents: false,
            showInAZ: true,
            isTopSport: true
        }
    ];
    const menuItemsMock2 = [
        {
            id: '000',
            svgId: '000',
            disabled: true,
            hasEvents: true,
            showInAZ: false,
            isTopSport: false
        },
        {
            id: '111',
            svgId: '111',
            disabled: false,
            hasEvents: true,
            showInAZ: true,
            isTopSport: true
        },
        {
            id: '222',
            svgId: '222',
            disabled: false,
            hasEvents: true,
            showInAZ: false,
            isTopSport: true
        },
        {
            id: '666',
            disabled: false,
            hasEvents: false,
            showInAZ: true,
            isTopSport: true
        }
    ];


    beforeEach(() => {
        menuItems = menuItemsMock.slice();
        moduleExtensionsStorageService = {
            getList: jasmine.createSpy('getMenuItems').and.returnValue([])
        };
        cmsService = {
            getMenuItems: jasmine.createSpy('getMenuItems').and.returnValue(of(menuItems)),
            getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
        };
        germanSupportService = {
            toggleItemsList: jasmine.createSpy('toggleItemsList').and.returnValue([category])
        };
        casinoLinkService = {
            decorateCasinoLink: jasmine.createSpy('decorateCasinoLink')
        };
        storageService = {
            get: jasmine.createSpy()
        }
        pubSubService = {
            subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb({},{})),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: pubSubApi
        };
        bonusSuppressionService = {
            checkIfYellowFlagDisabled : jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
        };
        user = {
            checkIfYellowFlagDisabled : jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true),
            status : true
        }

        component = new AzSportsPageLadbrokesMobileComponent(moduleExtensionsStorageService, cmsService, casinoLinkService, germanSupportService, pubSubService, storageService, user, filtersService, bonusSuppressionService);
    });

    it('should be created', () => {
        expect(component).toBeDefined();
    });

    it('should set topItems and azItems value', () => {
        component.ngOnInit();

        expect(component.showRetailMenu).toBeTrue();
        expect(component.topItems).toBeUndefined();
        expect(component.azItems).toBeUndefined();
    })

    it('should set topItems and azItems value as null', () => {
        cmsService.getMenuItems = jasmine.createSpy('getMenuItems').and.returnValue(of([]))
        component.ngOnInit();

        expect(component.showRetailMenu).toBeTrue();
        expect(component.topItems).toBeFalsy();
        expect(component.azItems).toBeFalsy();
    })

    it('should set topItems and azItems value as disabled false', () => {
        storageService.get = jasmine.createSpy().and.returnValue({ teamId: 'abc' });
        component.ngOnInit();

        expect(component.showRetailMenu).toBeTrue();
        expect(component.topItems).toBeUndefined();
        expect(component.azItems).toBeUndefined();
    })

    it('should set topItems and azItems value as disabled false when no selected fanzone data', () => {
        cmsService.getMenuItems = jasmine.createSpy('getMenuItems').and.returnValue(of(menuItemsMock2))
        storageService.get = jasmine.createSpy().and.returnValue({ teamId: 'abc' });
        component.ngOnInit();

        expect(component.showRetailMenu).toBeTrue();
        expect(component.topItems).toBeUndefined();
        expect(component.azItems).toBeUndefined();
    })

    it('ngOnDestroy', () => {
        component.ngOnDestroy();
        expect(pubSubService.unsubscribe).toHaveBeenCalledWith('LadbrokesAzSportsPageComponent');
    });
});
