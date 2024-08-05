import { LastMadeBetDirective } from '@shared/directives/last-made-bet.directive';

describe('LastMadeBetDirective', () => {
  const segmentsArray: { segmentName: string; url: string; }[] = [
    {
      segmentName: 'segmentName',
      url: 'url'
    }
  ];

  let directive: LastMadeBetDirective,
    backButtonService,
    storage;

  const windowRef = {
    nativeWindow: {
      location: {
        hash: '#superevent'
      }
    }
  } as any;

  beforeEach(() => {
    backButtonService = {
      getSegmentsArray: jasmine.createSpy('getSegmentsArray').and.returnValue(segmentsArray)
    };

    storage = {
      set: jasmine.createSpy('set')
    };

    directive = new LastMadeBetDirective(backButtonService, storage, windowRef);
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
    expect(directive.locationPath).toEqual('#superevent');
  });

  describe('onClick', () => {
    it('should getSegmentsArray and store them', () => {
      directive.onClick();

      expect(storage.set).toHaveBeenCalledWith('lastMadeBet', '#superevent');
      expect(backButtonService.getSegmentsArray).toHaveBeenCalled();
      expect(storage.set).toHaveBeenCalledWith('lastMadeBetSport', segmentsArray[0]);
    });

    it('should set only lastMadeBet place', () => {
      directive.locationPath = '';

      directive.onClick();

      expect(storage.set).toHaveBeenCalledTimes(1);
      expect(storage.set).toHaveBeenCalledWith('lastMadeBet', '');
      expect(backButtonService.getSegmentsArray).not.toHaveBeenCalled();
    });
  });
});
