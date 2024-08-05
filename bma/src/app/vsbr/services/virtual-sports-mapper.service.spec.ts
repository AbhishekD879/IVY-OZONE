import { VirtualSportsMapperService } from '@app/vsbr/services/virtual-sports-mapper.service';
import { IVirtualCategoryStructure } from '@app/vsbr/models/virtual-sports-structure.model';
import { IVirtualChild } from '@core/services/cms/models/virtual-sports.model';
import { ISportEvent } from '@core/models/sport-event.model';

describe('VirtualSportsMapperService', () => {
  let service;
  let parentCategory: IVirtualCategoryStructure;

  const classId: string = '287';
  const tracks: IVirtualChild[] = [{
    id: '5e85e070c9e77c0001805f6b',
    title: 'Inspired Cycling',
    classId: classId,
    streamUrl: 'zz',
    numberOfEvents: 4,
    showRunnerNumber: true,
    showRunnerImages: true
  }];

  const event: ISportEvent = {
    id: 230152170,
    name: 'Turin v Maribor Violets',
    eventStatusCode: 'S',
    displayOrder: 1,
    siteChannels: 'P,p,Q,R,C,I,M,',
    eventSortCode: 'MTCH',
    startTime: '2020-04-08T15:42:00Z',
    rawIsOffCode: '-',
    classId: classId,
    typeId: '32614',
    sportId: '39',
    liveServChannels: 'sEVENT0230152170,',
    liveServChildrenChannels: 'SEVENT0230152170,',
    categoryId: '39',
    categoryCode: 'VIRTUAL',
    categoryName: 'Virtual Sports',
    categoryDisplayOrder: '369',
    className: 'Virtual Football',
    classDisplayOrder: '202',
    classSortCode: 'VS',
    typeName: 'Striker Stadium',
    typeDisplayOrder: '0',
    isOpenEvent: 'true',
    isNext24HourEvent: 'true',
    cashoutAvail: 'N',
    startTimeUnix: 1586360520000
  };

  const child = {
    id: '5e85e070c9e77c0001805f6b',
    title: 'Inspired Cycling',
    classId: classId,
    streamUrl: 'zz',
    numberOfEvents: 4,
    alias: 'inspired-cycling',
    startTimeUnix: 1586360520000,
    timeLeft: -1897,
    events: [{
      'event': event
    }]
  };

  beforeEach(() => {
    parentCategory = {
      id: '5e85df97c9e77c0001d62999',
      title: 'Motorsports',
      tracks: tracks,
      svgId: '#icon-motor-bikes',
      svg: '',
      ctaButtonUrl: 'DO NOT TOUCH',
      ctaButtonText: 'THIS CONFIG!!!!',
      alias: 'motorsports',
      targetUri: '/virtual-sports/motorsports'
    } as any;

    service = new VirtualSportsMapperService();
  });

  it('get structure return [] if parent category not set', () => {
    expect(service.structure).toEqual([]);
  });

  it('get structure return [] is parent category doesn\'t contain childs', () => {
    service.setParentCategory(parentCategory);
    expect(service.categories[0]).toEqual(parentCategory);
    expect(service.structure.length).toEqual(0);
  });

  it('get structure return [] is parent category doesn\'t contain childs', () => {
    service.setParentCategory(parentCategory);
    service.setChildCategory(parentCategory.alias, child);

    expect(service.structure).toContain(parentCategory);
    expect(service.structure[0].childs.get(child.classId)).toEqual(child);
  });

  it('@setParentCategory should add new parent category', () => {
    service.setParentCategory(parentCategory);

    expect(service.categories).toContain(parentCategory);
    expect(service.categories[0].childs).toEqual(jasmine.any(Map));
  });

  it('@setParentCategory should add new parent category with childs', () => {
    const localParent = { ...parentCategory };
    const localChild = new Map();

    localChild.set(child.classId, child);
    localParent.childs = localChild;

    service.setParentCategory(localParent);

    expect(service.categories).toContain(localParent);
    expect(service.categories[0].childs).toEqual(jasmine.any(Map));
    expect(service.categories[0].childs.get(child.classId)).toEqual(child);
  });

  it('@setChildCategory should add new child category', () => {
    service.setParentCategory(parentCategory);
    service.setChildCategory(parentCategory.alias, child);

    expect(service.categories).toContain(parentCategory);
    expect(service.categories[0].childs.has(child.classId)).toBeTruthy();
  });

  it('@setChildCategory shouldn\'t add new child category if parent alias is incorrect', () => {
    service.setParentCategory(parentCategory);
    service.setChildCategory('', child);

    expect(service.categories).toContain(parentCategory);
    expect(service.categories[0].childs.has(child.classId)).toBeFalsy();
  });

  describe('Get methods', () => {
    beforeEach(() => {
      service.setParentCategory(parentCategory);
      service.setChildCategory(parentCategory.alias, child);
    });

    it('@getAliasesByClassId should return aliases for child and parent', () => {
      const aliases = service.getAliasesByClassId(child.classId);

      expect(aliases).toEqual({
        parentAlias: parentCategory.alias,
        childAlias: child.alias
      });
    });

    it('@getAliasesByClassId should return undefined is there is no category with classId', () => {
      const aliases = service.getAliasesByClassId('');

      expect(aliases).toBeUndefined();
    });

    it('@getParentByAlias should return parent category by alias', () => {
      const parentByAlias = service.getParentByAlias(parentCategory.alias);

      expect(parentCategory).toEqual(parentByAlias);
    });

    it('@getChildByAlias should return child category by child alias', () => {
      const childCategory = service.getChildByAlias(child.alias);

      expect(childCategory).toEqual(child);
    });

    it('@getChildByAlias should return undefined if there is no category for child alias', () => {
      const childCategory = service.getChildByAlias('');

      expect(childCategory).toBeUndefined();
    });

    it('@getChildByClassId should return undefined if there is no category for classId', () => {
      const childCategory = service.getChildByClassId('');

      expect(childCategory).toBeUndefined();
    });

    it('@getChildByClassId should return child category by child classId', () => {
      const childCategory = service.getChildByClassId(child.classId);

      expect(childCategory).toEqual(child);
    });

    it('@getAllClasses should return array of child classIds', () => {
      const classes = service.getAllClasses();

      expect(classes).toEqual([child.classId]);
    });

    it('@getAllClasses should return [] if there are no child categories', () => {
      const localeService = new VirtualSportsMapperService();
      const classes = localeService.getAllClasses();

      expect(classes).toEqual([]);
    });

    it('@getAllClasses should return array of child classIds', () => {
      const localParent = {...parentCategory};
      delete localParent.childs;

      service.structure = [localParent];

      const classes = service.getAllClasses();

      expect(classes).toEqual([]);
    });
  });
});
