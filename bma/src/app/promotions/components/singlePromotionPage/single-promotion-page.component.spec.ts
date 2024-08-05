import { SinglePromotionPageComponent } from './single-promotion-page.component';

describe('SinglePromotionPageComponent', () => {
    const component: SinglePromotionPageComponent = new SinglePromotionPageComponent();

    it('should get the title', () => {
        component.title = '';
        component.changeTitle('title');
        expect(component.title).toEqual('title');
    });
});
