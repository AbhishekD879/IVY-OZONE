package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.entity.BybMarket;
import com.ladbrokescoral.oxygen.cms.api.repository.BybMarketRepository;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;

@RunWith(MockitoJUnitRunner.class)
public class BybMarketServiceTest {

  @Mock private BybMarketRepository repoMock;

  private BybMarketService service;
  private BybMarket testMarket;

  @Before
  public void setUp() {
    service = new BybMarketService(repoMock);
    testMarket = prepareMarket();
    when(repoMock.findAll(PageRequest.of(0, 1, Sort.by(Sort.Direction.DESC, "sortOrder"))))
        .thenReturn(new PageImpl<>(new ArrayList<>()));
  }

  @Test
  public void testSave() {
    service.save(testMarket);
    verify(repoMock, times(1)).save(testMarket);
    Assert.assertTrue(testMarket.getSortOrder() == 1);
  }

  @Test
  public void testFindAllByBrandSorted() {
    String brand = "bma";
    when(repoMock.findAllByBrandOrderBySortOrderAsc(brand))
        .thenReturn(Collections.singletonList(testMarket));
    List<BybMarket> testMarkets = service.findAllByBrandSorted(brand);
    verify(repoMock, times(1)).findAllByBrandOrderBySortOrderAsc(brand);
    assertTrue(testMarkets.contains(testMarket));
  }

  private BybMarket prepareMarket() {
    BybMarket bybMarket = new BybMarket();
    bybMarket.setBrand("bma");
    bybMarket.setName("General");
    bybMarket.setBybMarket("BybMarket");
    bybMarket.setMarketGrouping(10);
    bybMarket.setIncidentGrouping(15);
    return bybMarket;
  }
}
