import { FreeBetLabelComponent } from './free-bet-label.component';

describe('#FreeBetLabelComponent', () => {
  let component;
  let filtersService;
  let deviceService;
  let fbService;
  let eventVideoStreamProviderService;

  beforeEach(() => {
    filtersService = {
      setFreebetCurrency: v => `$${v}`,
      setCurrency: v => `$${v}`

    };
    deviceService = {isDesktop:true};

    fbService = {
      isBetPack: jasmine.createSpy('isBetPack'),
      isFanzone: jasmine.createSpy('isFanzone')
      
    }
    eventVideoStreamProviderService = {
      isStreamAndBet: false
    }
    component = new FreeBetLabelComponent(filtersService, deviceService, fbService, eventVideoStreamProviderService);
    component['isFanzone']=false;  
  });
  describe('getFreebetLabelText', () => {
    it('get label text as freebet', () => {
      component.freeBetLabelText = 'FREEBET';
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(false);
      component['getFreebetLabelText']();
      expect(component['getFreebetLabelText']()).toBe('FREEBET');
    });
    it('get label text as betpack', () => {
      component.freeBetLabelText = 'BETPACK';
      fbService.isBetPack.and.returnValue(true);
      component['getFreebetLabelText']();
      expect(component['getFreebetLabelText']()).toBe('BET TOKEN');
    });
    it('get label text as fanzone', () => {
      component.freeBetLabelText = 'FANZONE';
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(true);
      component['getFreebetLabelText']();
      expect(component['getFreebetLabelText']()).toBe('Fanzone Free bet');
    });
  });
  it('should return device as true',()=>{ 
    expect(component.isDesktop).toBeTruthy();
  });
  it('should set value variable on selected set', () => {
    component.selected = '5.00';
    component.value = '$5.00 FREE BET';
    expect(component.value).toEqual('$5.00 FREE BET');
  });
  it('should set value variable on selected set', () => {
    component.selected = '5.20';
    component.value = '$5.20 FREE BET';
    expect(component.value).toEqual('$5.20 FREE BET');
  });
  it('should set value variable on selected set with SnB', () => {
    component.isStreamAndBet = true;
    component.selected = '5.00';
    component.value = '$5.00';
    expect(component.value).toEqual('$5.00');
  });

  it('should set value variable on selected Bet token', () => {
    component.freeBetLabelText = 'Bet Pack';
    component.selected = '5.00';
    fbService.isBetPack.and.returnValue(true);
    component.value = '$5.00 BET TOKEN';
    expect(component.value).toEqual('$5.00 BET TOKEN');
  }); 
  it('should set value variable on selected Bet token', () => {
    component.freeBetLabelText = 'FANZONE FREEBET';
    component.selected = '5.00';
    fbService.isFanzone.and.returnValue(true);
    component.value = '$5.00 FANZONE FREEBET';
    expect(component.value).toEqual('$5.00 FANZONE FREEBET');
  });

  it('should set value variable on selected Bet token & free bet', () => {
    component.freeBetLabelText = 'TOKEN & FREE BET';
    component.selected = '5.00';
    fbService.isBetPack.and.returnValue(false);
    component.value = '$5.00 TOKEN & FREE BET';
    expect(component.value).toEqual('$5.00 TOKEN & FREE BET');
  });

  it('should get "value" variable value (lol) on selected get', () => {
    component.value = '$3.00';
    expect(component.selected).toEqual('$3.00');
    });
});
