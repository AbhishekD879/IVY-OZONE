import { of } from "rxjs";
import { StatisticalContentInformationComponent } from "./statistical-content-information.component";

describe('StatisticalContentInformationComponent', () => {
  let component: StatisticalContentInformationComponent;
  let cmsService;
  let domSanitizer;
  beforeEach(() => {
    cmsService = {
      getStatisticalContent: jasmine.createSpy('getStatisticalContent').and.returnValue(of([
        {
          content: 'Testing Content',
          title: 'mockTitle',
          marketType: 'OB',
          eventId: '1234',
          marketId: '3456',
          enabled: true,
          marketDescription: 'Odds Booster'
        }
      ]))
    };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue('<p>Statistical Content</p>')
  };  
    component = new StatisticalContentInformationComponent(cmsService, domSanitizer);
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('#ngOnInit', () => {
    it('should call processFlags', () => {
      component['processFlags'] = jasmine.createSpy('processFlags');
      component.ngOnInit();
      expect(component['processFlags']).toHaveBeenCalled();
    });
  });
  describe('#parseFlags', () => {
    it('should call parseFlags', () => {
      const result = component.parseFlags('');
      expect(result.length).toEqual(0);
    });
  });
  describe('processFlags', () => {
    it('should update statistical content if flag is MKTFLAG_PB', () => {
      component.eventEntity = { categoryId: '16' };
      component.market = { name: 'Match Result', drilldownTagNames: 'MKTFLAG_PB,', id: '3456', eventId: '1234' }
      component.brand = 'bma';
      component.display = "MKTFLAG_PB";
      component['processFlags']();
      component['parseFlags'](component.display);
      expect(component.flagType).toEqual('OB');
    });

    it('should update statistical content if flag is MKTFLAG_PR1', () => {
      component.eventEntity = { categoryId: '16' };
      component.market = { name: 'Match Result', drilldownTagNames: 'MKTFLAG_PR1,', id: '3456', eventId: '1234' }
      component.brand = 'bma';
      component.display = "MKTFLAG_PR1";
      component['processFlags']();
      component['parseFlags'](component.display);
      expect(component.flagType).toEqual('BMOB');
    });
  });
});