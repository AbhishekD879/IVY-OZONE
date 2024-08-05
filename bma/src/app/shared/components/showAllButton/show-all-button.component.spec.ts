import { ShowAllButtonComponent } from '@shared/components/showAllButton/show-all-button.component';

describe('ShowAllButtonComponent', () => {
  let component;
  let locale;

  beforeEach(() => {
    locale = {
      // eslint-disable-next-line
      getString: (string: string) => string
    };

    component = new ShowAllButtonComponent(locale);
  });

  describe('getText', () => {
    it('should return sb.showAll', () => {
      expect(component.getText()).toEqual('sb.showAll');
    });

    it('should return sb.showMore', () => {
      component.showMoreMode = true;
      expect(component.getText()).toEqual('sb.showMore');
    });

    it('should return "custom showMore string"', () => {
      component.showMoreMode = true;
      component.showMoreLocaleStr = 'custom showMore string';
      expect(component.getText()).toEqual('custom showMore string');
    });

    it('should return sb.showLess', () => {
      component.allShown = true;
      expect(component.getText()).toEqual('sb.showLess');
    });

    it('should return "sb.seeMore"', () => {
      component.seeMoreMode = true;

      expect(component.getText()).toEqual('sb.seeMore');
    });

    it('should return "sb.seeLess"', () => {
      component.seeMoreMode = true;
      component.allShown = true;

      expect(component.getText()).toEqual('sb.seeLess');
    });
  });

  describe('@cssClass', () => {
    it('should return component[customStylesClass]', () => {
      component['customStylesClass'] = ['customStylesClass'];

      expect(component.cssClass).toEqual(['customStylesClass']);
    });

    it('should return string', () => {
      component['customStylesClass'] = [];

      expect(component.cssClass).toEqual('show-all-button');
    });
  });
});
