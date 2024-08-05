const fottballEventWithMarkets = {
  categoryId: '16'
};

const fottballEventWithToQualifyMarkets = {
  categoryId: '16'
};

export const surfaceBetModule = {
  '@type': 'SurfaceBetModule',
  'data': [{
    'categoryId': '16'
  }, {
    'categoryId': '16'
  }, {
    'categoryId': '16'
  }]
};

export const featuredModuleMock = {
  '@type': 'EventsModule',
  data: [
    fottballEventWithMarkets,
    fottballEventWithToQualifyMarkets,
    {
      categoryId: '16'
    }
  ]
};

export const featuredQuickLinksMock = {
  '@type': 'QuickLinkModule',
  data: [{
    id: '5bf3c940c9e77c0001238a52',
  }]
};

export const featuredDataMock = {
  modules: [featuredModuleMock, featuredQuickLinksMock, surfaceBetModule],
};
