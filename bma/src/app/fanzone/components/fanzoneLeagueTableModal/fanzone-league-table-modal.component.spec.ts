import { FanzoneLeagueTableModalComponent } from '@app/fanzone/components/fanzoneLeagueTableModal/fanzone-league-table-modal.component';

describe('FanzoneLeagueTableModalComponent', () => {
  let component: FanzoneLeagueTableModalComponent;

  beforeEach(() => {
    component = new FanzoneLeagueTableModalComponent();
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('close', () => {
    component.closeOverlay.emit = jasmine.createSpy('closeOverlay');
    component.close();
    expect(component.closeOverlay.emit).toHaveBeenCalledTimes(1);
  });
});