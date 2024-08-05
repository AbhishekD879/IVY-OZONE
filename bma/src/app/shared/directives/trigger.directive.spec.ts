import { TriggerDirective } from '@shared/directives/trigger.directive';

describe('TooltipDirective', () => {
  const event = {
    preventDefault: jasmine.createSpy('preventDefault').and.callFake(() => {})
  } as any;

  let directive: TriggerDirective,
    pubSubService;

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish')
    };

    directive = new TriggerDirective(pubSubService);
  });

  describe('onClick', () => {
    it('should preventDefault', () => {
      directive.onClick(event);

      expect(event.preventDefault).toHaveBeenCalled();
    });

    it('should call pubSubService.publish with relative params', () => {
      directive.trigger = 'triggerAPI';
      directive.triggerArgs = 'triggerArg';

      directive.onClick(event);

      expect(pubSubService.publish).toHaveBeenCalledWith('triggerAPI', 'triggerArg');
    });
  });
});
