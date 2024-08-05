import { OxygenDialogContainerDirective } from '@shared/directives/oxygen-dialog-container.directive';

describe('OxygenDialogContainerDirective', () => {
  let directive, viewContainerRef;
  beforeEach(() => {
    viewContainerRef = {};
    directive = new OxygenDialogContainerDirective(viewContainerRef);
  });
  it('should create instance', () => {
    expect(directive).toBeTruthy();
    expect(directive.viewContainerRef).toBeDefined();
  });
});
