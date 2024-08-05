import { InplayAllSportsPageComponent as
    AppInplayAllSportsPageComponent } from '@app/inPlay/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { InplayAllSportsPageComponent } from './inplay-all-sports-page.component';

describe('InplayAllSportsPageComponent', () => {
  let component: InplayAllSportsPageComponent,
    pubsubService,
    inplayMainService,
    cms,
    changeDetectorRef,
    inPlayConnectionService;


  beforeEach(() => {
    inPlayConnectionService = {};
    inplayMainService = {
      isNewUserFromOtherCountry: jasmine.createSpy().and.returnValue(true),
    };
    cms = {};
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('subscribe'),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN'
      }
    };

    component = new InplayAllSportsPageComponent(
      pubsubService,
      inplayMainService,
      cms,
      inPlayConnectionService,
      changeDetectorRef
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayAllSportsPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('#addEventListeners should run addEventListeners from parent and run reloadComponent', () => {
    // @ts-ignore
    spyOn(AppInplayAllSportsPageComponent.prototype, 'addEventListeners');
    spyOn<any>(component, 'reloadComponent');
    pubsubService.subscribe.and.callFake((name, api, cb) => { cb(); } );

    component['addEventListeners']();

    expect(AppInplayAllSportsPageComponent.prototype['addEventListeners']).toHaveBeenCalledTimes(1);

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayAllSportsPage', 'SESSION_LOGIN', jasmine.any(Function) );
    expect(component['reloadComponent']).toHaveBeenCalledTimes(1);
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('#addEventListeners should run addEventListeners from parent and NOT run reloadComponent', () => {
    // @ts-ignore
    spyOn(AppInplayAllSportsPageComponent.prototype, 'addEventListeners');
    spyOn<any>(component, 'reloadComponent');
    inplayMainService['isNewUserFromOtherCountry'].and.returnValue(false);
    pubsubService.subscribe.and.callFake((name, api, cb) => { cb(); } );

    component['addEventListeners']();

    expect(AppInplayAllSportsPageComponent.prototype['addEventListeners']).toHaveBeenCalledTimes(1);

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayAllSportsPage', 'SESSION_LOGIN', jasmine.any(Function) );
    expect(component['reloadComponent']).toHaveBeenCalledTimes(0);
    expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
  });

  it('#ngOnDestroy should run ngOnDestroy from parent', () => {
    // @ts-ignore
    spyOn(AppInplayAllSportsPageComponent.prototype, 'ngOnDestroy');

    component['ngOnDestroy']();

    expect(AppInplayAllSportsPageComponent.prototype['ngOnDestroy']).toHaveBeenCalledTimes(1);
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayAllSportsPage');
  });
});
