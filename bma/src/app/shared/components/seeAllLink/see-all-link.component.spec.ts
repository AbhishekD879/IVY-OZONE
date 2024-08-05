import { SeeAllLinkComponent } from './see-all-link.component';

describe('SeeAllLinkComponent', () => {
    let component: SeeAllLinkComponent;
    let gtmService;

    beforeEach(() => {

          gtmService = {
            push: jasmine.createSpy('push')
          };
          component = new SeeAllLinkComponent(
            gtmService
        );
    });

    describe('@ngOnInit', () => {
      it('call gtm service', () => {
       component.sportId = '18';
       component.targetTab = {name : 'golf_matches'}
       component.sendGTMData();
       expect(component['gtmService'].push).toHaveBeenCalled();
      });

      it('call gtm service with OR condition', () => {
        component.sportId = '18';
        component.targetTab = {name : 'sdasda'}
        component.sendGTMData();
        expect(component['gtmService'].push).toHaveBeenCalled();
       });

      it('call gtm service with 21', () => {
        component.sportId = '21';
        component.sendGTMData();
        expect(component['gtmService'].push).not.toHaveBeenCalled();
       });
    });
});