import { FanzoneGameLaunchDialogComponent } from '@app/lazy-modules/fanzone/components/fanzoneGameLaunchDialog/fanzone-game-launch-dialog.component';

describe('FanzoneGameLaunchDialogComponent', () => {
  let component: FanzoneGameLaunchDialogComponent;

  let device,
    windowRef,
    loc,
    fanzoneGamesService;

  beforeEach(() => {
    device = {};
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')  
      },
    };
    loc = {
      onPopState: jasmine.createSpy('onPopState')
    };
    fanzoneGamesService = {isGameClosedForcibly: false};
    component = new FanzoneGameLaunchDialogComponent(device,
      windowRef,
      loc,
      fanzoneGamesService
    );
    component.dialog = {};
    component.iframe = {
      nativeElement : {
        contentWindow : {
          postMessage: jasmine.createSpy('postMessage')
        }
      }
    };
  });

  describe('open', () => {
    it('should open popup', () => {
      const openSpy = spyOn(FanzoneGameLaunchDialogComponent.prototype['__proto__'], 'open');
      component.open();
      expect(openSpy).toHaveBeenCalled();
      expect(component.dialog.closeOnOutsideClick).toBeFalsy();
    });

    it('should open popup and clear timeout incase of game launch opened after closing from fallback scenario', () => {
      const openSpy = spyOn(FanzoneGameLaunchDialogComponent.prototype['__proto__'], 'open');
      fanzoneGamesService.isGameClosedForcibly = true;
      component.open();
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
      expect(openSpy).toHaveBeenCalled();
      expect(component.dialog.closeOnOutsideClick).toBeFalsy();
    });
  });

  describe('close', () => {
    it('should close popup', () => {
      component.close();
      expect(component.iframe.nativeElement.contentWindow.postMessage).toHaveBeenCalledWith("PREVIOUS_CASINO_GAME_CLOSED","*");
    });

    it('should close popup in case of postMessage failed', () => {
      component.dialog.visible = true;
      const closeDialogSpy = spyOn(FanzoneGameLaunchDialogComponent.prototype['__proto__'], 'closeDialog');
      component.close();
      expect(fanzoneGamesService.isGameClosedForcibly).toBeTruthy();
      expect(closeDialogSpy).toHaveBeenCalled();
    });
  });

  describe('onMessage', () => {
    it('should listen close acknowledgement from game launch iframe', () => {
      const closeDialogSpy = spyOn(FanzoneGameLaunchDialogComponent.prototype['__proto__'], 'closeDialog');
      const event = {data: "PREVIOUS_CASINO_GAME_CLOSED_ACK"} as MessageEvent;
      component.onMessage(event);
      expect(fanzoneGamesService.isGameClosedForcibly).toBeFalsy();
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
      expect(closeDialogSpy).toHaveBeenCalled();
    });

    it('should skip game close if different message from game launch iframe', () => {
      const closeDialogSpy = spyOn(FanzoneGameLaunchDialogComponent.prototype['__proto__'], 'closeDialog');
      const event = {data: "test"} as MessageEvent;
      component.onMessage(event);
      expect(closeDialogSpy).not.toHaveBeenCalled();
    });

    it('should listen close event on click of OK button', () => {
      const closeDialogSpy = spyOn(FanzoneGameLaunchDialogComponent.prototype['__proto__'], 'closeDialog');
      const event = {data: "CASINO_GAME_CLOSED"} as MessageEvent;
      component.onMessage(event);
      expect(closeDialogSpy).toHaveBeenCalled();
    });
  });
});
