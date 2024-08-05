import { of } from 'rxjs';

import { AzSportsPageComponent } from '@lazy-modules-module/aToZMenu/components/AzSportsPageComponent/az-sports-page.component';

describe('AzSportsPageComponent -', () => {
  let moduleExtensionsStorageService,
    cmsService,
    casinoLinkService,
    component,
    menuItems,filtersService,
    bonusSuppressionService;

  const genericSvg = 'icon-generic';
  const menuItemsMock = [
    {
      id: '000',
      svgId: '000',
      disabled: true,
      hasEvents: true,
      showInAZ: false,
      isTopSport: false,
      targetUri:'gajgdg'
    },
    {
      id: '111',
      svgId: '111',
      disabled: false,
      hasEvents: true,
      showInAZ: true,
      isTopSport: true,
      targetUri:'gajgdg'
    },
    {
      id: '222',
      svgId: '222',
      disabled: false,
      hasEvents: true,
      showInAZ: false,
      isTopSport: true,
      targetUri:'gajgdg'
    },
    {
      id: '333',
      svgId: '333',
      imageTitle: '333',
      disabled: false,
      hasEvents: true,
      showInAZ: true,
      isTopSport: true,
      targetUri:'gajgdg'
    },
    {
      id: '444',
      imageTitle: '444',
      disabled: false,
      hasEvents: true,
      showInAZ: true,
      isTopSport: false,
      targetUri:'rss'
    },
    {
      id: '555',
      imageTitle: '555',
      disabled: false,
      hasEvents: true,
      showInAZ: true,
      isTopSport: false,
      targetUri:'gajgdg'
    },
    {
      id: '666',
      disabled: false,
      hasEvents: false,
      showInAZ: true,
      isTopSport: true,
      targetUri:'gajgdg'
    },
    {
      id: '777',
      disabled: false,
      hasEvents: true,
      showInAZ: true,
      isTopSport: false,
      categoryId: 160,
      targetUri:'racingsuperseries'
    },
  ];
  const AZData = {
    topItems: [
      Object.assign({}, menuItemsMock[1], {title: undefined}),
      Object.assign({}, menuItemsMock[2], {title: undefined}),
      Object.assign({}, menuItemsMock[3], {title: '333'})
    ],
    azItems: [
      Object.assign({}, menuItemsMock[3], {title: '333'}),
      Object.assign({}, menuItemsMock[4], {svgId: genericSvg, title: '444',targetUri:'rss'}),
      Object.assign({}, menuItemsMock[5], {svgId: genericSvg, title: '555'}),
      Object.assign({}, menuItemsMock[1], {title: undefined}),
      Object.assign({}, {
        categoryId: 160,
        disabled: false,
        fzDisabled: false,
        hasEvents: true,
        id: "777",
        isTopSport: false,
        showInAZ: true,
        svgId: "icon-generic",
        title: undefined,
        targetUri:'promotion/details/exclusion'
      }),
    ]
  };

  beforeEach(() => {
    menuItems = menuItemsMock.slice();
    filtersService = {
      filterLinkforRSS: jasmine.createSpy('filterLinkforRSS').and.returnValue((of('promotion/details/exclusion'))),
    };
    moduleExtensionsStorageService = {
      getList: jasmine.createSpy('getMenuItems').and.returnValue([])
    };
    cmsService = {
      getMenuItems: jasmine.createSpy('getMenuItems').and.returnValue(of(menuItems))
    };
    casinoLinkService = {
      decorateCasinoLink: jasmine.createSpy('decorateCasinoLink').and.returnValue(of(menuItems))
    };
    bonusSuppressionService = {
      checkIfYellowFlagDisabled : jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    }

    component = new AzSportsPageComponent(moduleExtensionsStorageService, cmsService, casinoLinkService, filtersService, bonusSuppressionService);
  });

  it('should be created', () => {
    expect(component).toBeDefined();
  });

  describe('within onInit hook should get menu items', () => {

    beforeEach(() => {
      spyOn(component, 'processMenu').and.returnValue(AZData);
      component.ngOnInit();
    });

    it('showRetailMenu', () => {
      expect(component.showRetailMenu).toBeTruthy();
    });

    it('calling cmsService', () => {
      expect(cmsService.getMenuItems).toHaveBeenCalledWith();
    });

    it('assigning data to component', (done: DoneFn) => {
      cmsService.getMenuItems().subscribe( () => {
        expect(component.azItems).toBeTruthy();
        expect(component.topItems).toBeTruthy();

        done();
      });
    });
  });

  describe('when processing menu items it should', () => {
    let result;
    
    beforeEach(() => {
      result = component.processMenu(menuItems as any);
    });

    it('get extension list', () => {
      expect(moduleExtensionsStorageService.getList).toHaveBeenCalled();
    });

    it('decorate casino menu item', () => {

      expect(casinoLinkService.decorateCasinoLink).toHaveBeenCalledWith(menuItems);
    });

    describe('return expected result', () => {

      it('(with azItems items)', () => {
        expect(result.azItems.length).toBeGreaterThan(0);
      });

      it('(excluding disabled items)', () => {
        expect(result.topItems.filter(item => item.disabled).length).toBe(0);
        expect(result.azItems.filter(item => item.disabled).length).toBe(0);
      });

      it('(excluding items without events)', () => {
        expect(result.topItems.filter(item => !item.hasEvents).length).toBe(0);
        expect(result.azItems.filter(item => !item.hasEvents).length).toBe(0);
      });

      it('(topItems should include only top sports)', () => {
        expect(result.topItems.filter(item => !item.isTopSport).length).toBe(0);
      });

      it('(azItems should include only configured items)', () => {
        expect(result.azItems.filter(item => !item.showInAZ).length).toBe(0);
      });

      it('(items without svg should receive generic one)', () => {
        const item4 = result.azItems.filter(item => item.id === '444');

        expect(item4).toBeTruthy();
        expect(item4[0].svgId).toBe(genericSvg);
      });

      it('(basic)', () => {
        expect(result).toEqual(AZData);
      });
    });
  });
});
