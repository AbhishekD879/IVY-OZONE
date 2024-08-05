import { MyBetsButtonComponent } from '@shared/components/myBetsButton/my-bets-button.component';

describe('MyBetsButtonComponent', () => {
  let component: MyBetsButtonComponent;

  let device;
  let pubsub;
  let router;

  beforeEach(() => {
    device = {
      isMobile: false
    };
    pubsub = {
      publish: jasmine.createSpy()
    };
    router = {
      navigate: jasmine.createSpy()
    };
    component = new MyBetsButtonComponent(device, pubsub, router);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should call publish method when it\'s not mobile', () => {
    component.openMyBets();
    expect(pubsub.publish).toHaveBeenCalledWith('LOAD_UNSETTLED_BETS');
  });

  it('should call navigate method when it\'s mobile', () => {
    device.isMobile = true;
    component = new MyBetsButtonComponent(device, pubsub, router);
    component.openMyBets();
    expect(router.navigate).toHaveBeenCalledWith(jasmine.arrayContaining(['open-bets']));
  });
});
