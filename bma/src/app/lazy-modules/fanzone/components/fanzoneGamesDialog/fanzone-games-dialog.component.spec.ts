import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { FanzoneGamesDialogComponent } from '@app/lazy-modules/fanzone/components/fanzoneGamesDialog/fanzone-games-dialog.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('FanzoneGamesDialogComponent', () => {
  let component: FanzoneGamesDialogComponent;

  let device,
    windowRef,
    fanzoneStorageService,
    gtmService,
    fanzoneGamesService,
    pubsub,
    navigationService,
    loc,
    route,
    elementRef;
    

  beforeEach(() => {
    device = {};
    windowRef = {};
    fanzoneStorageService = {
      get: jasmine.createSpy('get').and.returnValue({ teamId: 'aresenal', teamName: 'arsenal' })
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    fanzoneGamesService = {
      setNewFanzoneGamesPopupSeen: jasmine.createSpy('setNewFanzoneGamesPopupSeen')
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      subscribe:jasmine.createSpy('subscribe'),
      unsubscribe:jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };
    route = {
      url: '/fanzone'
    };
    loc = {
      onPopState: jasmine.createSpy('onPopState')
    };
    elementRef = {
      nativeElement : { contains : jasmine.createSpy('element.contains').and.returnValue(false)},
    };
    component = new FanzoneGamesDialogComponent(device,
      windowRef,
      fanzoneStorageService,
      gtmService,
      fanzoneGamesService,
      pubsub,
      navigationService,
      loc,
      route,
      elementRef
    );
    component.dialog = {
      closeOnOutsideClick: false
    };
  });
  

  it('clickOutside', ()=>{
    elementRef.nativeElement.contains.and.returnValue(false);
  })

  describe('open', () => {
    it('should open popup', () => {
      const openSpy = spyOn(FanzoneGamesDialogComponent.prototype['__proto__'], 'open');
      component.open();
      expect(component.fanzoneTeam).toBeDefined();
      expect(fanzoneGamesService.setNewFanzoneGamesPopupSeen).toHaveBeenCalled();
      expect(openSpy).toHaveBeenCalled();
    });

    it('onoutsideclick on document click',  fakeAsync(() => {
      component.close = jasmine.createSpy('close');
      const event = { target: { tagName: 'target '},
      stopPropagation: jasmine.createSpy('stopPropagation') } as any;
      component.clickOutside(event as any);
      tick(100);
      expect(event.stopPropagation).toHaveBeenCalled();
      expect(component.close).toHaveBeenCalled(); 
    }));

    it('should not open popup in not in fanzone page', () => {
      const openSpy = spyOn(FanzoneGamesDialogComponent.prototype['__proto__'], 'open');
      route.url = "/home";
      const closeDialogSpy = spyOn(FanzoneGamesDialogComponent.prototype['__proto__'], 'closeDialog');
      pubsub.subscribe = jasmine.createSpy('subscribe')
      .and.callFake((filename: string, eventName: string, callback: Function) => {
        callback();
        expect(closeDialogSpy).toHaveBeenCalled();
      });
      component.open();
      expect(component.fanzoneTeam).toBeDefined();
      expect(openSpy).not.toHaveBeenCalled();
    });
  });

  describe('play', () => {
    it('should navigate to fanzone games tab on click of play button', () => {
      component.fanzoneTeam = { teamName: 'arsenal' };
      component.close = jasmine.createSpy('close');
      component.play();
      expect(navigationService.openUrl).toHaveBeenCalledWith('/fanzone/sport-football/arsenal/games', true);
      expect(component.close).toHaveBeenCalled();
    });
  });

  describe('close', () => {
    it('should close the popup', () => {
      const closeDialogSpy = spyOn(FanzoneGamesDialogComponent.prototype['__proto__'], 'closeDialog');
      component.close();
      expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.FANZONE_SHOW_GAMES_TOOLTIP);
      expect(closeDialogSpy).toHaveBeenCalled();
    });
  });
});
