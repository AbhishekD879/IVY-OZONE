import { StarRatingComponent } from '@shared/components/star-rating/star-rating.component';

describe('StarRatingComponent', () => {
    let component: StarRatingComponent;
    beforeEach(() => {
        component = new StarRatingComponent();
    });
    it('should create component instance', () => {
        expect(component).toBeTruthy();
    });
    it('should initialize start rating in ngonint', () => {
        component.rating = 3;
        component.ngOnInit();
        expect(component.startRating).toEqual([true, true, true, false, false]);
    });
    it('should return index based on input', () => {
        const response = component.trackByIndex(3);
        expect(response).toEqual(3);
    });
});
