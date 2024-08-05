import { fakeAsync, tick } from '@angular/core/testing';

import { QuickbetYourcallWrapperComponent } from '@app/quickbet/components/quickbetYourcallWrapper/quickbet-yourcall-wrapper.component';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';

describe('QuickbetYourcallWrapperComponent', () => {
  let component;
  let callbackHandler;

  beforeEach(() => {
    callbackHandler = jasmine.createSpy('callbackHandler');

    component = new QuickbetYourcallWrapperComponent();
  });

  it('should emit place bet event', fakeAsync(() => {
    component.placeBetFn.subscribe(callbackHandler);

    component.placeBet();
    tick();

    expect(callbackHandler).toHaveBeenCalled();
  }));

  it('should emit close panel event', fakeAsync(() => {
    component.closePanelFn.subscribe(callbackHandler);

    component.closePanel();
    tick();

    expect(callbackHandler).toHaveBeenCalled();
  }));

  it('should emit reuse selection event', fakeAsync(() => {
    component.reuseSelectionFn.subscribe(callbackHandler);

    component.reuseSelection();
    tick();

    expect(callbackHandler).toHaveBeenCalled();
  }));

  it('should return tracking id', () => {
    expect(component.trackById(1, { id: '123' } as IBetSelection)).toEqual('123 1');

  });
});
