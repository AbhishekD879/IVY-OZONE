import { ladbrokesGreyhoundConfig } from './greyhound.config';
import { greyhoundConfig } from '@core/services/racing/config/greyhound.config';

describe('LMGreyhoundConfig', () => {
  it('compare keys of greyhound config from core with keys config from platform', () => {
    expect(Object.keys(ladbrokesGreyhoundConfig)).toEqual(Object.keys(greyhoundConfig));
  });

  it('config.categoryType should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.categoryType).toEqual(greyhoundConfig.config.categoryType);
  });

  it('config.name should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.name).toEqual(greyhoundConfig.config.name);
  });

  it('config.path should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.path).toEqual(greyhoundConfig.config.path);
  });

  it('config.sportModule should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.sportModule).toEqual(greyhoundConfig.config.sportModule);
  });

  it('config.request.categoryId should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.request.categoryId).toEqual(greyhoundConfig.config.request.categoryId);
  });

  it('config.request.isRacing should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.request.isRacing).toEqual(greyhoundConfig.config.request.isRacing);
  });

  it('config.request.siteChannels should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.request.siteChannels).toEqual(greyhoundConfig.config.request.siteChannels);
  });

  it('config.request.breadcrumbsNavMenuFlags should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.request.breadcrumbsNavMenuFlags).toEqual(greyhoundConfig.config.request.breadcrumbsNavMenuFlags);
  });

  it('config.request.groupByFlagCodesSortOrder should be equal', () => {
    expect(ladbrokesGreyhoundConfig.config.request.groupByFlagCodesSortOrder)
      .toEqual(greyhoundConfig.config.request.groupByFlagCodesSortOrder);
  });

  it('filters should be equal', () => {
    expect(ladbrokesGreyhoundConfig.filters).toEqual(greyhoundConfig.filters);
  });

  it('order should be equal', () => {
    expect(ladbrokesGreyhoundConfig.order).toEqual(greyhoundConfig.order);
  });

  it('sectionTitle should be equal', () => {
    expect(ladbrokesGreyhoundConfig.sectionTitle).toEqual(ladbrokesGreyhoundConfig.sectionTitle);
  });

  it('isRunnerNumber should be equal', () => {
    expect(ladbrokesGreyhoundConfig.isRunnerNumber).toEqual(greyhoundConfig.isRunnerNumber);
  });

  it('tabs should have order', () => {
    expect(ladbrokesGreyhoundConfig.tabs.map(tab => tab.id)).toEqual([
      'tab-races', 'tab-today', 'tab-tomorrow', 'tab-future', 'tab-specials'
    ]);
  });

  it('MARKETS_NAME_SORT_ORDER should be equal', () => {
    expect(ladbrokesGreyhoundConfig.MARKETS_NAME_SORT_ORDER).toEqual(['Win or Each Way', 'Win Only', 'Place Only',
      'To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish', 'Top 3 Finish', 'Top 4 Finish',
      'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places',
      'Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
      'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4']);
  });
});
