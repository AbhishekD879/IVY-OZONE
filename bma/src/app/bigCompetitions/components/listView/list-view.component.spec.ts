import { ListViewComponent } from '@app/bigCompetitions/components/listView/list-view.component';
import { ISportEvent } from '@core/models/sport-event.model';

describe('ListViewComponent', () => {

  let component: ListViewComponent;

  beforeEach(() => {
    component = new ListViewComponent();
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component['getPrimaryMarketName'] = jasmine.createSpy().and.returnValue('market');
    component.maxDisplay = 5;
    component.events = [];
    component.ngOnInit();
    expect(component.limit).toBe(component.maxDisplay);
  });

  it('should set correct properties', () => {
    component.maxDisplay = 3;
    component.limit = 4;
    component.events = [];
    component.loadChunk();
    expect(component.limit).toBe(7);
  });

  it('should return correct result', () => {
    const event = { id: 4 } as ISportEvent;
    const index = 7;
    expect(component.trackById(index, event)).toBe('74');
  });

  it('should return correct value', () => {
    const events = [
      {
        markets: [
          { templateMarketName: 'marketName' },
          { templateMarketName: 'marketName1' }
        ]
      }
    ] as ISportEvent[];
    expect(component['getPrimaryMarketName'](events)).toBe('marketName');
  });

  describe('@hideShowNext', () => {
    it('should hide next events button', () => {
      component.limit = 5;
      component.events = [];

      expect(component.hideShowNext()).toBeTruthy();
    });

    it('should show next events button', () => {
      component.limit = 1;
      component.events = [{}, {}] as ISportEvent[];

      expect(component.hideShowNext()).toBeFalsy();
    });
  });
});
