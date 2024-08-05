import { FreeBetIconComponent } from '@desktop/components/freeBetIcon/free-bet-icon.component';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';


  describe('QuickLinksHeaderComponent', () => {
    let component: FreeBetIconComponent;

    let freeBetsService: FreeBetsService;

    beforeEach(() => {
      freeBetsService = {
        isFreeBetVisible: jasmine.createSpy().and.returnValue(true)
      } as any;

       component = new FreeBetIconComponent(freeBetsService);
    });

    it('constructor', () => {
      expect(component).toBeTruthy();
    });

    it('onInit', () => {
      component.ngOnInit();

      expect(component.freeBetVisible).toEqual(true);
    });
});
