package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerFilterRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackEnablerFilterService;
import java.util.Collections;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BetPackMarketPlacePublicFilterServiceTest {

  private BetPackMarketPlacePublicFilterService service;

  @Mock private BetPackEnablerFilterRepository repository;

  @Mock private CustomMongoRepository<BetPackFilter> mongoRepository;

  @Before
  public void init() {
    BetPackEnablerFilterService betPackEnablerFilterService =
        new BetPackEnablerFilterService(mongoRepository, repository);
    service = new BetPackMarketPlacePublicFilterService(betPackEnablerFilterService);
  }

  @Test
  public void testFindUninitializedEntityByFilterActive() {
    // arrange
    String brand = "bma";

    BetPackFilter entity = new BetPackFilter();
    when(repository.findByBrandAndFilterActiveTrue(brand))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackFilter> list = service.getActiveBetPackFilterByBrand(brand);
    // arrange
    assertEquals(1, list.size());

    BetPackFilter filter = list.iterator().next();
    assertNull(filter.getFilterName());
    assertNull(filter.getBrand());
  }

  @Test
  public void testFindByFilterActive() {
    // arrange
    String brand = "connect";

    BetPackFilter entity = new BetPackFilter();
    entity.setBrand("connect");
    entity.setFilterName("Football");

    when(repository.findByBrandAndFilterActiveTrue(brand))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackFilter> list = service.getActiveBetPackFilterByBrand(brand);

    // arrange
    assertEquals(1, list.size());
    BetPackFilter filter = list.iterator().next();
    assertEquals(entity.getBrand(), filter.getBrand());
    assertEquals(entity.getFilterName(), filter.getFilterName());
  }

  @Test
  public void testFindUninitializedEntityByAllFilter() {

    BetPackFilter entity = new BetPackFilter();
    when(mongoRepository.findAll()).thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackFilter> list = service.getAllBetPackFilter();
    // arrange
    assertEquals(1, list.size());

    BetPackFilter filter = list.iterator().next();
    assertNull(filter.getFilterName());
    assertNull(filter.getBrand());
  }

  @Test
  public void testFindByByAllFilter() {

    BetPackFilter entity = new BetPackFilter();
    entity.setBrand("connect");
    entity.setFilterName("Cricket");

    when(mongoRepository.findAll()).thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackFilter> list = service.getAllBetPackFilter();

    // arrange
    assertEquals(1, list.size());
    BetPackFilter filter = list.iterator().next();
    assertEquals(entity.getBrand(), filter.getBrand());
    assertEquals(entity.getFilterName(), filter.getFilterName());
  }
}
