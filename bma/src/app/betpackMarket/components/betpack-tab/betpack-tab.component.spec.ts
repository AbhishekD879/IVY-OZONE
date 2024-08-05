import { of } from "rxjs";
import { BetPackTabComponent } from '@app/betpackMarket/components/betpack-tab/betpack-tab.component';

describe('BetPackTabComponent', () => {
    let component: BetPackTabComponent;
    let betpackCmsService;
    let currencyPipe;
    let userService;
    let changeDetectorRef;
    let gtmService;

    beforeEach(() => {
        betpackCmsService = {
            getBetPackFilters: jasmine.createSpy('getBetPackFilters').and.returnValue(of({}))
        };
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
        };
        currencyPipe = {
            transform: jasmine.createSpy('transform')
        };
        userService = {
            currencySymbol: '$'
        }; gtmService = {
            push: jasmine.createSpy('push')
          };

        component = new BetPackTabComponent(betpackCmsService, currencyPipe, userService, changeDetectorRef,gtmService);
        component.tabs = [
            { filterName: 'Today',filterActive:false,isLinkedFilter:true,linkedFilterWarningText:'test' },
            { filterName: 'Accas',filterActive:false ,isLinkedFilter:true,linkedFilterWarningText:'test' },
            { filterName: 'tomorrow',filterActive:false ,isLinkedFilter:false,linkedFilterWarningText:'test' },
            { filterName: 'All',filterActive:false ,isLinkedFilter:false,linkedFilterWarningText:'test' },
            { filterName: '5',filterActive:false ,isLinkedFilter:false,linkedFilterWarningText:'test' }
        ]
    });

    it('should Init component', () => {
        (betpackCmsService.getBetPackFilters as jasmine.Spy).and.returnValue(of([{sortOrder: -90},{sortOrder: -80}]));
        spyOn(component, 'tabsProcess');
        component.ngOnInit();
        expect(component.tabsProcess).toHaveBeenCalled();
    });

    it('should Init component with different sort order', () => {
        (betpackCmsService.getBetPackFilters as jasmine.Spy).and.returnValue(of([{sortOrder: 90},{sortOrder: 80}]));
        spyOn(component, 'tabsProcess');
        component.ngOnInit();
        expect(component.tabsProcess).toHaveBeenCalled();
    });

    it('should Init component with equal sort order', () => {
        (betpackCmsService.getBetPackFilters as jasmine.Spy).and.returnValue(of([{sortOrder: 90},{sortOrder: 90}]));
        spyOn(component, 'tabsProcess');
        component.ngOnInit();
        expect(component.tabsProcess).toHaveBeenCalled();
    });

    it('should onchange when change happens', () => {
        spyOn(component, 'tabsProcess');
        component.ngOnChanges();
        expect(component.tabsProcess).toHaveBeenCalled();
    });

    it('Tab process', () => {
        component.cmsFilterVal = ['Today', 'Accas', '5', 'tomorrow'];
        component.filterValues = ['Today', 'Accas'];
        component.tabsProcess();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('Tab process with active filter', () => {
        component.cmsFilterVal = ['Today', 'Accas', '5', 'tomorrow'];
        component.filterValues = ['Today', 'Accas'];
        component.allFilterMsg='test'
        component.tabsProcess();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('onTabSelect', () => {
        const event = { filterName: 'Today',filterActive:false,isLinkedFilter:true,linkedFilterWarningText:'test'  };
        spyOn(component.tabChange, 'emit');
        component.onTabSelect(event);
        expect(component.tabChange.emit).toHaveBeenCalled();
    });
});