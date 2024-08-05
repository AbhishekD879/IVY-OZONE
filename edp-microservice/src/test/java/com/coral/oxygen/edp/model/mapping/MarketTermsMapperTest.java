package com.coral.oxygen.edp.model.mapping;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Market;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class MarketTermsMapperTest {

  private MarketTermsMapper mapper;

  @Mock private MarketMapper chain;

  @Before
  public void setUp() {
    Mockito.when(chain.map(any(), any())).thenReturn(new OutputMarket());
    mapper = new MarketTermsMapper(chain);
  }

  @Test
  public void testTerms() {
    // preparation
    Market market = new Market();
    market.setEachWayPlaces(5);
    market.setEachWayFactorNum(11);
    market.setEachWayFactorDen(22);

    // action
    OutputMarket outputMarket = mapper.map(null, market);

    // verification
    Assert.assertEquals("Each Way: 11/22 odds - places 1,2,3,4,5", outputMarket.getTerms());
  }

  @Test
  public void testNullTerms() {
    // preparation
    Market market = new Market();
    market.setEachWayPlaces(null);
    market.setEachWayFactorNum(11);

    // action
    OutputMarket outputMarket = mapper.map(null, market);

    // verification
    Assert.assertNull(outputMarket.getTerms());
  }
}
