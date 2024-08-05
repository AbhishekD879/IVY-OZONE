import { SvgListComponent } from '@shared/components/svgList/svg-list.component';

describe('SvgListComponent', () => {
  let component: SvgListComponent;

  const getInnerHTML = (symbolsHtmlStr: string): string => {
      return `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">${ symbolsHtmlStr }</svg>`;
    },
    elem = {
      nativeElement: {
        innerHTML: ''
      }
    };

  beforeEach(() => {
    component = new SvgListComponent(elem as any);
  });

  it('should use OnPush strategy', () => {
    expect(SvgListComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('ngOnInit', () => {
    it('should remove styles if item is present and has them', () => {
      component.list = '<p class="superClass">superP</p>';

      component.ngOnInit();

      expect(elem.nativeElement.innerHTML).toEqual(getInnerHTML('<p >superP</p>'));
    });

    it('should set empty string if no list was given', () => {
      component.list = '';

      component.ngOnInit();

      expect(elem.nativeElement.innerHTML).toEqual(getInnerHTML(''));
    });

    it('should keep styles', () => {
      component.list = [
        { svg: '<svg>1</svg>' },
        { svg: '<svg>2</svg>' },
        { svg: '<svg>3</svg>' }
      ] as any[];
      component.keepStyles = true;

      const result = component.list
        .filter(el => el.svg)
        .map(el => el.svg)
        .join('');

      component.ngOnInit();

      expect(elem.nativeElement.innerHTML).toEqual(getInnerHTML(result));
    });

    it('should keep fill property', () => {
      component.list = [
        { svg: '<svg xmlns="http://www.w3.org/2000/svg222"><title>title</title><style>.s{color: #000;}</style>' +
            '<rect class="s" fill="#000"></rect></svg>' }
      ] as any[];
      component.keepStyles = false;
      component.keepFill = true;

      component.ngOnInit();

      expect(elem.nativeElement.innerHTML).toEqual('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' +
        '<style>.s{color: #000;}</style><rect class="s" fill="#000"></rect></svg>');
    });
  });
});
