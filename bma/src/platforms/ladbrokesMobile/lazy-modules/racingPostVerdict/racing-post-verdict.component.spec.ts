import { RacingPostVerdictComponent } from '@app/lazy-modules/racingPostVerdict/racing-post-verdict.component';
import { IRacingPostVerdict } from '@racing/models/racing-post-verdict.model';

describe('RacingPostVerdictComponent', () => {
  let component: RacingPostVerdictComponent;
  beforeEach(() => {
    component = new RacingPostVerdictComponent();
  });

  it('should create', () => {
    expect(component).toBeDefined();
  });

  describe('methods', () => {
    beforeEach(() => {
      component.data = {
        starRatings: [
          {
            name: 'Name2',
            rating: 5,
          },
          {
            name: 'Name3',
            rating: 4,
          },
          {
            name: 'Name1',
            rating: 5,
          },
          {
            name: 'Name4',
            rating: 5,
          }],
        tips: [{
          name: 'tipname',
          value: 'tipvalue'
        }],
        verdict: 'verdict',
        imgUrl: 'imgurl',
        isFilled: true
      } as IRacingPostVerdict;
    });
    it('ngOnInit expect to have 3 items in rating', () => {
      component.ngOnInit();
      expect(component.data.starRatings.length).toBeLessThan(4);
    });
    it('compareByStarsAndName should return 1', () => {
      const result = component['compareByStarsAndName'](component.data.starRatings[1], component.data.starRatings[2]);
      expect(result).toEqual(1);
    });
    it('compareByStarsAndName should return -1', () => {
      const result = component['compareByStarsAndName'](component.data.starRatings[0], component.data.starRatings[1]);
      expect(result).toEqual(-1);
    });
    it('compareByStarsAndName should compare names and return -1', () => {
      const result = component['compareByStarsAndName'](component.data.starRatings[2], component.data.starRatings[3]);
      expect(result).toEqual(-1);
    });
    it('compareByStarsAndName should compare names and return 1', () => {
      const result = component['compareByStarsAndName'](component.data.starRatings[0], component.data.starRatings[2]);
      expect(result).toEqual(1);
    });
    it('trackByIndex should return number', () => {
      const result = component.trackByIndex(4);
      expect(typeof result).toEqual('number');
    });
  });
});
