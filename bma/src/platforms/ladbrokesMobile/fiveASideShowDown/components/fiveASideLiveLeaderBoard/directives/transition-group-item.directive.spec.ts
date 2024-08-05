import { TransitionGroupItemDirective } from './transition-group-item.directive';


describe('TransitionGroupItemDirective', () => {
  let tgiDirective: TransitionGroupItemDirective;
  let elRef;

  beforeEach(() => {
  elRef = {
      nativeElement: {}
  };
  tgiDirective = new TransitionGroupItemDirective(elRef);
  });

  it('should be instantiated', () => {
    expect(tgiDirective).toBeTruthy();
  });
});
