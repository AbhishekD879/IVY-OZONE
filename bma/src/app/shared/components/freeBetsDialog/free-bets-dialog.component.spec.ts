import { FreeBetsDialogComponent } from './free-bets-dialog.component';

describe('FreeBetsDialogComponent', () => {
  let component: FreeBetsDialogComponent;
  let device;
  let windowRef;
  let ezNavVanillaService;

  beforeEach(() => {
    device = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add')
          }
        }
      }
    };
    ezNavVanillaService = {};
    component = new FreeBetsDialogComponent(
      device, windowRef, ezNavVanillaService
    );
    component.dialog = {
      close: jasmine.createSpy('close'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('trackByIndex', () => {
    const result = component.trackByIndex(1);

    expect(result).toEqual(1);
  });

  describe('FreeBetsDialogComponent', () => {
    it('open (single token)', () => {
      component.isMyBetsInCasino = true;
      component.open();
      expect(component.dialog.visible).toBeFalsy();
    });

    it('open (multiple tokens)', () => {
      component.isMyBetsInCasino = false;
      component.open();
      expect(component.dialog.visible).toBeTruthy();
    });
  });
});
